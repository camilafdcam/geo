import pandas as pd
import streamlit as st
from streamlit_sortables import sort_items
import plotly.express as px
from streamlit_option_menu import option_menu


#from pyngrok import ngrok

# Iniciar o servidor do ngrok
#public_url = ngrok.connect(8501).public_url
#st.write(f"Seu app está rodando em: {public_url}")

#st.title("Meu Aplicativo Streamlit")
#st.write("Este é um app de teste para rodar com ngrok.")



st.set_page_config(
    page_title="Controle interno",
    page_icon="bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.image("./images/logo.png", width=300)

with st.sidebar:
    menu = option_menu(
        menu_title="Menu",  # Título do menu
        options=["Home", "INDICADORES", "EQUIPAMENTOS", "BACKLOG"],  # Opções do menu
        icons=["house", "journal-check", "truck-flatbed", "card-checklist"],  # Ícones das opções
        menu_icon="cast",  # Ícone principal do menu
        default_index=0,  # Primeira opção selecionada por padrão
        orientation="vertical",  # Menu vertical
        styles={  # Customização do estilo do menu
            "container": {"padding": "5px", "background-color": "#777777"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#5b5b5b"},
            "nav-link-selected": {"background-color": "#5972F1"},
        }
    )

if menu == 'Home':
    # Função para carregar e filtrar os dados do Excel
    @st.cache_data
    def load_data():
        df_geral = pd.read_excel(
            io='data.xlsx',  # Caminho do arquivo Excel
            dtype=str,  # Garante que os dados sejam strings
            engine='openpyxl',  # Usa a biblioteca openpyxl
            sheet_name='Planilha1',
            usecols='A:X',  # Seleciona as colunas A até XS
            nrows=4400  # Limita a quantidade de linhas lidas
        )

        # Remover espaços extras nas colunas 'STATUS' e 'TIPO DE MANUTENÇÃO'
        df_geral['STATUS'] = df_geral['STATUS'].str.strip()
        df_geral['LOCALIZAÇÃO'] = df_geral['LOCALIZAÇÃO'].str.strip()
        df_geral['TIPO DE MANUTENÇÃO'] = df_geral['TIPO DE MANUTENÇÃO'].str.strip()

        # Garantir que as colunas sejam do tipo string
        df_geral['STATUS'] = df_geral['STATUS'].astype(str)
        df_geral['LOCALIZAÇÃO'] = df_geral['LOCALIZAÇÃO'].astype(str)
        df_geral['TIPO DE MANUTENÇÃO'] = df_geral['TIPO DE MANUTENÇÃO'].astype(str)

        # Aplicando os filtros
        df_filtrado = df_geral[
            (df_geral['STATUS'].isin(['ABERTA', 'EM ANDAMENTO', 'AGUARDANDO'])) &  # Mantém apenas ABERTA e EM ANDAMENTO e AGUARDANDO
            (df_geral['LOCALIZAÇÃO'].isin(['PINTURA', 'CALDEIRARIA', 'MOBILIZAÇÃO', 'OFICINA', 'TORNEARIA'])) &
            (df_geral['TIPO DE MANUTENÇÃO'].isin(['CORRETIVA', 'PREVENTIVA', 'FABRICAÇÃO', 'MELHORIA', 'PINTURA', 'ADEQUAÇÃO DE SEGURANÇA', 'CORRETIVA PLANEJADA']))  # Mantém apenas CORRETIVA e PREVENTIVA
        ]

        return df_filtrado

    # Carregando os dados
    df_filtrado = load_data()

    # Criando um dicionário para armazenar as OS por status
    kanban_data = {
        "PINTURA": df_filtrado[df_filtrado["LOCALIZAÇÃO"] == "PINTURA"],
        "CALDEIRARIA": df_filtrado[df_filtrado["LOCALIZAÇÃO"] == "CALDEIRARIA"],
        "MOBILIZAÇÃO": df_filtrado[df_filtrado["LOCALIZAÇÃO"] == "MOBILIZAÇÃO"], 
        "OFICINA": df_filtrado[df_filtrado["LOCALIZAÇÃO"] == "OFICINA"], 
        "TORNEARIA": df_filtrado[df_filtrado["LOCALIZAÇÃO"] == "TORNEARIA"], 
        "ABERTA": df_filtrado[df_filtrado["STATUS"] == "ABERTA"],
        "EM ANDAMENTO": df_filtrado[df_filtrado["STATUS"] == "EM ANDAMENTO"],
        "AGUARDANDO": df_filtrado[df_filtrado["STATUS"] == "AGUARDANDO"]
    }

    # Cores para os títulos do Kanban
    status_colors = {
        "PINTURA": "#000066",   # Azul
        "CALDEIRARIA": "#000066",  # Azul
        "MOBILIZAÇÃO": "#000066",   # Azul
        "OFICINA": "#000066",   # Azul
        "TORNEARIA": "#000066",   # Azul
        "ABERTA": "#000066",   # Azul
        "EM ANDAMENTO": "#000066",   # Azul
        "AGUARDANDO": "#000066"   # Azul
    }

    import streamlit as st

    # Layout principal do Streamlit
    st.markdown(
        """
        <style>
            .header-container {
                background-color: #000066; /* Cor do fundo azul */
                color: white; /* Cor da fonte branca */
                text-align: center; /* Centraliza o texto */
                height: 50px; /* Define uma altura fixa para a barra */
                display: flex;
                justify-content: center;
                align-items: center; /* Alinha o texto verticalmente */
                width: 100%; /* Faz o retângulo ocupar toda a largura */
                box-sizing: border-box; /* Inclui o padding no cálculo da largura */
                margin-bottom: 30px; /* Adiciona um espaçamento abaixo da barra */
            }

            .header-container h1 {
                margin: 0; /* Remove as margens do h1 para evitar espaçamento extra */
                font-size: 25px; /* Ajusta o tamanho da fonte */
            }
        </style>
        <div class="header-container">
            <h1>KANBAN DE MANUTENÇÃO & FABRICAÇÃO</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Criando colunas no layout para exibição do Kanban
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Função para exibir as OS corretamente por status 
    def display_kanban(column, status, df):
        status_labels = {
            "MOBILIZAÇÃO": "#333399",  # Tomate
            "OFICINA": "#333399",  # Azul Aço
            "PINTURA": "#333399",  # Verde Lima
            "CALDEIRARIA": "#333399",  # Ouro
            "TORNEARIA": "#333399",  # Azul Violeta
            "AGUARDANDO": "#333399"  # Laranja Vermelho
        }

        # Exibindo apenas o retângulo de marcador de texto com a cor
        column.markdown(f"""
        <div style="background-color: {status_labels[status]}; padding: 10px 20px; border-radius: 8px; color: white; font-weight: bold; text-align: center; margin-bottom: 20px;">
            {status}
        </div>
        """, unsafe_allow_html=True)

        if df.empty:
            column.write("✅ Nenhuma OS nesse status")
        else:
            for _, row in df.iterrows():
                with column:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #ffffff;
                            padding: 10px;
                            margin: 10px 0;
                            border-radius: 8px;
                            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                            border-left: 5px solid {status_labels[status]};"
                            font-size: 18px;">
                            <p><strong>🔹 OS:</strong> {row.get('OS', 'Sem OS')}</p>
                            <p><strong>🔧 Equipamento:</strong> {row.get('EQUIPAMENTO', 'Sem Equipamento')}</p>
                            <p><strong>📝 Observação:</strong> {row.get('OBSERVAÇÃO', 'Sem Observação')}</p>
                            <p><strong>📅 Saída Prevista:</strong> {row.get('SAÍDA PREVISTA', 'Sem Data')}</p>
                            <p><strong>⏳ Aguardando:</strong> {row.get('FAZENDO', 'Nenhuma atividade registrada')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # Exibindo as OS em suas respectivas colunas no Kanban
    display_kanban(col1, "MOBILIZAÇÃO", kanban_data["MOBILIZAÇÃO"])
    display_kanban(col2, "OFICINA", kanban_data["OFICINA"])
    display_kanban(col3, "PINTURA", kanban_data["PINTURA"])
    display_kanban(col4, "CALDEIRARIA", kanban_data["CALDEIRARIA"])
    display_kanban(col5, "TORNEARIA", kanban_data["TORNEARIA"])
    display_kanban(col6, "AGUARDANDO", kanban_data["AGUARDANDO"])
    
if menu == 'INDICADORES':
    
    
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>CONTROLE INTERNO</h2>
        </div>
        """,
        unsafe_allow_html=True
        )
         #Configurações da página

    # Retângulos superiores para indicadores
    #html_code = """
    #<style>
    #/* Container principal para os indicadores */
    #.indicadores-container {
        #display: flex;
        #justify-content: space-around; /* Espaçamento uniforme */
        #align-items: center;
        #flex-wrap: wrap; /* Permite que os elementos quebrem linha */
        #gap: 5px; /* Espaçamento entre os retângulos */
        #padding: 20px;
        #border-radius: 10px;
#       }

    #/* Estilo para cada retângulo */
    #.indicador-box {
        #background: linear-gradient(135deg, #686767, #686767); /* Gradiente de cor */
        #color: white; /* Cor do texto */
        #text-align: center;
        #padding: 20px;
        #width: 160px; /* Largura fixa */
        #height: 90px; /* Altura fixa */
        #border-radius: 3px; /* Bordas arredondadas */
        #box-shadow: 0 4px 8px rgb(0, 0, 0); /* Sombra */
        #display: flex;
        #flex-direction: column;
        #justify-content: center;
        #align-items: center;
        #font-family: Arial, sans-serif;
        #font-size: 18px;
        #font-weight: bold;
        #transition: transform 0.3s ease-in-out; /* Animação ao passar o mouse */
    #}

    #/* Efeito hover nos retângulos */
    #.indicador-box:hover {
        #transform: scale(1.05); /* Leve aumento no tamanho */
        #cursor: pointer; /* Muda o cursor */
    #}
    #</style>

    #<!-- Estrutura dos Retângulos -->
    #<div class="indicadores-container">
        #<div class="indicador-box">
            #Finalizada<br>
            #<span style="font-size: 20px;">15</span>
        #</div>
        #<div class="indicador-box">
            #Em Andamento<br>
            #<span style="font-size: 20px;">7</span>
        #</div>
        #<div class="indicador-box">
            #Aberta<br>
            #<span style="font-size: 20px;">5</span>
        #</div>
        #<div class="indicador-box">
            #Cancelada<br>
            #<span style="font-size: 20px;">30%</span>
        #</div> 
        #<div class="indicador-box">
            #Indicador 4<br>
            #<span style="font-size: 20px;">30%</span>
        #</div>
        #<div class="indicador-box">
            #Indicador 4<br>
            #<span style="font-size: 20px;">30%</span>
        #</div>

    #</div>
#"""

    # Inserir HTML no Streamlit
    #st.markdown(html_code, unsafe_allow_html=True)

   

    #import pandas as pd
    #import plotly.express as px
    #import streamlit as st

    # Leitura do arquivo Excel
    #df_geral = pd.read_excel(
        #io='data.xlsx',  # endereço do arquivo
        #index_col=2,  # referência inicial para contagem de coluna
        #dtype=str,  # tipo de leitura de dados str
        #engine='openpyxl',  # biblioteca para leitura Excel
        #sheet_name='Planilha1',
        #usecols='A:W',  # delimitação de colunas
        #nrows=4400  # delimitação de linhas
    #)

    # Filtrando as colunas que precisamos
    #df_filtered = df_geral[['EQUIPAMENTO', 'STATUS']].dropna()

    # Criando o multiselect para selecionar os equipamentos
    #equipamentos_unicos = df_filtered['EQUIPAMENTO'].unique()
    #equipamentos_selecionados = st.multiselect(
        #'Selecione os equipamentos:', 
        #options=equipamentos_unicos, 
        #default=equipamentos_unicos.tolist()  # Definir todos como padrão
    #)

    # Filtrando os dados com base nos equipamentos selecionados
    #df_filtrado_equipamentos = df_filtered[df_filtered['EQUIPAMENTO'].isin(equipamentos_selecionados)]

    # Contagem dos status para os equipamentos selecionados
    #contagem_status = df_filtrado_equipamentos.groupby('STATUS').size().reset_index(name='Count')

    # Gráfico de barras usando Plotly
    #fig_bar = px.bar(contagem_status, 
                    #x='STATUS', 
                    #y='Count', 
                    #title=f'Distribuição de Status para Equipamentos Selecionados', 
                    #labels={'STATUS': 'Tipo de Status', 'Count': 'Quantidade'},
                    #color='STATUS', 
                    #color_discrete_sequence=['#B11515', '#4473C5', '#9DC3E7', 'grey'])
                    

    # Adicionar rótulos diretamente no topo das barras
 #   fig_bar.update_traces(
 #       text=contagem_status['Count'].astype(str),  # Passar a contagem diretamente nos rótulos
 #       textposition='outside',  # Coloca o texto fora da barra
 #       texttemplate='%{text}',   # Exibe o valor de contagem no rótulo
 #       showlegend=True
 #   )

    # Exibir o gráfico no Streamlit
 #   st.plotly_chart(fig_bar)

    
    # Gráfico de pizza

    # Exibir os gráficos no Streamlit
    #st.plotly_chart(fig_bar)
    #st.plotly_chart(fig_pie)
    
    
   # Ler dados do Excel
 #   df_geral = pd.read_excel(
 #      io='data.xlsx',  # endereço do arquivo
 #       index_col=2,  # Referência inicial para contagem de coluna
 #       dtype=str,  # Tipo de leitura de dados como string
 #       engine='openpyxl',  # Biblioteca para leitura Excel
 #       sheet_name='Planilha1',
 #       usecols='A:W',  # Delimitação de colunas
 #       nrows=4400  # Delimitação de linhas
#    )

 #   # Filtrar dados e contar tipos de manutenção
 #   df_filtered = df_geral[['TIPO DE MANUTENÇÃO']].dropna()  # Remove as linhas com valores ausentes
 #  count_adequacao = df_filtered[df_filtered['TIPO DE MANUTENÇÃO'] == 'Adequação de Segurança'].shape[0]
 #   count_corretiva = df_filtered[df_filtered['TIPO DE MANUTENÇÃO'] == 'Corretiva'].shape[0]
 #  count_fabricacao = df_filtered[df_filtered['TIPO DE MANUTENÇÃO'] == 'Fabricação'].shape[0]
 #   count_melhoria = df_filtered[df_filtered['TIPO DE MANUTENÇÃO'] == 'Melhoria'].shape[0]
 #   count_pintura = df_filtered[df_filtered['TIPO DE MANUTENÇÃO'] == 'Pintura'].shape[0]
 #   count_preventiva = df_filtered[df_filtered['TIPO DE MANUTENÇÃO'] == 'Preventiva'].shape[0]

 #   # Criar um DataFrame para os gráficos
 #   status_data = {
 #       'TIPO DE MANUTENÇÃO': ['Adequação de Segurança', 'Corretiva', 'Fabricação', 'Melhoria', 'Pintura', 'Preventiva'],
 #       'Count': [count_adequacao, count_corretiva, count_fabricacao, count_melhoria, count_pintura, count_preventiva]
 #   }
 #   df_status = pd.DataFrame(status_data)

    # Gráfico de barras
 #   fig_bar = px.bar(
 #       df_status,
 #       x='TIPO DE MANUTENÇÃO',
 #       y='Count',
 #       title='Distribuição de Tipos de Manutenção',
 #       labels={'TIPO DE MANUTENÇÃO': 'Tipo de Manutenção', 'Count': 'Quantidade'},
 #       color='TIPO DE MANUTENÇÃO',
 #       color_discrete_sequence= ['#B11515','#4473C5','#9DC3E7','grey', '#E1E6E3','#800000'] #cores personalizadas 
 #   )

    # Adicionar rótulos no topo das barras
  #  fig_bar.update_traces(
  #      text=df_status['Count'],  # Rótulo correto para cada barra
  #      textposition='outside',  # Coloca o texto fora da barra
  #      texttemplate='%{text}',  # Exibe o valor de contagem no rótulo
  #      showlegend=False  # Remove legenda desnecessária
  #  )

    # Exibir o gráfico no Streamlit
    #st.plotly_chart(fig_bar)

    #if menu == 'Requisições':
        
        #df_req = pd.read_excel(
        #io = 'dados.xlsx', # endereço do arquivo
        #index_col=0, # referência inicial para contagem de coluna 
        #dtype= str, # tipo de leitura de dados str
        #engine='openpyxl', # biblioteca para leitura excel
        #sheet_name='REQUISIÇÃO',
        #usecols='A:F', # delimitação de colunas
        #nrows=4400 # delimitação de linhas
        #)
        
        #df_req

# Verifica se a planta selecionada é "C"
#if menu == 'BACKLOG':
        
    # Leitura do arquivo Excel
#    df_log = pd.read_excel(
#        io='data.xlsx',  # endereço do arquivo
#        index_col=0,  # referência inicial para contagem de coluna 
#        dtype=str,  # tipo de leitura de dados str
#       engine='openpyxl',  # biblioteca para leitura excel
#        sheet_name='DISPONIBILIDADE',  # aba a ser lida
#        usecols='A:D',  # delimitação de colunas
#        nrows=4400  # delimitação de linhas
#    )