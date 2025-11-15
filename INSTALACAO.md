# 🚀 Guia Rápido de Instalação

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Google Cloud Platform
- Navegador web moderno

---

## Passo 1: Clonar/Baixar o Projeto

Se você ainda não tem os arquivos:
```bash
cd ~/Downloads
mkdir "trabalho marcio"
cd "trabalho marcio"
```

---

## Passo 2: Instalar Dependências Python

```bash
pip install -r requirements.txt
```

**Ou instalar manualmente:**
```bash
pip install googlemaps==4.10.0
pip install folium==0.15.1
```

**Verificar instalação:**
```bash
python -c "import googlemaps, folium; print('✅ Dependências OK!')"
```

---

## Passo 3: Obter API Key do Google Maps

### 3.1. Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Select a project"** → **"New Project"**
3. Nome do projeto: `roteamento-maps` (ou qualquer nome)
4. Clique em **"Create"**

### 3.2. Ativar as APIs Necessárias

1. No menu lateral, vá em **"APIs & Services"** → **"Library"**
2. Procure e ative as seguintes APIs:
   - ✅ **Directions API**
   - ✅ **Geocoding API**
   - ✅ **Maps JavaScript API** (opcional)

### 3.3. Criar API Key

1. Vá em **"APIs & Services"** → **"Credentials"**
2. Clique em **"+ CREATE CREDENTIALS"** → **"API Key"**
3. Copie a chave gerada (ex: `AIzaSyB1234567890abcdefGHIJKLMNOP`)
4. (Recomendado) Clique em **"Restrict Key"**:
   - **Application restrictions**: Nenhuma (para testes) ou IP addresses
   - **API restrictions**: Selecione apenas as APIs ativadas acima
5. Salve

### 3.4. Ativar Billing (Obrigatório)

⚠️ **Importante:** Mesmo com $200 de créditos grátis, é preciso cadastrar um cartão.

1. Menu **"Billing"** → **"Link a billing account"**
2. Adicione método de pagamento
3. Você receberá $200 USD gratuitos por mês (suficiente para ~40.000 requisições)

---

## Passo 4: Configurar Variável de Ambiente

### No Linux/macOS (Bash):

**Temporário (apenas sessão atual):**
```bash
export GOOGLE_MAPS_API_KEY='SUA_CHAVE_AQUI'
```

**Permanente (adicionar ao `~/.bashrc` ou `~/.bash_profile`):**
```bash
echo 'export GOOGLE_MAPS_API_KEY="SUA_CHAVE_AQUI"' >> ~/.bashrc
source ~/.bashrc
```

### No Windows (CMD):
```cmd
set GOOGLE_MAPS_API_KEY=SUA_CHAVE_AQUI
```

### No Windows (PowerShell):
```powershell
$env:GOOGLE_MAPS_API_KEY="SUA_CHAVE_AQUI"
```

### Verificar se está configurada:
```bash
echo $GOOGLE_MAPS_API_KEY
```
(Deve exibir sua chave)

---

## Passo 5: Executar o Programa

```bash
cd ~/Downloads/"trabalho marcio"
python rota_google.py
```

**Exemplo de uso:**
```
=== Planejador de Rotas (Google Maps API) ===
Digite o endereço de PARTIDA: Maricá, RJ
Digite o endereço de CHEGADA: Niterói, RJ

--- Gerando Mapa da Rota ---
Distância Total: 45.3 km
Duração Estimada: 52 mins
Mapa salvo com sucesso em 'mapa_rota.html'
```

O navegador abrirá automaticamente com o mapa!

---

## Passo 6: Visualizar o Resultado

O arquivo `mapa_rota.html` será criado no mesmo diretório.

**Para abrir manualmente:**
```bash
# Linux
xdg-open mapa_rota.html

# macOS
open mapa_rota.html

# Windows
start mapa_rota.html
```

---

## 🛠️ Solução de Problemas

### Erro: "Variável de ambiente 'GOOGLE_MAPS_API_KEY' não definida"

**Causa:** API Key não configurada.

**Solução:**
```bash
export GOOGLE_MAPS_API_KEY='sua_chave_aqui'
```

---

### Erro: "This API project is not authorized to use this API"

**Causa:** API não está ativada no projeto.

**Solução:**
1. Acesse Google Cloud Console
2. Vá em APIs & Services → Library
3. Procure "Directions API" e "Geocoding API"
4. Clique em "Enable"

---

### Erro: "The provided API key is invalid"

**Causa:** Chave incorreta ou com restrições muito rígidas.

**Solução:**
1. Verifique se copiou a chave completa
2. No Cloud Console, vá em Credentials
3. Edite a API Key → Remova restrições temporariamente para testar

---

### Erro: "You must enable Billing on the Google Cloud Project"

**Causa:** Billing não está ativado.

**Solução:**
1. Google Cloud Console → Billing
2. Link a billing account
3. Adicione método de pagamento

---

### Erro: `ModuleNotFoundError: No module named 'googlemaps'`

**Causa:** Dependências não instaladas.

**Solução:**
```bash
pip install googlemaps folium
```

---

### Erro: Mapa não abre automaticamente

**Causa:** Comando `webbrowser.open()` pode falhar em alguns ambientes.

**Solução:** Abra manualmente o arquivo `mapa_rota.html` no navegador.

---

### Erro: "Não foi possível geocodificar um dos endereços"

**Causa:** Endereço muito vago ou inexistente.

**Solução:**
- Use endereços mais específicos
- Adicione cidade e estado
- Exemplos válidos:
  - ✅ "Maricá, RJ, Brasil"
  - ✅ "Rua das Flores, 123, Niterói, RJ"
  - ❌ "Casa" (muito vago)

---

## 📊 Monitoramento de Uso da API

1. Acesse Google Cloud Console
2. Vá em **"APIs & Services"** → **"Dashboard"**
3. Visualize gráficos de uso por API
4. Configure alertas de quota

**Dica:** Configure um alerta para ser notificado se ultrapassar 80% da quota gratuita.

---

## 🔒 Segurança da API Key

### ❌ Nunca faça:
- Commitar a chave no Git/GitHub
- Compartilhar em fóruns públicos
- Usar a mesma chave em produção e desenvolvimento
- Deixar sem restrições

### ✅ Sempre faça:
- Use variáveis de ambiente
- Configure restrições de IP ou HTTP referrer
- Monitore o uso regularmente
- Rotacione chaves periodicamente
- Use diferentes chaves para dev/prod

### Exemplo de `.gitignore`:
```
# API Keys
.env
*.key
config/secrets.json

# Arquivos gerados
mapa_rota.html
__pycache__/
*.pyc
```

---

## 🧪 Testar a Instalação

Crie um script de teste simples:

```python
# test_setup.py
import os
import googlemaps
import folium

print("🧪 Testando instalação...")

# 1. Verificar API Key
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if api_key:
    print("✅ API Key encontrada")
else:
    print("❌ API Key não encontrada")
    exit(1)

# 2. Testar cliente Google Maps
try:
    gmaps = googlemaps.Client(key=api_key)
    print("✅ Cliente Google Maps OK")
except Exception as e:
    print(f"❌ Erro ao criar cliente: {e}")
    exit(1)

# 3. Testar Geocoding
try:
    result = gmaps.geocode("Rio de Janeiro, RJ")
    if result:
        print(f"✅ Geocoding OK: {result[0]['formatted_address']}")
    else:
        print("❌ Geocoding retornou vazio")
except Exception as e:
    print(f"❌ Erro no Geocoding: {e}")
    exit(1)

# 4. Testar Folium
try:
    mapa = folium.Map(location=[-22.9068, -43.1729], zoom_start=10)
    print("✅ Folium OK")
except Exception as e:
    print(f"❌ Erro no Folium: {e}")
    exit(1)

print("\n🎉 Tudo OK! Pode executar o programa principal.")
```

Execute:
```bash
python test_setup.py
```

---

## 📚 Próximos Passos

Após a instalação bem-sucedida:

1. ✅ Rode o programa com diferentes endereços
2. ✅ Experimente alterar o modo de transporte (`driving`, `walking`, `bicycling`)
3. ✅ Customize cores e estilos do mapa Folium
4. ✅ Leia a documentação completa no `README.md`
5. ✅ Prepare sua apresentação usando `docs/apresentacao.md`

---

## 🆘 Precisa de Ajuda?

- 📖 Documentação do Google Maps: https://developers.google.com/maps/documentation
- 🐍 Documentação googlemaps Python: https://github.com/googlemaps/google-maps-services-python
- 🗺️ Documentação Folium: https://python-visualization.github.io/folium/
- 💬 Stack Overflow: https://stackoverflow.com/questions/tagged/google-maps-api

---

**Boa sorte com o projeto! 🚀**
