import streamlit as st
from docx import Document
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Plano Quinzenal com Horários", layout="wide")
st.title("📘 Gerador de Plano Quinzenal com Horários Personalizados")

# 📥 Upload do plano analítico
uploaded_file = st.file_uploader("Carregue o plano analítico (.docx)", type="docx")

# 📅 Configurações
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data de início da quinzena", value=datetime.today())
with col2:
    curriculo_local = st.text_input("Currículo local", value="Currículo de Moçambique")

# ⏰ Inserir horários por tempo
st.subheader("⏰ Horários por tempo")
horarios = []
for i in range(1, 7):
    horarios.append(st.text_input(f"Tempo {i}", value=f"{7+i}:30 - {8+i}:15"))

# 🔍 Função para extrair dados do documento
def extrair_planos(doc):
    planos = []
    for tabela in doc.tables:
        for i in range(1, len(tabela.rows)):
            linha = tabela.rows[i].cells
            planos.append({
                "Disciplina": linha[0].text.strip(),
                "Unidade Temática": linha[1].text.strip(),
                "Objetivos": linha[2].text.strip(),
                "Conteúdos": linha[3].text.strip(),
                "Competências": linha[4].text.strip()
            })
    return planos

# 🧠 Processamento
if uploaded_file:
    from docx import Document
    doc_entrada = Document(uploaded_file)
    planos = extrair_planos(doc_entrada)
    disciplinas = list({p['Disciplina'] for p in planos})
    dias_letivos = [data_inicio + timedelta(days=i) for i in range(14) if (data_inicio + timedelta(days=i)).weekday() < 5]
    contador_licoes = {disc: 1 for disc in disciplinas}

    # 📄 Criar novo documento
    doc_saida = Document()
    doc_saida.add_heading("Plano Quinzenal Escolar", 0)
    doc_saida.add_paragraph(f"Currículo Local: {curriculo_local}")
    doc_saida.add_paragraph(" ")

    for dia in dias_letivos:
        doc_saida.add_heading(f"📅 {dia.strftime('%A, %d/%m/%Y')}", level=1)
        tabela = doc_saida.add_table(rows=1, cols=11)
        tabela.style = 'Table Grid'
        hdr = tabela.rows[0].cells
        hdr[0].text = "Tempo"
        hdr[1].text = "Horário"
        hdr[2].text = "Disciplina"
        hdr[3].text = "Nº Lição"
        hdr[4].text = "Unidade Temática"
        hdr[5].text = "Objetivos"
        hdr[6].text = "Conteúdos"
        hdr[7].text = "Competências"
        hdr[8].text = "Currículo Local"
        hdr[9].text = "Método de Ensino"
        hdr[10].text = "Material Didático"

        for tempo in range(1, 7):
            disciplina = disciplinas[(tempo - 1) % len(disciplinas)]
            plano = next((p for p in planos if p['Disciplina'] == disciplina), None)
            if plano:
                licao = contador_licoes[disciplina]
                contador_licoes[disciplina] += 1

                linha = tabela.add_row().cells
                linha[0].text = str(tempo)
                linha[1].text = horarios[tempo - 1]
                linha[2].text = disciplina
                linha[3].text = str(licao)
                linha[4].text = plano['Unidade Temática']
                linha[5].text = plano['Objetivos']
                linha[6].text = plano['Conteúdos']
                linha[7].text = plano['Competências']
                linha[8].text = curriculo_local
                linha[9].text = "__________________________"
                linha[10].text = "__________________________"

        doc_saida.add_paragraph(" ")

    # 📤 Exportar documento
    buffer = io.BytesIO()
    doc_saida.save(buffer)
    buffer.seek(0)
    st.download_button("📄 Baixar plano quinzenal", data=buffer, file_name="plano_quinzenal.docx")
else:
    st.info("Envie um arquivo .docx com os planos analíticos para começar.")
