import json
import os
import sys
import argparse
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..'))

sys.path.insert(0, REPO_ROOT)

MODULE_PATH = os.path.join(REPO_ROOT, 'coleta', 'api_coleta_365scores.py')


def load_collector_module():
    spec = importlib.util.spec_from_file_location('api_coleta_365scores', MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    parser = argparse.ArgumentParser(description='Reprocessa um jogo usando um JSON local (para testes).')
    parser.add_argument('--game', '-g', type=int, required=True, help='ID do jogo a reprocessar')
    parser.add_argument('--json', '-j', default=r'tools/playwright_captures/stats_direct_365531214467481.json', help='Caminho para o JSON salvo que contém dados de players')
    parser.add_argument('--dry-run', action='store_true', help='Modo de teste: parseia e mostra o que seria inserido, mas não salva no banco.')
    args = parser.parse_args()

    json_path = os.path.abspath(os.path.join(REPO_ROOT, args.json))
    if not os.path.exists(json_path):
        print(f"Arquivo JSON não encontrado: {json_path}")
        sys.exit(2)

    with open(json_path, 'r', encoding='utf-8') as f:
        sample = json.load(f)

    print(f"Carregado JSON de teste: {json_path}")

    collector = load_collector_module()

    # Substitui fetch_data para devolver o JSON local quando for chamada de stats/lineups/players
    def fetch_data_override(url: str):
        try:
            lu = url.lower()
        except Exception:
            lu = ''
        if 'web/game/stats' in lu or 'web/game/lineups' in lu or '/web/game/players' in lu or '/web/game/playersstats' in lu or '/web/game/playerstats' in lu:
            return sample
        # para o /web/game/?gameId=... devolve estrutura mínima
        if '/web/game/?' in lu or '/web/game/' in lu and 'gameid=' in lu:
            return {'game': {}}
        return None

    # Injeta monkeypatches no módulo carregado
    collector.fetch_data = fetch_data_override
    collector.PLAYWRIGHT_AVAILABLE = False

    print(f"Reprocessando jogo {args.game} usando payload local... (o script pode gravar no Supabase configurado no coletor)")
    try:
        collector.fetch_and_save_game_details(args.game, dry_run=args.dry_run)
        print("Reprocessamento finalizado.")
    except Exception as e:
        print(f"Erro durante reprocessamento: {e}")


if __name__ == '__main__':
    main()
