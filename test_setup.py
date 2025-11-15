#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para verificar a instalação e configuração do projeto.
Execute este arquivo antes de rodar o programa principal.

Uso:
    python test_setup.py
"""

import os
import sys

def test_imports():
    """Testa se as bibliotecas necessárias estão instaladas."""
    print("📦 Testando importações de bibliotecas...")
    
    try:
        import googlemaps
        print("  ✅ googlemaps instalado (versão {})".format(googlemaps.__version__))
    except ImportError:
        print("  ❌ googlemaps NÃO instalado")
        print("     Instale com: pip install googlemaps")
        return False
    
    try:
        import folium
        print("  ✅ folium instalado (versão {})".format(folium.__version__))
    except ImportError:
        print("  ❌ folium NÃO instalado")
        print("     Instale com: pip install folium")
        return False
    
    return True

def test_api_key():
    """Verifica se a API Key está configurada."""
    print("\n🔑 Testando API Key...")
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key:
        print("  ❌ Variável de ambiente 'GOOGLE_MAPS_API_KEY' não definida")
        print("     Configure com: export GOOGLE_MAPS_API_KEY='sua_chave_aqui'")
        return False
    
    if api_key == 'your_google_maps_api_key_here':
        print("  ❌ API Key ainda está com valor de exemplo")
        print("     Substitua pela sua chave real do Google Cloud")
        return False
    
    # Verificar formato básico (começa com AIza geralmente)
    if len(api_key) < 30:
        print("  ⚠️  API Key parece muito curta (pode estar incompleta)")
    
    print(f"  ✅ API Key encontrada ({len(api_key)} caracteres)")
    print(f"     Início: {api_key[:10]}...")
    
    return True

def test_google_maps_connection():
    """Testa a conexão com a API do Google Maps."""
    print("\n🌐 Testando conexão com Google Maps API...")
    
    import googlemaps
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    try:
        gmaps = googlemaps.Client(key=api_key)
        print("  ✅ Cliente Google Maps criado com sucesso")
    except Exception as e:
        print(f"  ❌ Erro ao criar cliente: {e}")
        return False
    
    # Testar Geocoding
    try:
        print("\n  Testando Geocoding API...")
        result = gmaps.geocode("Rio de Janeiro, RJ, Brasil")
        
        if not result:
            print("  ❌ Geocoding retornou vazio")
            return False
        
        location = result[0]['geometry']['location']
        address = result[0]['formatted_address']
        
        print(f"  ✅ Geocoding OK!")
        print(f"     Endereço: {address}")
        print(f"     Coordenadas: {location['lat']:.4f}, {location['lng']:.4f}")
        
    except googlemaps.exceptions.ApiError as e:
        print(f"  ❌ Erro na API: {e}")
        print("     Verifique se as APIs estão ativadas no Google Cloud:")
        print("     - Geocoding API")
        print("     - Directions API")
        return False
    except Exception as e:
        print(f"  ❌ Erro inesperado: {e}")
        return False
    
    # Testar Directions
    try:
        print("\n  Testando Directions API...")
        directions = gmaps.directions(
            origin="Maricá, RJ",
            destination="Niterói, RJ",
            mode="driving"
        )
        
        if not directions:
            print("  ❌ Directions retornou vazio")
            return False
        
        leg = directions[0]['legs'][0]
        distance = leg['distance']['text']
        duration = leg['duration']['text']
        
        print(f"  ✅ Directions OK!")
        print(f"     Rota: Maricá → Niterói")
        print(f"     Distância: {distance}")
        print(f"     Duração: {duration}")
        
    except googlemaps.exceptions.ApiError as e:
        print(f"  ❌ Erro na API: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Erro inesperado: {e}")
        return False
    
    return True

def test_folium():
    """Testa a criação de um mapa Folium simples."""
    print("\n🗺️  Testando Folium...")
    
    try:
        import folium
        
        # Criar mapa de teste
        mapa = folium.Map(location=[-22.9068, -43.1729], zoom_start=10)
        
        # Adicionar marcador
        folium.Marker(
            location=[-22.9068, -43.1729],
            popup="Rio de Janeiro",
            icon=folium.Icon(color='red')
        ).add_to(mapa)
        
        # Tentar salvar
        test_file = 'test_map.html'
        mapa.save(test_file)
        
        print(f"  ✅ Mapa de teste criado: {test_file}")
        
        # Limpar arquivo de teste
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"  🧹 Arquivo de teste removido")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao criar mapa: {e}")
        return False

def print_quota_info():
    """Exibe informações sobre quotas da API."""
    print("\n💰 Informações sobre Quotas (Google Maps API):")
    print("  • Crédito gratuito mensal: $200 USD")
    print("  • Geocoding API: ~$5 por 1.000 requisições")
    print("  • Directions API: ~$5 por 1.000 requisições")
    print("  • Estimativa: ~40.000 requisições grátis/mês")
    print("\n  📊 Monitore seu uso em:")
    print("     https://console.cloud.google.com/apis/dashboard")

def main():
    """Função principal do script de teste."""
    print("=" * 70)
    print("🧪 SCRIPT DE TESTE - Planejador de Rotas com Google Maps")
    print("=" * 70)
    
    all_tests_passed = True
    
    # Teste 1: Importações
    if not test_imports():
        all_tests_passed = False
    
    # Teste 2: API Key
    if not test_api_key():
        all_tests_passed = False
        print("\n⚠️  Não é possível continuar sem a API Key configurada.")
        print("   Configure e execute novamente este teste.")
        sys.exit(1)
    
    # Teste 3: Conexão Google Maps
    if not test_google_maps_connection():
        all_tests_passed = False
    
    # Teste 4: Folium
    if not test_folium():
        all_tests_passed = False
    
    # Resultado Final
    print("\n" + "=" * 70)
    if all_tests_passed:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 Você pode executar o programa principal:")
        print("   python rota_google.py")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("   Corrija os problemas acima antes de continuar.")
        sys.exit(1)
    print("=" * 70)
    
    # Informações adicionais
    print_quota_info()
    
    print("\n📚 Próximos passos:")
    print("  1. Execute: python rota_google.py")
    print("  2. Digite endereços de origem e destino")
    print("  3. Visualize o mapa gerado em 'mapa_rota.html'")
    print("\n")

if __name__ == "__main__":
    main()
