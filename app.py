import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Simulação de Pinocitose", layout="centered")
st.title("🧫 Simulação de Pinocitose Interativa")

# Estado inicial
if "energia" not in st.session_state:
    st.session_state.energia = 100

# Tradução automática
idioma = st.selectbox("🌍 Idioma da explicação:", ["pt", "en", "es", "fr"])
texto_base = "A pinocitose é um processo celular de absorção de líquidos e partículas pequenas."
texto_traduzido = GoogleTranslator(source='auto', target=idioma).translate(texto_base)

# Escolha de partícula
particulas = {
    "Nutriente": {"delta": 10, "mensagem": "✅ Nutriente absorvido!", "som": "assets/nutriente.mp3"},
    "Vírus": {"delta": -20, "mensagem": "⚠️ Vírus detectado!", "som": "assets/virus.mp3"},
    "Resíduo": {"delta": -5, "mensagem": "♻️ Resíduo absorvido.", "som": "assets/residuo.mp3"}
}
tipo = st.selectbox("Escolha a partícula:", list(particulas.keys()))

# Ação de absorção
if st.button("Absorver"):
    efeito = particulas[tipo]
    st.session_state.energia += efeito["delta"]
    st.success(efeito["mensagem"])
    st.audio(efeito["som"], autoplay=True)

# Energia
st.metric("Energia da Célula", f"{st.session_state.energia} unidades")
st.progress(min(st.session_state.energia, 100))

# Visualização 3D simulada
fig = go.Figure(data=[
    go.Mesh3d(
        x=[0, 1, 0.5], y=[0, 0, 1], z=[0, 1, 0.5],
        color='lightblue', opacity=0.5
    )
])
fig.update_layout(title="Célula 3D Simulada", margin=dict(l=0, r=0, b=0, t=30))
st.plotly_chart(fig)

# Explicação educativa
with st.expander("📘 O que é Pinocitose?"):
    st.write(texto_traduzido)

# Exportação de dados
dados = {
    "partícula": tipo,
    "energia": st.session_state.energia
}
df = pd.DataFrame([dados])
st.download_button("📥 Exportar como CSV", df.to_csv(index=False), "dados.csv", "text/csv")
st.download_button("📥 Exportar como JSON", json.dumps(dados), "dados.json", "application/json")

st.caption("Desenvolvido por Luís com apoio do Copilot ✨")
