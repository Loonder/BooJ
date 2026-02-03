# -*- coding: utf-8 -*-
"""
Interface de Usuário (CLI) Avançada.
Usa a biblioteca 'rich' para exibir tabelas e status bonitos.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from typing import List, Dict

console = Console()

def print_header():
    """Exibe o cabeçalho do sistema."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🎯 JobPulse - Estágio em TI[/bold cyan]\n"
        "[dim]Buscador de vagas profissional para estudantes brasileiros[/dim]",
        border_style="cyan",
        title="v2.0",
        subtitle="Powered by Python"
    ))
    console.print()

def print_status(message: str, style: str = "bold green"):
    """Exibe mensagem de status."""
    console.print(f"[{style}]> {message}[/{style}]")

def show_jobs_table(jobs: List[Dict], max_rows: int = 15):
    """
    Exibe uma tabela rica com as vagas encontradas.
    """
    if not jobs:
        console.print(Panel("[yellow]Nenhuma vaga para exibir com os filtros atuais.[/yellow]", title="Aviso"))
        return

    table = Table(title=f"Vagas Encontradas ({len(jobs)})", box=box.ROUNDED, show_lines=True)

    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Título", style="bold white")
    table.add_column("Empresa", style="green")
    table.add_column("Local", style="yellow")
    table.add_column("Fonte", style="magenta")
    table.add_column("Publicado", justify="right", style="dim")

    for i, job in enumerate(jobs[:max_rows], 1):
        # Truncar textos longos
        title = job['titulo'] if len(job['titulo']) < 50 else job['titulo'][:47] + "..."
        company = job['empresa'] if len(job['empresa']) < 25 else job['empresa'][:22] + "..."
        local = job['localizacao'] if len(job['localizacao']) < 20 else job['localizacao'][:17] + "..."
        
        table.add_row(
            str(i),
            title,
            company,
            local,
            job['plataforma'],
            job.get('data_publicacao', 'N/A')
        )

    console.print(table)
    
    if len(jobs) > max_rows:
        console.print(f"[dim]...e mais {len(jobs) - max_rows} vagas ocultas (ver CSV).[/dim]", justify="center")

def show_summary_panel(summary: Dict):
    """Exibe um painel de resumo."""
    total = summary.get("total", 0)
    
    # Montar texto das plataformas
    plat_text = ""
    if summary.get("por_plataforma"):
        for p, c in summary["por_plataforma"].items():
            plat_text += f"{p}: [bold]{c}[/bold]\n"
    
    content = f"""
[bold size=20]Total: {total}[/bold size]

[u]Por Plataforma:[/u]
{plat_text}
[dim]CSV gerado com sucesso![/dim]
    """
    
    console.print(Panel(content, title="Resumo da Coleta", border_style="green", expand=False))
