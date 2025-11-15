# 📸 Screenshots do Projeto

Este diretório deve conter as capturas de tela para a documentação e apresentação.

## Screenshots Necessários

### 1. Mapa Completo da Rota
**Arquivo:** `01_mapa_completo.png`
- Visão geral mostrando origem e destino
- Linha azul da rota visível
- Ambos os marcadores (verde e vermelho)

### 2. Marcador de Origem (Zoom)
**Arquivo:** `02_marcador_origem.png`
- Zoom no ponto de partida
- Marcador verde visível
- Popup aberto com informações

### 3. Marcador de Destino (Zoom)
**Arquivo:** `03_marcador_destino.png`
- Zoom no ponto de chegada
- Marcador vermelho visível
- Popup aberto mostrando distância e duração

### 4. Execução do Terminal
**Arquivo:** `04_terminal_execucao.png`
- Comando `python rota_google.py`
- Entrada de endereços
- Mensagens de sucesso

### 5. Google Cloud Console
**Arquivo:** `05_google_cloud_apis.png`
- Painel mostrando APIs ativadas
- Geocoding API e Directions API

### 6. Dashboard de Uso
**Arquivo:** `06_api_dashboard.png`
- Gráfico de uso das APIs
- Demonstrar monitoramento

## Como Capturar

### No Linux (usando gnome-screenshot):
```bash
# Tela inteira
gnome-screenshot -f screenshot.png

# Área selecionada
gnome-screenshot -a -f screenshot.png

# Janela específica
gnome-screenshot -w -f screenshot.png
```

### Usando scrot:
```bash
scrot screenshot.png
```

### Usando ImageMagick:
```bash
import screenshot.png
```

## Dimensões Recomendadas

- Resolução: 1920x1080 ou 1280x720
- Formato: PNG (melhor qualidade) ou JPG
- Para apresentação: Redimensionar para ~1280px de largura

## Dicas para Boas Capturas

1. ✅ Maximize a janela do navegador
2. ✅ Remova barras de ferramentas desnecessárias (F11)
3. ✅ Escolha uma rota interessante e clara
4. ✅ Certifique-se de que o texto está legível
5. ✅ Use zoom apropriado no mapa
6. ✅ Capture com boa iluminação (evite reflexos)

## Inserir nas Apresentações

### Markdown:
```markdown
![Descrição da imagem](screenshots/01_mapa_completo.png)
```

### HTML:
```html
<img src="screenshots/01_mapa_completo.png" alt="Mapa Completo" width="800">
```

### PowerPoint/Google Slides:
- Inserir → Imagem → Escolher arquivo
- Redimensionar conforme necessário
