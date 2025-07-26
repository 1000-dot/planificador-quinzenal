import streamlit as st
from docx import Document
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Plano Quinzenal com Orientações", layout="wide")
st.title("📘 Gerador de Plano Quinzenal com Orientações do Orientador")

# 📅 Configurações
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data de início da quinzena", value=datetime.today())
with col2:
    curriculo_local = st.text_input("Currículo local", value="Currículo de Moçambique")

# ⏰ Inserir horários e orientações por tempo
st.subheader("⏰ Horários e Orientações por Tempo")
orientacoes = []
for i in range(1, 7):
    col1, col2 = st.columns([1, 3])
    with col1:
        horario = st.text_input(f"Tempo {i} - Horário", value=f"{7+i}:30 - {8+i}:15")
    with col2:
        orientacao = st.text_area(f"Orientação para Tempo {i}", value=f"Instruções para o tempo {i}")
    orientacoes.append({"Tempo": i, "Horário": horario, "Orientação": orientacao})

# 🧠 Gerar plano quinzenal
dias_letivos = [data_inicio + timedelta(days=i) for i in range(14) if (data_inicio + timedelta(days=i)).weekday() < 5]

if st.button("📄 Gerar Plano Quinzenal"):
    doc = Document()
    doc.add_heading("Plano Quinzenal Escolar", 0)
    doc.add_paragraph(f"Currículo Local: {curriculo_local}")
    doc.add_paragraph(" ")

    for dia in dias_letivos:
        doc.add_heading(f"📅 {dia.strftime('%A, %d/%m/%Y')}", level=1)
        tabela = doc.add_table(rows=1, cols=6)
        tabela.style = 'Table Grid'
        hdr = tabela.rows[0].cells
        hdr[0].text = "Tempo"
        hdr[1].text = "Horário"
        hdr[2].text = "Orientações"
        hdr[3].text = "Método de Ensino"
        hdr[4].text = "Material Didático"
        hdr[5].text = "Observações"

        for item in orientacoes:
            linha = tabela.add_row().cells
            linha[0].text = str(item["Tempo"])
            linha[1].text = item["Horário"]
            linha[2].text = item["Orientação"]
            linha[3].text = "__________________________"
            linha[4].text = "__________________________"
            linha[5].text = "__________________________"

        doc.add_paragraph(" ")

    # 📤 Exportar documento
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    st.download_button("📥 Baixar plano quinzenal", data=buffer, file_name="plano_quinzenal_orientado.docx")
