"""Testes de integração do app Dash (sobe o servidor Flask em modo de teste)."""

import json

import pytest

from src.app import create_app


@pytest.fixture(scope="module")
def client():
    app = create_app(testing=True)
    return app.server.test_client()


def test_pagina_inicial_responde_200(client):
    # Antes: 500 por DuplicateIdError ("metrics-container" repetido no layout)
    assert client.get("/").status_code == 200


def test_layout_sem_ids_duplicados(client):
    resp = client.get("/_dash-layout")
    assert resp.status_code == 200
    ids = []

    def walk(node):
        if isinstance(node, dict):
            props = node.get("props", {})
            if "id" in props and isinstance(props["id"], str):
                ids.append(props["id"])
            for v in props.values() if "props" in node else node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(json.loads(resp.data))
    assert "metrics-container" in ids
    assert len(ids) == len(set(ids))


def test_aviso_de_dados_simulados(client):
    # Sem data/deliveries.json o loader usa dados gerados; o layout precisa avisar
    assert b"sample-data-alert" in client.get("/_dash-layout").data
