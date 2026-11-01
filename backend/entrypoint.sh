#!/bin/sh
set -e

echo "Waiting for database..."
python <<'PY'
import time, sys, os
import psycopg
from urllib.parse import urlparse

url = os.environ["DATABASE_URL"]
p = urlparse(url)
for i in range(30):
    try:
        psycopg.connect(
            dbname=p.path.lstrip("/"),
            user=p.username,
            password=p.password,
            host=p.hostname,
            port=p.port or 5432,
            connect_timeout=2,
        ).close()
        print("DB ready.")
        sys.exit(0)
    except Exception as exc:
        print(f"DB not ready ({i+1}/30): {exc}", file=sys.stderr)
        time.sleep(1)

print("DB not reachable after 30s", file=sys.stderr)
sys.exit(1)
PY

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting: $@"
exec "$@"