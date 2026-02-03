# -*- coding: utf-8 -*-
"""
Módulo de filtros e ordenação de vagas.
"""

import re
from typing import List, Dict
from datetime import datetime


def parse_relative_date(date_text: str) -> int:
    """
    Converte texto de data relativa para minutos.
    Ex: "Há 2 horas" -> 120, "Há 1 dia" -> 1440
    
    Args:
        date_text: Texto da data relativa
        
    Returns:
        Minutos desde a publicação (menor = mais recente)
    """
    if not date_text:
        return 999999  # Prioridade baixa para datas desconhecidas

    text = date_text.lower()

    # Padrões de tempo em português
    patterns = [
        (r"agora|just|acabou", 0),
        (r"(\d+)\s*(minuto|min)", lambda m: int(m.group(1))),
        (r"(\d+)\s*(hora|hour)", lambda m: int(m.group(1)) * 60),
        (r"(\d+)\s*(dia|day)", lambda m: int(m.group(1)) * 1440),
        (r"hoje|today", 720),  # ~12 horas
        (r"ontem|yesterday", 1440),  # 1 dia
        (r"(\d+)\s*(semana|week)", lambda m: int(m.group(1)) * 10080),
        (r"(\d+)\s*(m[eê]s|month)", lambda m: int(m.group(1)) * 43200),
    ]

    for pattern, value in patterns:
        match = re.search(pattern, text)
        if match:
            if callable(value):
                return value(match)
            return value

    # Tentar formatos de data absoluta (YYYY-MM-DD ou ISO)
    try:
        # Remover 'Z' se existir
        clean_text = text.replace("Z", "")
        # Tentar UTC simples YYYY-MM-DD
        if len(clean_text) == 10:
            dt = datetime.strptime(clean_text, "%Y-%m-%d")
        else:
            # Tentar ISO completa
            dt = datetime.fromisoformat(clean_text)
            
        # Calcular delta (ignorando fuso para simplicidade neste MVP)
        delta = datetime.now() - dt
        return int(delta.total_seconds() / 60)
    except (ValueError, TypeError):
        pass

    return 999999  # Fallback para datas não reconhecidas


def sort_by_date(jobs: List[Dict]) -> List[Dict]:
    """
    Ordena vagas por mais recentes primeiro.
    
    Args:
        jobs: Lista de vagas
        
    Returns:
        Lista ordenada por data (mais recentes primeiro)
    """
    return sorted(
        jobs,
        key=lambda x: parse_relative_date(x.get("data_publicacao", ""))
    )


def filter_by_keywords(jobs: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Filtra vagas que contêm palavras-chave no título.
    
    Args:
        jobs: Lista de vagas
        keywords: Palavras-chave para filtrar
        
    Returns:
        Lista filtrada
    """
    if not keywords:
        return jobs

    filtered = []
    keywords_lower = [kw.lower() for kw in keywords]

    for job in jobs:
        title = job.get("titulo", "").lower()
        if any(kw in title for kw in keywords_lower):
            filtered.append(job)

    return filtered


def filter_recent_only(jobs: List[Dict], max_days: int = 30) -> List[Dict]:
    """
    Filtra vagas - remove apenas anos muito antigos (2023 ou antes).
    Aceita vagas com data desconhecida.
    
    Args:
        jobs: Lista de vagas
        max_days: Não usado atualmente (mantido para compatibilidade)
        
    Returns:
        Lista filtrada
    """
    current_year = datetime.now().year  # 2026
    
    filtered = []
    for job in jobs:
        pub_date = str(job.get("data_publicacao", ""))
        
        # Se parece ter ano, verificar se é recente
        if pub_date and len(pub_date) >= 4:
            try:
                # Tentar extrair ano do início (formato YYYY-MM-DD)
                year = int(pub_date[:4])
                # Rejeitar apenas 2023 ou antes
                if year < 2024:
                    continue
            except (ValueError, TypeError):
                pass  # Se não conseguir parsear, aceita a vaga
        
        # Se não tem data ou é recente, aceita
        filtered.append(job)
    
    return filtered


def remove_duplicates(jobs: List[Dict]) -> List[Dict]:
    """
    Remove vagas duplicadas baseado no título e empresa.
    
    Args:
        jobs: Lista de vagas
        
    Returns:
        Lista sem duplicatas
    """
    seen = set()
    unique = []

    for job in jobs:
        key = (
            job.get("titulo", "").lower().strip(),
            job.get("empresa", "").lower().strip()
        )
        if key not in seen:
            seen.add(key)
            unique.append(job)

    return unique


def apply_all_filters(
    jobs: List[Dict],
    max_days: int = 30,
    keywords: List[str] = None
) -> List[Dict]:
    """
    Aplica todos os filtros e ordenação.
    
    Args:
        jobs: Lista de vagas
        max_days: Filtrar vagas dos últimos N dias (default 30)
        keywords: Palavras-chave opcionais para filtrar
        
    Returns:
        Lista filtrada, ordenada e sem duplicatas
    """
    # Pipeline de processamento
    result = remove_duplicates(jobs)
    
    if max_days:
        result = filter_recent_only(result, max_days)
    
    if keywords:
        result = filter_by_keywords(result, keywords)
    
    result = sort_by_date(result)
    
    return result
