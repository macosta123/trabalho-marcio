#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Grafos com Randomização
Implementa um grafo ponderado com randomização de arestas e pesos
"""

import random
from typing import Dict, List, Tuple, Optional, Set


class Grafo:
    """Classe que representa um grafo ponderado não direcionado."""
    
    def __init__(self, num_vertices: int, densidade: float = 0.3, peso_min: int = 1, peso_max: int = 100):
        """
        Inicializa um grafo com randomização.
        
        Args:
            num_vertices: Número de vértices no grafo
            densidade: Probabilidade de existir aresta entre dois vértices (0.0 a 1.0)
            peso_min: Peso mínimo das arestas
            peso_max: Peso máximo das arestas
        """
        self.num_vertices = num_vertices
        self.vertices = list(range(num_vertices))
        self.arestas: Dict[Tuple[int, int], int] = {}
        self.adjacencia: Dict[int, List[Tuple[int, int]]] = {v: [] for v in self.vertices}
        
        self._gerar_grafo_aleatorio(densidade, peso_min, peso_max)
    
    def _gerar_grafo_aleatorio(self, densidade: float, peso_min: int, peso_max: int) -> None:
        """Gera arestas aleatórias com pesos aleatórios."""
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if random.random() < densidade:
                    peso = random.randint(peso_min, peso_max)
                    self.adicionar_aresta(i, j, peso)
    
    def adicionar_aresta(self, v1: int, v2: int, peso: int) -> None:
        """Adiciona uma aresta entre dois vértices com um peso."""
        if v1 == v2:
            return
        
        # Normaliza para sempre ter tupla ordenada
        aresta = (min(v1, v2), max(v1, v2))
        self.arestas[aresta] = peso
        
        # Adiciona nas listas de adjacência
        self.adjacencia[v1].append((v2, peso))
        self.adjacencia[v2].append((v1, peso))
    
    def obter_peso(self, v1: int, v2: int) -> Optional[int]:
        """Retorna o peso da aresta entre v1 e v2, ou None se não existir."""
        aresta = (min(v1, v2), max(v1, v2))
        return self.arestas.get(aresta)
    
    def obter_vizinhos(self, vertice: int) -> List[Tuple[int, int]]:
        """Retorna lista de (vizinho, peso) para um vértice."""
        return self.adjacencia.get(vertice, [])
    
    def tem_aresta(self, v1: int, v2: int) -> bool:
        """Verifica se existe aresta entre v1 e v2."""
        aresta = (min(v1, v2), max(v1, v2))
        return aresta in self.arestas
    
    def obter_todas_arestas(self) -> List[Tuple[int, int, int]]:
        """Retorna lista de todas as arestas no formato (v1, v2, peso)."""
        return [(v1, v2, peso) for (v1, v2), peso in self.arestas.items()]
    
    def garantir_conectividade(self) -> None:
        """Garante que o grafo seja conexo adicionando arestas mínimas se necessário."""
        # Usa Union-Find para verificar componentes conexos
        parent = list(range(self.num_vertices))
        
        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Processa arestas existentes
        for (v1, v2), _ in self.arestas.items():
            union(v1, v2)
        
        # Adiciona arestas para conectar componentes desconexos
        componentes = {}
        for v in self.vertices:
            comp = find(v)
            if comp not in componentes:
                componentes[comp] = []
            componentes[comp].append(v)
        
        # Conecta componentes
        comps = list(componentes.values())
        for i in range(len(comps) - 1):
            v1 = random.choice(comps[i])
            v2 = random.choice(comps[i + 1])
            peso = random.randint(1, 50)
            self.adicionar_aresta(v1, v2, peso)

