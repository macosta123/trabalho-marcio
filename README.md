# 🗺️ Planejador de Rotas com Google Maps API

## 1. Introdução

Este projeto implementa um sistema de roteamento inteligente que encontra a **rota ótima entre dois endereços** utilizando a API do Google Maps. O objetivo é resolver o problema clássico de pathfinding no mundo real, permitindo que usuários visualizem de forma interativa o melhor caminho entre dois pontos geográficos.

### Problema
Como encontrar o caminho mais eficiente (em termos de distância e tempo) entre dois endereços reais, considerando:
- Ruas e vias disponíveis
- Condições de tráfego
- Regulamentação de trânsito
- Topografia e obstáculos naturais

### Solução
Substituímos algoritmos manuais de pathfinding (como Dijkstra ou A*) pela **Google Maps Directions API**, que já incorpora dados atualizados e complexos algoritmos de otimização. O resultado é apresentado em um mapa interativo usando **Folium**.

---

## 2. Metodologia

### 2.1. Ferramentas Utilizadas

| Ferramenta | Descrição |
|------------|-----------|
| **Python 3.x** | Linguagem de programação principal |
| **Google Cloud Platform** | Plataforma para acesso às APIs do Google Maps |
| **googlemaps** | Cliente Python oficial para Google Maps APIs |
| **Folium** | Biblioteca Python para criação de mapas interativos (Leaflet.js) |
| **webbrowser** | Módulo nativo para abrir o mapa gerado |

### 2.2. APIs do Google Maps Utilizadas

#### **Geocoding API**
- **Função**: Converte endereços de texto em coordenadas geográficas (latitude/longitude)
- **Uso**: Transformar "Maricá, RJ" em `{lat: -22.9194, lng: -42.8186}`

#### **Directions API**
- **Função**: Calcula a rota de navegação entre dois pontos
- **Retorna**:
  - Caminho otimizado (polyline codificada)
  - Distância total (km)
  - Duração estimada (minutos)
  - Instruções passo a passo

### 2.3. Fluxo de Dados

```
┌─────────────────┐
│ Input Usuário   │
│ (Origem/Destino)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Geocoding API   │ ← Converte strings em coordenadas
│ (Google Maps)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Directions API  │ ← Calcula rota ótima
│ (Google Maps)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ JSON Response   │
│ • Polyline      │ ← Geometria da rota codificada
│ • Distância     │
│ • Duração       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Decodificação   │ ← Converte polyline em pontos lat/lng
│ Polyline        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Folium          │ ← Renderiza mapa interativo HTML
│ • Marcadores    │
│ • Linha da Rota │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ mapa_rota.html  │ ← Arquivo final (navegador)
└─────────────────┘
```

### 2.4. Estrutura do Código

O programa está dividido em **4 fases principais**:

#### **Fase 1: Configuração do Cliente**
```python
configurar_cliente()
```
- Carrega a API Key da variável de ambiente
- Inicializa o cliente `googlemaps`
- Valida credenciais

#### **Fase 2: Obter Rota**
```python
obter_rota_google(gmaps_client, origem_str, destino_str)
```
- Geocodifica origem e destino
- Solicita direções à API
- Retorna dados da rota (JSON)

#### **Fase 3: Criar Mapa**
```python
criar_mapa_com_rota(rota, loc_origem, loc_destino)
```
- Decodifica a polyline
- Cria mapa Folium
- Adiciona marcadores (verde=origem, vermelho=destino)
- Desenha a rota em azul
- Salva como HTML

#### **Fase 4: Main**
```python
main()
```
- Orquestra o fluxo completo
- Gerencia entrada do usuário
- Abre o mapa no navegador

---

## 3. Instalação e Configuração

### 3.1. Pré-requisitos
- Python 3.7 ou superior
- Conta no Google Cloud Platform
- Chave de API do Google Maps

### 3.2. Configurar API Key

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative as APIs:
   - ✅ Directions API
   - ✅ Geocoding API
   - ✅ Maps JavaScript API (opcional)
4. Crie uma credencial do tipo **API Key**
5. Configure restrições de segurança (IPs, referrers)

### 3.3. Definir Variável de Ambiente

**Linux/macOS:**
```bash
export GOOGLE_MAPS_API_KEY='SUA_CHAVE_AQUI'
```

**Windows (CMD):**
```cmd
set GOOGLE_MAPS_API_KEY=SUA_CHAVE_AQUI
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_MAPS_API_KEY="SUA_CHAVE_AQUI"
```

### 3.4. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3.5. Executar o Programa

```bash
python rota_google.py
```

---

## 4. Uso do Sistema

### Exemplo de Execução

```
=== Planejador de Rotas (Google Maps API) ===
Digite o endereço de PARTIDA: Maricá, RJ
Digite o endereço de CHEGADA: Niterói, RJ

--- Gerando Mapa da Rota ---
Distância Total: 45.3 km
Duração Estimada: 52 mins
Mapa salvo com sucesso em 'mapa_rota.html'
```

### Recursos do Mapa Gerado

- 🟢 **Marcador Verde**: Ponto de origem
- 🔴 **Marcador Vermelho**: Ponto de destino
- 🔵 **Linha Azul**: Rota otimizada
- 🖱️ **Interativo**: Zoom, pan, clique nos marcadores
- 📊 **Informações**: Distância e duração no popup

---

## 5. Resultados

### 5.1. Exemplo de Rota: Maricá → Niterói

**Dados Retornados:**
- **Distância**: ~45 km
- **Duração**: ~52 minutos
- **Modo**: Carro (driving)

**Visualização:**
O mapa `mapa_rota.html` mostra:
1. A rota otimizada pela BR-101
2. Marcadores nos pontos inicial e final
3. Polyline azul indicando o caminho exato
4. Interface responsiva e interativa

### 5.2. Capturas de Tela

*[Screenshot 1: Visão geral da rota completa]*
- Mostra ambos os marcadores e a linha completa da rota

*[Screenshot 2: Zoom no ponto de origem]*
- Detalhe do marcador verde com popup de informações

*[Screenshot 3: Zoom no ponto de destino]*
- Detalhe do marcador vermelho com distância e duração

---

## 6. Vantagens da Abordagem

### ✅ Vantagens de Usar a API vs. Algoritmos Manuais

| Aspecto | API Google Maps | Algoritmo Manual (Dijkstra/A*) |
|---------|-----------------|--------------------------------|
| **Dados** | Mapa mundial atualizado | Requer dataset próprio |
| **Precisão** | Alta (considera tráfego real) | Depende da qualidade dos dados |
| **Manutenção** | Zero (gerenciado pelo Google) | Alta (atualizar mapas) |
| **Complexidade** | Simples (chamadas de API) | Alta (implementação complexa) |
| **Custo Computacional** | Baixo (processamento remoto) | Alto (processamento local) |

### 🎯 Casos de Uso

- Aplicativos de navegação
- Sistemas de logística e entregas
- Planejamento de viagens
- Análise de rotas comerciais
- Estudos de mobilidade urbana

---

## 7. Limitações e Considerações

### 7.1. Limitações da API Gratuita
- **Crédito mensal**: $200 USD grátis
- **Após o limite**: Cobrança por requisição
- **Quota**: ~40.000 requisições/mês gratuitas

### 7.2. Segurança
⚠️ **NUNCA** commite a API Key no código!
- Use variáveis de ambiente
- Configure restrições de IP/domínio
- Monitore o uso no Google Cloud Console

### 7.3. Possíveis Melhorias
- [ ] Adicionar seleção de modo de transporte (carro, bicicleta, a pé)
- [ ] Implementar rotas alternativas
- [ ] Adicionar waypoints intermediários
- [ ] Exibir instruções passo a passo
- [ ] Calcular custo estimado (pedágios, combustível)
- [ ] Exportar GPX para GPS

---

## 8. Conclusão

Este projeto demonstra como integrar serviços de geolocalização modernos em aplicações Python, substituindo algoritmos complexos de pathfinding por APIs especializadas. A solução é:

- ✅ **Prática**: Usa dados reais e atualizados
- ✅ **Eficiente**: Aproveita infraestrutura do Google
- ✅ **Escalável**: Fácil de expandir com novas funcionalidades
- ✅ **Educacional**: Ilustra integração de APIs RESTful

A API do Google Maps atua como a "solução de triangulação/pathfinding", fornecendo o caminho ótimo com alta precisão, liberando o desenvolvedor para focar na experiência do usuário e visualização dos dados.

---

## 9. Referências

- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [Directions API Guide](https://developers.google.com/maps/documentation/directions)
- [Geocoding API Guide](https://developers.google.com/maps/documentation/geocoding)
- [googlemaps Python Client](https://github.com/googlemaps/google-maps-services-python)
- [Folium Documentation](https://python-visualization.github.io/folium/)

---

## 📁 Estrutura do Projeto

```
trabalho-marcio/
│
├── rota_google.py          # Script principal
├── requirements.txt        # Dependências Python
├── README.md              # Esta documentação
├── mapa_rota.html         # Mapa gerado (após execução)
│
└── docs/                  # Documentação adicional
    ├── apresentacao.md    # Roteiro da apresentação
    └── screenshots/       # Capturas de tela
```

---

## 👨‍💻 Autor

Diego Silva  
Trabalho de Márcio  
Novembro de 2025

---

## 📄 Licença

Este projeto é para fins educacionais. A API do Google Maps possui termos de uso próprios que devem ser respeitados.
