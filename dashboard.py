import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# Lista de times e palavras alternativas
times_alternativos = {
   "Atlético Mineiro": ["Atlético","Atlético Mineiro","atletico-mineiro", "atletico-mg", "galo"],
   "Athletico": ["Athletico","Athletico Paranaense", "atletico-paranaense", "atletico-pr", "furacão"],
   "Bahia": ["bahia", "esquadrão"],
   "Botafogo": ["botafogo", "fogão"],
   "Bragantino": ["bragantino", "massa bruta"],
   "Corinthians": ["corinthians", "timão"],
   "Criciúma": ["Criciúma","Criciuma", "criciuma", "tigre"],
   "Cruzeiro": ["cruzeiro", "raposa"],
   "Cuiabá": ["Cuiabá","Cuiaba", "cuiaba", "dourado"],
   "Flamengo": ["flamengo", "mengão"],
   "Fluminense": ["fluminense", "flu"],
   "Fortaleza": ["fortaleza", "leão"],
   "Grêmio": ["Grêmio","Gremio", "gremio", "tricolor gaúcho"],
   "Internacional": ["internacional", "inter"],
   "Palmeiras": ["palmeiras", "verdão"],
   "Santos": ["santos", "peixe"],
   "São Paulo": ["São Paulo","Sao Paulo", "sao-paulo", "tricolor paulista"],
   "Vasco": ["vasco", "vascão"],
   "Vitória": ["Vitória","Vitoria", "vitoria", "leão da barra"]
}

# Função para carregar os dados
@st.cache_data
def load_data():
    file_path = 'noticias_lance.csv'
    df = pd.read_csv(file_path)
    df['Local'] = df['Local'].fillna('').astype(str).apply(lambda x: x.split(',')[0])
    # df = df[df['Local'] != "Redação do Lance!"]
    df['Conteúdo'] = df['Conteúdo'].fillna('').astype(str)
    return df

df = load_data()

# Título do dashboard
st.title("Dashboard de Notícias")

# Filtro por data
st.sidebar.header("Filtrar por Data")
start_date = st.sidebar.date_input("Data Inicial", pd.to_datetime(df['Data']).min().date())
end_date = st.sidebar.date_input("Data Final", pd.to_datetime(df['Data']).max().date())
filtered_df = df[(pd.to_datetime(df['Data']) >= pd.to_datetime(start_date)) & (pd.to_datetime(df['Data']) <= pd.to_datetime(end_date))]

# Filtro por palavra-chave no conteúdo
st.sidebar.header("Filtrar por Palavra-chave")
keyword = st.sidebar.text_input("Palavra-chave")
if keyword:
    filtered_df = filtered_df[filtered_df['Conteúdo'].str.contains(keyword, case=False, na=False)]

# Filtro por times
st.sidebar.header("Filtrar por Times")
selected_teams = st.sidebar.multiselect("Times", options=list(times_alternativos.keys()), default=list(times_alternativos.keys()))
if selected_teams:
    keywords = [keyword for team in selected_teams for keyword in times_alternativos[team]]
    filtered_df = filtered_df[filtered_df['Conteúdo'].str.contains('|'.join(keywords), case=False, na=False)]

# Exibir dataframe filtrado
st.write("Notícias Filtradas", filtered_df)

# Contagem de citações por time
team_counts = {team: 0 for team in times_alternativos}
for content in filtered_df['Conteúdo']:
    for team, keywords in times_alternativos.items():
        if any(keyword.lower() in content.lower() for keyword in keywords):
            team_counts[team] += 1

team_counts_df = pd.DataFrame.from_dict(team_counts, orient='index', columns=['Count']).reset_index()
team_counts_df.columns = ['Time', 'Count']

# Gráfico de barras
st.bar_chart(team_counts_df.set_index('Time'))

# Rodar o aplicativo com `streamlit run <nome_do_arquivo.py>`
