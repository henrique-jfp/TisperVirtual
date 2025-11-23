#!/usr/bin/env python3
"""
Debug do processamento NLP
"""

import re
from football_nlp_processor import FootballQueryProcessor

def debug_nlp():
    """Debug do processamento NLP"""

    processor = FootballQueryProcessor()

    test_queries = [
        "Como está o Palmeiras nas estatísticas?",
        "Qual o histórico de Palmeiras x Corinthians?",
        "Como está o Gabigol jogando?",
        "Qual a odd para vitória do Palmeiras contra o Corinthians?"
    ]

    for query in test_queries:
        print(f"\n🔍 Testando: {query}")
        query_lower = query.lower().strip()

        for query_type, patterns in processor.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, query_lower)
                if match:
                    print(f"  ✅ Match: {query_type} -> {pattern}")
                    print(f"     Groups: {match.groups()}")
                    break

if __name__ == "__main__":
    debug_nlp()