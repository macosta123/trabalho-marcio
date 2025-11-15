# 🎯 Exemplos de Uso do Sistema

Este arquivo contém exemplos práticos de rotas para testar o programa.

---

## 📍 Exemplos de Rotas

### 1. Rotas Curtas (Mesma Cidade)

#### Rio de Janeiro - Centro ao Cristo Redentor
```
Origem: Praça XV, Rio de Janeiro, RJ
Destino: Cristo Redentor, Rio de Janeiro, RJ

Distância Esperada: ~10-15 km
Duração Esperada: ~20-30 min
```

#### São Paulo - Paulista à USP
```
Origem: Avenida Paulista, São Paulo, SP
Destino: Universidade de São Paulo, São Paulo, SP

Distância Esperada: ~10-12 km
Duração Esperada: ~25-35 min
```

#### Niterói - Centro ao MAC
```
Origem: Centro, Niterói, RJ
Destino: Museu de Arte Contemporânea, Niterói, RJ

Distância Esperada: ~5-7 km
Duração Esperada: ~15-20 min
```

---

### 2. Rotas Médias (Entre Cidades Próximas)

#### Maricá → Niterói
```
Origem: Maricá, RJ
Destino: Niterói, RJ

Distância Esperada: ~40-50 km
Duração Esperada: ~45-60 min
Observação: Passa pela BR-101
```

#### Niterói → Rio de Janeiro
```
Origem: Niterói, RJ
Destino: Centro, Rio de Janeiro, RJ

Distância Esperada: ~15-20 km
Duração Esperada: ~25-35 min
Observação: Ponte Rio-Niterói
```

#### Santos → São Paulo
```
Origem: Santos, SP
Destino: São Paulo, SP

Distância Esperada: ~70-80 km
Duração Esperada: ~60-90 min
Observação: Via Anchieta ou Imigrantes
```

---

### 3. Rotas Longas (Viagens Intermunicipais)

#### Rio de Janeiro → São Paulo
```
Origem: Rio de Janeiro, RJ
Destino: São Paulo, SP

Distância Esperada: ~430-450 km
Duração Esperada: ~5-6 horas
Observação: Via Dutra (BR-116)
```

#### Belo Horizonte → Rio de Janeiro
```
Origem: Belo Horizonte, MG
Destino: Rio de Janeiro, RJ

Distância Esperada: ~430-450 km
Duração Esperada: ~6-7 horas
Observação: BR-040
```

#### Curitiba → Florianópolis
```
Origem: Curitiba, PR
Destino: Florianópolis, SC

Distância Esperada: ~300-320 km
Duração Esperada: ~4-5 horas
Observação: BR-376 e BR-101
```

---

### 4. Rotas Turísticas

#### Rota dos Pontos Turísticos - Rio
```
Origem: Copacabana, Rio de Janeiro, RJ
Destino: Pão de Açúcar, Rio de Janeiro, RJ

Interesse: Turismo
```

#### Rota Histórica - Ouro Preto
```
Origem: Praça Tiradentes, Ouro Preto, MG
Destino: Mina da Passagem, Mariana, MG

Interesse: Patrimônio histórico
```

#### Rota da Natureza - Paraty
```
Origem: Centro Histórico de Paraty, RJ
Destino: Praia do Sono, Paraty, RJ

Interesse: Ecoturismo
```

---

## 🚗 Testando Diferentes Modos de Transporte

Para testar diferentes modos, modifique a linha no código:

```python
# Em rota_google.py, linha ~68
directions_result = gmaps_client.directions(
    origin=loc_origem,
    destination=loc_destino,
    mode="driving"  # Mude aqui!
)
```

### Modos Disponíveis:

1. **`"driving"`** (padrão)
   - Rota de carro
   - Considera vias automotivas

2. **`"walking"`**
   - Rota a pé
   - Usa calçadas e caminhos pedestres
   - Exemplo: "Centro RJ → Cristo Redentor"

3. **`"bicycling"`**
   - Rota de bicicleta
   - Prioriza ciclovias
   - Exemplo: "Copacabana → Ipanema"

4. **`"transit"`**
   - Transporte público
   - Ônibus, metrô, trem
   - Exemplo: "Barra da Tijuca → Centro RJ"

---

## 🧪 Testes de Validação

### Teste 1: Endereços Válidos
```
✅ DEVE FUNCIONAR
Origem: Rua das Flores, 123, Niterói, RJ
Destino: Avenida Brasil, Rio de Janeiro, RJ
```

### Teste 2: Endereços Vagos (mas válidos)
```
✅ DEVE FUNCIONAR
Origem: Maricá
Destino: Niterói

(API consegue geocodificar)
```

### Teste 3: Endereços Inválidos
```
❌ DEVE FALHAR
Origem: asdkjhasd
Destino: xyzabc123

Mensagem esperada: "Não foi possível geocodificar um dos endereços"
```

### Teste 4: Coordenadas Diretas
```
✅ PODE FUNCIONAR (modificando o código)
Origem: -22.9194, -42.8186
Destino: -22.8833, -43.1036

(Precisa passar como tupla, não string)
```

---

## 📊 Comparação de Rotas

Execute o programa várias vezes com diferentes rotas e compare:

| Origem | Destino | Distância | Duração | Via Principal |
|--------|---------|-----------|---------|---------------|
| Maricá, RJ | Niterói, RJ | 45.3 km | 52 min | BR-101 |
| Rio Centro | São Paulo | 430 km | 5h 30min | BR-116 (Dutra) |
| Santos | São Paulo | 72 km | 1h 15min | Via Anchieta |

---

## 🎨 Personalizações no Mapa

### Mudar Cores dos Marcadores

No arquivo `rota_google.py`, linha ~95:

```python
# Origem - Verde (padrão)
folium.Marker(..., icon=folium.Icon(color='green'))

# Destino - Vermelho (padrão)
folium.Marker(..., icon=folium.Icon(color='red'))

# Outras cores disponíveis:
# 'blue', 'darkblue', 'purple', 'orange', 'lightred',
# 'beige', 'darkgreen', 'cadetblue', 'darkpurple', 'pink'
```

### Mudar Cor da Rota

Linha ~107:

```python
folium.PolyLine(
    locations=pontos_rota,
    color='blue',      # Mude aqui: 'red', 'green', 'black', '#FF5733'
    weight=5,          # Espessura da linha
    opacity=0.7        # Transparência (0.0 a 1.0)
)
```

### Mudar Estilo do Mapa

Linha ~88:

```python
# Estilo padrão
mapa = folium.Map(location=[...], zoom_start=13)

# Estilo de satélite
mapa = folium.Map(
    location=[...], 
    zoom_start=13,
    tiles='Stamen Terrain'  # ou 'OpenStreetMap', 'Stamen Toner'
)
```

---

## 🔧 Casos de Uso Avançados

### 1. Adicionar Waypoints (Paradas Intermediárias)

Modifique a chamada da API:

```python
directions_result = gmaps_client.directions(
    origin=loc_origem,
    destination=loc_destino,
    waypoints=[
        "Niterói, RJ",        # Parada 1
        "São Gonçalo, RJ"     # Parada 2
    ],
    mode="driving"
)
```

### 2. Evitar Pedágios

```python
directions_result = gmaps_client.directions(
    origin=loc_origem,
    destination=loc_destino,
    avoid=["tolls"],  # ou ["highways", "ferries"]
    mode="driving"
)
```

### 3. Rotas Alternativas

```python
directions_result = gmaps_client.directions(
    origin=loc_origem,
    destination=loc_destino,
    alternatives=True,  # Retorna múltiplas rotas
    mode="driving"
)

# Processar todas as rotas
for i, rota in enumerate(directions_result):
    print(f"Rota {i+1}: {rota['legs'][0]['distance']['text']}")
```

### 4. Horário de Partida Específico

```python
import datetime

# Partir amanhã às 14h
departure_time = datetime.datetime.now() + datetime.timedelta(days=1, hours=14)

directions_result = gmaps_client.directions(
    origin=loc_origem,
    destination=loc_destino,
    departure_time=departure_time,
    mode="driving"
)
```

---

## 📝 Notas de Execução

### Tempo de Resposta Esperado
- Rotas curtas: ~1-2 segundos
- Rotas longas: ~2-4 segundos
- Depende da conexão com internet

### Consumo de API
- Cada execução = 2 requisições:
  - 1x Geocoding (origem)
  - 1x Geocoding (destino)
  - 1x Directions
- Total: ~3 requisições por teste

### Limite Gratuito
- ~40.000 requisições/mês grátis
- = ~13.333 execuções do programa
- = ~440 testes por dia

---

## 🐛 Troubleshooting de Exemplos

### Problema: "Rota não encontrada"
**Solução:** Use endereços mais específicos ou verifique se há conexão terrestre.

```
❌ Origem: Rio de Janeiro  Destino: Fernando de Noronha
(Não há rota terrestre!)

✅ Origem: Rio de Janeiro  Destino: São Paulo
```

### Problema: "Múltiplos resultados de geocoding"
**Solução:** Seja mais específico no endereço.

```
❌ Origem: Centro
(Qual cidade?)

✅ Origem: Centro, Niterói, RJ, Brasil
```

---

## 🎓 Exercícios Propostos

1. **Exercício 1:** Encontre a rota da sua casa até a universidade
2. **Exercício 2:** Compare rotas `driving` vs `walking` para o mesmo destino
3. **Exercício 3:** Teste 5 rotas diferentes e crie uma tabela comparativa
4. **Exercício 4:** Modifique o código para exibir 3 rotas alternativas
5. **Exercício 5:** Adicione um waypoint intermediário em uma viagem longa

---

**Bons testes! 🚀**
