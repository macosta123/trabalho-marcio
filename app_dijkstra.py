#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Streamlit para Algoritmo de Dijkstra
Sistema de grafos com randomização e visualização
Inclui múltiplas aplicações práticas do algoritmo
"""

import streamlit as st
import random
from grafo import Grafo
from dijkstra import Dijkstra
from visualizacao import VisualizadorGrafo
from aplicacoes import AplicacoesDijkstra
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Algoritmo de Dijkstra - Aplicações Práticas",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Algoritmo de Dijkstra - Aplicações Práticas")
st.markdown("""
Este sistema demonstra diferentes aplicações do algoritmo de Dijkstra além do caminho mínimo simples.
Explore as abas abaixo para ver casos de uso reais em diferentes contextos.
""")
st.markdown("---")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações do Grafo")
    
    num_vertices = st.slider(
        "Número de Vértices",
        min_value=5,
        max_value=30,
        value=15,
        help="Quantidade de vértices no grafo"
    )
    
    densidade = st.slider(
        "Densidade do Grafo",
        min_value=0.1,
        max_value=0.8,
        value=0.3,
        step=0.05,
        help="Probabilidade de existir aresta entre dois vértices"
    )
    
    peso_min = st.number_input(
        "Peso Mínimo",
        min_value=1,
        max_value=50,
        value=1,
        help="Peso mínimo das arestas"
    )
    
    peso_max = st.number_input(
        "Peso Máximo",
        min_value=1,
        max_value=200,
        value=100,
        help="Peso máximo das arestas"
    )
    
    seed = st.number_input(
        "Seed (para reprodutibilidade)",
        min_value=0,
        value=0,
        help="Seed para randomização (0 = aleatório)"
    )
    
    if st.button("🔄 Gerar Novo Grafo", type="primary"):
        st.session_state['gerar_novo'] = True
    
    st.markdown("---")
    st.markdown("### 📊 Informações")
    st.caption("Este sistema implementa o algoritmo de Dijkstra para encontrar o caminho mínimo entre vértices em um grafo ponderado.")

# Inicializar ou regenerar grafo
if 'grafo' not in st.session_state or st.session_state.get('gerar_novo', False):
    if seed > 0:
        random.seed(seed)
    
    grafo = Grafo(num_vertices, densidade, peso_min, peso_max)
    grafo.garantir_conectividade()
    
    st.session_state['grafo'] = grafo
    st.session_state['dijkstra'] = Dijkstra(grafo)
    st.session_state['visualizador'] = VisualizadorGrafo(grafo)
    st.session_state['aplicacoes'] = AplicacoesDijkstra(grafo)
    st.session_state['gerar_novo'] = False
    st.rerun()

grafo = st.session_state['grafo']
dijkstra = st.session_state['dijkstra']
visualizador = st.session_state['visualizador']
aplicacoes = st.session_state['aplicacoes']

# Abas com diferentes aplicações
aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs([
    "📍 Caminho Mínimo",
    "🌐 Roteamento de Redes",
    "⭐ Centralidade",
    "🚚 Logística",
    "👥 Redes Sociais",
    "💰 Otimização de Custos",
    "📊 Análise de Conectividade"
])

# ============================================
# ABA 1: CAMINHO MÍNIMO (Básico)
# ============================================
with aba1:
    st.header("📍 Caminho Mínimo")
    st.markdown("Aplicação básica: encontrar o caminho mais curto entre dois vértices.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        vertices_disponiveis = list(range(grafo.num_vertices))
        
        origem = st.selectbox(
            "Vértice de Partida (Origem)",
            options=vertices_disponiveis,
            index=0,
            key="aba1_origem"
        )
        
        destino = st.selectbox(
            "Vértice de Destino",
            options=vertices_disponiveis,
            index=min(1, len(vertices_disponiveis) - 1),
            key="aba1_destino"
        )
        
        if st.button("🔍 Calcular Caminho Mínimo", key="aba1_btn"):
            caminho, distancia = dijkstra.encontrar_caminho_minimo(origem, destino)
            
            if caminho is None:
                st.error(f"❌ Não existe caminho entre o vértice {origem} e o vértice {destino}!")
            else:
                st.session_state['aba1_caminho'] = caminho
                st.session_state['aba1_distancia'] = distancia
                st.session_state['aba1_origem'] = origem
                st.session_state['aba1_destino'] = destino
                st.rerun()
        
        if 'aba1_caminho' in st.session_state:
            caminho = st.session_state['aba1_caminho']
            distancia = st.session_state['aba1_distancia']
            
            st.success(f"✅ Caminho encontrado!")
            st.info(f"**Distância Total:** {distancia}")
            caminho_str = " → ".join(str(v) for v in caminho)
            st.markdown(f"**Caminho:** {caminho_str}")
    
    with col2:
        caminho_viz = st.session_state.get('aba1_caminho')
        origem_viz = st.session_state.get('aba1_origem')
        destino_viz = st.session_state.get('aba1_destino')
        distancia_viz = st.session_state.get('aba1_distancia')
        
        fig, ax = plt.subplots(figsize=(10, 8))
        visualizador.visualizar_grafo(
            caminho_minimo=caminho_viz,
            origem=origem_viz,
            destino=destino_viz,
            distancia_total=distancia_viz,
            titulo="Caminho Mínimo",
            ax=ax,
            fig=fig
        )
        st.pyplot(fig)
        plt.close(fig)

# ============================================
# ABA 2: ROTEAMENTO DE REDES
# ============================================
with aba2:
    st.header("🌐 Roteamento de Redes")
    st.markdown("Simula roteamento de pacotes em uma rede de computadores. Os pesos representam latência (ms) entre roteadores.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        vertices_disponiveis = list(range(grafo.num_vertices))
        
        roteador_origem = st.selectbox(
            "Roteador de Origem",
            options=vertices_disponiveis,
            index=0,
            key="aba2_origem"
        )
        
        roteador_destino = st.selectbox(
            "Roteador de Destino",
            options=vertices_disponiveis,
            index=min(1, len(vertices_disponiveis) - 1),
            key="aba2_destino"
        )
        
        if st.button("📡 Calcular Rota", key="aba2_btn"):
            resultado = aplicacoes.roteamento_rede(roteador_origem, roteador_destino)
            st.session_state['aba2_resultado'] = resultado
            st.rerun()
        
        if 'aba2_resultado' in st.session_state:
            resultado = st.session_state['aba2_resultado']
            
            if resultado['sucesso']:
                st.success("✅ Rota encontrada!")
                st.metric("Latência Total", f"{resultado['latencia_total_ms']} ms")
                st.metric("Número de Hops", resultado['numero_hops'])
                
                st.write("**Roteadores no caminho:**")
                st.code(" → ".join(str(r) for r in resultado['roteadores']))
                
                with st.expander("📋 Detalhes dos Hops"):
                    for hop in resultado['hops']:
                        st.write(f"Roteador {hop['de']} → Roteador {hop['para']}: {hop['latencia_ms']} ms")
            else:
                st.error(resultado['mensagem'])
    
    with col2:
        if 'aba2_resultado' in st.session_state and st.session_state['aba2_resultado']['sucesso']:
            resultado = st.session_state['aba2_resultado']
            fig, ax = plt.subplots(figsize=(10, 8))
            visualizador.visualizar_grafo(
                caminho_minimo=resultado['caminho'],
                origem=roteador_origem,
                destino=roteador_destino,
                distancia_total=resultado['latencia_total_ms'],
                titulo="Roteamento de Rede",
                ax=ax,
                fig=fig
            )
            st.pyplot(fig)
            plt.close(fig)

# ============================================
# ABA 3: CENTRALIDADE
# ============================================
with aba3:
    st.header("⭐ Análise de Centralidade")
    st.markdown("Encontra o vértice mais central do grafo (menor soma de distâncias para todos os outros).")
    
    if st.button("🔍 Encontrar Vértice Mais Central", key="aba3_btn"):
        resultado = aplicacoes.encontrar_vertice_mais_central()
        st.session_state['aba3_resultado'] = resultado
        st.rerun()
    
    if 'aba3_resultado' in st.session_state:
        resultado = st.session_state['aba3_resultado']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.success(f"✅ Vértice mais central: **{resultado['vertice_central']}**")
            st.metric("Soma de Distâncias", resultado['soma_distancias'])
            st.metric("Distância Média", f"{resultado['media_distancias']:.2f}")
            
            st.write("**Ranking de centralidade (menor = mais central):**")
            ranking = sorted(resultado['distancias_totais'].items(), key=lambda x: x[1])
            for i, (vertice, soma) in enumerate(ranking[:10], 1):
                marcador = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                st.write(f"{marcador} Vértice {vertice}: {soma}")
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 8))
            visualizador.visualizar_grafo(
                caminho_minimo=None,
                origem=resultado['vertice_central'],
                destino=None,
                distancia_total=None,
                titulo=f"Vértice Central: {resultado['vertice_central']}",
                ax=ax,
                fig=fig
            )
            st.pyplot(fig)
            plt.close(fig)

# ============================================
# ABA 4: LOGÍSTICA
# ============================================
with aba4:
    st.header("🚚 Planejamento de Logística")
    st.markdown("Planeja rotas de entrega a partir de um depósito central. Os pesos representam custo de transporte.")
    
    vertices_disponiveis = list(range(grafo.num_vertices))
    
    deposito = st.selectbox(
        "Depósito Central",
        options=vertices_disponiveis,
        index=0,
        key="aba4_deposito"
    )
    
    destinos = st.multiselect(
        "Pontos de Entrega",
        options=vertices_disponiveis,
        default=[min(1, len(vertices_disponiveis) - 1), min(2, len(vertices_disponiveis) - 1)] if len(vertices_disponiveis) > 2 else [min(1, len(vertices_disponiveis) - 1)],
        key="aba4_destinos"
    )
    
    if st.button("📦 Calcular Rotas de Entrega", key="aba4_btn"):
        if not destinos:
            st.warning("Selecione pelo menos um ponto de entrega!")
        else:
            resultado = aplicacoes.planejamento_logistica(deposito, destinos)
            st.session_state['aba4_resultado'] = resultado
            st.rerun()
    
    if 'aba4_resultado' in st.session_state:
        resultado = st.session_state['aba4_resultado']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.success(f"✅ Planejamento concluído!")
            st.metric("Custo Total", f"{resultado['custo_total']}")
            st.metric("Número de Entregas", resultado['numero_entregas'])
            st.metric("Custo Médio por Entrega", f"{resultado['custo_medio']:.2f}")
            
            st.write("**Rotas de entrega:**")
            for destino, info in resultado['rotas'].items():
                caminho_str = " → ".join(str(v) for v in info['caminho'])
                st.write(f"**Para {destino}:** {caminho_str} (Custo: {info['custo']})")
        
        with col2:
            # Visualizar todas as rotas
            fig, ax = plt.subplots(figsize=(10, 8))
            visualizador.visualizar_grafo(
                caminho_minimo=None,
                origem=deposito,
                destino=None,
                distancia_total=None,
                titulo="Planejamento de Logística",
                ax=ax,
                fig=fig
            )
            st.pyplot(fig)
            plt.close(fig)

# ============================================
# ABA 5: REDES SOCIAIS
# ============================================
with aba5:
    st.header("👥 Análise de Redes Sociais")
    st.markdown("Calcula o grau de separação entre duas pessoas. Os pesos representam força da conexão (menor = mais forte).")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        vertices_disponiveis = list(range(grafo.num_vertices))
        
        pessoa1 = st.selectbox(
            "Pessoa 1",
            options=vertices_disponiveis,
            index=0,
            key="aba5_pessoa1"
        )
        
        pessoa2 = st.selectbox(
            "Pessoa 2",
            options=vertices_disponiveis,
            index=min(1, len(vertices_disponiveis) - 1),
            key="aba5_pessoa2"
        )
        
        if st.button("🔗 Calcular Grau de Separação", key="aba5_btn"):
            resultado = aplicacoes.grau_separacao(pessoa1, pessoa2)
            st.session_state['aba5_resultado'] = resultado
            st.rerun()
        
        if 'aba5_resultado' in st.session_state:
            resultado = st.session_state['aba5_resultado']
            
            if resultado['conectadas']:
                st.success(f"✅ Pessoas conectadas!")
                st.metric("Grau de Separação", resultado['grau_separacao'])
                st.metric("Força da Conexão", resultado['forca_conexao'])
                
                st.write("**Cadeia de amizade:**")
                cadeia = " → ".join(str(p) for p in resultado['cadeia_amizade'])
                st.code(cadeia)
            else:
                st.error(resultado['mensagem'])
    
    with col2:
        if 'aba5_resultado' in st.session_state and st.session_state['aba5_resultado']['conectadas']:
            resultado = st.session_state['aba5_resultado']
            fig, ax = plt.subplots(figsize=(10, 8))
            visualizador.visualizar_grafo(
                caminho_minimo=resultado['caminho'],
                origem=pessoa1,
                destino=pessoa2,
                distancia_total=resultado['forca_conexao'],
                titulo="Rede Social - Grau de Separação",
                ax=ax,
                fig=fig
            )
            st.pyplot(fig)
            plt.close(fig)

# ============================================
# ABA 6: OTIMIZAÇÃO DE CUSTOS
# ============================================
with aba6:
    st.header("💰 Otimização de Custos")
    st.markdown("Calcula o custo mínimo para alcançar todos os vértices a partir de uma origem.")
    
    vertices_disponiveis = list(range(grafo.num_vertices))
    
    origem = st.selectbox(
        "Vértice de Origem",
        options=vertices_disponiveis,
        index=0,
        key="aba6_origem"
    )
    
    if st.button("💵 Calcular Custos", key="aba6_btn"):
        resultado = aplicacoes.otimizar_custos(origem)
        st.session_state['aba6_resultado'] = resultado
        st.rerun()
    
    if 'aba6_resultado' in st.session_state:
        resultado = st.session_state['aba6_resultado']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Custo Total", resultado['custo_total'])
        
        with col2:
            st.metric("Vértices Alcançáveis", resultado['vertices_alcancaveis'])
        
        with col3:
            st.metric("Custo Médio", f"{resultado['custo_medio']:.2f}")
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.write("**Vértice mais distante:**")
            st.info(f"Vértice {resultado['mais_distante']['vertice']}: {resultado['mais_distante']['custo']}")
        
        with col_info2:
            st.write("**Vértice mais próximo:**")
            st.info(f"Vértice {resultado['mais_proximo']['vertice']}: {resultado['mais_proximo']['custo']}")
        
        with st.expander("📋 Distâncias para todos os vértices"):
            for vertice, custo in sorted(resultado['distancias'].items()):
                st.write(f"Vértice {vertice}: {custo}")

# ============================================
# ABA 7: ANÁLISE DE CONECTIVIDADE
# ============================================
with aba7:
    st.header("📊 Análise de Conectividade")
    st.markdown("Analisa métricas globais de conectividade do grafo: diâmetro, raio, distâncias médias, etc.")
    
    if st.button("📈 Analisar Conectividade", key="aba7_btn"):
        resultado = aplicacoes.analisar_conectividade()
        st.session_state['aba7_resultado'] = resultado
        st.rerun()
    
    if 'aba7_resultado' in st.session_state:
        resultado = st.session_state['aba7_resultado']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Diâmetro", resultado['diametro'])
        
        with col2:
            st.metric("Raio", resultado['raio'])
        
        with col3:
            st.metric("Distância Média", f"{resultado['distancia_media']:.2f}")
        
        with col4:
            st.metric("Distância Máxima", resultado['distancia_maxima'])
        
        st.write("**Métricas por vértice:**")
        ranking = sorted(resultado['distancias_por_vertice'].items(), key=lambda x: x[1]['soma'])
        
        for vertice, metricas in ranking[:10]:
            st.write(f"**Vértice {vertice}:** Soma={metricas['soma']}, Média={metricas['media']:.2f}, Máxima={metricas['maxima']}")

# Rodapé
st.markdown("---")
st.caption("💡 **Dica:** Explore as diferentes abas para ver como o algoritmo de Dijkstra é aplicado em contextos reais!")
