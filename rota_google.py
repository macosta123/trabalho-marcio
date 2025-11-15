#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Planejador de Rotas com Google Maps API + Folium

Fluxo:
  (Entrada usuário) -> Geocoding -> Directions -> Decodificar polyline -> Folium -> mapa_rota.html

Pré-requisitos:
  - Definir a variável de ambiente GOOGLE_MAPS_API_KEY
	Ex: export GOOGLE_MAPS_API_KEY='SUA_CHAVE_AQUI'
  - Alternativamente, crie um arquivo .env com a linha:
	  GOOGLE_MAPS_API_KEY=xxxxxxxxxxxxxxxx
"""

from __future__ import annotations

import os
import sys
import webbrowser
from typing import Any, Dict, List, Optional, Tuple

try:
	# Carrega .env se disponível (opcional)
	from dotenv import load_dotenv  # type: ignore
	load_dotenv()  # não falha se .env não existir
except Exception:
	# Segue em frente caso python-dotenv não esteja instalado
	pass

import googlemaps
from googlemaps import exceptions as gmaps_exceptions
import folium


# =============================
# FASE 1: CONFIGURAÇÃO DO CLIENTE
# =============================
def configurar_cliente() -> Optional[googlemaps.Client]:
	"""Carrega a API Key do ambiente e inicializa o cliente Google Maps."""
	api_key = os.getenv("GOOGLE_MAPS_API_KEY")
	if not api_key:
		print("Erro: Variável de ambiente 'GOOGLE_MAPS_API_KEY' não definida.")
		print("Dica: export GOOGLE_MAPS_API_KEY='SUA_CHAVE_AQUI' (ou use um arquivo .env)")
		return None

	try:
		return googlemaps.Client(key=api_key)
	except Exception as e:
		print(f"Erro ao criar cliente Google Maps: {e}")
		return None


# =============================
# FASE 2: OBTÉM ROTA (DIRECTIONS API)
# =============================
def _decode_route_overview(rota: Dict[str, Any]) -> List[Tuple[float, float]]:
	"""Decodifica a overview_polyline, com fallback para steps se necessário."""
	pontos: List[Tuple[float, float]] = []

	# 1) Tenta usar overview_polyline
	try:
		if "overview_polyline" in rota and rota["overview_polyline"].get("points"):
			dec = googlemaps.convert.decode_polyline(rota["overview_polyline"]["points"])  # type: ignore[attr-defined]
			pontos = [(p["lat"], p["lng"]) for p in dec]
			if pontos:
				return pontos
	except Exception:
		# tenta fallback
		pass

	# 2) Fallback: concatenar polylines de cada step
	try:
		legs = rota.get("legs", [])
		for leg in legs:
			for step in leg.get("steps", []):
				poly = step.get("polyline", {}).get("points")
				if not poly:
					continue
				dec = googlemaps.convert.decode_polyline(poly)  # type: ignore[attr-defined]
				pontos.extend((p["lat"], p["lng"]) for p in dec)
	except Exception:
		pass

	return pontos


def obter_rota_google(
	gmaps_client: googlemaps.Client,
	origem_str: str,
	destino_str: str,
	mode: str = "driving",
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, float]], Optional[Dict[str, float]]]:
	"""
	Solicita à API Directions a rota entre dois endereços.
	Retorna (rota, loc_origem, loc_destino).
	"""
	try:
		geocode_origem = gmaps_client.geocode(origem_str)
		geocode_destino = gmaps_client.geocode(destino_str)

		if not geocode_origem or not geocode_destino:
			print("Erro: Não foi possível geocodificar um dos endereços.")
			return None, None, None

		loc_origem = geocode_origem[0]["geometry"]["location"]  # {lat: float, lng: float}
		loc_destino = geocode_destino[0]["geometry"]["location"]

		directions_result = gmaps_client.directions(
			origin=loc_origem,
			destination=loc_destino,
			mode=mode,
			alternatives=False,
		)

		if not directions_result:
			print("Erro: Nenhuma rota encontrada entre os locais.")
			return None, None, None

		rota = directions_result[0]
		return rota, loc_origem, loc_destino

	except gmaps_exceptions.ApiError as e:
		print(f"Erro na API do Google Maps: {e}")
		return None, None, None
	except (gmaps_exceptions.Timeout, gmaps_exceptions.TransportError) as e:  # type: ignore[attr-defined]
		print(f"Erro de rede/timeout ao chamar a API: {e}")
		return None, None, None
	except Exception as e:
		print(f"Ocorreu um erro inesperado: {e}")
		return None, None, None


# =============================
# FASE 3: CRIAR MAPA (FOLIUM)
# =============================
def criar_mapa_com_rota(rota: Dict[str, Any], loc_origem: Dict[str, float], loc_destino: Dict[str, float]) -> None:
	"""Cria um arquivo HTML com um mapa Folium interativo mostrando a rota."""
	print("\n--- Gerando Mapa da Rota ---")

	# Extrair informações principais
	try:
		perna = rota["legs"][0]
		distancia = perna["distance"]["text"]
		duracao = perna["duration"]["text"]
		start_address = perna.get("start_address", "Origem")
		end_address = perna.get("end_address", "Destino")
	except (KeyError, IndexError) as e:
		print(f"Erro ao processar os dados da rota: {e}")
		return

	print(f"Distância Total: {distancia}")
	print(f"Duração Estimada: {duracao}")

	# Decodificar geometria
	pontos_rota = _decode_route_overview(rota)
	if not pontos_rota:
		print("Aviso: Não foi possível decodificar a geometria da rota.")
		print("O mapa será criado apenas com marcadores.")

	# Criar mapa centralizado na origem
	mapa = folium.Map(location=[loc_origem["lat"], loc_origem["lng"]], zoom_start=13)

	# Marcadores de início e fim
	folium.Marker(
		location=[loc_origem["lat"], loc_origem["lng"]],
		popup=f"<b>Origem:</b> {start_address}",
		icon=folium.Icon(color="green"),
	).add_to(mapa)

	folium.Marker(
		location=[loc_destino["lat"], loc_destino["lng"]],
		popup=f"<b>Destino:</b> {end_address}<br><b>Dist:</b> {distancia}<br><b>Tempo:</b> {duracao}",
		icon=folium.Icon(color="red"),
	).add_to(mapa)

	# Linha da rota
	if pontos_rota:
		folium.PolyLine(locations=pontos_rota, color="blue", weight=5, opacity=0.7).add_to(mapa)

		# Ajustar bounds para caber a rota
		try:
			lats = [p[0] for p in pontos_rota]
			lngs = [p[1] for p in pontos_rota]
			sw = [min(lats), min(lngs)]  # sudoeste
			ne = [max(lats), max(lngs)]  # nordeste
			mapa.fit_bounds([sw, ne])
		except Exception:
			# Não é crítico se falhar
			pass

	# Salvar e abrir
	nome_arquivo = "mapa_rota.html"
	mapa.save(nome_arquivo)
	print(f"Mapa salvo com sucesso em '{nome_arquivo}'")

	try:
		webbrowser.open(f"file://{os.path.realpath(nome_arquivo)}")
	except Exception:
		print("Não foi possível abrir o navegador automaticamente. Abra o arquivo manualmente.")


# =============================
# FASE 4: MAIN
# =============================
def main() -> None:
	gmaps = configurar_cliente()
	if not gmaps:
		sys.exit(1)

	print("=== Planejador de Rotas (Google Maps API) ===")
	try:
		origem = input("Digite o endereço de PARTIDA: ").strip()
		destino = input("Digite o endereço de CHEGADA: ").strip()
	except (EOFError, KeyboardInterrupt):
		print("\nExecução cancelada pelo usuário.")
		return

	if not origem or not destino:
		print("Erro: Origem e destino são obrigatórios.")
		return

	rota, loc_origem, loc_destino = obter_rota_google(gmaps, origem, destino, mode="driving")

	if rota and loc_origem and loc_destino:
		criar_mapa_com_rota(rota, loc_origem, loc_destino)
	else:
		print("Não foi possível gerar a rota. Verifique os endereços ou sua API Key.")


if __name__ == "__main__":
	main()

