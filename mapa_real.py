#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para trabalhar com mapas reais usando OpenStreetMap
Adapta o algoritmo de Dijkstra para grafos de ruas reais
"""

import osmnx as ox
import networkx as nx
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Dict, List, Optional, Tuple
import heapq


class MapaReal:
    def get_rotas_alternativas(self, origem: int, destino: int, k: int = 3) -> List[Tuple[List[int], float]]:
        """
        Retorna até k menores caminhos (alternativas) entre origem e destino.
        Cada caminho é uma lista de nós e seu custo total (soma dos pesos).
        """
        if self.grafo_ruas is None:
            return []
        try:
            caminhos = []
            # Usa shortest_simple_paths do networkx
            for path in nx.shortest_simple_paths(self.grafo_ruas, origem, destino, weight='length'):
                # Calcula o custo total do caminho
                custo = 0.0
                for i in range(len(path) - 1):
                    aresta_data = self.grafo_ruas.get_edge_data(path[i], path[i+1])
                    if aresta_data:
                        primeiro_edge = list(aresta_data.values())[0]
                        peso = primeiro_edge.get('length', 0)
                        custo += peso
                caminhos.append((path, custo))
                if len(caminhos) >= k:
                    break
            return caminhos
            except Exception as e:
                print(f"Erro ao calcular rotas alternativas: {e}")
                return []
    """Classe para trabalhar com mapas reais e aplicar Dijkstra."""
    
    def __init__(self, cidade: str = "Maricá, RJ, Brasil"):
        """
        Inicializa o mapa real da cidade.
        
        Args:
            cidade: Nome da cidade (formato: "Cidade, Estado, País")
        """
        self.cidade = cidade
        self.grafo_ruas: Optional[nx.MultiDiGraph] = None
        self.geocoder = Nominatim(user_agent="dijkstra_marica")
        self.coordenadas_origem: Optional[Tuple[float, float]] = None
        self.coordenadas_destino: Optional[Tuple[float, float]] = None
        self.no_origem: Optional[int] = None
        self.no_destino: Optional[int] = None
    
    def carregar_mapa(self) -> bool:
        """
        Carrega o grafo de ruas da cidade do OpenStreetMap.
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            # Busca o grafo de ruas da cidade
            # Usa network_type='drive' para apenas ruas para carros
            self.grafo_ruas = ox.graph_from_place(
                self.cidade,
                network_type='drive'
            )
            
            # Mantém em lat/lon para facilitar geocodificação
            # Não projeta para manter compatibilidade com coordenadas
            
            return True
        except Exception as e:
            print(f"Erro ao carregar mapa: {e}")
            return False
    
    def geocodificar_endereco(self, endereco: str) -> Optional[Tuple[float, float]]:
        """
        Converte um endereço em coordenadas (latitude, longitude).
        
        Args:
            endereco: Endereço como string (ex: "Rua Principal, Maricá")
            
        Returns:
            Tupla (lat, lon) ou None se não encontrou
        """
        try:
            # Adiciona cidade se não estiver no endereço
            if "Maricá" not in endereco and "RJ" not in endereco:
                endereco_completo = f"{endereco}, {self.cidade}"
            else:
                endereco_completo = endereco
            
            location = self.geocoder.geocode(endereco_completo, timeout=10)
            
            if location:
                return (location.latitude, location.longitude)
            return None
        except Exception as e:
            print(f"Erro ao geocodificar: {e}")
            return None
    
    def encontrar_no_mais_proximo(self, lat: float, lon: float) -> Optional[int]:
        """
        Encontra o nó do grafo mais próximo de uma coordenada.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            ID do nó mais próximo ou None
        """
        if self.grafo_ruas is None:
            return None
        
        try:
            # OSMnx nearest_nodes espera (lon, lat) e grafo em EPSG:4326
            no_proximo = ox.distance.nearest_nodes(self.grafo_ruas, lon, lat)
            return no_proximo
        except Exception:
            # Método alternativo: busca manual
            if len(self.grafo_ruas.nodes()) == 0:
                return None
            
            menor_distancia = float('inf')
            no_mais_proximo = None
            
            for no in self.grafo_ruas.nodes():
                no_lat = self.grafo_ruas.nodes[no].get('y')
                no_lon = self.grafo_ruas.nodes[no].get('x')
                
                if no_lat is None or no_lon is None:
                    continue
                
                try:
                    distancia = geodesic((lat, lon), (no_lat, no_lon)).meters
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        no_mais_proximo = no
                except Exception:
                    continue
            
            return no_mais_proximo
    
    def dijkstra_ruas(self, origem: int, destino: int) -> Tuple[Optional[List[int]], Optional[float]]:
        """
        Aplica algoritmo de Dijkstra no grafo de ruas.
        Usa distância real em metros como peso.
        
        Args:
            origem: ID do nó de origem
            destino: ID do nó de destino
            
        Returns:
            Tupla (caminho, distancia_metros)
        """
        if self.grafo_ruas is None:
            return None, None
        
        if origem == destino:
            return [origem], 0.0
        
        # Inicialização
        distancias: Dict[int, float] = {no: float('inf') for no in self.grafo_ruas.nodes()}
        distancias[origem] = 0.0
        
        fila: List[Tuple[float, int]] = [(0.0, origem)]
        heapq.heapify(fila)
        
        predecessores: Dict[int, Optional[int]] = {no: None for no in self.grafo_ruas.nodes()}
        visitados: set = set()
        
        while fila:
            dist_atual, no_atual = heapq.heappop(fila)
            
            if no_atual in visitados:
                continue
            
            visitados.add(no_atual)
            
            if no_atual == destino:
                break
            
            # Explora vizinhos
            for vizinho in self.grafo_ruas.successors(no_atual):
                if vizinho in visitados:
                    continue
                
                # Obtém o comprimento da aresta do OSMnx (já está em metros)
                try:
                    # Tenta pegar o comprimento da aresta diretamente
                    aresta_data = self.grafo_ruas.get_edge_data(no_atual, vizinho)
                    if aresta_data:
                        # Pega o primeiro edge (pode haver múltiplos)
                        primeiro_edge = list(aresta_data.values())[0]
                        distancia = primeiro_edge.get('length', 0)
                        
                        # Se não tiver 'length', calcula geodésica
                        if distancia == 0 or distancia is None:
                            lat1 = self.grafo_ruas.nodes[no_atual].get('y')
                            lon1 = self.grafo_ruas.nodes[no_atual].get('x')
                            lat2 = self.grafo_ruas.nodes[vizinho].get('y')
                            lon2 = self.grafo_ruas.nodes[vizinho].get('x')
                            
                            if lat1 and lon1 and lat2 and lon2:
                                distancia = geodesic((lat1, lon1), (lat2, lon2)).meters
                            else:
                                continue
                    else:
                        # Fallback: calcula geodésica
                        lat1 = self.grafo_ruas.nodes[no_atual].get('y')
                        lon1 = self.grafo_ruas.nodes[no_atual].get('x')
                        lat2 = self.grafo_ruas.nodes[vizinho].get('y')
                        lon2 = self.grafo_ruas.nodes[vizinho].get('x')
                        
                        if lat1 and lon1 and lat2 and lon2:
                            distancia = geodesic((lat1, lon1), (lat2, lon2)).meters
                        else:
                            continue
                    
                    nova_distancia = dist_atual + distancia
                    
                    if nova_distancia < distancias[vizinho]:
                        distancias[vizinho] = nova_distancia
                        predecessores[vizinho] = no_atual
                        heapq.heappush(fila, (nova_distancia, vizinho))
                except Exception as e:
                    # Em caso de erro, tenta calcular geodésica
                    try:
                        lat1 = self.grafo_ruas.nodes[no_atual].get('y')
                        lon1 = self.grafo_ruas.nodes[no_atual].get('x')
                        lat2 = self.grafo_ruas.nodes[vizinho].get('y')
                        lon2 = self.grafo_ruas.nodes[vizinho].get('x')
                        
                        if lat1 and lon1 and lat2 and lon2:
                            distancia = geodesic((lat1, lon1), (lat2, lon2)).meters
                            nova_distancia = dist_atual + distancia
                            
                            if nova_distancia < distancias[vizinho]:
                                distancias[vizinho] = nova_distancia
                                predecessores[vizinho] = no_atual
                                heapq.heappush(fila, (nova_distancia, vizinho))
                    except Exception:
                        continue
        
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
    
    def criar_mapa_folium(self, caminho: Optional[List[int]] = None) -> folium.Map:
        """
        Cria um mapa Folium com o caminho destacado.
        
        Args:
            caminho: Lista de IDs dos nós do caminho
            
        Returns:
            Mapa Folium
        """
        if self.grafo_ruas is None:
            # Mapa vazio centrado em Maricá
            mapa = folium.Map(location=[-22.9194, -42.8186], zoom_start=13)
            return mapa
        
        # Centro do mapa (centro de Maricá)
        centro_lat = -22.9194
        centro_lon = -42.8186
        
        # Se temos coordenadas de origem/destino, usa elas
        if self.coordenadas_origem:
            centro_lat, centro_lon = self.coordenadas_origem
        
        mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=13)
        
        # Desenha o caminho se fornecido, mostrando segmentos e pesos
        if caminho and len(caminho) > 1:
            coordenadas_caminho = []
            for i in range(len(caminho) - 1):
                no_atual = caminho[i]
                no_prox = caminho[i + 1]
                lat1 = self.grafo_ruas.nodes[no_atual].get('y')
                lon1 = self.grafo_ruas.nodes[no_atual].get('x')
                lat2 = self.grafo_ruas.nodes[no_prox].get('y')
                lon2 = self.grafo_ruas.nodes[no_prox].get('x')
                if lat1 and lon1 and lat2 and lon2:
                    # Adiciona segmento
                    folium.PolyLine(
                        [[lat1, lon1], [lat2, lon2]],
                        color='blue',
                        weight=5,
                        opacity=0.7
                    ).add_to(mapa)
                    # Obtém peso (distância)
                    aresta_data = self.grafo_ruas.get_edge_data(no_atual, no_prox)
                    peso = None
                    if aresta_data:
                        primeiro_edge = list(aresta_data.values())[0]
                        peso = primeiro_edge.get('length', None)
                    # Adiciona popup no meio do segmento
                    latm = (lat1 + lat2) / 2
                    lonm = (lon1 + lon2) / 2
                    popup_text = f"Segmento: {no_atual} → {no_prox}<br>Distância: {peso:.1f} m" if peso else f"Segmento: {no_atual} → {no_prox}"
                    folium.Marker(
                        location=[latm, lonm],
                        popup=popup_text,
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(mapa)
        
        # Marca origem
        if self.coordenadas_origem:
            folium.Marker(
                location=self.coordenadas_origem,
                popup="Origem",
                icon=folium.Icon(color='green')
            ).add_to(mapa)
        
        # Marca destino
        if self.coordenadas_destino:
            folium.Marker(
                location=self.coordenadas_destino,
                popup="Destino",
                icon=folium.Icon(color='red')
            ).add_to(mapa)
        
        return mapa

