# 🚀 Guia de Deploy - Algoritmo de Dijkstra

## Opções de Deploy para Streamlit

### ✅ Opção 1: Streamlit Cloud (Recomendado - Gratuito)

**Melhor opção para aplicações Streamlit!**

#### Passos:

1. **Acesse:** https://share.streamlit.io/
2. **Faça login** com sua conta GitHub
3. **Clique em "New app"**
4. **Configure:**
   - Repository: `macosta123/trabalho-marcio`
   - Branch: `master`
   - Main file: `app_dijkstra.py`
5. **Clique em "Deploy"**

**Pronto!** Seu app estará online em alguns minutos.

**URL será:** `https://trabalho-marcio.streamlit.app` (ou similar)

---

### ✅ Opção 2: Render (Gratuito)

1. **Acesse:** https://render.com
2. **Crie conta** (pode usar GitHub)
3. **New → Web Service**
4. **Configure:**
   - Repository: `macosta123/trabalho-marcio`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app_dijkstra.py --server.port=$PORT --server.address=0.0.0.0`
   - Environment: Python 3

---

### ✅ Opção 3: Railway (Gratuito com limites)

1. **Acesse:** https://railway.app
2. **New Project → Deploy from GitHub**
3. **Selecione o repositório**
4. **Railway detecta automaticamente** e configura

---

### ✅ Opção 4: Heroku (Pode ter custos)

1. **Crie arquivo `Procfile`:**
```
web: streamlit run app_dijkstra.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Crie arquivo `setup.sh`:**
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. **Deploy via Heroku CLI ou dashboard**

---

## ⚠️ Vercel (Não Recomendado)

O Vercel **não suporta aplicações Python/Streamlit** diretamente. Ele é focado em:
- Next.js
- React
- Vue
- Node.js
- Sites estáticos

Para usar Vercel, você precisaria:
1. Converter o app para uma API REST (Flask/FastAPI)
2. Criar um frontend em React/Next.js
3. Fazer deploy separado

**Isso é muito mais complexo e não vale a pena para este projeto.**

---

## 🎯 Recomendação Final

**Use Streamlit Cloud!** É:
- ✅ Gratuito
- ✅ Oficial do Streamlit
- ✅ Muito fácil de configurar
- ✅ Deploy automático do GitHub
- ✅ Atualizações automáticas

---

## 📝 Checklist para Deploy

Antes de fazer deploy, certifique-se:

- [x] `requirements.txt` está atualizado
- [x] Código está no GitHub
- [x] `app_dijkstra.py` é o arquivo principal
- [ ] Testar localmente: `streamlit run app_dijkstra.py`

---

## 🔧 Configurações Adicionais (Opcional)

### Arquivo `.streamlit/config.toml` (para configurações customizadas)

```toml
[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

### Arquivo `packages.txt` (se precisar de pacotes do sistema)

```
libgomp1
```

---

## 📚 Links Úteis

- Streamlit Cloud: https://share.streamlit.io/
- Documentação Streamlit: https://docs.streamlit.io/
- Render: https://render.com
- Railway: https://railway.app

