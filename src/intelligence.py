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
            # Geral TI (Termos genéricos para garantir que é TI)
            "general_tech": {
                "keywords": ["ti", "t.i.", "tecnologia", "informática", "computação", 
                             "sistemas", "software", "desenvolvimento", "programação", "análise de dados",
                             "desenvolvedor", "developer", "programador", "engenharia de software"],
                "points": 10
            },
            # Bronze: Coisas que você sabe, mas não é o foco principal
            "secondary": {
                "keywords": ["django", "flask", "fastapi", "pandas", "react", 
                             "javascript", "api", "rest", "html", "css", "java", "node", "c#", ".net",
                             "golang", "go", "ruby", "php", "laravel", "spring", "vue", "angular",
                             "ia", "ai", "artificial intelligence", "nlp", "llm"],
                "points": 10
            }
        }

        # Anti-patterns (Agora divididos por severidade)
        # Block List: Mata a vaga imediatamente
        self.block_list = [
            "sênior", "senior", "specialist", "especialista", "manager", "gerente", "coordenador",
            "motorista", "recepcionista", "estoquista", "operador de caixa", "atendente", "loja",
            "auxiliar administrativo", "secretária", "enfermeiro", "técnico de enfermagem", "médico", 
            "advogado", "cozinheiro", "garçom", "manobrista", "portaria", "vigilante", "limpeza",
            "obra", "pedreiro", "servente", "eletricista predial", "mecânico", "produção",
            "telemarketing", "call center", "cobrança", "rh", "recursos humanos", "departamento pessoal",
            "contábil", "fiscal", "financeiro", "almoxarife", "logística"
        ]
        
        self.penalty_list = ["pleno"] # Vendas removido da penalidade

        # Adicionar Sales como categoria de interesse
        self.weights["sales"] = {
            "keywords": ["sdr", "bdr", "vendas", "comercial", "closer", "inside sales", "customer success"],
            "points": 20 # Pontuação alta para Vendas
        }

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

    def safe_match(self, keyword, text):
        """Verifica se a keyword está no texto respeitando fronteiras de palavra para termos curtos."""
        keyword = keyword.lower().strip()
        text = text.lower()
        
        # Keywords curtas (< 4 chars) ou perigosas exigem regex \bWORD\b
        # Ex: "ti", "go", "r", "c", "net", "ia", "bio", "agro"
        dangerous = ["ti", "go", "r", "c", "net", "ia", "bio", "agro", "dev", "mec", "rh", "law", "qa", "ux", "ui"]
        if len(keyword) < 4 or keyword in dangerous:
            # Escape keyword special chars (like . or +)
            # C# -> c\#
            if keyword == "c++": pattern = r'\bc\+\+\b'
            elif keyword == "c#": pattern = r'\bc#\b'
            elif keyword == ".net": pattern = r'\.net\b'
            elif keyword == "node.js": pattern = r'node\.js\b'
            else: pattern = f'\\b{re.escape(keyword)}\\b'
            
            return bool(re.search(pattern, text))
        
        # Keywords longas podem usar substring (mas 'banco' em 'banco de dados' ok, mas 'bancario'?)
        # 'Java' -> 'Javascript'? Não.
        # Melhor usar regex pra tudo que for tech.
        return keyword in text

    def calculate_match_score(self, job: Dict) -> int:
        score = 0
        topic_hits = 0 # Contador de tópicos relevantes
        
        # Normaliza texto (Junta Título + Empresa + Descrição se tiver)
        text = (str(job.get('titulo', '') or '') + " " + str(job.get('empresa', '') or '')).lower()
        
        # 0. Filtro de SPAM (Kill Switch)
        is_spam, _ = self.verify_spam(text)
        if is_spam: return -999 
        
        # 1. Bloqueio Hard (Mata a vaga)
        for block in self.block_list:
            if block in text: return -1

        # 2. Penalidade Soft
        for penalty in self.penalty_list:
            if penalty in text:
                score -= 10

        # 3. Cálculo de Pesos (Categorias)
        for category, data in self.weights.items():
            for kw in data["keywords"]:
                if self.safe_match(kw, text):
                    score += data["points"]
                    topic_hits += 1
                    break # Pontua apenas uma vez por categoria (evita spam de keywords)

        # 4. Validação de Relevância
        # Se não bateu em NENHUM tópico técnico ou de vendas, é lixo (ex: "Estágio em Direito")
        if topic_hits == 0:
            return 0
        
        # Bônus Crítico: Se for explicitamente "Estágio" ou "Junior" E tem relevância de tópico
        if "estágio" in text or "estagiário" in text or "intern" in text:
            score += 20
        if "junior" in text or "júnior" in text or "trainee" in text:
            score += 10
            
        return min(max(score, 0), 100) # Mantém entre 0 e 100

    def is_duplicate(self, job: Dict, existing_jobs: List[Dict]) -> bool:
        # Mantive sua lógica Fuzzy que está perfeita
        if not existing_jobs: return False
        current_sig = f"{str(job.get('titulo', '') or '')} {str(job.get('empresa', '') or '')}".lower()

        for existing in existing_jobs:
            if job.get('link') == existing.get('link'): return True
            existing_sig = f"{str(existing.get('titulo', '') or '')} {str(existing.get('empresa', '') or '')}".lower()
            
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
        
        # Extração de Salário
        job['salario'] = self.extract_salary(str(job.get('descricao', '') or '') + " " + str(job.get('titulo', '') or ''))

        return job

    def extract_salary(self, text: str) -> str:
        """Extrai menções de salário ou bolsa do texto."""
        import re
        text = text.lower()
        
        # Padrões de salário (R$ 1000, 1.000,00, etc)
        # Regex captura: (R$ ou Bolsa) + (espaços opcionais) + (números com ponto/vírgula)
        patterns = [
            r'(?:salário|bolsa|remuneração)(?:\s+(?:auxílio|mensal|estágio))?\s*:?\s*(?:de\s*)?(?:r\$\s*)?([\d\.,]{3,})',
            r'r\$\s*([\d\.,]{3,})',
        ]
        
        for p in patterns:
            match = re.search(p, text)
            if match:
                value = match.group(1).strip()
                # Limpeza básica (ignora valores muito pequenos que podem ser horas ou lixo)
                clean_val = value.replace('.', '').replace(',', '.')
                try:
                    num = float(clean_val)
                    if num > 300: # Filtra valores irreais para mensal
                        return f"R$ {value}"
                except:
                    pass
                    
        return None