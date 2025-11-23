# Extrator de PDF para Markdown

Script rápido para baixar PDFs da internet ou processar arquivos locais e convertê-los para Markdown organizado.

**✅ Otimizado para PDFs Grandes** - Suporte completo para documentos com 100+ páginas!

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Sintaxe Básica
```bash
python tools/extract_pdf_to_md.py <URL_ou_caminho_PDF> [nome_arquivo_saida.md] [opções]
```

### Exemplos

1. **Extração simples** (nome automático):
```bash
python tools/extract_pdf_to_md.py https://www.exemplo.com/documento.pdf
```

2. **Com nome de saída personalizado**:
```bash
python tools/extract_pdf_to_md.py https://www.exemplo.com/relatorio.pdf relatorio_formatado.md
```

3. **PDF grande (pula formatação para velocidade)**:
```bash
python tools/extract_pdf_to_md.py https://exemplo.com/livro-grande.pdf livro.md --no-format
```

4. **Exemplo real** (documento público):
```bash
python tools/extract_pdf_to_md.py https://www.gov.br/mec/pt-br/centrais-de-conteudo/publicacoes/educacao-superior/arquivos/2023-09-15-sinopse-estatistica-educacao-superior-2022.pdf
```

## Funcionalidades

- ✅ **Download inteligente** com streaming para arquivos grandes
- ✅ **Processamento de arquivos locais** (não precisa baixar da internet)
- ✅ **Indicadores de progresso** em tempo real
- ✅ **Processamento incremental** página por página (não carrega tudo na memória)
- ✅ **Suporte a PDFs gigantes** (100+ páginas, vários MB)
- ✅ **Extração robusta** com tratamento de erros por página
- ✅ **Formatação opcional** (--no-format para PDFs muito grandes)
- ✅ **Limpeza automática** de arquivos temporários
- ✅ **Metadados completos** (fonte, data, número total de páginas)

## Opções Avançadas

- `--no-format`: Pula a etapa de formatação final (recomendado para PDFs > 50MB ou 500+ páginas)

## Capacidades para PDFs Grandes

| Característica | Suporte |
|---|---|
| **Tamanho máximo** | Limitado apenas pela RAM/disco disponível |
| **Número de páginas** | Testado com 1000+ páginas |
| **Download** | Streaming com progresso em tempo real |
| **Processamento** | Incremental, página por página |
| **Memória** | Uso otimizado, não carrega PDF inteiro na RAM |
| **Tempo** | ~2-5 segundos por página (depende do conteúdo) |
| **Recuperação de erros** | Continua mesmo se algumas páginas falharem |

## Arquivos Locais vs URLs

O script detecta automaticamente se você forneceu uma URL ou um caminho de arquivo local:

- **URLs**: `https://` ou `http://` - faz download e processa
- **Arquivos locais**: Qualquer outro caminho - processa diretamente do disco

### Vantagens dos Arquivos Locais

- ✅ **Mais rápido** - não precisa baixar
- ✅ **Sem limite de tamanho** de download
- ✅ **Funciona offline**
- ✅ **Preserva arquivos originais** intactos

O arquivo Markdown gerado terá:

```markdown
# Documento Extraído de PDF

**Fonte:** https://exemplo.com/documento.pdf
**Data de extração:** 22 de novembro de 2025
**Total de páginas:** 150

---

## Página 1

Conteúdo da primeira página...

## Página 2

Conteúdo da segunda página...

[...continua para todas as páginas...]
```

## Tratamento de Erros

- URLs inválidas ou inacessíveis
- PDFs corrompidos ou protegidos
- Arquivos locais não encontrados
- Páginas individuais com problemas (continua processando outras)
- Falhas de formatação (opção de pular)
- Limitações de memória/disco

## Recomendações para PDFs Grandes

1. **Use `--no-format`** para PDFs > 50MB
2. **Verifique espaço em disco** (arquivo MD pode ser 2-3x maior que o PDF)
3. **Monitore o progresso** através dos indicadores em tempo real
4. **Para PDFs muito grandes**, considere dividir em partes menores se possível

## Limitações

- Funciona melhor com PDFs baseados em texto (não imagens escaneadas)
- Preserva formatação básica, mas não tabelas complexas ou imagens
- Não extrai metadados avançados do PDF
- Formatação pode ser lenta em documentos muito grandes (> 1000 páginas)