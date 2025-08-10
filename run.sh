#!/usr/bin/env bash
set -e

if ! python3 -c 'import sys; exit(not (sys.version_info >= (3,8)))'; then
    echo 'ERROR: Python 3.8+ is required.'
    exit 1
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

python scripts/setup_environment.py
python scripts/install_dependencies.py
mkdir -p data/documents
mkdir -p logs
python scripts/init_database.py
python scripts/process_documents.py
python scripts/verify_setup.py

echo "[INFO] FAQ Knowledge Base setup complete. Ready for RAG development."