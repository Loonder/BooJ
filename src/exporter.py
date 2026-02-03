import pandas as pd
import os
import sys
from typing import List, Dict
from config import OUTPUT_FILENAME, DATA_DIR

def save_jobs_append(jobs: List[Dict]):
    """Salva vagas no CSV em modo append (para o Hunter Bot)."""
    if not jobs:
        return
        
    # Garantir diretório
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    filepath = os.path.join(DATA_DIR, OUTPUT_FILENAME.replace("data/", ""))
    
    # Converter para DataFrame
    new_df = pd.DataFrame(jobs)
    
    # Se arquivo existe, carregar e concatenar para evitar duplicatas totais
    if os.path.exists(filepath):
        try:
            existing_df = pd.read_csv(filepath)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            # Remove duplicatas baseadas no Link
            combined_df.drop_duplicates(subset=['link'], keep='last', inplace=True)
            combined_df.to_csv(filepath, index=False)
        except Exception as e:
            print(f"Erro ao append CSV: {e}")
    else:
        new_df.to_csv(filepath, index=False)

def export_to_csv(jobs: List[Dict], filename: str = None) -> str:
    """
    Exporta a lista de vagas para um arquivo CSV.
    Retorna o caminho do arquivo gerado.
    """
    if not jobs:
        print("[!] Nenhuma vaga para exportar")
        return None

    if filename is None:
        filename = OUTPUT_FILENAME

    # Garantir que o diretório data existe
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Caminho completo (se filename não tiver path)
    if not os.path.dirname(filename):
        filepath = os.path.join(DATA_DIR, filename)
    else:
        filepath = filename

    try:
        df = pd.DataFrame(jobs)
        
        # Reordenar colunas se possível para ficar bonito
        cols = ['titulo', 'empresa', 'localizacao', 'plataforma', 'data_publicacao', 'link', 'data_coleta']
        existing_cols = [c for c in cols if c in df.columns]
        # Adicionar colunas extras que não estão na lista padrão
        extra_cols = [c for c in df.columns if c not in cols]
        
        df = df[existing_cols + extra_cols]
        
        df.to_csv(filepath, index=False)
        # print(f"[+] Arquivo salvo: {filepath}")
        return filepath
    except Exception as e:
        print(f"[!] Erro ao salvar CSV: {e}")
        return None

def display_jobs(jobs: List[Dict], max_display: int = 10):
    """Exibe as vagas no terminal de forma legível."""
    print(f"\n--- Top {max_display} Vagas Encontradas ---")
    for i, job in enumerate(jobs[:max_display], 1):
        print(f"{i}. {job.get('titulo')} | {job.get('empresa')}")
        print(f"   Local: {job.get('localizacao')} | Fonte: {job.get('plataforma')}")
        print(f"   Link: {job.get('link')}\n")

def generate_summary(jobs: List[Dict]) -> Dict:
    """Gera dados resumidos para exibição."""
    if not jobs:
        return {}
    
    df = pd.DataFrame(jobs)
    summary = {
        "total": len(jobs),
        "por_plataforma": df['plataforma'].value_counts().to_dict() if 'plataforma' in df.columns else {},
        "por_local": df['localizacao'].value_counts().head(5).to_dict() if 'localizacao' in df.columns else {}
    }
    return summary

def print_summary(summary: Dict):
    """Imprime o resumo."""
    if not summary:
        return

    print("\n=== RESUMO DA COLETA ===")
    print(f"Total de Vagas: {summary['total']}")
    
    print("\nPor Plataforma:")
    for plat, count in summary['por_plataforma'].items():
        print(f"  - {plat}: {count}")
        
    print("\nTop Locais:")
    for loc, count in summary['por_local'].items():
        print(f"  - {loc}: {count}")
