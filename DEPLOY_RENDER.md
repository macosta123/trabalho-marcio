# 🚀 Deploy no Render.com

## Comparação: Render vs Streamlit Cloud

### Streamlit Cloud (Recomendado para Streamlit)
✅ **Vantagens:**
- Feito especificamente para Streamlit
- Deploy automático via GitHub
- Gratuito para projetos públicos
- Suporte nativo a `streamlit-folium`
- Configuração mínima necessária

❌ **Desvantagens:**
- Apenas para aplicações Streamlit
- Limitações de recursos no plano gratuito

### Render.com
✅ **Vantagens:**
- Suporta múltiplos tipos de aplicações
- Mais controle sobre o ambiente
- Planos pagos com mais recursos

❌ **Desvantagens:**
- Requer configuração manual mais complexa
- Pode ter problemas com `streamlit-folium`
- Necessita arquivo de configuração adicional

## 📋 Deploy no Render.com

### 1. Preparar o Projeto

Certifique-se de que o `requirements.txt` está completo:

```txt
networkx>=3.1
matplotlib>=3.8.0
streamlit>=1.39.0
streamlit-folium>=0.20.0
osmnx>=1.6.0
folium>=0.15.1
geopy>=2.4.1
pyproj>=3.6.1
```

### 2. Criar arquivo `render.yaml` (opcional)

```yaml
services:
  - type: web
    name: dijkstra-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app_dijkstra.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.13
```

### 3. Passos no Render.com

1. Acesse [render.com](https://render.com) e crie uma conta
2. Conecte seu repositório GitHub
3. Crie um novo **Web Service**
4. Configure:
   - **Name**: `dijkstra-marcio` (ou outro nome)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app_dijkstra.py --server.port=$PORT --server.address=0.0.0.0`
   - **Instance Type**: Free (ou pago para melhor performance)

### 4. Variáveis de Ambiente (se necessário)

No painel do Render, adicione variáveis de ambiente se necessário:
- `PYTHON_VERSION=3.10.13`

### 5. Deploy

Clique em **Create Web Service** e aguarde o deploy.

## ⚠️ Problemas Comuns no Render

### Problema: Mapa não aparece
**Solução**: O Render pode ter problemas com `streamlit-folium`. O código já tem fallback para HTML.

### Problema: Dependências não instalam
**Solução**: Verifique se todas as dependências estão no `requirements.txt` sem comentários.

### Problema: Timeout no build
**Solução**: OSMnx pode demorar para instalar. Considere usar um plano pago ou aumentar o timeout.

## 🎯 Recomendação

**Para este projeto, recomendo Streamlit Cloud** porque:
1. É feito especificamente para Streamlit
2. Funciona melhor com `streamlit-folium`
3. Deploy mais simples
4. Gratuito para projetos públicos

### Deploy no Streamlit Cloud:

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte com GitHub
3. Selecione o repositório `macosta123/trabalho-marcio`
4. Selecione `app_dijkstra.py` como arquivo principal
5. Clique em **Deploy**

Pronto! O app estará online em alguns minutos.

## 🔧 Melhorias no Código para Render

O código já foi atualizado com:
- ✅ Fallback para exibição de mapa via HTML se `st_folium` falhar
- ✅ Tratamento de erros melhorado
- ✅ Suporte a diferentes ambientes de deploy

