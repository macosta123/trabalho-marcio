# 🗺️ Algoritmo de Dijkstra para Caminho Mínimo

## 📋 Descrição do Projeto

Este projeto implementa o **algoritmo de Dijkstra** para encontrar o caminho mínimo entre vértices distintos em um grafo com arestas ponderadas, conforme as especificações do trabalho.

## ✅ Requisitos Implementados

### Entrega 1: Implementação do Algoritmo (4 pontos)

- ✅ **Algoritmo de Dijkstra (2 pontos)**
  - ✅ Implementação correta do algoritmo (1 ponto)
  - ✅ Classe própria do grupo (`Dijkstra`) (0,5 pontos)
  - ✅ Retorna caminho mínimo e distância (0,5 pontos)

- ✅ **Sistema de Grafos (1,5 pontos)**
  - ✅ Randomização de arestas (0,75 pontos)
  - ✅ Randomização de pesos (0,75 pontos)

- ✅ **Interface Básica (0,5 pontos)**
  - ✅ Seleção de vértices de partida e destino
  - ✅ Funcionalidade básica de entrada/saída

### Entrega 2: Sistema de Visualização (3 pontos)

- ✅ **Visualização do Grafo (1,5 pontos)**
  - ✅ Exibição do grafo com NetworkX (0,75 pontos)
  - ✅ Visualização com matplotlib (0,75 pontos)

- ✅ **Interface Gráfica (1 ponto)**
  - ✅ Streamlit (framework web) funcional (0,5 pontos)
  - ✅ Integração com o algoritmo (0,5 pontos)

- ✅ **Exibição do Caminho (0,5 pontos)**
  - ✅ Destaque visual do caminho mínimo
  - ✅ Mostrar distância total

## 🏗️ Estrutura do Projeto

```
trabalho-marcio/
│
├── grafo.py              # Classe Grafo com randomização
├── dijkstra.py           # Implementação do algoritmo de Dijkstra
├── visualizacao.py       # Visualização com NetworkX e matplotlib
├── app_dijkstra.py       # Interface Streamlit (web)
├── main.py               # Script principal
├── requirements.txt      # Dependências
└── README_DIJKSTRA.md    # Esta documentação
```

## 📦 Instalação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Programa

**Interface Web (Streamlit)**
```bash
streamlit run app_dijkstra.py
```
ou
```bash
python main.py
```

## 🎮 Como Usar

### Interface Web (Streamlit)

1. Execute `streamlit run app_dijkstra.py` ou `python main.py`
2. Abra o navegador em `http://localhost:8501`
3. Configure os parâmetros do grafo na barra lateral:
   - Número de vértices (5-30)
   - Densidade (0.1-0.8)
   - Peso mínimo e máximo
   - Seed (para reprodutibilidade)
4. Clique em "🔄 Gerar Novo Grafo"
5. Selecione o vértice de partida e destino
6. Clique em "🔍 Calcular Caminho Mínimo"
7. Visualize o grafo com o caminho destacado em azul

## 🔧 Componentes Principais

### 1. Classe `Grafo` (`grafo.py`)

Representa um grafo ponderado não direcionado com:
- Randomização de arestas baseada em densidade
- Randomização de pesos das arestas
- Garantia de conectividade

**Métodos principais:**
- `__init__(num_vertices, densidade, peso_min, peso_max)`: Cria grafo aleatório
- `adicionar_aresta(v1, v2, peso)`: Adiciona aresta
- `obter_peso(v1, v2)`: Retorna peso da aresta
- `obter_vizinhos(vertice)`: Retorna vizinhos de um vértice
- `garantir_conectividade()`: Garante que o grafo seja conexo

### 2. Classe `Dijkstra` (`dijkstra.py`)

Implementa o algoritmo de Dijkstra para encontrar caminho mínimo.

**Métodos principais:**
- `encontrar_caminho_minimo(origem, destino)`: Retorna (caminho, distância)
- `obter_distancias_minimas(origem)`: Retorna distâncias para todos os vértices

### 3. Classe `VisualizadorGrafo` (`visualizacao.py`)

Visualiza grafos usando NetworkX e matplotlib.

**Métodos principais:**
- `visualizar_grafo(caminho_minimo, origem, destino, distancia_total)`: Cria visualização
- `mostrar_grafico(...)`: Exibe gráfico na tela
- `salvar_grafico(caminho_arquivo, ...)`: Salva gráfico em arquivo

## 🎨 Visualização

O grafo é visualizado com:
- **Vértices:**
  - 🟢 Verde: Vértice de origem
  - 🔴 Vermelho: Vértice de destino
  - 🔵 Azul claro: Vértices no caminho mínimo
  - ⚪ Cinza: Outros vértices

- **Arestas:**
  - 🔵 Azul (tracejada, espessa): Caminho mínimo
  - ⚪ Cinza (fina): Outras arestas

- **Labels:**
  - Números nos vértices
  - Pesos nas arestas

## 📊 Exemplo de Uso

```python
from grafo import Grafo
from dijkstra import Dijkstra
from visualizacao import VisualizadorGrafo

# Criar grafo com 10 vértices, densidade 0.3, pesos entre 1 e 50
grafo = Grafo(10, densidade=0.3, peso_min=1, peso_max=50)
grafo.garantir_conectividade()

# Criar instância do algoritmo
dijkstra = Dijkstra(grafo)

# Encontrar caminho mínimo entre vértice 0 e 5
caminho, distancia = dijkstra.encontrar_caminho_minimo(0, 5)

print(f"Caminho: {caminho}")
print(f"Distância: {distancia}")

# Visualizar
visualizador = VisualizadorGrafo(grafo)
visualizador.mostrar_grafico(caminho_minimo=caminho, origem=0, destino=5, distancia_total=distancia)
```

## 🧪 Testes

Para testar o algoritmo:

```python
python -c "
from grafo import Grafo
from dijkstra import Dijkstra

grafo = Grafo(10, 0.3, 1, 50)
grafo.garantir_conectividade()
dijkstra = Dijkstra(grafo)

caminho, dist = dijkstra.encontrar_caminho_minimo(0, 5)
print(f'Caminho: {caminho}')
print(f'Distância: {dist}')
"
```

## 📝 Notas Técnicas

- **Complexidade do Dijkstra:** O(n²) para implementação com lista, O((n+m)log n) com heap (usado aqui)
- **Randomização:** A cada execução, um novo grafo é gerado com arestas e pesos aleatórios
- **Conectividade:** O método `garantir_conectividade()` garante que sempre existe caminho entre quaisquer dois vértices

## 🎯 Próximos Passos (Melhorias Futuras)

- [ ] Adicionar animação do algoritmo em execução
- [ ] Comparar com outros algoritmos (A*, Bellman-Ford)
- [ ] Exportar grafo para diferentes formatos
- [ ] Adicionar modo de grafo direcionado
- [ ] Implementar interface para edição manual do grafo

## 👥 Autores

Trabalho desenvolvido conforme especificações do projeto.

## 📄 Licença

Este projeto é para fins educacionais.

