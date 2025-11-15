#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
App Streamlit para rotas com Google Maps API + Folium

Recursos:
- Rota simples (Origem -> Destino)
- Triangulação (Origem -> Intermediário -> Destino via waypoint)
- Triangulação Otimizada (melhor ordem entre B e C):
    - Avalia A->B->C e A->C->B e escolhe a menor duração
- Modo de transporte selecionável (driving / walking / bicycling / transit)
- Visualização interativa com Folium (via streamlit-folium)

Requer variável de ambiente GOOGLE_MAPS_API_KEY (ou arquivo .env)
"""

from __future__ import annotations

import os
import datetime as dt
from typing import Any, Dict, List, Optional, Tuple, cast

import streamlit as st
from streamlit_folium import st_folium

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

import googlemaps
from googlemaps import exceptions as gmaps_exceptions
import folium

# =====================================
# Utilitários compartilhados
# =====================================

def get_gmaps_client() -> Optional[Any]:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return None
    try:
        return googlemaps.Client(key=api_key)
    except Exception:
        return None


def decode_route_overview(rota: Dict[str, Any]) -> List[Tuple[float, float]]:
    """Decodifica a geometria da rota, com fallback para steps."""
    pontos: List[Tuple[float, float]] = []
    try:
        if "overview_polyline" in rota and rota["overview_polyline"].get("points"):
            dec = googlemaps.convert.decode_polyline(rota["overview_polyline"]["points"])  # type: ignore[attr-defined]
            pontos = [(p["lat"], p["lng"]) for p in dec]
            if pontos:
                return pontos
    except Exception:
        pass

    try:
        for leg in rota.get("legs", []):
            for step in leg.get("steps", []):
                poly = step.get("polyline", {}).get("points")
                if not poly:
                    continue
                dec = googlemaps.convert.decode_polyline(poly)  # type: ignore[attr-defined]
                pontos.extend((p["lat"], p["lng"]) for p in dec)
    except Exception:
        pass

    return pontos


def build_map(rota: Dict[str, Any], markers: List[Tuple[float, float, str, str]]) -> folium.Map:
    """Cria um mapa Folium com a rota e os marcadores.

    markers: lista de tuplas (lat, lng, cor, popup_html)
    """
    # Centraliza no primeiro marcador (origem)
    lat0, lng0, _, _ = markers[0]
    mapa = folium.Map(location=[lat0, lng0], zoom_start=13)

    # Marcadores
    for lat, lng, cor, popup in markers:
        folium.Marker(
            location=[lat, lng],
            popup=popup,
            icon=folium.Icon(color=cor)
        ).add_to(mapa)

    # Polyline da rota
    pontos_rota = decode_route_overview(rota)
    if pontos_rota:
        folium.PolyLine(locations=pontos_rota, color="blue", weight=5, opacity=0.7).add_to(mapa)
        try:
            lats = [p[0] for p in pontos_rota]
            lngs = [p[1] for p in pontos_rota]
            sw = [min(lats), min(lngs)]
            ne = [max(lats), max(lngs)]
            mapa.fit_bounds([sw, ne])
        except Exception:
            pass

    return mapa


# =====================================
# Lógica Directions
# =====================================

def geocode(gmaps: Any, s: str) -> Optional[Dict[str, float]]:
    res = gmaps.geocode(s)
    if not res:
        return None
    return res[0]["geometry"]["location"]


def directions_simple(
    gmaps: Any, origem: str, destino: str, mode: str
) -> Optional[Dict[str, Any]]:
    o = geocode(gmaps, origem)
    d = geocode(gmaps, destino)
    if not o or not d:
        return None
    res = gmaps.directions(origin=o, destination=d, mode=mode)
    return res[0] if res else None


def directions_with_waypoint(
    gmaps: Any, origem: str, waypoint: str, destino: str, mode: str
) -> Optional[Dict[str, Any]]:
    o = geocode(gmaps, origem)
    w = geocode(gmaps, waypoint)
    d = geocode(gmaps, destino)
    if not o or not w or not d:
        return None
    res = gmaps.directions(origin=o, destination=d, waypoints=[w], mode=mode)
    return res[0] if res else None


def directions_best_of_two(
    gmaps: Any, origem: str, b: str, c: str, mode: str
) -> Tuple[Optional[Dict[str, Any]], str]:
    """Compara A->B->C e A->C->B e retorna (rota_escolhida, ordem)."""
    rota1 = directions_with_waypoint(gmaps, origem, b, c, mode)
    rota2 = directions_with_waypoint(gmaps, origem, c, b, mode)

    def total_seconds(r: Optional[Dict[str, Any]]) -> float:
        if not r:
            return float("inf")
        try:
            legs = r.get("legs", [])
            return float(sum(l["duration"]["value"] for l in legs))
        except Exception:
            return float("inf")

    s1 = total_seconds(rota1)
    s2 = total_seconds(rota2)

    if s1 <= s2:
        return rota1, "A → B → C"
    return rota2, "A → C → B"


# =====================================
# UI Streamlit
# =====================================

st.set_page_config(page_title="Roteador (Triangulação) - Google Maps", layout="wide")

st.title("🗺️ Planejador de Rotas com Triangulação (Google Maps API)")

with st.sidebar:
    st.header("Configuração")
    api_ok = bool(os.getenv("GOOGLE_MAPS_API_KEY"))
    st.markdown("**API Key**: {}".format("✅ Encontrada" if api_ok else "❌ Não encontrada"))
    st.caption("Defina GOOGLE_MAPS_API_KEY no .env ou no ambiente.")

    mode = st.selectbox(
        "Modo de transporte",
        options=["driving", "walking", "bicycling", "transit"],
        index=0,
        help="Para 'transit', recomenda-se especificar departure_time."
    )
    use_departure = False
    departure_time = None
    if mode == "transit":
        use_departure = st.checkbox("Usar horário de partida (agora)", value=True)
        if use_departure:
            departure_time = dt.datetime.now()

st.markdown("""
Este app permite:
- Rota simples (Origem → Destino)
- Triangulação (Origem → Intermediário → Destino via waypoint)
- Triangulação Otimizada: escolhe automaticamente a melhor ordem entre B e C
""")

client = get_gmaps_client()
if not client:
    st.error("API Key não configurada. Crie um arquivo .env com GOOGLE_MAPS_API_KEY=... ou exporte no ambiente.")
    st.stop()

# Abas de funcionalidade
aba1, aba2, aba3 = st.tabs([
    "Rota Simples",
    "Triangulação (A → B → C)",
    "Triangulação Otimizada (A → B ↔ C)"
])

with aba1:
    st.subheader("Rota Simples")
    c1, c2 = st.columns(2)
    with c1:
        origem = st.text_input("Origem", placeholder="Ex: Maricá, RJ")
    with c2:
        destino = st.text_input("Destino", placeholder="Ex: Niterói, RJ")

    if st.button("Calcular rota simples", type="primary"):
        try:
            kwargs: Dict[str, Any] = {"mode": mode}
            if mode == "transit" and departure_time is not None:
                kwargs["departure_time"] = departure_time
            gm: Any = client
            res = gm.directions(origin=origem, destination=destino, **kwargs)
            if not res:
                st.warning("Nenhuma rota encontrada.")
            else:
                rota = res[0]
                leg = rota["legs"][0]
                dist = leg["distance"]["text"]
                dur = leg["duration"]["text"]
                o_loc = leg["start_location"]
                d_loc = leg["end_location"]
                mapa = build_map(
                    rota,
                    [
                        (o_loc["lat"], o_loc["lng"], "green", f"<b>Origem</b>: {leg.get('start_address','')}") ,
                        (d_loc["lat"], d_loc["lng"], "red", f"<b>Destino</b>: {leg.get('end_address','')}<br>Dist: {dist}<br>Tempo: {dur}")
                    ]
                )
                st.success(f"Distância: {dist} | Duração: {dur}")
                st_folium(mapa, width=1000, height=600)
        except gmaps_exceptions.ApiError as e:
            st.error(f"Erro da API: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

with aba2:
    st.subheader("Triangulação: Origem → Intermediário → Destino")
    c1, c2, c3 = st.columns(3)
    with c1:
        origem_t = st.text_input("Origem (A)", key="tri_origem", placeholder="Ex: Maricá, RJ")
    with c2:
        inter_t = st.text_input("Intermediário (B)", key="tri_inter", placeholder="Ex: São Gonçalo, RJ")
    with c3:
        destino_t = st.text_input("Destino (C)", key="tri_dest", placeholder="Ex: Niterói, RJ")

    if st.button("Calcular triangulação (A→B→C)", type="primary"):
        try:
            kwargs: Dict[str, Any] = {"mode": mode}
            if mode == "transit" and departure_time is not None:
                kwargs["departure_time"] = departure_time
            gm: Any = client
            res = gm.directions(origin=origem_t, destination=destino_t, waypoints=[inter_t], **kwargs)
            if not res:
                st.warning("Nenhuma rota encontrada.")
            else:
                rota = res[0]
                legs = rota["legs"]
                total_dist_m = sum(l["distance"]["value"] for l in legs)
                total_dur_s = sum(l["duration"]["value"] for l in legs)
                dist_txt = f"{total_dist_m/1000:.1f} km"
                dur_txt = f"{int(total_dur_s//60)} mins"
                o_loc = legs[0]["start_location"]
                i_loc = legs[0]["end_location"]  # término da perna A->B
                d_loc = legs[-1]["end_location"]  # término da perna B->C

                mapa = build_map(
                    rota,
                    [
                        (o_loc["lat"], o_loc["lng"], "green", f"<b>Origem</b>: {legs[0].get('start_address','')}") ,
                        (i_loc["lat"], i_loc["lng"], "orange", f"<b>Intermediário</b>: {legs[0].get('end_address','')}") ,
                        (d_loc["lat"], d_loc["lng"], "red", f"<b>Destino</b>: {legs[-1].get('end_address','')}<br>Dist: {dist_txt}<br>Tempo: {dur_txt}")
                    ]
                )
                st.success(f"Distância total: {dist_txt} | Duração total: {dur_txt}")
                st_folium(mapa, width=1000, height=600)
        except gmaps_exceptions.ApiError as e:
            st.error(f"Erro da API: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

with aba3:
    st.subheader("Triangulação Otimizada: melhor ordem entre B e C")
    c1, c2, c3 = st.columns(3)
    with c1:
        origem_o = st.text_input("Origem (A)", key="opt_origem", placeholder="Ex: Maricá, RJ")
    with c2:
        b_o = st.text_input("Ponto B", key="opt_b", placeholder="Ex: São Gonçalo, RJ")
    with c3:
        c_o = st.text_input("Ponto C", key="opt_c", placeholder="Ex: Niterói, RJ")

    if st.button("Calcular melhor ordem (A→B↔C)", type="primary"):
        try:
            # Avaliar A->B->C vs A->C->B
            gm: Any = client
            rota_1 = gm.directions(origin=origem_o, destination=c_o, waypoints=[b_o], mode=mode)
            rota_2 = gm.directions(origin=origem_o, destination=b_o, waypoints=[c_o], mode=mode)
            if not rota_1 and not rota_2:
                st.warning("Nenhuma rota encontrada.")
            else:
                def total_seconds(r: Dict[str, Any]) -> float:
                    legs = r.get("legs", [])
                    try:
                        return float(sum(l["duration"]["value"] for l in legs))
                    except Exception:
                        return float("inf")

                cand: List[Tuple[Dict[str, Any], str]] = []
                if rota_1:
                    cand.append((rota_1[0], "A → B → C"))
                if rota_2:
                    cand.append((rota_2[0], "A → C → B"))

                cand.sort(key=lambda t: total_seconds(t[0]))
                rota, ordem = cand[0]

                legs = rota["legs"]
                total_dist_m = sum(l["distance"]["value"] for l in legs)
                total_dur_s = sum(l["duration"]["value"] for l in legs)
                dist_txt = f"{total_dist_m/1000:.1f} km"
                dur_txt = f"{int(total_dur_s//60)} mins"

                o_loc = legs[0]["start_location"]
                mid_loc = legs[0]["end_location"]
                d_loc = legs[-1]["end_location"]

                mapa = build_map(
                    rota,
                    [
                        (o_loc["lat"], o_loc["lng"], "green", f"<b>Origem</b>: {legs[0].get('start_address','')}") ,
                        (mid_loc["lat"], mid_loc["lng"], "orange", f"<b>Intermediário</b>: {legs[0].get('end_address','')}") ,
                        (d_loc["lat"], d_loc["lng"], "red", f"<b>Destino</b>: {legs[-1].get('end_address','')}<br>Dist: {dist_txt}<br>Tempo: {dur_txt}")
                    ]
                )
                st.success(f"Ordem escolhida: {ordem} | Distância: {dist_txt} | Duração: {dur_txt}")
                st_folium(mapa, width=1000, height=600)
        except gmaps_exceptions.ApiError as e:
            st.error(f"Erro da API: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
