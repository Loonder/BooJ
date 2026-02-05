import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Config
DB_PATH = "data/jobs.db"

def verify_jobs():
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado em: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # Query jobs
    query = """
    SELECT titulo, empresa, plataforma, data_publicacao, data_coleta, created_at
    FROM jobs 
    ORDER BY created_at DESC
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        
        print("\n=== 🔎 JobPulse Hunter Verification ===\n")
        print(f"📦 Total de vagas no banco: {len(df)}")
        
        # Helper to categorize
        def categorize(title):
            t = title.lower()
            if 'junior' in t or 'júnior' in t or 'jr' in t:
                return '👶 Junior'
            elif 'estágio' in t or 'estagio' in t or 'intern' in t:
                return '🎓 Estágio'
            elif any(x in t for x in ['sdr', 'bdr', 'vendas', 'comercial', 'sales', 'closer']):
                return '💰 Vendas/SDR'
            elif 'trainee' in t:
                return '🚀 Trainee'
            else:
                return '❓ Outros'

        df['categoria'] = df['titulo'].apply(categorize)
        
        # Filter: Last 24 hours (based on Coleta/Created At)
        # Handle formats
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        
        # Convert created_at to datetime if needed
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df['data_coleta'] = pd.to_datetime(df['data_coleta'], errors='coerce')
        
        # Get new jobs (collected in last 24h)
        new_jobs = df[df['created_at'] > yesterday]
        
        print(f"\n⚡ Vagas coletadas nas últimas 24h: {len(new_jobs)}")
        
        if len(new_jobs) > 0:
            print("\n📊 Distribuição das Novas Vagas:")
            print(new_jobs['categoria'].value_counts().to_string())
            
            print("\n🔍 Exemplos Recentes (Top 5):")
            print(new_jobs[['titulo', 'empresa', 'plataforma', 'categoria']].head(5).to_string(index=False))
        else:
            print("\n⚠️ Nenhuma vaga coletada nas últimas 24h. O bot pode estar parado ou reiniciando.")

        print("\n=========================================")

    except Exception as e:
        print(f"❌ Erro ao ler banco de dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify_jobs()
