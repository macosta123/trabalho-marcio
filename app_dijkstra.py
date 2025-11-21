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

# Importação do mapa real
from mapa_real import MapaReal
# Tenta importar streamlit-folium, mas não é obrigatório
try:
    from streamlit_folium import st_folium
    ST_FOLIUM_DISPONIVEL = True
except ImportError:
    ST_FOLIUM_DISPONIVEL = False
    st_folium = None

MAPA_REAL_DISPONIVEL = True

import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para evitar problemas de display
import matplotlib.pyplot as plt
# Configurar matplotlib para evitar problemas de fontes
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

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

# Inicializar mapa real
if MAPA_REAL_DISPONIVEL and 'mapa_real' not in st.session_state:
    st.session_state['mapa_real'] = None

grafo = st.session_state['grafo']
dijkstra = st.session_state['dijkstra']
visualizador = st.session_state['visualizador']
aplicacoes = st.session_state['aplicacoes']

# Abas com diferentes aplicações
abas_nomes = [
    "📍 Caminho Mínimo",
    "🌐 Roteamento de Redes",
    "⭐ Centralidade",
    "🚚 Logística",
    "👥 Redes Sociais",
    "📊 Análise de Conectividade"
]

# Adiciona aba de mapa real apenas se disponível
if MAPA_REAL_DISPONIVEL:
    abas_nomes.append("🗺️ Mapa Real - Maricá")

abas = st.tabs(abas_nomes)
aba1, aba2, aba3, aba4, aba5, aba6 = abas[:6]
if MAPA_REAL_DISPONIVEL:
    aba7 = abas[6]

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
                # Limpa resultados anteriores se não há caminho
                if 'aba1_caminho' in st.session_state:
                    del st.session_state['aba1_caminho']
                if 'aba1_distancia' in st.session_state:
                    del st.session_state['aba1_distancia']
            else:
                st.session_state['aba1_caminho'] = caminho
                st.session_state['aba1_distancia'] = distancia
        
        if 'aba1_caminho' in st.session_state:
            caminho = st.session_state['aba1_caminho']
            distancia = st.session_state['aba1_distancia']
            
            st.success(f"✅ Caminho encontrado!")
            st.info(f"**Distância Total:** {distancia}")
            caminho_str = " → ".join(str(v) for v in caminho)
            st.markdown(f"**Caminho:** {caminho_str}")
    
    with col2:
        caminho_viz = st.session_state.get('aba1_caminho')
        # Usa os valores do selectbox que já estão no session_state via key
        origem_viz = st.session_state.get('aba1_origem', origem)
        destino_viz = st.session_state.get('aba1_destino', destino)
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
        st.write("**Visualização:**")
        fig, ax = plt.subplots(figsize=(10, 8))
        if 'aba2_resultado' in st.session_state and st.session_state['aba2_resultado']['sucesso']:
            resultado = st.session_state['aba2_resultado']
            visualizador.visualizar_grafo(
                caminho_minimo=resultado['caminho'],
                origem=roteador_origem,
                destino=roteador_destino,
                distancia_total=resultado['latencia_total_ms'],
                titulo="Roteamento de Rede",
                ax=ax,
                fig=fig
            )
        else:
            visualizador.visualizar_grafo(
                caminho_minimo=None,
                origem=roteador_origem,
                destino=roteador_destino,
                distancia_total=None,
                titulo="Roteamento de Rede\n(Selecione origem e destino)",
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
            caminhos = [info['caminho'] for info in resultado['rotas'].values()]
            visualizador.visualizar_multiplos_caminhos(
                caminhos=caminhos,
                origem=deposito,
                destinos=destinos,
                titulo=f"Planejamento de Logística\nCusto Total: {resultado['custo_total']}",
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
        st.write("**Visualização:**")
        fig, ax = plt.subplots(figsize=(10, 8))
        if 'aba5_resultado' in st.session_state and st.session_state['aba5_resultado']['conectadas']:
            resultado = st.session_state['aba5_resultado']
            visualizador.visualizar_grafo(
                caminho_minimo=resultado['caminho'],
                origem=pessoa1,
                destino=pessoa2,
                distancia_total=resultado['forca_conexao'],
                titulo="Rede Social - Grau de Separação",
                ax=ax,
                fig=fig
            )
        else:
            visualizador.visualizar_grafo(
                caminho_minimo=None,
                origem=pessoa1,
                destino=pessoa2,
                distancia_total=None,
                titulo="Rede Social\n(Selecione duas pessoas)",
                ax=ax,
                fig=fig
            )
        st.pyplot(fig)
        plt.close(fig)

# ============================================
# ABA 6: ANÁLISE DE CONECTIVIDADE
# ============================================
with aba6:
    st.header("📊 Análise de Conectividade")
    st.markdown("Analisa métricas globais de conectividade do grafo: diâmetro, raio, distâncias médias, etc.")
    
    if st.button("📈 Analisar Conectividade", key="aba7_btn"):
        resultado = aplicacoes.analisar_conectividade()
        st.session_state['aba7_resultado'] = resultado
    
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
        
        col_met1, col_met2 = st.columns([1, 1])
        
        with col_met1:
            st.write("**Métricas por vértice:**")
            ranking = sorted(resultado['distancias_por_vertice'].items(), key=lambda x: x[1]['soma'])
            
            for vertice, metricas in ranking[:10]:
                st.write(f"**Vértice {vertice}:** Soma={metricas['soma']}, Média={metricas['media']:.2f}, Máxima={metricas['maxima']}")
        
        with col_met2:
            st.write("**Visualização do grafo:**")
            fig, ax = plt.subplots(figsize=(10, 8))
            visualizador.visualizar_grafo(
                caminho_minimo=None,
                origem=None,
                destino=None,
                distancia_total=None,
                titulo=f"Análise de Conectividade\nDiâmetro: {resultado['diametro']}, Raio: {resultado['raio']}",
                ax=ax,
                fig=fig
            )
            st.pyplot(fig)
            plt.close(fig)
            
            # Gráfico de barras com soma de distâncias
            st.write("**Soma de distâncias por vértice:**")
            vertices_list = [v for v, _ in ranking[:10]]
            somas_list = [m['soma'] for _, m in ranking[:10]]
            
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.bar(vertices_list, somas_list, color='coral', alpha=0.7)
            ax2.set_xlabel('Vértice')
            ax2.set_ylabel('Soma de Distâncias')
            ax2.set_title('Centralidade (menor = mais central)')
            ax2.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

# ============================================
# ABA 7: MAPA REAL DE MARICÁ (Opcional)
# ============================================
if MAPA_REAL_DISPONIVEL:
    with aba7:
        st.header("🗺️ Navegação em Maricá - Mapa Real")
        st.markdown("""
        Use endereços reais de Maricá para calcular o caminho mais rápido usando o algoritmo de Dijkstra.
        O sistema carrega o mapa real da cidade do OpenStreetMap e calcula rotas baseadas nas ruas reais.
        """)
        
        # Inicializar mapa real
        if 'mapa_real' not in st.session_state:
            with st.spinner("Carregando mapa de Maricá do OpenStreetMap... (pode levar 30-60 segundos)"):
                try:
                    mapa_real = MapaReal("Maricá, RJ, Brasil")
                    if mapa_real.carregar_mapa():
                        if mapa_real.grafo_ruas and len(mapa_real.grafo_ruas.nodes()) > 0:
                            st.session_state['mapa_real'] = mapa_real
                            num_nos = len(mapa_real.grafo_ruas.nodes())
                            num_arestas = len(mapa_real.grafo_ruas.edges())
                            st.success(f"✅ Mapa carregado com sucesso! ({num_nos} nós, {num_arestas} arestas)")
                        else:
                            st.warning("⚠️ Mapa carregado mas grafo está vazio. Criando mapa básico...")
                            # Cria mapa mesmo sem grafo para permitir uso básico
                            st.session_state['mapa_real'] = mapa_real
                    else:
                        st.error("❌ Erro ao carregar mapa do OpenStreetMap.")
                        st.info("💡 Tentando criar mapa básico sem dados de ruas...")
                        # Cria instância mesmo sem grafo para permitir uso básico
                        mapa_real = MapaReal("Maricá, RJ, Brasil")
                        st.session_state['mapa_real'] = mapa_real
                        st.warning("⚠️ Mapa básico criado. Funcionalidade limitada (sem rotas de ruas).")
                except Exception as e:
                    st.error(f"❌ Erro ao inicializar mapa: {str(e)}")
                    with st.expander("🔍 Detalhes do erro (clique para ver)"):
                        import traceback
                        st.code(traceback.format_exc())
                    # Cria instância básica mesmo com erro para não quebrar a interface
                    try:
                        mapa_real = MapaReal("Maricá, RJ, Brasil")
                        st.session_state['mapa_real'] = mapa_real
                        st.warning("⚠️ Mapa básico criado. Funcionalidade limitada.")
                    except:
                        st.session_state['mapa_real'] = None
        
        # Mostra interface mesmo se mapa_real for None ou sem grafo
        mapa_real = st.session_state.get('mapa_real')
        
        if mapa_real is None:
            st.error("❌ Não foi possível inicializar o mapa.")
            st.info("""
            **💡 Soluções:**
            1. Recarregue a página
            2. Verifique sua conexão com a internet
            3. No Streamlit Cloud, verifique os logs em "Manage app" → "Logs"
            """)
            if st.button("🔄 Tentar Novamente", key="retry_mapa"):
                if 'mapa_real' in st.session_state:
                    del st.session_state['mapa_real']
                st.rerun()
        else:
            # Mapa foi inicializado, mostra interface
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📍 Endereços")
                
                # Verifica se o grafo foi carregado
                grafo_carregado = mapa_real.grafo_ruas is not None and len(mapa_real.grafo_ruas.nodes()) > 0
                
                if not grafo_carregado:
                    st.warning("⚠️ **Atenção:** Grafo de ruas não foi carregado. Apenas geocodificação está disponível.")
                    st.info("💡 Você ainda pode geocodificar endereços e ver marcadores no mapa, mas não será possível calcular rotas.")
                
                endereco_origem = st.text_input(
                    "Endereço de Origem",
                    placeholder="Ex: Praça Orlando de Barros Pimentel, Maricá",
                    key="mapa_origem"
                )
                
                endereco_destino = st.text_input(
                    "Endereço de Destino",
                    placeholder="Ex: Praia de Itaipuaçu, Maricá",
                    key="mapa_destino"
                )
                
                if st.button("🔍 Calcular Rota", type="primary", key="mapa_btn", disabled=not grafo_carregado):
                    if not endereco_origem or not endereco_destino:
                        st.warning("Por favor, preencha ambos os endereços!")
                    else:
                        with st.spinner("Geocodificando endereços e calculando rota..."):
                            # Geocodificar origem
                            coords_origem = mapa_real.geocodificar_endereco(endereco_origem)
                            if not coords_origem:
                                st.error(f"Não foi possível encontrar o endereço de origem: {endereco_origem}")
                            else:
                                mapa_real.coordenadas_origem = coords_origem
                                
                                # Geocodificar destino
                                coords_destino = mapa_real.geocodificar_endereco(endereco_destino)
                                if not coords_destino:
                                    st.error(f"Não foi possível encontrar o endereço de destino: {endereco_destino}")
                                else:
                                    mapa_real.coordenadas_destino = coords_destino
                                    
                                    # Só tenta calcular rota se o grafo estiver carregado
                                    if grafo_carregado:
                                        no_origem = mapa_real.encontrar_no_mais_proximo(coords_origem[0], coords_origem[1])
                                        no_destino = mapa_real.encontrar_no_mais_proximo(coords_destino[0], coords_destino[1])
                                        
                                        if no_origem and no_destino:
                                            # Calcular rota com Dijkstra
                                            caminho, distancia_metros = mapa_real.dijkstra_ruas(no_origem, no_destino)
                                            
                                            if caminho:
                                                st.session_state['mapa_caminho'] = caminho
                                                st.session_state['mapa_distancia'] = distancia_metros
                                                st.session_state['mapa_no_origem'] = no_origem
                                                st.session_state['mapa_no_destino'] = no_destino
                                                st.success("✅ Rota calculada com sucesso!")
                                            else:
                                                st.error("❌ Não foi possível encontrar uma rota entre os endereços.")
                                        else:
                                            st.error("❌ Não foi possível encontrar os pontos no mapa.")
                                    else:
                                        # Sem grafo, apenas salva coordenadas para mostrar no mapa
                                        st.session_state['mapa_coords_origem'] = coords_origem
                                        st.session_state['mapa_coords_destino'] = coords_destino
                                        st.info("✅ Endereços geocodificados! (Rotas não disponíveis sem grafo de ruas)")
                
                # Mostrar resultados
                if 'mapa_caminho' in st.session_state:
                    distancia_km = st.session_state['mapa_distancia'] / 1000
                    st.success(f"✅ Rota encontrada!")
                    st.metric("Distância Total", f"{distancia_km:.2f} km")
                    st.metric("Distância em Metros", f"{st.session_state['mapa_distancia']:.0f} m")
                    st.info(f"**Número de segmentos:** {len(st.session_state['mapa_caminho']) - 1}")
            
            with col2:
                st.subheader("🗺️ Mapa Interativo")
                
                # Criar e exibir mapa (método original simples que funcionava)
                try:
                    # Verifica se temos um caminho para mostrar
                    caminho_para_mostrar = None
                    if 'mapa_caminho' in st.session_state and st.session_state['mapa_caminho']:
                        caminho_para_mostrar = st.session_state['mapa_caminho']
                    
                    # Se temos coordenadas mas não caminho (grafo não carregado), adiciona marcadores
                    if not caminho_para_mostrar:
                        if 'mapa_coords_origem' in st.session_state:
                            mapa_real.coordenadas_origem = st.session_state['mapa_coords_origem']
                        if 'mapa_coords_destino' in st.session_state:
                            mapa_real.coordenadas_destino = st.session_state['mapa_coords_destino']
                    
                    # Cria o mapa
                    mapa_folium = mapa_real.criar_mapa_folium(caminho_para_mostrar)
                    
                    # Exibe o mapa usando st_folium (método original que funcionava)
                    if mapa_folium is not None:
                        if ST_FOLIUM_DISPONIVEL and st_folium is not None:
                            # Método original simples
                            st_folium(mapa_folium, width=700, height=500)
                        else:
                            # Fallback para HTML se st_folium não estiver disponível
                            import tempfile
                            import os
                            
                            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                                temp_file = f.name
                            
                            mapa_folium.save(temp_file)
                            
                            with open(temp_file, 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            
                            try:
                                os.unlink(temp_file)
                            except:
                                pass
                            
                            if html_content and len(html_content) > 100:
                                st.components.v1.html(html_content, width=700, height=500, scrolling=False)
                            else:
                                st.error("❌ Erro ao gerar HTML do mapa")
                    else:
                        st.warning("⚠️ Não foi possível criar o mapa.")
                            
                except Exception as e:
                    st.error(f"❌ Erro ao criar/exibir mapa: {str(e)}")
                    with st.expander("🔍 Detalhes do erro"):
                        import traceback
                        st.code(traceback.format_exc())
            
            st.markdown("---")
            st.info("""
            **💡 Dicas:**
            - Use endereços específicos de Maricá para melhores resultados
            - Exemplos: "Praça Orlando de Barros Pimentel", "Praia de Itaipuaçu", "Centro, Maricá"
            - O sistema usa dados do OpenStreetMap e calcula rotas baseadas nas ruas reais
            - O algoritmo de Dijkstra próprio é aplicado no grafo de ruas da cidade
            """)
else:
    # Se mapa real não estiver disponível, mostra mensagem informativa
    if MAPA_REAL_DISPONIVEL == False and len(abas) > 6:
        with abas[6]:
            st.header("🗺️ Mapa Real - Maricá")
            st.info("""
            **Funcionalidade de mapa real não está disponível neste ambiente.**
            
            Para habilitar esta funcionalidade, instale as dependências opcionais:
            ```bash
            pip install osmnx folium geopy pyproj
            ```
            
            **Nota:** Esta funcionalidade requer dependências adicionais que podem não estar disponíveis em todos os ambientes de deploy.
            """)

# Rodapé
st.markdown("---")
st.caption("💡 **Dica:** Explore as diferentes abas para ver como o algoritmo de Dijkstra é aplicado em contextos reais!")
