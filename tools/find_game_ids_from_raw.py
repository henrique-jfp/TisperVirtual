"""Extrai potenciais game IDs dos arquivos em `dados_raw`.

Roda uma busca por números com 6-8 dígitos nos arquivos JSON/HTML e lista os mais comuns.
"""
import re
from pathlib import Path
from collections import Counter


def find_numbers_in_file(p: Path):
    nums = []
    text = p.read_text(errors='ignore')
    # busca números com 6 a 8 dígitos (ex.: 4309082)
    for m in re.finditer(r"\b(\d{6,8})\b", text):
        nums.append(m.group(1))
    return nums


def main():
    base = Path(__file__).resolve().parents[1] / 'dados_raw'
    if not base.exists():
        print(f"Diretório não encontrado: {base}")
        return
    ctr = Counter()
    for f in base.glob('**/*'):
        if f.is_file():
            try:
                nums = find_numbers_in_file(f)
                ctr.update(nums)
            except Exception:
                continue

    if not ctr:
        print("Nenhum número encontrado em dados_raw.")
        return

    # mostra os 50 mais comuns
    most = ctr.most_common(50)
    print("10 IDs candidatos (mais frequentes):")
    selected = []
    for n, c in most:
        # descarta timestamps prováveis (começando por 17xxxxxxx ou 1763...) - heurística
        if n.startswith('17'):
            continue
        selected.append(int(n))
        if len(selected) >= 10:
            break

    for sid in selected:
        print(sid)


if __name__ == '__main__':
    main()
