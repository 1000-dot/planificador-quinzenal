import streamlit as st
import random

# Configuração inicial
st.set_page_config(page_title="Simulação de Pinocitose", layout="centered")
st.title("🧫 Simulação de Pinocitose")
st.markdown("Explore como uma célula absorve partículas através da pinocitose!")

# Estado da célula
energia = st.session_state.get("energia", 100)
particulas = ["Nutriente", "Vírus", "Resíduo"]
tipo = st.selectbox("Escolha o tipo de partícula para absorver:", particulas)

# Função de absorção
def absorver(tipo):
    if tipo == "Nutriente":
        return 10, "✅ Nutriente absorvido! Energia aumentada."
    elif tipo == "Vírus":
        return -20, "⚠️ Vírus detectado! Alerta ativado e energia reduzida."
    elif tipo == "Resíduo":
        return -5, "♻️ Resíduo absorvido. Energia levemente reduzida."

# Botão de ação
if st.button("Absorver Partícula"):
    delta, mensagem = absorver(tipo)
    energia += delta
    st.session_state.energia = energia
    st.success(mensagem)

# Exibição da energia
st.progress(min(energia, 100))
st.metric(label="Energia da Célula", value=f"{energia} unidades")

# Mensagem educativa
with st.expander("📘 O que é Pinocitose?"):
    st.write("""
    A pinocitose é um tipo de endocitose em que a célula absorve pequenas partículas líquidas.
    É essencial para a nutrição celular e defesa contra agentes externos.
    """)

# Rodapé
st.caption("Desenvolvido por Luís com apoio do Copilot ✨")
import streamlit as st
import random

# Configuração inicial
st.set_page_config(page_title="Simulação de Pinocitose", layout="centered")
st.title("🧫 Simulação de Pinocitose com Sons e Animações")

# Estado da célula
energia = st.session_state.get("energia", 100)
particulas = ["Nutriente", "Vírus", "Resíduo"]
tipo = st.selectbox("Escolha a partícula:", particulas)

# Função de absorção com som
def absorver(tipo):
    if tipo == "Nutriente":
        st.audio("assets/nutriente.mp3", autoplay=True)
        return 10, "✅ Nutriente absorvido!"
    elif tipo == "Vírus":
        st.audio("assets/virus.mp3", autoplay=True)
        return -20, "⚠️ Vírus detectado!"
    elif tipo == "Resíduo":
        st.audio("assets/residuo.mp3", autoplay=True)
        return -5, "♻️ Resíduo absorvido."

# Botão de ação
if st.button("Absorver"):
    delta, mensagem = absorver(tipo)
    energia += delta
    st.session_state.energia = energia
    st.success(mensagem)

# 🎞️ Gráfico animado de energia
st.markdown("### 🔋 Energia da Célula")
st.bar_chart({"Energia": [energia]})

# 📘 Explicação educativa
with st.expander("O que é Pinocitose?"):
    st.write("""
    A pinocitose é um processo celular de absorção de líquidos e partículas pequenas.
    Esta simulação mostra como diferentes substâncias afetam a energia da célula.
    """)

# Rodapé
st.caption("Desenvolvido por Luís com apoio do Copilot ✨")
