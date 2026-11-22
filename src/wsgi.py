"""Entrada WSGI para produção (ex.: ``waitress-serve --port=8050 src.wsgi:server``)."""

from src.app import create_app

app = create_app()
server = app.server
