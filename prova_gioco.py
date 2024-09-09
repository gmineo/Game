 
# import streamlit as st
# import yfinance as yf
# import plotly.graph_objs as go
# import time
# 
# 
# # Titolo dell'app
# st.header("Confronto Titoli Azionari - Variazione Percentuale")
# 
# # Input dell'utente per selezionare i simboli azionari
# stock_symbol_1 = st.sidebar.text_input("Inserisci il simbolo del primo titolo azionario (es: AAPL, TSLA, MSFT):", "AAPL")
# stock_symbol_2 = st.sidebar.text_input("Inserisci il simbolo del secondo titolo azionario (es: GOOGL, AMZN, FB):", "GOOGL")
# 
# # Input dell'utente per selezionare il periodo
# period = st.sidebar.selectbox("Seleziona il periodo di tempo:",
#                       ("1mo", "3mo", "6mo", "1y", "5y", "10y"))
# 
# 
# # Bottone per iniziare la generazione del grafico
# if st.button("Start"):
#     # Mostra un messaggio di caricamento
#     with st.spinner("Caricamento dei dati in corso..."):
#         # Carica i dati per entrambi i titoli selezionati
#         stock_data_1 = yf.download(stock_symbol_1, period=period)
#         stock_data_2 = yf.download(stock_symbol_2, period=period)
# 
#     # Calcola la variazione percentuale per il primo titolo
#     stock_data_1['Percent Change'] = (stock_data_1['Close'] - stock_data_1['Close'][0]) / stock_data_1['Close'][0] * 100
# 
#     # Calcola la variazione percentuale per il secondo titolo
#     stock_data_2['Percent Change'] = (stock_data_2['Close'] - stock_data_2['Close'][0]) / stock_data_2['Close'][0] * 100
# 
#     # Inizializza il grafico vuoto
#     fig = go.Figure()
# 
#     # Aggiungi una traccia vuota per il primo titolo
#     fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=stock_symbol_1))
# 
#     # Aggiungi una traccia vuota per il secondo titolo
#     fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=stock_symbol_2))
# 
#     # Imposta layout del grafico
#     fig.update_layout(title=f"Confronto Variazione Percentuale: {stock_symbol_1} vs {stock_symbol_2}",
#                       xaxis_title="Data",
#                       yaxis_title="Variazione Percentuale (%)")
# 
#     # Mostra il grafico iniziale vuoto
#     plotly_chart = st.plotly_chart(fig,width=30, height=8, use_container_width=False)
# 
#     # Determina la lunghezza minima dei dati per gestire il confronto (nel caso i due dataset abbiano lunghezze diverse)
#     min_length = min(len(stock_data_1), len(stock_data_2))
# 
#     # Inizializza i placeholder per mostrare le percentuali in tempo reale
#     percent_text_1 = st.empty()
#     percent_text_2 = st.empty()
# 
#     # Aggiungi i dati progressivamente per entrambi i titoli
#     for i in range(min_length):
#         # Aggiungi il punto successivo per il primo titolo
#         fig.data[0].x = stock_data_1.index[:i+1]
#         fig.data[0].y = stock_data_1['Percent Change'][:i+1]
# 
#         # Aggiungi il punto successivo per il secondo titolo
#         fig.data[1].x = stock_data_2.index[:i+1]
#         fig.data[1].y = stock_data_2['Percent Change'][:i+1]
# 
#         # Aggiorna il grafico
#         plotly_chart.plotly_chart(fig)
# 
#         # Aggiorna le percentuali in tempo reale sotto il grafico
#         percent_text_1.text(f"{stock_symbol_1}: {stock_data_1['Percent Change'][i]:.2f}%")
#         percent_text_2.text(f"{stock_symbol_2}: {stock_data_2['Percent Change'][i]:.2f}%")
# 
#         # Aspetta un secondo prima di aggiungere il punto successivo
#         time.sleep(0.1)
# 
#

!pip install -q streamlit

!npm install localtunnel

!streamlit run app.py &>/content/logs.txt &

!npx localtunnel --port 8501 & curl ipv4.icanhazip.com

