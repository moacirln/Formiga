import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

#Criação de um DataFrame vazio para evitar error até upload
def frame_prov():
    colunas = ['CNPJ', 'NCM', 'COD_PRO', 'LOTE', 'PEDIDO',
               'NF', 'SERIE', 'TIPO', 'STATUS', 'COND', 'COND_PAG', 'NF_ORIG', 'PRCUNIT',
               'PERCIC', 'CFOP', 'NOVA_COMISS', 'COD_VEND', 'PERC1', 'COD_GER', 'COMIS_GER',
               'PERC3', 'TOT_COMISS', 'MENNOTA', 'D2_PEDIDO', 'D2_ITEMPV', 'F2_TRANSP',
               'COD_VEND2', 'PERC2', 'COMIS_VEND2','RECEITA', 'TIPONF','UM', 'TOTAL','PRODUTO','VENDEDOR','CLIENTE','COMIS_VEND','UF','QUANTIDADE','EMISSAO','ICMS','LOJA','NOME_MÊS','MÊS','ANO','DIA']

    # Criando um DataFrame vazio com as colunas especificadas
    df = pd.DataFrame(columns=colunas)
    return df


#Função de agregação por data
def agreg (df, data, metrica):
    df_data = df.groupby(data)[metrica].sum()
    return(df_data)

#Função de filtro do DataFrame
def filtro(df, filtros):
    df_filtrado = df.copy()

    for coluna, filtro in filtros.items():
        if filtro:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(filtro)]

    return df_filtrado

def n_filtro(df, filtros):
    df_filtrado = df.copy()

    for coluna, filtro in filtros.items():
        if filtro:
            df_filtrado = df_filtrado[~df_filtrado[coluna].isin(filtro)]

    return df_filtrado

#Função para formatar números R$
def format (valor):

    str_valor = '{:,.2f}'.format(valor)
    partes = str_valor.split('.')

    # Adicionando pontos a cada três dígitos na parte inteira
    parte_inteira_com_pontos = partes[0].replace(',', '.')

    # Juntando a parte inteira com os pontos e a parte decimal
    return f'R${parte_inteira_com_pontos},{partes[1]}'

def format_num(valor):
    str_valor = '{:,.2f}'.format(valor)
    partes = str_valor.split('.')

    # Adicionando pontos a cada três dígitos na parte inteira
    parte_inteira_com_pontos = partes[0].replace(',', '.')

    # Juntando a parte inteira com os pontos e a parte decimal
    return f'{parte_inteira_com_pontos},{partes[1]}'

@st.cache_data
def tratar_dados(upload):
    # Importação da base de dados
    if upload:
        df = pd.read_csv(upload, sep=';', low_memory=False)
        df = df.drop(['CNPJ', 'NCM', 'COD_PRO', 'LOTE', 'PEDIDO',
                              'NF', 'SERIE', 'TIPO', 'STATUS',
                              'COND', 'COND_PAG', 'NF_ORIG', 'PRCUNIT',
                              'PERCIC', 'CFOP', 'NOVA_COMISS', 'COD_VEND',
                              'PERC1', 'COD_GER', 'COMIS_GER', 'PERC3', 'TOT_COMISS', 'MENNOTA',
                              'D2_PEDIDO', 'D2_ITEMPV', 'F2_TRANSP', 'COD_VEND2', 'PERC2',
                              'COMIS_VEND2', 'TIPONF'
                              ], axis=1)

        # Definição dos tipos de variáveis e novas colunas
        df['TOTAL'] = df['TOTAL'].str.replace(',', '.').astype(float)
        df['LOJA'] = 'LOJA ' + df['LOJA'].astype(str)
        df['LOJA'] = df['LOJA'].astype(str)
        df['COMIS_VEND'] = df['COMIS_VEND'].str.replace(',', '.').astype(float)
        df['QUANTIDADE'] = df['QUANTIDADE'].str.replace(',', '.').astype(float)
        df['ICMS'] = df['ICMS'].str.replace(',', '.').astype(float)
        df['DIA'] = pd.to_datetime(df['EMISSAO'], format='%Y%m%d', errors='coerce')
        df['RECEITA'] = df['TOTAL'] - df['ICMS']
        df['MÊS'] = df['DIA'].dt.month
        df['NOME_MÊS'] = df['DIA'].dt.strftime('%B')
        df['ANO'] = df['DIA'].dt.year
        return df


nome_toggle = 'Retirar Itens'

def main():
    #Configuração página inicial
    st.set_page_config(page_title='Dashboard Financeiro', layout= 'wide', initial_sidebar_state='collapsed')

    uploaded_files = st.file_uploader("Upload CSV", accept_multiple_files=False)

    if uploaded_files:
        df = tratar_dados(uploaded_files)
    else:
        df= frame_prov()



    # Estilos de Fontes
    st.markdown("""
                   <style>
                       .header {
                           font-size: 30px;
                           font-weight: bold;
                           font-family: 'Helvetica', sans-serif;
                           margin-bottom: -20px;
                           text-align: center;
                       }
                   </style>
               """, unsafe_allow_html=True)

    st.markdown("""
                      <style>
                          .header2 {
                              font-size: 35px;
                              font-weight: bold;
                              font-family: 'Helvetica', sans-serif;
                              margin-bottom: -20px;
                              margin-top: 26px;
                              text-align: center;
                          }
                      </style>
                  """, unsafe_allow_html=True)

    st.markdown("""
                       <style>
                           .value {
                               font-size: 22px;
                               font-family: 'Helvetica', sans-serif;
                               text-align: center;
                           }
                       </style>
                   """, unsafe_allow_html=True)

    st.markdown("""
                           <style>
                               .value2 {
                                   font-size: 18px;
                                   font-family: 'Helvetica', sans-serif;
                                   text-align: center;
                               }
                           </style>
                       """, unsafe_allow_html=True)

    st.markdown("""
                              <style>
                                  .title2 {
                                      font-size: 70px;
                                      font-family: 'Helvetica', sans-serif;
                                      font-weight: bold;
                                      margin-bottom: 60px;
                                      
                                  }
                              </style>
                          """, unsafe_allow_html=True)


    #SIDEBAR ---------------------------------------------------------------
    st.sidebar.title('Filtros')

    #Toggle para adicionar ou retirar
    on = st.sidebar.toggle('Excluir Itens')

    #Seleção de Filtros
    selected_months = st.sidebar.multiselect("Selecione os meses", df['NOME_MÊS'].unique())
    selected_years = st.sidebar.multiselect("Selecione os anos", df['ANO'].unique())
    selected_vendedor = st.sidebar.multiselect("Selecione o vendedor", sorted(df['VENDEDOR'].unique()))
    selected_loja = st.sidebar.multiselect("Selecione a loja", sorted(df['LOJA'].unique()))
    selected_UF = st.sidebar.multiselect("Selecione as regiões", df['UF'].unique())

    # Aplicação de Filtros
    filtros = {
        'NOME_MÊS': selected_months,
        'ANO': selected_years,
        'LOJA': selected_loja,
        'VENDEDOR': selected_vendedor,
        'UF': selected_UF
    }

    # DataFrame Filtrado***********
    if on:
        st.sidebar.write('Excluindo')
        df_filtrado = n_filtro(df, filtros)

    else:
        st.sidebar.write('Adicionando')
        df_filtrado = filtro(df, filtros)

    #BACK-END----------------------------------------------------------------------------
    # Qtd. por Kg, Lt, Pc e Un
    qtd = df_filtrado.groupby('UM')['QUANTIDADE'].sum()
    qtd = qtd.reset_index()

    qtd_kg = qtd[qtd['UM'] == 'KG']['QUANTIDADE']
    qtd_kg = qtd_kg.values[0] if not qtd_kg.empty else 0

    qtd_lt = qtd[qtd['UM'].str.startswith('L')]['QUANTIDADE']
    qtd_lt = qtd_lt.values[0] if not qtd_lt.empty else 0

    qtd_pc = qtd[qtd['UM'] == 'PC']['QUANTIDADE']
    qtd_pc = qtd_pc.values[0] if not qtd_pc.empty else 0

    qtd_un = qtd[qtd['UM'] == 'UN']['QUANTIDADE']
    qtd_un = qtd_un.values[0] if not qtd_un.empty else 0

    #Faturamento
    faturamento = df_filtrado['TOTAL'].sum()

    # Receita
    receita = df_filtrado['RECEITA'].sum()

    # Ticket Médio por Kg, Lt, Pc, Un
    tckt_med_kg = receita / qtd_kg if not qtd_kg == 0 else 0
    tckt_med_lt = receita / qtd_lt if not qtd_lt == 0 else 0
    tckt_med_pc = receita / qtd_pc if not qtd_pc == 0 else 0
    tckt_med_un = receita / qtd_un if not qtd_un == 0 else 0

    if uploaded_files:
        #FRONT-END---------------------------------------------------------------
        #Primeira Tela
        st.markdown('<p class="title2">{}</p>'.format('VISÃO GERAL'), unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3.5])

        container1 = col1.container(border=True, height=825)
        container1.markdown('<p class="header2">{}</p>'.format('Faturamento'), unsafe_allow_html=True)
        container1.markdown('<p class="value">{}</p>'.format(format(faturamento)), unsafe_allow_html=True)

        container1.markdown('<p class="header2">{}</p>'.format('Receita'), unsafe_allow_html=True)
        container1.markdown('<p class="value">{}</p>'.format(format(receita)), unsafe_allow_html=True)

        container1.markdown('<p class="header2">{}</p>'.format('Qtd. Vendas'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format_num(qtd_kg)} (Kg)'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format_num(qtd_lt)} (Lt)'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format_num(qtd_pc)} (Pct.)'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format_num(qtd_un)} (Unit.)'), unsafe_allow_html=True)

        container1.markdown('<p class="header2">{}</p>'.format('Ticket Médio'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format(tckt_med_kg)} (Kg)'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format(tckt_med_lt)} (Lt)'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format(tckt_med_pc)} (Pct.)'), unsafe_allow_html=True)
        container1.markdown('<p class="value2">{}</p>'.format(f'{format(tckt_med_un)} (Unit.)'), unsafe_allow_html=True)

        df_data = agreg(df_filtrado, 'UF', 'TOTAL')
        df_data = df_data[df_data.values > 1000]

        profundidade = col2.slider('Camadas de Visualização:', 1,3,3)
        fig = px.sunburst(df_filtrado, path=['UF', 'LOJA', 'VENDEDOR'], values='TOTAL',color_discrete_sequence=px.colors.qualitative.Pastel, width=800, height=800,maxdepth=profundidade)
        fig.update_layout(margin=dict(t=0))  # Reduz a margem superior
        config = {'scrollZoom': True}
        col2.plotly_chart(fig,use_container_width=True, config=config)


        #Segunda Tela
        st.divider()
        st.markdown('<p class="title2">{}</p>'.format('FATURAMENTO'), unsafe_allow_html=True)
        freq = st.selectbox('Selecione a agregação', ['MÊS', 'DIA', 'ANO'])

        col1, col2 = st.columns([1, 0.3])
        container2 = col1.container(border=True, height=550)
        df_data = agreg(df_filtrado, freq, 'TOTAL')
        fig = px.area(df_data, x=df_data.index, y=df_data.values, pattern_shape_sequence="x")
        fig.update_yaxes(title='FATURAMENTO')
        container2.plotly_chart(fig, use_container_width=True)

        #col2.markdown('<div style="margin-top: 37px;"></div>', unsafe_allow_html=True)
        col2.dataframe(df_data, height=550, use_container_width=True)

        #Terceita Tela
        st.divider()

        st.markdown('<p class="title2">{}</p>'.format('TOP N'), unsafe_allow_html=True)
        metrica = st.selectbox('Selecione a agregação', ['VENDEDOR', 'PRODUTO', 'NOME_CLIENTE', 'UF','LOJA'])
        n = st.slider('Número de Visualizações', 1, df_filtrado[metrica].nunique(), 10)
        top = df_filtrado.groupby(metrica)['TOTAL'].sum().reset_index()
        top = top.sort_values(by='TOTAL', ascending=False)
        top = top.drop(index=top.index[n:]).reset_index(drop=True)

        col1,col2 = st.columns([1,2.5])
        container3 = col1.container(border=False, height=700)
        container4 = col2.container(border=True, height=550)
        fig = go.Figure(data=[go.Table(
            header=dict(values=[metrica, 'FATURAMENTO'],
                        line_color='darkblue',
                        fill_color='#83c9ff',
                        height = 35,
                        font=dict(color='darkblue', size=18),  # Corrigido aqui
                        align='left'),
            cells=dict(values=[top[metrica],  # 1st column
                               top['TOTAL']],  # 2nd column
                       line_color='white',
                       fill_color='black',
                       font=dict(color='white', size=15),
                       height = 30,
                       align='left'))
        ])

        fig.update_layout(margin=dict(t=1,b=0,l=1,r=1))
        fig.update_layout(height = 548)
        container3.plotly_chart(fig, use_container_width=True)

        x = top[top.columns[0]].tolist()
        y = top[top.columns[1]].tolist()

        # Gráfico Barras
        fig = px.bar(x=x, y=y, width=1000)
        fig.update_yaxes(title='FATURAMENTO')
        fig.update_xaxes(title='')
        fig.update_layout(margin=dict(t=1, b=0, l=1, r=1))
        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.7)
        #config = {'scrollZoom': True}
        container4.plotly_chart(fig,use_container_width=True)



        #Quarta Tela
        st.divider()
        st.markdown('<p class="title2">{}</p>'.format('DESEMPENHO'), unsafe_allow_html=True)

        dimensao = st.selectbox('Escolha uma dimensão', options=['NOME_CLIENTE', 'PRODUTO', 'VENDEDOR', 'UF', 'LOJA'])
        lista_selecao = ['NOME_CLIENTE', 'PRODUTO', 'VENDEDOR', 'UF', 'LOJA']
        lista_selecao.remove(dimensao)
        df_vendedores = df_filtrado.drop(
            columns=[*lista_selecao, 'COMIS_VEND', 'QUANTIDADE', 'CLIENTE', 'EMISSAO', 'UM', 'ICMS', 'ANO', 'DIA', 'MÊS',
                     'NOME_MÊS'])

        df_vendedores = df_vendedores.groupby(dimensao).sum().reset_index()
        df_vendedores = df_vendedores.sort_values(by='TOTAL', ascending=False)
        df_vendedores['% TOTAL'] = df_vendedores['TOTAL']/faturamento
        # Calcule a porcentagem acumulada
        df_vendedores['% ACUMULADA'] = df_vendedores['TOTAL'].cumsum() / df_vendedores['TOTAL'].sum() * 100



        # Gráfico de curva ABC
        fig = px.line(df_vendedores, x=dimensao, y='% ACUMULADA', markers=True,
                      labels={'% ACUMULADA': 'Porcentagem Acumulada'}, width=1000)
        fig.update_traces(hovertemplate='%{y:.2f}%<br>%{x}')
        fig.update_layout(
            xaxis_title='Dimensão',
            yaxis_title='Porcentagem Acumulada',
            title='Curva ABC',
            height = 800,
        )
        st.plotly_chart(fig,use_container_width=True)

        # Exibir o DataFrame estilizado no Streamlit
        st.dataframe(df_vendedores, hide_index=True, width=1000, use_container_width=True)


if __name__ == '__main__':
    main()

