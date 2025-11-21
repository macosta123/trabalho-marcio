# 🔧 Troubleshooting: Mapa não aparece no Streamlit Cloud

## Problemas Comuns e Soluções

### 1. Mapa não aparece após deploy

**Sintomas:**
- O mapa não é exibido na aba "Mapa Real - Maricá"
- Tela em branco onde o mapa deveria aparecer
- Mensagem de erro genérica

**Possíveis Causas:**

#### A) Dependências não instaladas corretamente
**Solução:**
1. Verifique se o `requirements.txt` contém todas as dependências:
   ```
   streamlit-folium>=0.20.0
   osmnx>=1.6.0
   folium>=0.15.1
   geopy>=2.4.1
   pyproj>=3.6.1
   ```

2. No Streamlit Cloud, vá em "Manage app" → "Settings" → "Dependencies"
3. Certifique-se de que o arquivo `requirements.txt` está sendo usado

#### B) `streamlit-folium` não funciona no ambiente
**Solução:**
O código já tem fallback automático para HTML. Se o mapa não aparecer:
1. Verifique os logs do Streamlit Cloud (Manage app → Logs)
2. Procure por erros relacionados a `st_folium` ou `streamlit-folium`

#### C) Problema com arquivos temporários no Streamlit Cloud
**Solução:**
O código foi atualizado para usar buffer de memória primeiro, depois arquivo temporário como fallback.

#### D) Mapa não carrega do OpenStreetMap
**Sintomas:**
- Mensagem "Erro ao carregar mapa"
- Spinner fica rodando indefinidamente

**Solução:**
1. Verifique a conexão com a internet no Streamlit Cloud
2. O OSMnx pode demorar para baixar dados da primeira vez
3. Tente recarregar a página após alguns segundos

### 2. Mapa aparece mas está vazio

**Sintomas:**
- Mapa é exibido mas não mostra ruas ou caminhos
- Apenas um mapa base do OpenStreetMap

**Possíveis Causas:**

#### A) Grafo de ruas não foi carregado
**Solução:**
1. Verifique se a mensagem "✅ Mapa carregado com sucesso!" aparece
2. Se não aparecer, verifique os logs para erros do OSMnx

#### B) Endereços não foram encontrados
**Solução:**
1. Use endereços específicos de Maricá
2. Exemplos que funcionam:
   - "Praça Orlando de Barros Pimentel, Maricá"
   - "Centro, Maricá, RJ"
   - "Praia de Itaipuaçu, Maricá"

### 3. Erro ao calcular rota

**Sintomas:**
- Endereços são encontrados mas rota não é calculada
- Mensagem "Não foi possível encontrar uma rota"

**Solução:**
1. Verifique se os endereços estão dentro da área de Maricá
2. Tente endereços mais próximos
3. O grafo pode não ter conexão entre os pontos escolhidos

## 🔍 Como Diagnosticar

### Verificar Logs no Streamlit Cloud

1. Acesse seu app no Streamlit Cloud
2. Clique em "Manage app" (canto inferior direito)
3. Vá na aba "Logs"
4. Procure por:
   - Erros relacionados a `osmnx`
   - Erros relacionados a `folium`
   - Erros relacionados a `streamlit-folium`
   - Erros de importação

### Testar Localmente

Para testar se o problema é específico do Streamlit Cloud:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar localmente
streamlit run app_dijkstra.py
```

Se funcionar localmente mas não no Streamlit Cloud, o problema é específico do ambiente de deploy.

## ✅ Melhorias Implementadas

O código foi atualizado com:

1. **Múltiplos fallbacks para exibição:**
   - Tenta `st_folium` primeiro (interativo)
   - Fallback para HTML via buffer de memória
   - Fallback para HTML via arquivo temporário
   - Mensagens de erro detalhadas

2. **Melhor tratamento de erros:**
   - Expansores com detalhes do erro
   - Traceback completo para debug
   - Mensagens informativas

3. **Verificações de estado:**
   - Verifica se o mapa foi criado
   - Verifica se há caminho para exibir
   - Validação de dados antes de exibir

## 🚀 Próximos Passos

Se o mapa ainda não aparecer:

1. **Verifique os logs** no Streamlit Cloud
2. **Teste localmente** para isolar o problema
3. **Verifique as dependências** no `requirements.txt`
4. **Considere usar uma versão mais antiga** do `streamlit-folium` se houver incompatibilidade:
   ```
   streamlit-folium==0.15.0
   ```

## 📝 Nota sobre Streamlit Cloud

O Streamlit Cloud tem algumas limitações:
- Recursos limitados no plano gratuito
- Algumas bibliotecas podem ter problemas de compatibilidade
- Arquivos temporários podem ter restrições

O código foi otimizado para funcionar dentro dessas limitações.

