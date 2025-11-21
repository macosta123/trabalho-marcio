#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementação do Algoritmo de Dijkstra para Caminho Mínimo
Classe própria do grupo para encontrar o caminho mínimo entre vértices
"""

import heapq
from typing import Dict, List, Optional, Tuple
from grafo import Grafo


class Dijkstra:
    """Classe que implementa o algoritmo de Dijkstra para encontrar caminho mínimo."""
    
    def __init__(self, grafo: Grafo):
        """
        Inicializa o algoritmo de Dijkstra com um grafo.
        
        Args:
            grafo: Instância da classe Grafo
        """
        self.grafo = grafo
    
    def encontrar_caminho_minimo(self, origem: int, destino: int) -> Tuple[Optional[List[int]], Optional[int]]:
        """
        Encontra o caminho mínimo entre origem e destino usando Dijkstra.
        
        Args:
            origem: Vértice de partida
            destino: Vértice de destino
            
        Returns:
            Tupla (caminho, distancia_total):
            - caminho: Lista de vértices do caminho mínimo, ou None se não houver caminho
            - distancia_total: Distância total do caminho, ou None se não houver caminho
        """
        if origem == destino:
            return [origem], 0
        
        if origem < 0 or origem >= self.grafo.num_vertices:
            return None, None
        
        if destino < 0 or destino >= self.grafo.num_vertices:
            return None, None
        
        # Inicialização
        distancias: Dict[int, int] = {v: float('inf') for v in self.grafo.vertices}
        distancias[origem] = 0
        
        # Fila de prioridade: (distancia, vertice)
        fila: List[Tuple[int, int]] = [(0, origem)]
        heapq.heapify(fila)
        
        # Para reconstruir o caminho
        predecessores: Dict[int, Optional[int]] = {v: None for v in self.grafo.vertices}
        visitados: set = set()
        
        while fila:
            dist_atual, vertice_atual = heapq.heappop(fila)
            
            # Se já visitamos este vértice com distância menor, ignora
            if vertice_atual in visitados:
                continue
            
            visitados.add(vertice_atual)
            
            # Se chegamos ao destino, podemos parar
            if vertice_atual == destino:
                break
            
            # Explora vizinhos
            for vizinho, peso in self.grafo.obter_vizinhos(vertice_atual):
                if vizinho in visitados:
                    continue
                
                nova_distancia = dist_atual + peso
                
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = vertice_atual
                    heapq.heappush(fila, (nova_distancia, vizinho))
        
        # Reconstruir caminho
        if distancias[destino] == float('inf'):
            return None, None
        
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = predecessores[atual]
        
        caminho.reverse()
        distancia_total = distancias[destino]
        
        return caminho, distancia_total
    
    def obter_distancias_minimas(self, origem: int) -> Dict[int, int]:
        """
        Retorna um dicionário com as distâncias mínimas de origem para todos os vértices.
        
        Args:
            origem: Vértice de partida
            
        Returns:
            Dicionário {vertice: distancia_minima}
        """
        if origem < 0 or origem >= self.grafo.num_vertices:
            return {}
        
        distancias: Dict[int, int] = {v: float('inf') for v in self.grafo.vertices}
        distancias[origem] = 0
        
        fila: List[Tuple[int, int]] = [(0, origem)]
        heapq.heapify(fila)
        visitados: set = set()
        
        while fila:
            dist_atual, vertice_atual = heapq.heappop(fila)
            
            if vertice_atual in visitados:
                continue
            
            visitados.add(vertice_atual)
            
            for vizinho, peso in self.grafo.obter_vizinhos(vertice_atual):
                if vizinho in visitados:
                    continue
                
                nova_distancia = dist_atual + peso
                
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    heapq.heappush(fila, (nova_distancia, vizinho))
        
        # Converte float('inf') para None para vértices inalcançáveis
        resultado = {}
        for v, d in distancias.items():
            if d != float('inf'):
                resultado[v] = int(d)
        
        return resultado

