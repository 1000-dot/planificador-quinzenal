import streamlit as st
import pandas as pd
from docx import Document
import pytz
from datetime import datetime

# 🌍 Fuso horário de Maputo
tz = pytz.timezone("Africa/Maputo")
hora_local = datetime.now(tz).strftime("%A, %d %B %Y - %H:%M")

st.set_page_config(page_title="Planificador Quinzenal", layout="wide")
st.title("📘 Planificador Quinzenal de Aulas")
st.caption(f"🕒 Horário local: {hora_local}")

# 📤 Upload de arquivos
uploaded_files = st.file_uploader("Envie planos analíticos (.docx)", type="docx", accept_multiple_files=True)

# 📄 Função para ler plano analítico
def ler_plano(file):
    doc = Document(file)
    tabela = doc.tables[0]
    dados = []
    for row in tabela.rows[1:]:
        try:
            licao = int(row.cells[1].text.strip())
        except ValueError:
            continue  # pula linhas com erro

        dados.append({
            "Disciplina": row.cells[0].text.strip(),
            "Lição": licao,
            "Objetivos": row.cells[2].text.strip(),
            "Conteúdos": row.cells[3].text.strip(),
            "Estratégias": row.cells[4].text.strip(),
            "Recursos": row.cells[5].text.strip(),
        })
    return pd.DataFrame(dados)

# 📅 Dias e horários disponíveis
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios_padrao = ["07:00–08:00", "08:00–09:00", "09:00–10:00", "10:30–11:30", "11:30–12:30"]

# 🧮 Interface para montar grade horária semanal
st.sidebar.header("📆 Grade Horária Semanal")
grade_horaria = {}

for dia in dias_semana:
    st.sidebar.subheader(f"📅 {dia}")
    grade_horaria[dia] = {}
    for horario in horarios_padrao:
        disciplina = st.sidebar.text_input(f"{dia} {horario}", "", key=f"{dia}_{horario}")
        grade_horaria[dia][horario] = disciplina

# 📊 Processamento dos planos
if uploaded_files:
    planos = {}
    for file in uploaded_files:
        nome = file.name.replace(".docx", "")
        planos[nome] = ler_plano(file)

    st.subheader("📚 Planos Analíticos Carregados")
    for nome, df in planos.items():
        st.markdown(f"**Plano:** {nome}")
        st.dataframe(df)

    # 🗓️ Montar plano quinzenal (2 semanas)
    st.markdown("## 🗓️ Plano Quinzenal de Aulas")
    plano_quinzenal = []

    for semana_num in range(1, 3):  # Semana 1 e 2
        for dia in dias_semana:
            for horario in horarios_padrao:
                disciplina = grade_horaria[dia][horario]
                if disciplina:
                    df = planos.get(disciplina)
                    if df is not None and not df.empty:
                        index = ((semana_num - 1) * len(dias_semana) * len(horarios_padrao)) + len(plano_quinzenal)
                        plano = df.iloc[index % len(df)]  # distribui ciclicamente
                        plano_quinzenal.append({
                            "Semana": f"Semana {semana_num}",
                            "Dia": dia,
                            "Horário": horario,
                            "Disciplina": plano["Disciplina"],
                            "Lição": plano["Lição"],
                            "Objetivos": plano["Objetivos"],
                            "Conteúdos": plano["Conteúdos"],
                            "Estratégias": plano["Estratégias"],
                            "Recursos": plano["Recursos"],
                        })
                    else:
                        plano_quinzenal.append({
                            "Semana": f"Semana {semana_num}",
                            "Dia": dia,
                            "Horário": horario,
                            "Disciplina": disciplina,
                            "Lição": "❌ Não encontrado",
                            "Objetivos": "",
                            "Conteúdos": "",
                            "Estratégias": "",
                            "Recursos": "",
                        })

    df_quinzenal = pd.DataFrame(plano_quinzenal)
    st.dataframe(df_quinzenal)

else:
    st.info("Envie pelo menos um arquivo .docx para começar.")
