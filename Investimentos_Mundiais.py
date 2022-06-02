import investpy as ip
import pandas as pd
import plotly.graph_objects as go 
from datetime import datetime, timedelta
import streamlit as st
import os 

dt_min = datetime.today() - timedelta(days=365)
dt_max = datetime.today()

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)



##BARRA LATERAL
st.sidebar.title('Investimentos')
barra_lateral = st.sidebar.empty()

df_acoes = ip.get_stocks_dict()

df_acoes = pd.DataFrame(list(df_acoes),
                   columns=['country', 'currency', 'full_name','symbol'])

selecionador_pais = st.sidebar.selectbox("Selecione o País",df_acoes['country'].unique())
#Ao filtrar o país aparecerá apenas as acçoes do respectivo país
selecionador_acao = st.sidebar.selectbox("Selecione a ação",df_acoes.loc[df_acoes['country'] == selecionador_pais]['symbol'])
nome_acao = list(df_acoes.loc[(df_acoes['country'] == selecionador_pais) & (df_acoes['symbol'] == selecionador_acao)]['full_name'])

st.title(nome_acao[0])


dt_min = st.sidebar.date_input('De: ', dt_min)
dt_max = st.sidebar.date_input('Até: ', dt_max)



df = ip.get_stock_historical_data(stock=selecionador_acao,
                                        country=selecionador_pais,
                                        from_date = format_date(dt_min),
                                        to_date = format_date(dt_max))

df = df.reset_index()

# Gerar medias moveis
Media_Movel = df['Close'].rolling(5).mean()
Media_Tendencia = df['Close'].rolling(30).mean()

##Gera os graficos

grafico_candle = st.empty()


fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])


## Adicionado a média movel
fig.add_trace(
    go.Scatter(
        x = df['Date'],
        y = Media_Movel,
        mode = 'lines',
        name = 'Média Móvel',
        marker_color = '#d62728',
        opacity = 0.5,
    )
)

## Adicionado a Tendencia
fig.add_trace(
    go.Scatter(
        x = df['Date'],
        y = Media_Tendencia,
        mode = 'lines',
        name = 'Tendência',
        marker_color = '#2ca02c'
    )
)

## Ajustes no layout
fig.update_layout(
    
    # Titulo
    title=f'Análise do fechamento - {selecionador_acao}<br><sup>{format_date(dt_min)} - {format_date(dt_max)}</sup>',
    # Tamanho
    titlefont_size=30,
    

    # Ajustando eixo x
    xaxis = dict(
        title='Período Histórico',
        titlefont_size = 14,
        tickfont_size=10,
    ),

    # Ajustando eixo y
    yaxis = dict(
        title='Preço fechamento ($)',
        titlefont_size = 14,
        tickfont_size=10,
    ),

    # Parametros para Legenda
    legend = dict (
        y=1,
        x=1,
        bgcolor='rgba(255, 255, 255, 1)',
        bordercolor='rgba(255, 255, 255, 1)'
    )
    
)
#fig.show()

grafico_candle = st.plotly_chart(fig)


#print('getcwd:      ', os.getcwd())
#print('__file__:    ', __file__)
#caminho_do_app = __file__

#os.system(f'streamlit run {caminho_do_app}')

