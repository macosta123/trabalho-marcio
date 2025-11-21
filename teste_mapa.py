#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se o mapa Folium funciona
"""

import folium
import tempfile
import os

print("🧪 Testando criação de mapa Folium...")

# Cria um mapa simples
mapa = folium.Map(location=[-22.9194, -42.8186], zoom_start=13)

# Adiciona um marcador
folium.Marker(
    location=[-22.9194, -42.8186],
    popup="Maricá",
    icon=folium.Icon(color='green')
).add_to(mapa)

print("✅ Mapa criado com sucesso!")

# Testa salvar em arquivo temporário
try:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        temp_file = f.name
    
    mapa.save(temp_file)
    print(f"✅ Mapa salvo em: {temp_file}")
    
    # Lê o conteúdo
    with open(temp_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✅ HTML gerado: {len(html_content)} caracteres")
    
    # Remove arquivo temporário
    os.unlink(temp_file)
    print("✅ Arquivo temporário removido")
    
    if len(html_content) > 100:
        print("\n🎉 TUDO FUNCIONANDO! O mapa pode ser exibido no Streamlit.")
        print(f"   Tamanho do HTML: {len(html_content)} caracteres")
    else:
        print("\n❌ ERRO: HTML muito pequeno ou vazio")
        
except Exception as e:
    print(f"\n❌ ERRO ao salvar mapa: {e}")
    import traceback
    traceback.print_exc()

