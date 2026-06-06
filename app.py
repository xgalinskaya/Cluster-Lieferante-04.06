import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# 1. Page Configuration
st.set_page_config(page_title="Kraljic Matrix Dashboard", layout="wide")

# 2. Caching Data Loader
@st.cache_data
def load_data():
    df = pd.read_csv('Merged dataset with Scores.csv', sep=';', decimal=',')
    df['Order Value USD'] = (
        df['Order Value USD']
        .astype(str)
        .str.replace(' ', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )  
    df['Quarter'] = pd.PeriodIndex(pd.to_datetime(df['Month']), freq='Q').astype(str)
    return df

# 3. Main Application Logic
def main():
    st.title("Sustainable Supply Chain: Kraljic Matrix")
    df = load_data()

    # --- INITIALISIERUNG DER GRENZEN (Einmal pro Jahr / Initial) ---
    if 'threshold_x' not in st.session_state or 'threshold_y' not in st.session_state:
        # Initialer Lauf über den gesamten Datensatz zur Festlegung
        scaler_init = MinMaxScaler(feature_range=(0, 100))
        # Einfache Aggregation für die Initialisierung
        init_df = df.groupby('Supplier_ID').agg({'Order Value USD': 'sum', 'Nachhaltigkeitsscore': 'mean'}).reset_index()
        init_df['Normalized_Spend'] = scaler_init.fit_transform(init_df[['Order Value USD']])
        
        # KMeans für die Initialisierung (feste Trennung)
        kmeans_init = KMeans(n_clusters=4, random_state=42, n_init=10).fit(init_df[['Normalized_Spend', 'Nachhaltigkeitsscore']])
        st.session_state.threshold_x = kmeans_init.cluster_centers_[:, 0].mean()
        st.session_state.threshold_y = kmeans_init.cluster_centers_[:, 1].mean()

    # Sidebar für manuelle Neuberechnung der Grenzen
    if st.sidebar.button("Grenzen neu berechnen (Reset)"):
        del st.session_state.threshold_x
        del st.session_state.threshold_y
        st.rerun()

    # --- SIDEBAR INTERFACE ---
    st.sidebar.header("Risk Component Weights")
    w1 = st.sidebar.slider("Performance Quality", 0, 100, 20)
    w2 = st.sidebar.slider("Financial Risk", 0, 100, 20)
    w3 = st.sidebar.slider("Sustainability Score", 0, 100, 20)
    w4 = st.sidebar.slider("Standards Risk", 0, 100, 20)
    w5 = st.sidebar.slider("Political Risk", 0, 100, 20)

    if (w1 + w2 + w3 + w4 + w5) != 100:
        st.error("Weights must sum to 100%.")
        st.stop()

    # --- FILTERING ---
    selected_cats = st.sidebar.multiselect("Product Category", options=df['Product_Category'].unique(), default=df['Product_Category'].unique())
    df_f = df[df['Product_Category'].isin(selected_cats)]

    # --- PREPROCESSING & AXES ---
    agg_df = df_f.groupby('Supplier_ID').agg({
        'Order Value USD': 'sum',
        'Performance_Quality_Score': 'mean',
        'Financial_Risk_Score_Quarterly': 'mean',
        'Nachhaltigkeitsscore': 'mean',
        'Standards Risks_Score': 'mean',
        'Risikoscore Political': 'mean'
    }).reset_index()

    scaler = MinMaxScaler(feature_range=(0, 100))
    agg_df['Normalized_Spend'] = scaler.fit_transform(agg_df[['Order Value USD']])
    
    risk_cols = ['Performance_Quality_Score', 'Financial_Risk_Score_Quarterly', 'Nachhaltigkeitsscore', 'Standards Risks_Score', 'Risikoscore Political']
    agg_df['Weighted_Risk'] = (agg_df[risk_cols].values * np.array([w1, w2, w3, w4, w5]) / 100).sum(axis=1) * 100

    # --- QUARDRANT ZUWEISUNG (Feste Grenzen) ---
    def map_quadrant(row):
        if row['Normalized_Spend'] > st.session_state.threshold_x and row['Weighted_Risk'] > st.session_state.threshold_y: return "Strategic"
        if row['Normalized_Spend'] > st.session_state.threshold_x and row['Weighted_Risk'] <= st.session_state.threshold_y: return "Leverage"
        if row['Normalized_Spend'] <= st.session_state.threshold_x and row['Weighted_Risk'] > st.session_state.threshold_y: return "Bottleneck"
        return "Non-Critical"

    agg_df['Kraljic_Quadrant'] = agg_df.apply(map_quadrant, axis=1)

    # --- VISUALIZATION ---
    st.write(f"Aktive Grenzwerte: X={st.session_state.threshold_x:.2f}, Y={st.session_state.threshold_y:.2f}")
    fig = px.scatter(agg_df, x="Normalized_Spend", y="Weighted_Risk", color="Kraljic_Quadrant", 
                     hover_data=['Supplier_ID'], title="Kraljic Matrix (Fixe Jahresgrenzen)")
    
    fig.add_hline(y=st.session_state.threshold_y, line_dash="dash", line_color="red")
    fig.add_vline(x=st.session_state.threshold_x, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(agg_df)

if __name__ == "__main__":
    main()
