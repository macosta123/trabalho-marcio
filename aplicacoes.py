#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo com diferentes aplicações práticas do Algoritmo de Dijkstra
Demonstra casos de uso reais além do caminho mínimo simples
"""

from typing import Dict, List, Tuple, Optional
from dijkstra import Dijkstra
from grafo import Grafo


class AplicacoesDijkstra:
    """Classe com diferentes aplicações práticas do algoritmo de Dijkstra."""
    
    def __init__(self, grafo: Grafo):
        """
        Inicializa as aplicações com um grafo.
        
        Args:
            grafo: Instância da classe Grafo
        """
        self.grafo = grafo
        self.dijkstra = Dijkstra(grafo)
    
    # ============================================
    # 1. ROTEAMENTO DE REDES (Network Routing)
    # ============================================
    def roteamento_rede(self, origem: int, destino: int) -> Dict:
        """
        Simula roteamento de pacotes em uma rede de computadores.
        Os pesos representam latência (ms) entre roteadores.
        
        Args:
            origem: Roteador de origem
            destino: Roteador de destino
            
        Returns:
            Dicionário com informações do roteamento
        """
        caminho, latencia_total = self.dijkstra.encontrar_caminho_minimo(origem, destino)
        
        if caminho is None:
            return {
                'sucesso': False,
                'mensagem': 'Roteadores não conectados'
            }
        
        # Calcular latência por hop
        hops = []
        for i in range(len(caminho) - 1):
            v1, v2 = caminho[i], caminho[i + 1]
            peso = self.grafo.obter_peso(v1, v2)
            hops.append({
                'de': v1,
                'para': v2,
                'latencia_ms': peso
            })
        
        return {
            'sucesso': True,
            'caminho': caminho,
            'latencia_total_ms': latencia_total,
            'numero_hops': len(caminho) - 1,
            'hops': hops,
            'roteadores': caminho
        }
    
    # ============================================
    # 2. ANÁLISE DE CENTRALIDADE (Centrality Analysis)
    # ============================================
    def encontrar_vertice_mais_central(self) -> Dict:
        """
        Encontra o vértice mais central do grafo.
        Centralidade = menor soma de distâncias para todos os outros vértices.
        
        Returns:
            Dicionário com informações do vértice mais central
        """
        melhor_vertice = None
        menor_soma = float('inf')
        distancias_totais = {}
        
        for vertice in self.grafo.vertices:
            distancias = self.dijkstra.obter_distancias_minimas(vertice)
            soma = sum(distancias.values())
            distancias_totais[vertice] = soma
            
            if soma < menor_soma:
                menor_soma = soma
                melhor_vertice = vertice
        
        return {
            'vertice_central': melhor_vertice,
            'soma_distancias': menor_soma,
            'distancias_totais': distancias_totais,
            'media_distancias': menor_soma / (self.grafo.num_vertices - 1) if self.grafo.num_vertices > 1 else 0
        }
    
    # ============================================
    # 3. PLANEJAMENTO DE LOGÍSTICA (Logistics Planning)
    # ============================================
    def planejamento_logistica(self, origem: int, destinos: List[int]) -> Dict:
        """
        Planeja rotas de entrega a partir de um depósito central.
        Os pesos representam custo de transporte entre pontos.
        
        Args:
            origem: Depósito central
            destinos: Lista de pontos de entrega
            
        Returns:
            Dicionário com planejamento de rotas
        """
        rotas = {}
        custo_total = 0
        
        for destino in destinos:
            caminho, custo = self.dijkstra.encontrar_caminho_minimo(origem, destino)
            if caminho:
                rotas[destino] = {
                    'caminho': caminho,
                    'custo': custo,
                    'distancia': len(caminho) - 1
                }
                custo_total += custo
        
        return {
            'deposito': origem,
            'pontos_entrega': destinos,
            'rotas': rotas,
            'custo_total': custo_total,
            'numero_entregas': len(rotas),
            'custo_medio': custo_total / len(rotas) if rotas else 0
        }
    
    # ============================================
    # 4. ANÁLISE DE REDES SOCIAIS (Social Network Analysis)
    # ============================================
    def grau_separacao(self, pessoa1: int, pessoa2: int) -> Dict:
        """
        Calcula o grau de separação entre duas pessoas em uma rede social.
        Os pesos representam força da conexão (menor = mais forte).
        
        Args:
            pessoa1: Primeira pessoa
            pessoa2: Segunda pessoa
            
        Returns:
            Dicionário com informações do grau de separação
        """
        caminho, distancia_total = self.dijkstra.encontrar_caminho_minimo(pessoa1, pessoa2)
        
        if caminho is None:
            return {
                'conectadas': False,
                'grau_separacao': None,
                'mensagem': 'Pessoas não estão conectadas na rede'
            }
        
        grau = len(caminho) - 1
        
        return {
            'conectadas': True,
            'grau_separacao': grau,
            'caminho': caminho,
            'forca_conexao': distancia_total,  # Menor = mais forte
            'cadeia_amizade': caminho
        }
    
    # ============================================
    # 5. OTIMIZAÇÃO DE CUSTOS (Cost Optimization)
    # ============================================
    def otimizar_custos(self, origem: int) -> Dict:
        """
        Calcula o custo mínimo para alcançar todos os vértices a partir de uma origem.
        Útil para planejamento de infraestrutura ou distribuição.
        
        Args:
            origem: Vértice de origem
            
        Returns:
            Dicionário com análise de custos e caminhos
        """
        distancias = self.dijkstra.obter_distancias_minimas(origem)
        
        if not distancias:
            return {
                'origem': origem,
                'custo_total': 0,
                'vertices_alcancaveis': 0,
                'distancias': {},
                'caminhos': {}
            }
        
        custo_total = sum(distancias.values())
        vertices_alcancaveis = len(distancias)
        
        # Encontrar vértice mais distante e mais próximo
        mais_distante = max(distancias.items(), key=lambda x: x[1])
        mais_proximo = min((k, v) for k, v in distancias.items() if k != origem)
        
        # Calcular caminhos mínimos para todos os vértices alcançáveis
        caminhos = {}
        for destino in distancias.keys():
            if destino != origem:
                caminho, _ = self.dijkstra.encontrar_caminho_minimo(origem, destino)
                if caminho:
                    caminhos[destino] = caminho
        
        return {
            'origem': origem,
            'custo_total': custo_total,
            'vertices_alcancaveis': vertices_alcancaveis,
            'custo_medio': custo_total / vertices_alcancaveis if vertices_alcancaveis > 0 else 0,
            'mais_distante': {
                'vertice': mais_distante[0],
                'custo': mais_distante[1]
            },
            'mais_proximo': {
                'vertice': mais_proximo[0],
                'custo': mais_proximo[1]
            },
            'distancias': distancias,
            'caminhos': caminhos
        }
    
    # ============================================
    # 6. ANÁLISE DE CONECTIVIDADE (Connectivity Analysis)
    # ============================================
    def analisar_conectividade(self) -> Dict:
        """
        Analisa a conectividade do grafo.
        Calcula distâncias médias, diâmetro, raio, etc.
        
        Returns:
            Dicionário com métricas de conectividade
        """
        todas_distancias = []
        distancias_por_vertice = {}
        
        for vertice in self.grafo.vertices:
            distancias = self.dijkstra.obter_distancias_minimas(vertice)
            soma = sum(distancias.values())
            distancias_por_vertice[vertice] = {
                'soma': soma,
                'media': soma / len(distancias) if distancias else 0,
                'maxima': max(distancias.values()) if distancias else 0
            }
            todas_distancias.extend(distancias.values())
        
        if not todas_distancias:
            return {
                'grafo_vazio': True
            }
        
        # Calcular métricas globais
        distancia_maxima = max(todas_distancias)
        distancia_minima = min(todas_distancias)
        distancia_media = sum(todas_distancias) / len(todas_distancias)
        
        # Diâmetro = maior distância entre quaisquer dois vértices
        # Raio = menor excentricidade (menor distância máxima de um vértice)
        excentricidades = [distancias_por_vertice[v]['maxima'] for v in self.grafo.vertices]
        raio = min(excentricidades) if excentricidades else 0
        diametro = distancia_maxima
        
        return {
            'numero_vertices': self.grafo.num_vertices,
            'numero_arestas': len(self.grafo.arestas),
            'diametro': diametro,
            'raio': raio,
            'distancia_maxima': distancia_maxima,
            'distancia_minima': distancia_minima,
            'distancia_media': distancia_media,
            'distancias_por_vertice': distancias_por_vertice
        }
    
    # ============================================
    # 7. PLANEJAMENTO DE ROTAS MÚLTIPLAS (Multi-Route Planning)
    # ============================================
    def rotas_multiplas(self, origem: int, destinos: List[int], ordem_otima: bool = True) -> Dict:
        """
        Planeja múltiplas rotas a partir de uma origem.
        Se ordem_otima=True, tenta encontrar a ordem que minimiza o custo total.
        
        Args:
            origem: Ponto de partida
            destinos: Lista de destinos a visitar
            ordem_otima: Se True, tenta otimizar a ordem de visita
            
        Returns:
            Dicionário com planejamento de rotas
        """
        if not destinos:
            return {
                'rotas': [],
                'custo_total': 0
            }
        
        if ordem_otima:
            # Tenta encontrar ordem que minimize custo total
            # Algoritmo simples: nearest neighbor
            rotas = []
            atual = origem
            visitados = set()
            custo_total = 0
            ordem = [origem]
            
            while len(visitados) < len(destinos):
                melhor_destino = None
                menor_custo = float('inf')
                
                for destino in destinos:
                    if destino in visitados:
                        continue
                    
                    caminho, custo = self.dijkstra.encontrar_caminho_minimo(atual, destino)
                    if caminho and custo < menor_custo:
                        menor_custo = custo
                        melhor_destino = destino
                
                if melhor_destino is not None:
                    caminho, custo = self.dijkstra.encontrar_caminho_minimo(atual, melhor_destino)
                    rotas.append({
                        'de': atual,
                        'para': melhor_destino,
                        'caminho': caminho,
                        'custo': custo
                    })
                    custo_total += custo
                    ordem.append(melhor_destino)
                    visitados.add(melhor_destino)
                    atual = melhor_destino
                else:
                    break
            
            return {
                'rotas': rotas,
                'custo_total': custo_total,
                'ordem_visita': ordem,
                'otimizado': True
            }
        else:
            # Visita na ordem fornecida
            rotas = []
            atual = origem
            custo_total = 0
            
            for destino in destinos:
                caminho, custo = self.dijkstra.encontrar_caminho_minimo(atual, destino)
                if caminho:
                    rotas.append({
                        'de': atual,
                        'para': destino,
                        'caminho': caminho,
                        'custo': custo
                    })
                    custo_total += custo
                    atual = destino
            
            return {
                'rotas': rotas,
                'custo_total': custo_total,
                'ordem_visita': [origem] + destinos,
                'otimizado': False
            }

