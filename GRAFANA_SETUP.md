# 📊 Guia de Configuração Grafana Cloud - JobPulse

## 🎯 Configuração Rápida (10 minutos)

### Passo 1: Criar Conta Gratuita
1. Acesse: https://grafana.com/auth/sign-up/create-user
2. Escolha o plano "Grafana Cloud Free"
   - ✅ 10.000 métricas/mês
   - ✅ 50GB logs/mês
   - ✅ Retenção de 14 dias
   - ✅ $0/mês para sempre

### Passo 2: Obter Suas Credenciais
Após o cadastro, anote:
- **URL do Grafana**: `https://SUA_ORG.grafana.net`
- **Usuário**: Seu email
- **API Key**: (vamos criar isso)

---

## 🔧 Configurar Prometheus → Grafana

### Opção 1: Remote Write (Recomendado)

1. **No Grafana Cloud:**
   - Vá em: "Configuration" → "Data Sources"
   - Encontre sua instância Prometheus
   - Copie o endpoint "Remote Write"

2. **Criar prometheus.yml:**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'jobpulse'
    static_configs:
      - targets: ['localhost:8000']  # Seu endpoint de métricas

remote_write:
  - url: https://prometheus-SEU_ID.grafana.net/api/prom/push
    basic_auth:
      username: SEU_USUARIO
      password: SUA_API_KEY
```

3. **Executar Prometheus (Docker):**
```bash
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

### Opção 2: Grafana Agent (Mais Fácil!)

1. **Baixar Grafana Agent:**
   - Windows: https://github.com/grafana/agent/releases
   - Extrair para `C:\grafana-agent\`

2. **Criar agent-config.yaml:**
```yaml
server:
  log_level: info

metrics:
  global:
    scrape_interval: 15s
    remote_write:
    - url: https://prometheus-SEU_ID.grafana.net/api/prom/push
      basic_auth:
        username: SEU_USUARIO
        password: SUA_API_KEY

  configs:
  - name: jobpulse
    scrape_configs:
    - job_name: jobpulse_metrics
      static_configs:
      - targets: ['localhost:8000']
```

3. **Executar Agent:**
```bash
grafana-agent-windows-amd64.exe --config.file=agent-config.yaml
```

---

## 📈 Criar Dashboards

### Dashboard 1: Visão Geral JobPulse

**Importar JSON ou criar painéis:**

#### Painel 1: Total de Vagas Coletadas
```promql
sum(jobs_scraped_total)
```
- Visualização: Stat
- Título: "Total de Vagas Coletadas"

#### Painel 2: Vagas por Hora
```promql
rate(jobs_scraped_total[1h])
```
- Visualização: Gráfico
- Título: "Taxa de Vagas Coletadas"

#### Painel 3: Taxa de Sucesso por Fonte
```promql
rate(jobs_scraped_total[5m])
```
- Visualização: Gráfico de barras
- Agrupar por: label `source`

#### Painel 4: Duração do Scraping
```promql
scrape_duration_seconds
```
- Visualização: Heatmap
- Título: "Tempo de Scraping por Fonte"

#### Painel 5: Taxa de Erros
```promql
rate(scrape_errors_total[5m])
```
- Visualização: Gráfico
- Alerta quando > 0.1/s

#### Painel 6: Vagas Ativas
```promql
active_jobs_total
```
- Visualização: Gauge
- Título: "Vagas no Banco de Dados"

---

## 🚨 Configurar Alertas

### Alerta 1: Falhas de Scraper
```yaml
expr: rate(scrape_errors_total[5m]) > 0.5
for: 5m
annotations:
  summary: "Scraper {{ $labels.source }} falhando"
  description: "Taxa de erro acima de 50%"
```

### Alerta 2: Nenhuma Vaga Coletada
```yaml
expr: rate(jobs_scraped_total[30m]) == 0
for: 30m
annotations:
  summary: "Nenhuma vaga coletada em 30 minutos"
```

### Alerta 3: Scraping Lento
```yaml
expr: scrape_duration_seconds > 120
annotations:
  summary: "{{ $labels.source }} levando >2min"
```

---

## 📱 Canais de Notificação

### Discord Webhook
1. No Discord: Configurações do Servidor → Integrações → Webhooks
2. Copiar URL do webhook
3. No Grafana: Alerting → Contact Points → Adicionar Discord
4. Colar URL do webhook

### Telegram
1. No Grafana: Alerting → Contact Points → Adicionar Telegram
2. Adicionar token do bot do seu notificador Telegram existente
3. Adicionar chat ID

---

## 🎯 Verificações Rápidas

**Após a configuração, verificar:**

```bash
# 1. Endpoint de métricas funcionando
curl http://localhost:8000/metrics

# 2. Prometheus coletando (se usando Prometheus)
curl http://localhost:9090/api/v1/targets

# 3. Grafana recebendo dados
# Ir em Grafana → Explore → Query: jobs_scraped_total
```

---

## 🆘 Solução de Problemas

### Métricas não aparecem no Grafana
- ✅ Verificar se agent/Prometheus está rodando
- ✅ Verificar credenciais (usuário/API key)
- ✅ Garantir que servidor de métricas JobPulse está ativo (:8000)
- ✅ Verificar firewall/antivírus

### "No data" nos painéis
- ✅ Aguardar 1-2 minutos para primeira coleta
- ✅ Verificar intervalo de tempo (últimos 15 minutos)
- ✅ Verificar sintaxe da query PromQL

### Problemas com API key
- ✅ Regenerar API key no Grafana Cloud
- ✅ Usar role "Editor", não "Viewer"

---

## 💡 Dicas Profissionais

1. **Use pastas** para organizar dashboards
2. **Variáveis de template** para seleção dinâmica de fonte
3. **Configure refresh** para 30s para visão em tempo real
4. **Exporte dashboards** como JSON para backup
5. **Compartilhe dashboards** via link público

---

## 📊 Exemplo de Dashboard JSON

Posso criar um dashboard JSON pronto para importar se precisar!

**Precisa de ajuda?** É só pedir! Vou te guiar em qualquer etapa. 🚀
