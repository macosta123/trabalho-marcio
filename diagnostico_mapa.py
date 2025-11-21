#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para identificar problemas com o mapa real
"""

print("=" * 60)
print("🔍 DIAGNÓSTICO DO MAPA REAL")
print("=" * 60)

# Teste 1: Importações
print("\n1️⃣ Testando importações...")
try:
    import osmnx as ox
    print("   ✅ osmnx importado")
except ImportError as e:
    print(f"   ❌ Erro ao importar osmnx: {e}")
    exit(1)

try:
    import folium
    print("   ✅ folium importado")
except ImportError as e:
    print(f"   ❌ Erro ao importar folium: {e}")
    exit(1)

try:
    from geopy.geocoders import Nominatim
    print("   ✅ geopy importado")
except ImportError as e:
    print(f"   ❌ Erro ao importar geopy: {e}")
    exit(1)

# Teste 2: Criar instância do MapaReal
print("\n2️⃣ Testando criação do MapaReal...")
try:
    from mapa_real import MapaReal
    mapa_real = MapaReal("Maricá, RJ, Brasil")
    print("   ✅ MapaReal criado")
    print(f"   📍 Cidade: {mapa_real.cidade}")
    print(f"   📊 Grafo de ruas: {'Carregado' if mapa_real.grafo_ruas else 'Não carregado'}")
except Exception as e:
    print(f"   ❌ Erro ao criar MapaReal: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Teste 3: Carregar mapa do OpenStreetMap
print("\n3️⃣ Testando carregamento do mapa do OpenStreetMap...")
print("   ⏳ Isso pode levar alguns segundos...")
try:
    sucesso = mapa_real.carregar_mapa()
    if sucesso:
        print("   ✅ Mapa carregado com sucesso!")
        if mapa_real.grafo_ruas:
            num_nos = len(mapa_real.grafo_ruas.nodes())
            num_arestas = len(mapa_real.grafo_ruas.edges())
            print(f"   📊 Nós no grafo: {num_nos}")
            print(f"   📊 Arestas no grafo: {num_arestas}")
        else:
            print("   ⚠️ Mapa carregado mas grafo_ruas é None")
    else:
        print("   ❌ Falha ao carregar mapa")
        print("   💡 Possíveis causas:")
        print("      - Problema de conexão com internet")
        print("      - Timeout ao baixar dados do OpenStreetMap")
        print("      - Cidade não encontrada no OpenStreetMap")
except Exception as e:
    print(f"   ❌ Erro ao carregar mapa: {e}")
    import traceback
    traceback.print_exc()

# Teste 4: Geocodificação
print("\n4️⃣ Testando geocodificação...")
try:
    endereco_teste = "Centro, Maricá, RJ"
    print(f"   📍 Testando endereço: {endereco_teste}")
    coords = mapa_real.geocodificar_endereco(endereco_teste)
    if coords:
        print(f"   ✅ Coordenadas encontradas: {coords}")
    else:
        print("   ❌ Não foi possível geocodificar o endereço")
        print("   💡 Possíveis causas:")
        print("      - Problema de conexão com Nominatim")
        print("      - Rate limit do Nominatim")
        print("      - Endereço não encontrado")
except Exception as e:
    print(f"   ❌ Erro na geocodificação: {e}")
    import traceback
    traceback.print_exc()

# Teste 5: Criar mapa Folium
print("\n5️⃣ Testando criação de mapa Folium...")
try:
    mapa_folium = mapa_real.criar_mapa_folium()
    if mapa_folium:
        print("   ✅ Mapa Folium criado")
        
        # Testa salvar o mapa
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            temp_file = f.name
        
        mapa_folium.save(temp_file)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        os.unlink(temp_file)
        
        if len(html_content) > 100:
            print(f"   ✅ HTML gerado: {len(html_content)} caracteres")
        else:
            print(f"   ⚠️ HTML muito pequeno: {len(html_content)} caracteres")
    else:
        print("   ❌ Falha ao criar mapa Folium")
except Exception as e:
    print(f"   ❌ Erro ao criar mapa Folium: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ DIAGNÓSTICO CONCLUÍDO")
print("=" * 60)

