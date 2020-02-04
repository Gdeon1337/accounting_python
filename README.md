# accounting_python

in system
    python3.7 -m venv .venv
    source .venv/bin/activate
    pip install poetry
    poetry update
    start server: python -m sanic autoapp.app
    start tests: pytest tests/test.py 

docker
    docker-compose build
    docker-compose up
