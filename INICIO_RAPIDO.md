# 🚀 Início Rápido - 5 Minutos

## ⚡ TL;DR (Too Long; Didn't Read)

Este é um programa Python que usa a API do Google Maps para encontrar rotas entre endereços e exibir em mapa interativo.

---

## 📋 Pré-requisitos

✅ Python 3.7+  
✅ Conta no Google Cloud Platform  
✅ API Key do Google Maps  
✅ Conexão com internet  

---

## 🏃 3 Passos para Executar

### 1️⃣ Instalar Dependências
```bash
pip install googlemaps folium
```

### 2️⃣ Configurar API Key
```bash
export GOOGLE_MAPS_API_KEY='sua_chave_aqui'
```

**Como obter a chave:**
1. Acesse: https://console.cloud.google.com/
2. Crie um projeto
3. Ative: "Directions API" e "Geocoding API"
4. Crie uma API Key
5. Adicione método de pagamento (tem $200 grátis/mês)

### 3️⃣ Executar
```bash
python rota_google.py
```

Digite origem e destino quando solicitado.

---

## 📖 Documentação Completa

- **Instalação Detalhada:** `INSTALACAO.md`
- **Documentação Completa:** `README.md`
- **Exemplos de Uso:** `EXEMPLOS.md`
- **Apresentação:** `docs/apresentacao.md`

---

## 🧪 Testar Antes de Usar

```bash
python test_setup.py
```

Este script verifica:
- ✅ Bibliotecas instaladas
- ✅ API Key configurada
- ✅ Conexão com Google Maps
- ✅ Criação de mapas

---

## 💡 Exemplo de Uso

```
$ python rota_google.py

=== Planejador de Rotas (Google Maps API) ===
Digite o endereço de PARTIDA: Maricá, RJ
Digite o endereço de CHEGADA: Niterói, RJ

--- Gerando Mapa da Rota ---
Distância Total: 45.3 km
Duração Estimada: 52 mins
Mapa salvo com sucesso em 'mapa_rota.html'
```

O mapa abre automaticamente no navegador! 🎉

---

## 🗂️ Estrutura do Projeto

```
trabalho-marcio/
├── rota_google.py         ⭐ Programa principal
├── test_setup.py          🧪 Script de teste
├── requirements.txt       📦 Dependências
├── README.md              📖 Documentação completa
├── INSTALACAO.md          🔧 Guia de instalação
├── EXEMPLOS.md            💡 Casos de uso
└── docs/
    ├── apresentacao.md        🎤 Slides (20 slides)
    ├── ROTEIRO_DEMO.md        🎬 Roteiro de demonstração
    └── SUMARIO_EXECUTIVO.md   📊 Visão executiva
```

---

## ❓ Problemas Comuns

### Erro: "API Key não definida"
```bash
export GOOGLE_MAPS_API_KEY='sua_chave'
```

### Erro: "Module not found"
```bash
pip install googlemaps folium
```

### Erro: "API not enabled"
- Ative as APIs no Google Cloud Console
- Geocoding API
- Directions API

### Erro: "Billing not enabled"
- Adicione método de pagamento no Google Cloud
- Você tem $200 grátis/mês

---

## 📞 Precisa de Ajuda?

Consulte a documentação completa em:
- `README.md` - Tudo sobre o projeto
- `INSTALACAO.md` - Passo a passo detalhado
- `EXEMPLOS.md` - Casos de uso práticos

---

## 🎯 Próximos Passos

1. ✅ Execute o teste: `python test_setup.py`
2. ✅ Rode o programa: `python rota_google.py`
3. ✅ Leia a doc completa: `README.md`
4. ✅ Veja exemplos: `EXEMPLOS.md`
5. ✅ Prepare apresentação: `docs/apresentacao.md`

---

**Boa sorte! 🚀**
