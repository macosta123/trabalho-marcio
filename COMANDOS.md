# 🔧 Comandos Úteis - Referência Rápida

## 📦 Instalação

### Instalar Dependências
```bash
# Método 1: Usando requirements.txt (recomendado)
pip install -r requirements.txt

# Método 2: Instalação manual
pip install googlemaps==4.10.0
pip install folium==0.15.1

# Verificar instalação
pip list | grep -E 'googlemaps|folium'
```

### Configurar API Key

**Linux/macOS (Bash):**
```bash
# Temporário (sessão atual)
export GOOGLE_MAPS_API_KEY='AIzaSyB1234567890abcdefGHIJKLMNOP'

# Permanente (adicionar ao ~/.bashrc)
echo 'export GOOGLE_MAPS_API_KEY="sua_chave_aqui"' >> ~/.bashrc
source ~/.bashrc

# Verificar
echo $GOOGLE_MAPS_API_KEY
```

**Windows (CMD):**
```cmd
set GOOGLE_MAPS_API_KEY=sua_chave_aqui
echo %GOOGLE_MAPS_API_KEY%
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_MAPS_API_KEY="sua_chave_aqui"
echo $env:GOOGLE_MAPS_API_KEY
```

---

## 🚀 Execução

### Executar Programa Principal
```bash
python rota_google.py
```

### Executar com Python 3 explicitamente
```bash
python3 rota_google.py
```

### Executar Script de Teste
```bash
python test_setup.py
```

---

## 🧪 Testes e Validação

### Testar Importações
```bash
python -c "import googlemaps; import folium; print('OK')"
```

### Verificar Versões
```bash
python -c "import googlemaps; print(googlemaps.__version__)"
python -c "import folium; print(folium.__version__)"
```

### Teste Completo de API
```bash
python -c "
import os
import googlemaps

api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if not api_key:
    print('❌ API Key não definida')
    exit(1)

gmaps = googlemaps.Client(key=api_key)
result = gmaps.geocode('Rio de Janeiro, RJ')
if result:
    print('✅ API funcionando!')
    print(f'Endereço: {result[0][\"formatted_address\"]}')
else:
    print('❌ API retornou vazio')
"
```

---

## 📄 Visualização de Arquivos

### Ver Documentação
```bash
# No terminal (com less)
less README.md

# No navegador
xdg-open README.md       # Linux
open README.md           # macOS
start README.md          # Windows

# Com VS Code
code README.md

# Converter Markdown para HTML (requer pandoc)
pandoc README.md -o README.html
xdg-open README.html
```

### Listar Estrutura do Projeto
```bash
# Com tree (se instalado)
tree -L 3 -I '__pycache__|*.pyc'

# Alternativa com find
find . -type f -o -type d | grep -v '__pycache__' | sort

# Alternativa com ls
ls -R
```

---

## 🗺️ Trabalhar com o Mapa Gerado

### Abrir Mapa
```bash
# Linux
xdg-open mapa_rota.html

# macOS
open mapa_rota.html

# Windows
start mapa_rota.html

# Navegador específico (Firefox)
firefox mapa_rota.html &

# Navegador específico (Chrome)
google-chrome mapa_rota.html &
```

### Ver Tamanho do Arquivo
```bash
ls -lh mapa_rota.html
du -h mapa_rota.html
```

### Remover Mapa Antigo
```bash
rm mapa_rota.html
```

---

## 🔍 Debugging e Diagnóstico

### Verificar Python Instalado
```bash
python --version
python3 --version
which python
which python3
```

### Verificar pip
```bash
pip --version
pip3 --version
which pip
```

### Listar Todos os Pacotes Python
```bash
pip list
pip freeze > installed_packages.txt
```

### Ver Informações de um Pacote
```bash
pip show googlemaps
pip show folium
```

### Testar Conexão com Google APIs
```bash
curl -I https://maps.googleapis.com/maps/api/directions/json
```

### Ver Logs de Execução (se implementado)
```bash
python rota_google.py 2>&1 | tee execucao.log
```

---

## 📸 Screenshots

### Linux (gnome-screenshot)
```bash
# Tela inteira
gnome-screenshot -f screenshot.png

# Área selecionada
gnome-screenshot -a -f area_selecionada.png

# Janela atual
gnome-screenshot -w -f janela.png

# Com atraso de 5 segundos
gnome-screenshot -d 5 -f screenshot.png
```

### Linux (scrot)
```bash
# Tela inteira
scrot screenshot.png

# Área selecionada (clique e arraste)
scrot -s screenshot.png

# Janela ativa
scrot -u screenshot.png
```

### Linux (ImageMagick)
```bash
# Seleção interativa
import screenshot.png

# Janela específica
import -window root screenshot.png
```

### macOS
```bash
# Tela inteira
screencapture screenshot.png

# Área selecionada
screencapture -i screenshot.png

# Janela específica
screencapture -w screenshot.png
```

---

## 🔐 Segurança e Limpeza

### Verificar .gitignore
```bash
cat .gitignore
```

### Ver Arquivos que Seriam Ignorados pelo Git
```bash
git status --ignored
```

### Limpar Cache Python
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
find . -type f -name '*.pyo' -delete
```

### Limpar Arquivos Temporários
```bash
rm -f mapa_rota.html
rm -f test_map.html
rm -f *.log
```

---

## 📦 Criar Arquivo Compactado para Entrega

### Criar ZIP (excluindo arquivos sensíveis)
```bash
zip -r trabalho-marcio.zip . \
  -x "*.pyc" \
  -x "__pycache__/*" \
  -x ".env" \
  -x "mapa_rota.html" \
  -x ".git/*"
```

### Criar TAR.GZ
```bash
tar -czf trabalho-marcio.tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='.env' \
  --exclude='mapa_rota.html' \
  --exclude='.git' \
  .
```

### Verificar Conteúdo do Arquivo
```bash
# ZIP
unzip -l trabalho-marcio.zip

# TAR.GZ
tar -tzf trabalho-marcio.tar.gz
```

---

## 🐛 Solução de Problemas

### Reinstalar Dependências
```bash
pip uninstall googlemaps folium -y
pip install googlemaps folium
```

### Usar Ambiente Virtual (recomendado para evitar conflitos)
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Desativar (quando terminar)
deactivate
```

### Limpar Cache do pip
```bash
pip cache purge
```

### Atualizar pip
```bash
python -m pip install --upgrade pip
```

---

## 📊 Monitoramento de Uso da API

### Ver Uso da API (via gcloud CLI)
```bash
# Instalar Google Cloud SDK primeiro
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Listar projetos
gcloud projects list

# Ver uso de APIs
gcloud services list --enabled --project=SEU_PROJETO_ID
```

### Acesso via Navegador
```bash
# Abrir Dashboard
xdg-open "https://console.cloud.google.com/apis/dashboard"

# Abrir Billing
xdg-open "https://console.cloud.google.com/billing"

# Abrir Credentials
xdg-open "https://console.cloud.google.com/apis/credentials"
```

---

## 📝 Git (se estiver versionando)

### Inicializar Repositório
```bash
git init
git add .
git commit -m "Initial commit: Projeto de roteamento com Google Maps"
```

### Verificar Status
```bash
git status
git log --oneline
```

### Criar Branch para Features
```bash
git checkout -b feature/melhorias
# Fazer modificações
git add .
git commit -m "Adiciona funcionalidade X"
git checkout main
git merge feature/melhorias
```

---

## 🎨 Personalização

### Mudar Cores do Mapa (editar rota_google.py)
```bash
# Abrir no editor
code rota_google.py
nano rota_google.py
vim rota_google.py

# Buscar linhas específicas
grep -n "color=" rota_google.py
```

### Testar Modificações Rapidamente
```bash
# Editar
vim rota_google.py

# Testar
python rota_google.py

# Ver diferenças (se usando git)
git diff rota_google.py
```

---

## 📱 Compartilhamento

### Criar GitHub Gist
```bash
# Instalar gh CLI primeiro
# https://cli.github.com/

gh gist create rota_google.py --public
```

### Enviar para GitHub
```bash
git remote add origin https://github.com/seu-usuario/trabalho-marcio.git
git push -u origin main
```

---

## 🧹 Limpeza Completa

```bash
# Remover todos os arquivos gerados
rm -f mapa_rota.html
rm -f test_map.html
rm -rf __pycache__
find . -name "*.pyc" -delete

# Remover ambiente virtual (se criou)
rm -rf venv/

# Remover logs
rm -f *.log
```

---

## 📖 Ajuda e Documentação

### Ajuda dos Comandos Python
```bash
python --help
pip --help
```

### Documentação Online
```bash
# Abrir documentação do Google Maps
xdg-open "https://developers.google.com/maps/documentation"

# Abrir documentação do Folium
xdg-open "https://python-visualization.github.io/folium/"

# Abrir documentação do Python googlemaps
xdg-open "https://github.com/googlemaps/google-maps-services-python"
```

### Buscar Ajuda no Código
```bash
python -c "import googlemaps; help(googlemaps.Client.directions)"
python -c "import folium; help(folium.Map)"
```

---

## 🎯 Atalhos Úteis

### Criar Alias (Bash)
```bash
# Adicionar ao ~/.bashrc
alias rota='cd "/home/diego-silva/Downloads/trabalho marcio" && python rota_google.py'
alias teste-rota='cd "/home/diego-silva/Downloads/trabalho marcio" && python test_setup.py'

# Recarregar
source ~/.bashrc

# Usar
rota
teste-rota
```

### Script de Inicialização Rápida
```bash
# Criar arquivo start.sh
cat > start.sh << 'EOF'
#!/bin/bash
export GOOGLE_MAPS_API_KEY='sua_chave_aqui'
cd "/home/diego-silva/Downloads/trabalho marcio"
python rota_google.py
EOF

# Dar permissão de execução
chmod +x start.sh

# Executar
./start.sh
```

---

## 📋 Comandos Mais Usados (Top 10)

```bash
# 1. Executar programa
python rota_google.py

# 2. Testar setup
python test_setup.py

# 3. Configurar API Key
export GOOGLE_MAPS_API_KEY='sua_chave'

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Abrir mapa
xdg-open mapa_rota.html

# 6. Ver documentação
less README.md

# 7. Verificar API Key
echo $GOOGLE_MAPS_API_KEY

# 8. Listar arquivos
ls -lh

# 9. Limpar cache
find . -name "*.pyc" -delete

# 10. Ver versão Python
python --version
```

---

**Salve esta página como referência! 🔖**
