# -*- coding: utf-8 -*-
"""
JobPulse - Agregador de Vagas de Estágio em TI
==============================================

Ponto de entrada principal do sistema.
Coleta vagas de múltiplas fontes:
- GitHub Vagas (Brasil) - NOVO!
- Indeed Brasil (Scraping)
- RemoteOK (API)
- RSS Feeds (WeWorkRemotely, etc.)

Uso:
    python src/main.py
    python src/main.py --demo  # Usar dados de exemplo
"""

import sys
import os
import time

# Adicionar diretório src ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SEARCH_TERMS, HOURS_FILTER, OUTPUT_FILENAME
# from scraper_indeed import IndeedScraper # Arquivo ausente
from scraper_remoteok import RemoteOKScraper # Corrigido nome do arquivo e classe
from scraper_rss import RssScraper
from scraper_github import GithubScraper
from filters import apply_all_filters
from exporter import export_to_csv, generate_summary
from cli_ui import print_header, print_status, show_jobs_table, show_summary_panel, console

from rich.progress import Progress, SpinnerColumn, TextColumn


def get_demo_jobs():
    """
    Retorna vagas de exemplo para demonstração.
    """
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return [
        {
            "titulo": "Estágio em Frontend (React/Vue)",
            "empresa": "Tech Brasil Ltda",
            "localizacao": "São Paulo, SP",
            "link": "https://github.com/frontend-br/vagas/issues/1234",
            "data_publicacao": "Há 2 horas",
            "data_coleta": now,
            "plataforma": "GitHub (frontend-br)",
        },
        {
            "titulo": "Estagiário de Backend Python",
            "empresa": "Startup Inovadora",
            "localizacao": "Remoto",
            "link": "https://remoteok.com/l/123",
            "data_publicacao": "Há 5 horas",
            "data_coleta": now,
            "plataforma": "RemoteOK API",
        },
        {
            "titulo": "Estágio de Suporte N1",
            "empresa": "Corporação XYZ",
            "localizacao": "Curitiba, PR",
            "link": "https://br.indeed.com/viewjob?jk=123",
            "data_publicacao": "Há 1 dia",
            "data_coleta": now,
            "plataforma": "Indeed Brasil",
        }
    ]


def main():
    """
    Função principal do JobPulse.
    """
    print_header()

    # Verificar modo demo
    demo_mode = "--demo" in sys.argv
    
    raw_jobs = []

    if demo_mode:
        print_status("MODO DEMO: Carregando vagas de exemplo...", "bold yellow")
        raw_jobs = get_demo_jobs()
        time.sleep(1) # Simular loading
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task_total = progress.add_task("[green]Iniciando coleta...", total=None)

            # --- 1. GitHub Vagas (Prioridade para BR) ---
            progress.update(task_total, description="Varrendo GitHub Issues (Brasil)...")
            try:
                gh_scraper = GithubScraper()
                gh_jobs = gh_scraper.fetch_jobs()
                raw_jobs.extend(gh_jobs)
            except Exception as e:
                console.print(f"[red]Erro no GitHub: {e}[/red]")

            # --- 2. APIs Públicas (RemoteOK) ---
            progress.update(task_total, description="Consultando RemoteOK API...")
            try:
                api_scraper = RemoteOKScraper()
                api_jobs = api_scraper.fetch_jobs(SEARCH_TERMS)
                raw_jobs.extend(api_jobs)
            except Exception as e:
                console.print(f"[red]Erro na API RemoteOK: {e}[/red]")

            # --- 3. RSS Feeds ---
            progress.update(task_total, description="Lendo RSS Feeds...")
            try:
                rss_scraper = RssScraper()
                rss_jobs = rss_scraper.fetch_all(SEARCH_TERMS)
                raw_jobs.extend(rss_jobs)
            except Exception as e:
                console.print(f"[red]Erro no RSS: {e}[/red]")

            # --- 4. LinkedIn Stealth (Selenium) ---
            progress.update(task_total, description="Conectando ao LinkedIn (Stealth Mode)...")
            try:
                # Import lazy para não travar inicio se faltar lib
                from scraper_linkedin_stealth import LinkedinStealthScraper
                li_scraper = LinkedinStealthScraper()
                # Buscar apenas um termo genérico para ser rápido, ou iterar
                # Vamos focar em "Estágio TI" geral
                li_jobs = li_scraper.fetch_jobs("estágio ti")
                raw_jobs.extend(li_jobs)
            except Exception as e:
                console.print(f"[red]Erro no LinkedIn: {e}[/red]")

            # --- 5. Empregos.com.br (Novo) ---
            progress.update(task_total, description="Buscando no Empregos.com.br...")
            try:
                from scraper_empregos import EmpregosScraper
                emp_scraper = EmpregosScraper()
                emp_jobs = emp_scraper.fetch_jobs()
                raw_jobs.extend(emp_jobs)
            except Exception as e:
                console.print(f"[red]Erro no Empregos.com.br: {e}[/red]")

            # --- 6. Indeed (Desativado - Módulo ausente) ---
            # progress.update(task_total, description="Tentando Indeed (pode falhar)...")
            # try:
            #     indeed = IndeedScraper()
            #     indeed_jobs = indeed.collect_all(SEARCH_TERMS)
            #     raw_jobs.extend(indeed_jobs)
            # except Exception as e:
            #     pass

            progress.update(task_total, description="Finalizando...")

    if not raw_jobs:
        console.print(Panel("[bold red]Nenhuma vaga encontrada![/bold red]\n\nTente verificar sua conexão ou usar o modo demo:\n[cyan]python src/main.py --demo[/cyan]", border_style="red"))
        sys.exit(1)

    # Aplicar filtros
    print_status(f"Processando {len(raw_jobs)} vagas brutas...", "blue")
    
    # Nota: GitHub geralmente não tem "data exata" relativa fácil de parsear p/ horas, 
    # mas o filtro tenta. Se falhar, ele mantém (fallback).
    filtered_jobs = apply_all_filters(
        raw_jobs,
        recent_hours=HOURS_FILTER, # 24h por padrão, cuidado pois GitHub pode ter vagas de dias atrás que ainda valem
        keywords=None
    )

    # Exibir tabela rica
    show_jobs_table(filtered_jobs, max_rows=20)

    # Gerar resumo
    summary = generate_summary(filtered_jobs)
    show_summary_panel(summary)

    # Exportar para CSV
    print_status("Salvando arquivo...", "yellow")
    csv_path = export_to_csv(filtered_jobs, OUTPUT_FILENAME)

    if csv_path:
        print_status(f"Sucesso! Arquivo salvo em: {csv_path}", "bold green")
    
    if demo_mode:
        console.print("[dim]Nota: Execute sem --demo para buscar vagas reais.[/dim]")

    console.print()

if __name__ == "__main__":
    main()
