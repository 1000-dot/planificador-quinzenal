import streamlit as st
import pandas as pd
from docx import Document
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Gerador de Planificação Quinzenal", layout="wide")
st.title("📘 Gerador de Planificação Quinzenal")

st.markdown("""
Este aplicativo permite gerar uma planificação quinzenal com base em planos analíticos enviados em formato Word (.docx).  
Cada arquivo deve conter uma **tabela** com as seguintes colunas:

**Disciplina | Lição | Objetivos | Conteúdos | Estratégias | Recursos**
""")

# Upload dos arquivos
uploaded_files = st.file_uploader("📥 Envie os planos analíticos (.docx)", type="docx", accept_multiple_files=True)

# Horário semanal
st.subheader("🕒 Horário semanal por disciplina")
horario = {}
if uploaded_files:
    for file in uploaded_files:
        nome_disciplina = file.name.replace(".docx", "")
        tempos = st.number_input(f"{nome_disciplina} - tempos por dia", min_value=1, max_value=5, value=1)
        horario[nome_disciplina] = tempos

# Datas da quinzena
st.subheader("🗓️ Período da quinzena")
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data de início", value=datetime.today())
with col2:
    data_fim = st.date_input("Data de fim", value=datetime.today() + timedelta(days=14))

# Função para ler planos analíticos
def ler_plano(file):
    doc = Document(file)
    tabela = doc.tables[0]
    dados = []
    for row in tabela.rows[1:]:
        dados.append({
            "Disciplina": row.cells[0].text.strip(),
            "Lição": int(row.cells[1].text.strip()),
            "Objetivos": row.cells[2].text.strip(),
            "Conteúdos": row.cells[3].text.strip(),
            "Estratégias": row.cells[4].text.strip(),
            "Recursos": row.cells[5].text.strip(),
        })
    return pd.DataFrame(dados)

# Função para gerar planificação
def gerar_planificacao(planos, horario, data_inicio, data_fim):
    dias_letivos = pd.date_range(start=data_inicio, end=data_fim, freq='B')
    documento = Document()
    documento.add_heading('Planificação Quinzenal', 0)

    for dia in dias_letivos:
        documento.add_heading(f"{dia.strftime('%A, %d/%m/%Y')}", level=1)
        tabela = documento.add_table(rows=1, cols=8)
        tabela.style = 'Table Grid'
        hdr_cells = tabela.rows[0].cells
        hdr_cells[0].text = 'Disciplina'
        hdr_cells[1].text = 'Data'
        hdr_cells[2].text = 'Lição'
        hdr_cells[3].text = 'Objetivos'
        hdr_cells[4].text = 'Conteúdos'
        hdr_cells[5].text = 'Tema Transversal'
        hdr_cells[6].text = 'Métodos Didáticos'
        hdr_cells[7].text = 'Material Didático'

        for disciplina, tempos in horario.items():
            if disciplina in planos:
                plano = planos[disciplina]
                for _ in range(tempos):
                    if not plano.empty:
                        linha = plano.iloc[0]
                        plano.drop(index=plano.index[0], inplace=True)
                        row_cells = tabela.add_row().cells
                        row_cells[0].text = disciplina
                        row_cells[1].text = dia.strftime('%d/%m/%Y')
                        row_cells[2].text = str(linha['Lição'])
                        row_cells[3].text = linha['Objetivos']
                        row_cells[4].text = linha['Conteúdos']
                        row_cells[5].text = 'Cidadania'  # Tema fixo (pode ser adaptado)
                        row_cells[6].text = linha['Estratégias']
                        row_cells[7].text = linha['Recursos']

    buffer = io.BytesIO()
    documento.save(buffer)
    buffer.seek(0)
    return buffer

# Botão para gerar
if st.button("🚀 Gerar planificação"):
    if uploaded_files and horario:
        planos = {file.name.replace(".docx", ""): ler_plano(file) for file in uploaded_files}
        docx_file = gerar_planificacao(planos, horario, data_inicio, data_fim)
        st.success("✅ Planificação gerada com sucesso!")
        st.download_button("📄 Baixar planificação", data=docx_file, file_name="planificacao_quinzenal.docx")
    else:
        st.warning("Por favor, envie os arquivos e defina o horário.")
