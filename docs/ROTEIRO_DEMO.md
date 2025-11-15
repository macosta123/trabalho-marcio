# 🎤 Roteiro de Demonstração - 5 Minutos

## ⏱️ Cronograma

| Tempo | Atividade |
|-------|-----------|
| 0:00 - 0:30 | Introdução ao problema |
| 0:30 - 1:30 | Mostrar a solução (API vs Manual) |
| 1:30 - 3:00 | Demonstração ao vivo |
| 3:00 - 4:30 | Mostrar o código e resultados |
| 4:30 - 5:00 | Conclusões e perguntas |

---

## 🎬 Script da Demonstração

### [0:00 - 0:30] Abertura

**Você diz:**
> "Bom dia/Boa tarde! Hoje vou apresentar um sistema de roteamento que usa a API do Google Maps para encontrar o melhor caminho entre dois endereços reais."

**Mostrar:**
- Slide de título

---

### [0:30 - 1:00] O Problema

**Você diz:**
> "Imagine que você está em Maricá e precisa ir para Niterói. Qual o melhor caminho? Quantos quilômetros? Quanto tempo vai levar? Esse é um problema clássico de pathfinding, mas aplicado ao mundo real."

**Mostrar:**
- Slide 2 (O Problema)
- Mapa do Google Maps mostrando as duas cidades

---

### [1:00 - 1:30] A Solução

**Você diz:**
> "Tradicionalmente, implementaríamos algoritmos como Dijkstra ou A* com dados de mapas. Mas existe uma forma muito melhor: usar a API do Google Maps, que já tem dados globais atualizados e considera tráfego em tempo real."

**Mostrar:**
- Slide 3 (Comparação Tradicional vs Moderna)
- Destacar as vantagens da API

---

### [1:30 - 2:00] Antes da Demo

**Você diz:**
> "O programa é simples. Primeiro, configuramos a API Key..."

**Mostrar no terminal:**
```bash
# (Já deve estar configurado antes)
echo $GOOGLE_MAPS_API_KEY
```

**Você diz:**
> "...depois executamos o script Python."

---

### [2:00 - 3:00] DEMONSTRAÇÃO AO VIVO ⭐

**Você faz:**

1. **Abrir terminal**
```bash
cd ~/Downloads/"trabalho marcio"
python rota_google.py
```

2. **Digitar endereços** (escolha um dos exemplos):

**Opção 1 - Rota Média (Recomendado):**
```
Digite o endereço de PARTIDA: Maricá, RJ
Digite o endereço de CHEGADA: Niterói, RJ
```

**Opção 2 - Rota Curta (Alternativa):**
```
Digite o endereço de PARTIDA: Centro, Niterói, RJ
Digite o endereço de CHEGADA: Museu de Arte Contemporânea, Niterói, RJ
```

3. **Aguardar resposta** (falar enquanto espera):
> "A API está geocodificando os endereços, calculando a rota otimizada..."

4. **Mostrar output:**
```
--- Gerando Mapa da Rota ---
Distância Total: 45.3 km
Duração Estimada: 52 mins
Mapa salvo com sucesso em 'mapa_rota.html'
```

5. **Navegador abre automaticamente** 🎉

---

### [3:00 - 3:30] Mostrar o Mapa

**No navegador:**

1. **Zoom Out** - Mostrar rota completa
   > "Aqui temos a visão geral. Marcador verde é a origem, vermelho o destino, e a linha azul é a rota otimizada."

2. **Clicar no marcador de origem** (verde)
   > "O popup mostra o endereço exato."

3. **Clicar no marcador de destino** (vermelho)
   > "Aqui vemos a distância e duração estimada."

4. **Fazer Zoom em parte da rota**
   > "O mapa é totalmente interativo, podemos ver detalhes de cada trecho."

---

### [3:30 - 4:00] Mostrar o Código (Rápido)

**Abrir `rota_google.py` no VS Code**

**Você diz:**
> "O código é dividido em 4 fases:"

**Scrollar pelo código mostrando:**

1. **Fase 1** (linha ~18)
```python
def configurar_cliente():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
```
> "Carrega a API Key do ambiente."

2. **Fase 2** (linha ~30)
```python
directions_result = gmaps_client.directions(...)
```
> "Chama a API para obter a rota."

3. **Fase 3** (linha ~60)
```python
folium.Map(...)
folium.Marker(...)
folium.PolyLine(...)
```
> "Cria o mapa interativo com Folium."

**Não detalhar muito - tempo é curto!**

---

### [4:00 - 4:30] Resultados e Vantagens

**Você diz:**
> "Com apenas ~150 linhas de código, conseguimos:"

**Listar rapidamente:**
- ✅ Geocodificar qualquer endereço do mundo
- ✅ Calcular a rota ótima considerando tráfego
- ✅ Visualizar em mapa interativo
- ✅ Sem precisar manter dados de mapas
- ✅ Grátis até 40.000 requisições/mês

**Mostrar slide de comparação (Slide 11)**

---

### [4:30 - 4:50] Conclusão

**Você diz:**
> "Este projeto demonstra como APIs modernas permitem criar aplicações robustas rapidamente, focando no valor para o usuário em vez de reinventar algoritmos complexos."

**Casos de uso:**
> "Isso pode ser usado em apps de entrega, navegação, turismo, logística..."

---

### [4:50 - 5:00] Encerramento

**Você diz:**
> "Obrigado! Alguma pergunta?"

**Estar preparado para:**
- Mostrar outra rota se alguém sugerir
- Explicar custos da API
- Falar sobre limitações
- Mostrar o README se perguntarem detalhes

---

## ✅ Checklist PRÉ-APRESENTAÇÃO

### 1 Dia Antes:
- [ ] API Key configurada e testada
- [ ] Programa executado com sucesso pelo menos 3x
- [ ] Screenshots tiradas e salvas
- [ ] Slides preparados (ou apresentação em Markdown pronta)
- [ ] Ensaiar apresentação completa (cronometrar!)

### 1 Hora Antes:
- [ ] Testar conexão com internet
- [ ] Verificar se API Key ainda está válida
- [ ] Abrir VS Code com o projeto
- [ ] Abrir terminal no diretório correto
- [ ] Fechar abas desnecessárias do navegador
- [ ] Aumentar fonte do terminal (Ctrl + Shift + +)
- [ ] Testar audio/vídeo se for remoto

### 5 Minutos Antes:
- [ ] Fechar notificações do sistema
- [ ] Colocar celular em silencioso
- [ ] Ter um copo de água por perto
- [ ] Respirar fundo 🧘

---

## 🎯 Dicas de Oratória

### Linguagem Corporal:
- ✅ Fale de frente para a audiência
- ✅ Mantenha contato visual
- ✅ Use gestos para enfatizar pontos
- ✅ Sorria (demonstra confiança)

### Voz:
- ✅ Fale com clareza e pausadamente
- ✅ Varie o tom (não fale monotonamente)
- ✅ Faça pausas para respirar
- ✅ Projete a voz (não grite, mas seja audível)

### Conteúdo:
- ✅ Seja entusiasta sobre o projeto
- ✅ Use exemplos concretos
- ✅ Evite jargão excessivo
- ✅ Admita se não souber algo ("Boa pergunta, vou pesquisar e respondo depois")

---

## ❓ Perguntas Esperadas e Respostas

### P1: "Quanto custa usar a API?"
**R:** "O Google oferece $200 USD grátis por mês, o que dá cerca de 40 mil requisições. Depois disso, é cerca de $5 por 1.000 requisições. Para este projeto educacional, ficamos bem dentro do limite gratuito."

### P2: "E se a internet cair?"
**R:** "Como a API é online, precisamos de conexão. Em produção, poderíamos implementar cache de rotas frequentes ou ter um fallback para dados locais."

### P3: "Por que não implementar Dijkstra?"
**R:** "Para fins educacionais, Dijkstra é excelente para aprender grafos. Mas para uso real, a API é superior porque tem dados atualizados do mundo todo e considera fatores complexos como tráfego, construções, eventos, etc."

### P4: "Funciona em outros países?"
**R:** "Sim! A API do Google Maps é global, funciona em mais de 220 países e territórios."

### P5: "Posso adicionar mais paradas no meio do caminho?"
**R:** "Sim! A API suporta waypoints (pontos intermediários). É só adicionar o parâmetro `waypoints` na chamada da API."

### P6: "E a privacidade dos dados?"
**R:** "Os endereços são enviados ao Google para processamento. Em aplicações sensíveis, seria necessário avaliar isso e possivelmente usar soluções on-premise ou com maior controle de dados."

---

## 🚨 Plano B (Se Algo Der Errado)

### Se a API não responder:
> "Parece que a API está com latência. Mas eu tenho screenshots do resultado esperado..."
(Mostrar screenshots preparadas)

### Se a internet cair:
> "Sem conexão no momento, mas vou mostrar o código e explicar o fluxo..."
(Focar nos slides e código offline)

### Se o navegador não abrir:
```bash
# Abrir manualmente
xdg-open mapa_rota.html
```

### Se der erro de API Key:
```bash
# Verificar
echo $GOOGLE_MAPS_API_KEY

# Reconfigurar
export GOOGLE_MAPS_API_KEY='...'
```

---

## 📱 Versão SUPER RÁPIDA (2 minutos)

Se o tempo for muito curto:

1. **[0:00 - 0:15]** "Sistema de roteamento com Google Maps API"
2. **[0:15 - 0:30]** "Problema: encontrar melhor caminho entre endereços"
3. **[0:30 - 1:30]** DEMO AO VIVO (pular explicação de código)
4. **[1:30 - 1:50]** "Vantagens: simples, preciso, dados globais"
5. **[1:50 - 2:00]** "Obrigado! Perguntas?"

---

## 🎓 Após a Apresentação

- [ ] Agradecer pela atenção
- [ ] Compartilhar o repositório/código se solicitado
- [ ] Anotar feedback recebido
- [ ] Tirar foto do grupo (se apropriado)
- [ ] Pedir avaliação ao professor

---

**Você está pronto! Boa apresentação! 🎉**
