import re
from typing import List, Dict
try:
    from fuzzywuzzy import fuzz
except ImportError:
    fuzz = None 

class Intelligence:
    def __init__(self):
        # CATEGORIAS COM PESOS (Scoring System)
        self.weights = {
            # Ouro: Se tiver isso, o score explode (Cyber & Infra)
            "dream_job": {
                "keywords": ["segurança", "security", "cyber", "ciber", "pentest", 
                             "vulnerabilidade", "defensiva", "offensive", "red team", 
                             "blue team", "nmap", "burp", "owasp", "soc", "noc"],
                "points": 30
            },
            # Prata: O Core da sua busca (Dev & Suporte)
            "core_tech": {
                "keywords": ["python", "sql", "linux", "docker", "aws", "git", 
                             "selenium", "automação", "script", "bash", "suporte", 
                             "infraestrutura", "redes", "help desk", "service desk"],
                "points": 15
            },
            # Bronze: Coisas que você sabe, mas não é o foco principal
            "secondary": {
                "keywords": ["django", "flask", "fastapi", "pandas", "react", 
                             "javascript", "api", "rest", "html", "css"],
                "points": 10
            }
        }

        # Anti-patterns (Agora divididos por severidade)
        self.block_list = ["sênior", "senior", "specialist", "especialista", "manager", "gerente", "coordenador"]
        self.penalty_list = ["pleno", "rh", "marketing", "vendas", "comercial"]

    def verify_spam(self, text):
        """Verifica se a vaga tem cara de spam/golpe/curso/candidato."""
        # Mantive sua lista que estava ótima, só adicionei uns gatilhos de 'bomba'
        spam_keywords = [
            "renda extra", "ganhar dinheiro", "seja seu chefe",
            "marketing multinível", "sem investimento", "fature alto",
            "trabalhe em casa digitando", "assistente de envio",
            "ganhe dinheiro assistindo", "vagas ilimitadas",
            "curso completo", "mentoria paga", "taxa de adesão",
            "investimento inicial", "compre seu kit", "apenas com celular",
            "pix diario", "pix diário", "ganhos rápidos", "dinheiro extra",
            "for hire", "[for hire]", "seeking job", "seeking work",
            "looking for job", "looking for work", "available for",
            "procurando vaga", "busco oportunidade", "tenho experiência em",
            "my portfolio", "meu portfólio", "open to work"
        ]
        
        text_lower = str(text).lower()
        for kw in spam_keywords:
            if kw in text_lower:
                return True, kw
        return False, None

    def calculate_match_score(self, job: Dict) -> int:
        score = 0
        # Normaliza texto (Junta Título + Empresa + Descrição se tiver)
        text = (job.get('titulo', '') + " " + job.get('empresa', '')).lower()
        
        # 0. Filtro de SPAM (Kill Switch)
        is_spam, _ = self.verify_spam(text)
        if is_spam: return -999 

        # 1. Bloqueio Hard (Sênior/Especialista) - Mata a vaga
        for block in self.block_list:
            if block in text: return -1

        # 2. Penalidade Soft (Pleno/Vendas) - Só tira pontos, mas deixa passar se for muito boa
        for penalty in self.penalty_list:
            if penalty in text:
                score -= 50 # Penalidade pesada

        # 3. Cálculo de Pesos (A Mágica)
        # Verifica Dream Jobs (Cyber)
        for kw in self.weights["dream_job"]["keywords"]:
            if kw in text: score += self.weights["dream_job"]["points"]
            
        # Verifica Core Tech (Python/Linux/Suporte)
        for kw in self.weights["core_tech"]["keywords"]:
            if kw in text: score += self.weights["core_tech"]["points"]

        # Verifica Secundários
        for kw in self.weights["secondary"]["keywords"]:
            if kw in text: score += self.weights["secondary"]["points"]
        
        # Bônus Crítico: Se for explicitamente "Estágio" ou "Junior"
        if "estágio" in text or "estagiário" in text or "intern" in text:
            score += 20
        if "junior" in text or "júnior" in text or "trainee" in text:
            score += 10
            
        return min(max(score, 0), 100) # Mantém entre 0 e 100

    def is_duplicate(self, job: Dict, existing_jobs: List[Dict]) -> bool:
        # Mantive sua lógica Fuzzy que está perfeita
        if not existing_jobs: return False
        current_sig = f"{job['titulo']} {job['empresa']}".lower()

        for existing in existing_jobs:
            if job['link'] == existing['link']: return True
            existing_sig = f"{existing['titulo']} {existing['empresa']}".lower()
            
            if fuzz:
                ratio = fuzz.token_set_ratio(current_sig, existing_sig)
                if ratio > 90: return True
            else:
                if current_sig == existing_sig: return True     
        return False

    def enhance_job_data(self, job: Dict) -> Dict:
        job['score'] = self.calculate_match_score(job)
        job['is_relevant'] = job['score'] > 0 # Só é relevante se pontuar positivo
        
        # Tagging automático pra ficar bonito no painel
        job['tags'] = []
        if job['score'] >= 80: job['tags'].append("🔥 HOT")
        if "segurança" in str(job).lower() or "cyber" in str(job).lower(): job['tags'].append("🛡️ CYBER")
        if "python" in str(job).lower(): job['tags'].append("🐍 PYTHON")
        
        return job