import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import time
import random
from datetime import datetime, timedelta

# Funzione per ottenere un intervallo di 3 anni casuali
def random_3_years():
    # Data corrente
    today = datetime.today()

    # Calcola una data casuale entro gli ultimi 20 anni
    random_start = today - timedelta(days=random.randint(3*365, 20*365))

    # Data finale è 3 anni dopo la data casuale di partenza
    random_end = random_start + timedelta(days=3*365)

    return random_start.strftime('%Y-%m-%d'), random_end.strftime('%Y-%m-%d')


# Titolo dell'app
st.header("Confronto Titoli Azionari - Portafoglio e S&P 500 (3 anni casuali)")

# Input dell'utente per selezionare i simboli azionari
stock_symbol_1 = st.sidebar.text_input("Inserisci il simbolo del primo titolo azionario (es: AAPL, TSLA, MSFT):", "AAPL")
stock_symbol_2 = st.sidebar.text_input("Inserisci il simbolo del secondo titolo azionario (es: GOOGL, AMZN, FB):", "GOOGL")

# Input dell'utente per inserire le percentuali del portafoglio per ogni titolo
weight_1 = st.sidebar.number_input(f"Inserisci la percentuale di {stock_symbol_1} nel portafoglio:", min_value=0, max_value=100, value=50)
weight_2 = st.sidebar.number_input(f"Inserisci la percentuale di {stock_symbol_2} nel portafoglio:", min_value=0, max_value=100, value=50)

# Controllo che la somma delle percentuali sia 100%
if weight_1 + weight_2 != 100:
    st.error("La somma delle percentuali deve essere esattamente 100%.")
else:
    # Bottone per iniziare la generazione del grafico
    if st.button("Start"):
        # Seleziona un intervallo di 3 anni casuale
        start_date, end_date = random_3_years()

        # Mostra le date scelte casualmente
        st.write(f"Periodo selezionato casualmente: dal **{start_date}** al **{end_date}**")

        # Mostra un messaggio di caricamento
        with st.spinner("Caricamento dei dati in corso..."):
            # Carica i dati per entrambi i titoli selezionati
            stock_data_1 = yf.download(stock_symbol_1, start=start_date, end=end_date)
            stock_data_2 = yf.download(stock_symbol_2, start=start_date, end=end_date)

            # Carica i dati per l'indice S&P 500
            sp500_data = yf.download("^GSPC", start=start_date, end=end_date)

        # Calcola la variazione percentuale per il primo titolo
        stock_data_1['Percent Change'] = (stock_data_1['Close'] - stock_data_1['Close'][0]) / stock_data_1['Close'][0] * 100

        # Calcola la variazione percentuale per il secondo titolo
        stock_data_2['Percent Change'] = (stock_data_2['Close'] - stock_data_2['Close'][0]) / stock_data_2['Close'][0] * 100

        # Calcola la variazione percentuale per l'S&P 500
        sp500_data['Percent Change'] = (sp500_data['Close'] - sp500_data['Close'][0]) / sp500_data['Close'][0] * 100

        # Calcola la variazione percentuale del portafoglio ponderato
        portfolio_change = (stock_data_1['Percent Change'] * (weight_1 / 100)) + (stock_data_2['Percent Change'] * (weight_2 / 100))

        # Inizializza il grafico vuoto
        fig = go.Figure()

        # Aggiungi una traccia vuota per il primo titolo
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=stock_symbol_1))

        # Aggiungi una traccia vuota per il secondo titolo
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=stock_symbol_2))

        # Aggiungi una traccia per l'indice S&P 500 (linea rossa)
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name="S&P 500", line=dict(color='red', width=2)))

        # Aggiungi una traccia per il portafoglio
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name="Portafoglio", line=dict(color='green', width=2, dash='dash')))

        # Imposta layout del grafico
        fig.update_layout(title=f"Confronto Variazione Percentuale: {stock_symbol_1} vs {stock_symbol_2} vs Portafoglio vs S&P 500",
                          xaxis_title="Data",
                          yaxis_title="Variazione Percentuale (%)")

        # Mostra il grafico iniziale vuoto
        plotly_chart = st.plotly_chart(fig, width=30, height=8, use_container_width=False)

        # Determina la lunghezza minima dei dati per gestire il confronto (nel caso i due dataset abbiano lunghezze diverse)
        min_length = min(len(stock_data_1), len(stock_data_2), len(sp500_data))

        # Calcola il tempo di attesa per ogni punto (in modo che il grafico si completi in 10 secondi)
        delay_per_point = 10 / min_length

        # Inizializza i placeholder per mostrare le percentuali in tempo reale
        percent_text_1 = st.empty()
        percent_text_2 = st.empty()
        percent_text_sp500 = st.empty()
        percent_text_portfolio = st.empty()

        # Aggiungi i dati progressivamente per entrambi i titoli, l'S&P 500 e il portafoglio
        for i in range(min_length):
            # Aggiungi il punto successivo per il primo titolo
            fig.data[0].x = stock_data_1.index[:i+1]
            fig.data[0].y = stock_data_1['Percent Change'][:i+1]

            # Aggiungi il punto successivo per il secondo titolo
            fig.data[1].x = stock_data_2.index[:i+1]
            fig.data[1].y = stock_data_2['Percent Change'][:i+1]

            # Aggiungi il punto successivo per l'S&P 500
            fig.data[2].x = sp500_data.index[:i+1]
            fig.data[2].y = sp500_data['Percent Change'][:i+1]

            # Aggiungi il punto successivo per il portafoglio
            fig.data[3].x = stock_data_1.index[:i+1]  # Le date sono le stesse del primo titolo
            fig.data[3].y = portfolio_change[:i+1]

            # Aggiorna il grafico
            plotly_chart.plotly_chart(fig)

            # Aggiorna le percentuali in tempo reale sotto il grafico
            percent_text_1.text(f"{stock_symbol_1}: {stock_data_1['Percent Change'][i]:.2f}%")
            percent_text_2.text(f"{stock_symbol_2}: {stock_data_2['Percent Change'][i]:.2f}%")
            percent_text_sp500.text(f"S&P 500: {sp500_data['Percent Change'][i]:.2f}%")
            percent_text_portfolio.text(f"Portafoglio: {portfolio_change[i]:.2f}%")

            # Aspetta il tempo calcolato prima di aggiungere il punto successivo
            time.sleep(delay_per_point)
