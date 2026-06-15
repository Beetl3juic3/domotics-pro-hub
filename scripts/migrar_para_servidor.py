#!/usr/bin/env python3
"""
Migracao Lovable Cloud -> Servidor PostgreSQL proprio.

O que faz:
  1. Liga-se ao Lovable Cloud (Supabase) e ao teu servidor Postgres.
  2. Cria as tabelas (obras, apartamentos, checklist_items, profiles)
     e o tipo obra_estado no servidor de destino, se nao existirem.
  3. Copia todos os dados em lote (UPSERT por id, idempotente).
  4. Pode ser corrido varias vezes - so atualiza o que mudou.

Requisitos:
    pip install psycopg2-binary

Uso:
    # Define as variaveis de ambiente (ou edita DEFAULTS abaixo)
    export SOURCE_DSN="postgresql://postgres:<password>@<host>:5432/postgres"
    export TARGET_DSN="postgresql://utilizador:password@meuservidor.pt:5432/minha_db"
    python migrar_para_servidor.py

SOURCE_DSN: pede o connection string do Lovable Cloud ao suporte
(nao e exposto na app). Em alternativa exporta as tabelas para CSV
no painel Backend > Database e usa --from-csv ./pasta_csv.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Iterable

import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

# --- Configuracao -----------------------------------------------------------

TABLES = ["profiles", "obras", "apartamentos", "checklist_items"]

# Chave primaria usada para UPSERT em cada tabela.
PK = {
    "profiles": "user_id",
    "obras": "id",
    "apartamentos": "id",
    "checklist_items": "id",
}

SCHEMA_SQL = """
DO $$ BEGIN
    CREATE TYPE obra_estado AS ENUM ('pendente', 'em_curso', 'concluido');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

CREATE TABLE IF NOT EXISTS profiles (
    user_id    uuid PRIMARY KEY,
    nome       text NOT NULL,
    email      text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS obras (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id        uuid NOT NULL,
    nome           text NOT NULL,
    created_at     timestamptz NOT NULL DEFAULT now(),
    updated_at     timestamptz NOT NULL DEFAULT now(),
    modificado_por uuid,
    modificado_em  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS apartamentos (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    obra_id        uuid NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    nome           text NOT NULL,
    estado         obra_estado NOT NULL DEFAULT 'pendente',
    created_at     timestamptz NOT NULL DEFAULT now(),
    updated_at     timestamptz NOT NULL DEFAULT now(),
    modificado_por uuid,
    modificado_em  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS checklist_items (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    apartamento_id uuid NOT NULL REFERENCES apartamentos(id) ON DELETE CASCADE,
    descricao      text NOT NULL,
    concluido      boolean NOT NULL DEFAULT false,
    ordem          integer NOT NULL DEFAULT 0,
    created_at     timestamptz NOT NULL DEFAULT now(),
    modificado_por uuid,
    modificado_em  timestamptz NOT NULL DEFAULT now()
);
"""


# --- Helpers ----------------------------------------------------------------

def log(msg: str) -> None:
    print(f"[migracao] {msg}", flush=True)


def ensure_schema(target_conn) -> None:
    log("A garantir schema no servidor de destino...")
    with target_conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)
    target_conn.commit()


def fetch_rows(source_conn, table: str) -> list[dict]:
    with source_conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f'SELECT * FROM public.{table}')
        return cur.fetchall()


def upsert_rows(target_conn, table: str, rows: Iterable[dict]) -> int:
    rows = list(rows)
    if not rows:
        return 0
    cols = list(rows[0].keys())
    pk = PK[table]
    update_cols = [c for c in cols if c != pk]
    set_clause = ", ".join(f'"{c}" = EXCLUDED."{c}"' for c in update_cols)
    sql = (
        f'INSERT INTO {table} ({", ".join(f"""\"{c}\"""" for c in cols)}) '
        f"VALUES %s "
        f'ON CONFLICT ("{pk}") DO UPDATE SET {set_clause}'
    )
    values = [[r[c] for c in cols] for r in rows]
    with target_conn.cursor() as cur:
        execute_values(cur, sql, values, page_size=500)
    target_conn.commit()
    return len(rows)


def load_csv(folder: Path, table: str) -> list[dict]:
    path = folder / f"{table}.csv"
    if not path.exists():
        log(f"  (sem ficheiro {path.name}, ignorado)")
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return [
            {k: (None if v == "" else v) for k, v in row.items()}
            for row in csv.DictReader(fh)
        ]


# --- Main -------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Migrar dados para o teu servidor.")
    parser.add_argument(
        "--from-csv",
        type=Path,
        help="Pasta com CSVs exportados (profiles.csv, obras.csv, ...). "
             "Se omitido, le directamente do SOURCE_DSN.",
    )
    parser.add_argument(
        "--target-dsn",
        default=os.environ.get("TARGET_DSN"),
        help="Connection string do teu servidor Postgres (ou env TARGET_DSN).",
    )
    parser.add_argument(
        "--source-dsn",
        default=os.environ.get("SOURCE_DSN"),
        help="Connection string do Lovable Cloud (ou env SOURCE_DSN).",
    )
    args = parser.parse_args()

    if not args.target_dsn:
        log("ERRO: define TARGET_DSN (env ou --target-dsn).")
        return 1

    target_conn = psycopg2.connect(args.target_dsn)
    ensure_schema(target_conn)

    source_conn = None
    if not args.from_csv:
        if not args.source_dsn:
            log("ERRO: define SOURCE_DSN ou usa --from-csv <pasta>.")
            return 1
        source_conn = psycopg2.connect(args.source_dsn)

    total = 0
    for table in TABLES:
        log(f"Tabela {table}:")
        rows = (
            load_csv(args.from_csv, table)
            if args.from_csv
            else fetch_rows(source_conn, table)
        )
        n = upsert_rows(target_conn, table, rows)
        log(f"  {n} registos copiados.")
        total += n

    log(f"Concluido. {total} registos no total.")
    target_conn.close()
    if source_conn:
        source_conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())