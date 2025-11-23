#!/usr/bin/env python3
"""
Script para extrair PDFs da internet e converter para Markdown organizado
Uso: python extract_pdf_to_md.py <URL_DO_PDF> [nome_arquivo_saida.md]
"""

import sys
import os
import requests
from urllib.parse import urlparse
import pdfplumber
from typing import Optional
import shutil

def download_pdf(url: str, output_path: str, chunk_size: int = 8192) -> bool:
    """Baixa o PDF da URL especificada com streaming para arquivos grandes"""
    try:
        print(f"📥 Baixando PDF de: {url}")
        with requests.get(url, stream=True, timeout=60) as response:  # Timeout aumentado
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Mostra progresso para arquivos grandes
                        if total_size > 1024 * 1024:  # > 1MB
                            progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                            print(f"📥 Progresso: {progress:.1f}% ({downloaded/1024/1024:.1f}MB)", end='\r')

        print(f"\n✅ PDF baixado com sucesso: {output_path} ({downloaded/1024/1024:.1f}MB)")
        return True

    except Exception as e:
        print(f"\n❌ Erro ao baixar PDF: {e}")
        return False

def process_local_pdf(pdf_path: str, output_md_path: str, source_path: str) -> bool:
    """Processa um PDF local diretamente"""
    try:
        print(f"📖 Processando PDF local: {pdf_path}")

        if not extract_text_from_pdf(pdf_path, output_md_path, source_path):
            return False

        return True

    except Exception as e:
        print(f"\n❌ Erro ao processar PDF local: {e}")
        return False

def extract_text_from_pdf(pdf_path: str, output_md_path: str, source_url: str) -> bool:
    """Extrai texto do PDF página por página e salva incrementalmente"""
    try:
        print(f"📖 Extraindo texto de: {pdf_path}")

        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"📄 Total de páginas: {total_pages}")

            # Cria arquivo de saída com cabeçalho
            dir_path = os.path.dirname(output_md_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(output_md_path, 'w', encoding='utf-8') as f:
                # Cabeçalho do documento
                f.write("# Documento Extraído de PDF\n\n")
                f.write(f"**Fonte:** {source_url}\n")
                f.write(f"**Data de extração:** 22 de novembro de 2025\n")
                f.write(f"**Total de páginas:** {total_pages}\n\n")
                f.write("---\n\n")

            # Processa página por página
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        # Adiciona ao arquivo
                        with open(output_md_path, 'a', encoding='utf-8') as f:
                            f.write(f"## Página {page_num}\n\n")
                            f.write(page_text.strip())
                            f.write("\n\n")

                    # Mostra progresso
                    if total_pages > 10:
                        progress = (page_num / total_pages) * 100
                        print(f"📖 Processando página {page_num}/{total_pages} ({progress:.1f}%)", end='\r')

                except Exception as page_error:
                    print(f"⚠️  Erro na página {page_num}: {page_error}")
                    continue

        print(f"\n✅ Texto extraído com sucesso ({total_pages} páginas)")
        return True

    except Exception as e:
        print(f"\n❌ Erro ao extrair texto: {e}")
        return False

def clean_and_format_markdown(text: str) -> str:
    """Limpa e formata o texto extraído para Markdown organizado"""
    if not text:
        return ""

    # Remove linhas vazias excessivas
    lines = text.split('\n')
    cleaned_lines = []

    prev_empty = False
    for line in lines:
        line = line.strip()
        if line:  # Só adiciona linhas não vazias
            cleaned_lines.append(line)
            prev_empty = False
        elif not prev_empty:  # Adiciona no máximo uma linha vazia
            cleaned_lines.append('')
            prev_empty = True

    return '\n'.join(cleaned_lines)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Extrai PDFs da internet ou arquivos locais e converte para Markdown organizado",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # PDF da internet
  python extract_pdf_to_md.py https://exemplo.com/documento.pdf
  python extract_pdf_to_md.py https://exemplo.com/documento.pdf saida.md

  # PDF local
  python extract_pdf_to_md.py documento.pdf
  python extract_pdf_to_md.py /caminho/para/arquivo.pdf saida.md
  python extract_pdf_to_md.py "Odds API Documentation V4 _ The Odds API.pdf"

  # Opções avançadas
  python extract_pdf_to_md.py documento.pdf --no-format
        """
    )

    parser.add_argument('source', help='URL do PDF ou caminho para arquivo PDF local')
    parser.add_argument('output', nargs='?', help='Nome do arquivo de saída (opcional)')
    parser.add_argument('--no-format', action='store_true',
                       help='Pula a formatação final (recomendado para PDFs muito grandes)')

    args = parser.parse_args()

    source = args.source
    output_md = args.output
    skip_formatting = args.no_format

    # Detecta se é URL ou arquivo local
    is_url = source.startswith(('http://', 'https://'))

    if is_url:
        # Processamento de URL
        # Define nome do arquivo de saída se não fornecido
        if not output_md:
            parsed_url = urlparse(source)
            filename = os.path.basename(parsed_url.path)
            if not filename or not filename.endswith('.pdf'):
                filename = 'documento_extraido.md'
            else:
                output_md = filename.replace('.pdf', '.md')

        # Arquivos temporários
        temp_pdf = f"temp_{os.path.basename(source).replace('.pdf', '')}.pdf"

        try:
            # Passo 1: Baixar PDF
            if not download_pdf(source, temp_pdf):
                sys.exit(1)

            # Passo 2: Extrair texto e salvar diretamente
            if not extract_text_from_pdf(temp_pdf, output_md, source):
                sys.exit(1)

        finally:
            # Limpa arquivo temporário
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
                print(f"🧹 Arquivo temporário removido: {temp_pdf}")

    else:
        # Processamento de arquivo local
        pdf_path = source

        # Verifica se o arquivo existe
        if not os.path.exists(pdf_path):
            print(f"❌ Arquivo não encontrado: {pdf_path}")
            sys.exit(1)

        # Verifica se é um PDF
        if not pdf_path.lower().endswith('.pdf'):
            print(f"❌ Arquivo deve ter extensão .pdf: {pdf_path}")
            sys.exit(1)

        # Define nome do arquivo de saída se não fornecido
        if not output_md:
            output_md = pdf_path.replace('.pdf', '.md')

        # Passo 1: Processar PDF local diretamente
        if not process_local_pdf(pdf_path, output_md, pdf_path):
            sys.exit(1)

    # Passo 3: Limpar e formatar (opcional, pode ser pesado para arquivos grandes)
    if not skip_formatting:
        print("🧹 Aplicando formatação final...")
        try:
            with open(output_md, 'r', encoding='utf-8') as f:
                content = f.read()

            formatted_content = clean_and_format_markdown(content)

            with open(output_md, 'w', encoding='utf-8') as f:
                f.write(formatted_content)

            print("✅ Formatação aplicada com sucesso")
        except Exception as format_error:
            print(f"⚠️  Erro na formatação (continuando sem formatação): {format_error}")
    else:
        print("⏭️  Formatação pulada (--no-format)")

    print("\n🎉 Processo concluído com sucesso!")
    print(f"📄 Arquivo Markdown criado: {output_md}")

if __name__ == "__main__":
    main()