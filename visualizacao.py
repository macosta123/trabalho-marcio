#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Visualização do Grafo
Usa NetworkX e matplotlib para exibir o grafo e o caminho mínimo
"""

import matplotlib
matplotlib.use('Agg')  # Backend não-interativo
import matplotlib.pyplot as plt
# Configurar matplotlib para evitar problemas de fontes
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
import networkx as nx
from typing import List, Optional, Tuple
from grafo import Grafo


class VisualizadorGrafo:
    """Classe para visualizar grafos usando NetworkX e matplotlib."""
    
    def __init__(self, grafo: Grafo):
        """
        Inicializa o visualizador com um grafo.
        
        Args:
            grafo: Instância da classe Grafo
        """
        self.grafo = grafo
        self.nx_grafo = self._criar_nx_grafo()
    
    def _criar_nx_grafo(self) -> nx.Graph:
        """Cria um grafo NetworkX a partir do nosso grafo."""
        G = nx.Graph()
        
        # Adiciona vértices
        G.add_nodes_from(self.grafo.vertices)
        
        # Adiciona arestas com pesos
        for (v1, v2), peso in self.grafo.arestas.items():
            G.add_edge(v1, v2, weight=peso)
        
        return G
    
    def visualizar_grafo(
        self,
        caminho_minimo: Optional[List[int]] = None,
        origem: Optional[int] = None,
        destino: Optional[int] = None,
        distancia_total: Optional[int] = None,
        titulo: str = "Grafo com Caminho Mínimo",
        ax: Optional[plt.Axes] = None,
        fig: Optional[plt.Figure] = None
    ) -> None:
        """
        Visualiza o grafo destacando o caminho mínimo.
        
        Args:
            caminho_minimo: Lista de vértices do caminho mínimo
            origem: Vértice de origem (para destacar)
            destino: Vértice de destino (para destacar)
            distancia_total: Distância total do caminho
            titulo: Título do gráfico
            ax: Eixos matplotlib para desenhar (opcional)
            fig: Figura matplotlib (opcional, usado se ax não fornecido)
        """
        # Se não forneceu ax, cria nova figura ou usa a atual
        if ax is None:
            if fig is None:
                fig = plt.figure(figsize=(12, 8))
                ax = fig.add_subplot(111)
            else:
                fig.clear()
                ax = fig.add_subplot(111)
        
        # Verifica se o grafo tem vértices
        if len(self.nx_grafo.nodes()) == 0:
            ax.text(0.5, 0.5, 'Grafo vazio', ha='center', va='center', transform=ax.transAxes)
            return
        
        # Layout do grafo (usando spring layout para melhor visualização)
        # Ajusta k baseado no número de vértices
        num_vertices = len(self.nx_grafo.nodes())
        k_value = max(1.0, 3.0 / (num_vertices ** 0.5))
        pos = nx.spring_layout(self.nx_grafo, k=k_value, iterations=50, seed=42)
        
        # Desenha todas as arestas (cinza claro)
        nx.draw_networkx_edges(
            self.nx_grafo,
            pos,
            edge_color='lightgray',
            width=1,
            alpha=0.5,
            ax=ax
        )
        
        # Desenha arestas do caminho mínimo (azul, mais espessas)
        if caminho_minimo and len(caminho_minimo) > 1:
            arestas_caminho = [
                (caminho_minimo[i], caminho_minimo[i + 1])
                for i in range(len(caminho_minimo) - 1)
            ]
            nx.draw_networkx_edges(
                self.nx_grafo,
                pos,
                edgelist=arestas_caminho,
                edge_color='blue',
                width=3,
                alpha=0.8,
                style='dashed',
                ax=ax
            )
        
        # Desenha todos os vértices
        cores_vertices = []
        for v in self.nx_grafo.nodes():
            if v == origem:
                cores_vertices.append('green')
            elif v == destino:
                cores_vertices.append('red')
            elif caminho_minimo and v in caminho_minimo:
                cores_vertices.append('lightblue')
            else:
                cores_vertices.append('lightgray')
        
        nx.draw_networkx_nodes(
            self.nx_grafo,
            pos,
            node_color=cores_vertices,
            node_size=500,
            alpha=0.9,
            ax=ax
        )
        
        # Labels dos vértices
        labels = {v: str(v) for v in self.nx_grafo.nodes()}
        nx.draw_networkx_labels(
            self.nx_grafo,
            pos,
            labels,
            font_size=10,
            font_weight='bold',
            ax=ax
        )
        
        # Labels dos pesos das arestas
        edge_labels = {}
        for (v1, v2), peso in self.grafo.arestas.items():
            edge_labels[(v1, v2)] = str(peso)
        
        nx.draw_networkx_edge_labels(
            self.nx_grafo,
            pos,
            edge_labels,
            font_size=8,
            ax=ax
        )
        
        # Título com informações
        titulo_completo = titulo
        if distancia_total is not None:
            titulo_completo += f"\nDistância Total: {distancia_total}"
        
        if ax:
            ax.set_title(titulo_completo, fontsize=14, fontweight='bold')
            ax.axis('off')
        else:
            plt.title(titulo_completo, fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
    
    def visualizar_multiplos_caminhos(
        self,
        caminhos: List[List[int]],
        origem: Optional[int] = None,
        destinos: Optional[List[int]] = None,
        titulo: str = "Grafo com Múltiplos Caminhos",
        ax: Optional[plt.Axes] = None,
        fig: Optional[plt.Figure] = None
    ) -> None:
        """
        Visualiza o grafo destacando múltiplos caminhos (útil para logística).
        
        Args:
            caminhos: Lista de listas de vértices (cada lista é um caminho)
            origem: Vértice de origem comum
            destinos: Lista de vértices de destino
            titulo: Título do gráfico
            ax: Eixos matplotlib
            fig: Figura matplotlib
        """
        if ax is None:
            if fig is None:
                fig = plt.figure(figsize=(12, 8))
                ax = fig.add_subplot(111)
            else:
                fig.clear()
                ax = fig.add_subplot(111)
        
        if len(self.nx_grafo.nodes()) == 0:
            ax.text(0.5, 0.5, 'Grafo vazio', ha='center', va='center', transform=ax.transAxes)
            return
        
        num_vertices = len(self.nx_grafo.nodes())
        k_value = max(1.0, 3.0 / (num_vertices ** 0.5))
        pos = nx.spring_layout(self.nx_grafo, k=k_value, iterations=50, seed=42)
        
        # Desenha todas as arestas (cinza claro)
        nx.draw_networkx_edges(
            self.nx_grafo,
            pos,
            edge_color='lightgray',
            width=1,
            alpha=0.3,
            ax=ax
        )
        
        # Desenha cada caminho com cor diferente
        cores_caminhos = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        vertices_em_caminhos = set()
        
        for idx, caminho in enumerate(caminhos):
            if len(caminho) > 1:
                arestas_caminho = [
                    (caminho[i], caminho[i + 1])
                    for i in range(len(caminho) - 1)
                ]
                cor = cores_caminhos[idx % len(cores_caminhos)]
                nx.draw_networkx_edges(
                    self.nx_grafo,
                    pos,
                    edgelist=arestas_caminho,
                    edge_color=cor,
                    width=3,
                    alpha=0.7,
                    style='dashed',
                    ax=ax
                )
                vertices_em_caminhos.update(caminho)
        
        # Desenha vértices
        cores_vertices = []
        for v in self.nx_grafo.nodes():
            if v == origem:
                cores_vertices.append('green')
            elif destinos and v in destinos:
                cores_vertices.append('red')
            elif v in vertices_em_caminhos:
                cores_vertices.append('lightblue')
            else:
                cores_vertices.append('lightgray')
        
        nx.draw_networkx_nodes(
            self.nx_grafo,
            pos,
            node_color=cores_vertices,
            node_size=500,
            alpha=0.9,
            ax=ax
        )
        
        # Labels
        labels = {v: str(v) for v in self.nx_grafo.nodes()}
        nx.draw_networkx_labels(
            self.nx_grafo,
            pos,
            labels,
            font_size=10,
            font_weight='bold',
            ax=ax
        )
        
        # Labels dos pesos
        edge_labels = {}
        for (v1, v2), peso in self.grafo.arestas.items():
            edge_labels[(v1, v2)] = str(peso)
        
        nx.draw_networkx_edge_labels(
            self.nx_grafo,
            pos,
            edge_labels,
            font_size=8,
            ax=ax
        )
        
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.axis('off')
    
    def salvar_grafico(self, caminho_arquivo: str, caminho_minimo: Optional[List[int]] = None,
                      origem: Optional[int] = None, destino: Optional[int] = None,
                      distancia_total: Optional[int] = None) -> None:
        """
        Salva o gráfico em um arquivo.
        
        Args:
            caminho_arquivo: Caminho do arquivo para salvar
            caminho_minimo: Lista de vértices do caminho mínimo
            origem: Vértice de origem
            destino: Vértice de destino
            distancia_total: Distância total do caminho
        """
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        self.visualizar_grafo(caminho_minimo, origem, destino, distancia_total, ax=ax, fig=fig)
        plt.savefig(caminho_arquivo, dpi=150, bbox_inches='tight')
        plt.close(fig)
    
    def mostrar_grafico(self, caminho_minimo: Optional[List[int]] = None,
                       origem: Optional[int] = None, destino: Optional[int] = None,
                       distancia_total: Optional[int] = None) -> None:
        """
        Mostra o gráfico na tela.
        
        Args:
            caminho_minimo: Lista de vértices do caminho mínimo
            origem: Vértice de origem
            destino: Vértice de destino
            distancia_total: Distância total do caminho
        """
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        self.visualizar_grafo(caminho_minimo, origem, destino, distancia_total, ax=ax, fig=fig)
        plt.tight_layout()
        plt.show()

