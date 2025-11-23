import json
import os
import sys
import pytest

# Adicionar o repo root ao path
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, REPO_ROOT)

from coleta.api_coleta_365scores import fetch_and_save_game_details

def test_no_false_players():
    """Testa que o JSON de stats não insere jogadores incorretos."""
    json_path = os.path.join(REPO_ROOT, 'tools', 'playwright_captures', 'stats_direct_365531214467481.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        sample = json.load(f)

    # Mock fetch_data para devolver o JSON
    def mock_fetch_data(url: str):
        if 'web/game/stats' in url.lower():
            return sample
        return None

    # Monkey patch
    import coleta.api_coleta_365scores as mod
    original_fetch = mod.fetch_data
    mod.fetch_data = mock_fetch_data
    mod.PLAYWRIGHT_AVAILABLE = False

    try:
        # Capturar prints ou usar dry_run
        # Como dry_run imprime, podemos testar indiretamente
        # Para teste unitário, mockar os upserts e verificar chamadas
        # Mas por simplicidade, usar dry_run e verificar output (não ideal, mas funciona)
        from io import StringIO
        import contextlib

        f = StringIO()
        with contextlib.redirect_stdout(f):
            fetch_and_save_game_details(4467481, dry_run=True)
        output = f.getvalue()

        assert "Jogadores: 0" in output, f"Esperado 'Jogadores: 0', mas output foi: {output}"
        assert "Times: 2" in output, "Esperado times do JSON"
    finally:
        mod.fetch_data = original_fetch

def test_with_player_data():
    """Teste com dados simulados de players (se houver JSON com players)."""
    # Placeholder: adicionar quando houver JSON com players reais
    pass