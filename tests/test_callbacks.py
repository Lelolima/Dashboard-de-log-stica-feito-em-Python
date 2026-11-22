"""Testes dos callbacks do dashboard (executados diretamente, sem navegador)."""

import pytest

import src.callbacks as cb
from src.data.loader import DataLoader


@pytest.fixture(scope="module")
def store():
    df = DataLoader(data_source="sample").load_deliveries()
    return df, {"df_json": df.to_json()}


def test_update_dashboard_com_store_json(store):
    # Antes: pd.read_json(str) quebrava no pandas 3 (FileNotFoundError)
    df, data = store
    out = cb.update_dashboard(None, None, None, None, data)
    assert len(out) == 6


def test_filtro_estado_considera_todos_os_selecionados(store, monkeypatch):
    df, data = store
    capturado = {}
    real = cb.DataProcessor.calcular_metricas

    def spy(self):
        capturado["n"] = len(self.df)
        return real(self)

    monkeypatch.setattr(cb.DataProcessor, "calcular_metricas", spy)
    estados = sorted(df["state"].unique())
    cb.update_dashboard(estados, None, None, None, data)
    assert capturado["n"] == len(df)  # todos os estados marcados = todos os dados

    cb.update_dashboard(["RJ", "MG"], None, None, None, data)
    assert capturado["n"] == int(df["state"].isin(["RJ", "MG"]).sum())


def test_download_csv(store):
    _, data = store
    result = cb.download_data(1, data)
    assert result["filename"] == "dashboard_export.csv"
