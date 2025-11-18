import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Simulador Algomix", layout="wide")

# --- CSS PARA ESTILIZAR (OPCIONAL) ---
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; color: #003366; }
    .metric-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS FIXOS DA TABELA (SEU SEGREDO INDUSTRIAL) ---
# Transcrito exatamente das colunas fixas e fórmulas enviadas
dados_base = [
    # Fator de ajuste: Nas primeiras semanas sua fórmula é (PesoInicial + X%). 
    # Da semana 16 em diante é Média (Inicial+Final)/2.
    # Vou usar 'tipo_calc': 'fator' ou 'media'.
    {"semana": 1,  "fase": "Berçário 1", "dias": 7,  "p_ini": 0.500,   "p_fim": 2.500,   "bio": 0.1300, "fator_ajuste": 0.10, "tipo_calc": "fator"},
    {"semana": 2,  "fase": "Berçário 1", "dias": 14, "p_ini": 2.500,   "p_fim": 4.600,   "bio": 0.1200, "fator_ajuste": 0.15, "tipo_calc": "fator"},
    {"semana": 3,  "fase": "Berçário 2", "dias": 21, "p_ini": 4.600,   "p_fim": 7.820,   "bio": 0.0900, "fator_ajuste": 0.20, "tipo_calc": "fator"},
    {"semana": 4,  "fase": "Berçário 2", "dias": 28, "p_ini": 7.820,   "p_fim": 12.686,  "bio": 0.0800, "fator_ajuste": 0.20, "tipo_calc": "fator"},
    {"semana": 5,  "fase": "Recria 1",   "dias": 35, "p_ini": 12.686,  "p_fim": 19.592,  "bio": 0.0700, "fator_ajuste": 0.20, "tipo_calc": "fator"},
    {"semana": 6,  "fase": "Recria 1",   "dias": 42, "p_ini": 19.592,  "p_fim": 27.821,  "bio": 0.0600, "fator_ajuste": 0.20, "tipo_calc": "fator"},
    {"semana": 7,  "fase": "Recria 2",   "dias": 49, "p_ini": 27.821,  "p_fim": 39.117,  "bio": 0.0580, "fator_ajuste": 0.20, "tipo_calc": "fator"},
    {"semana": 8,  "fase": "Recria 2",   "dias": 56, "p_ini": 39.117,  "p_fim": 54.177,  "bio": 0.0550, "fator_ajuste": 0.05, "tipo_calc": "fator"},
    {"semana": 9,  "fase": "Recria 2",   "dias": 63, "p_ini": 54.177,  "p_fim": 71.415,  "bio": 0.0500, "fator_ajuste": 0.05, "tipo_calc": "fator"},
    {"semana": 10, "fase": "Engorda 1",  "dias": 70, "p_ini": 71.415,  "p_fim": 91.865,  "bio": 0.0450, "fator_ajuste": 0.05, "tipo_calc": "fator"},
    {"semana": 11, "fase": "Engorda 1",  "dias": 77, "p_ini": 91.865,  "p_fim": 117.003, "bio": 0.0430, "fator_ajuste": 0.10, "tipo_calc": "fator"},
    {"semana": 12, "fase": "Engorda 1",  "dias": 84, "p_ini": 117.003, "p_fim": 146.786, "bio": 0.0400, "fator_ajuste": 0.10, "tipo_calc": "fator"},
    {"semana": 13, "fase": "Engorda 1",  "dias": 91, "p_ini": 146.786, "p_fim": 182.281, "bio": 0.0380, "fator_ajuste": 0.10, "tipo_calc": "fator"},
    {"semana": 14, "fase": "Engorda 1",  "dias": 98, "p_ini": 182.281, "p_fim": 219.497, "bio": 0.0350, "fator_ajuste": 0.10, "tipo_calc": "fator"},
    {"semana": 15, "fase": "Engorda 1",  "dias": 105,"p_ini": 219.497, "p_fim": 261.750, "bio": 0.0330, "fator_ajuste": 0.10, "tipo_calc": "fator"},
    # A partir daqui (Semana 16), a fórmula muda para média simples (Inicial+Final)/2
    {"semana": 16, "fase": "Engorda 2",  "dias": 112,"p_ini": 261.750, "p_fim": 304.033, "bio": 0.0300, "tipo_calc": "media"},
    {"semana": 17, "fase": "Engorda 2",  "dias": 119,"p_ini": 304.033, "p_fim": 349.872, "bio": 0.0280, "tipo_calc": "media"},
    {"semana": 18, "fase": "Engorda 2",  "dias": 126,"p_ini": 349.872, "p_fim": 400.737, "bio": 0.0270, "tipo_calc": "media"},
    {"semana": 19, "fase": "Engorda 2",  "dias": 133,"p_ini": 400.737, "p_fim": 447.490, "bio": 0.0250, "tipo_calc": "media"},
    {"semana": 20, "fase": "Engorda 2",  "dias": 140,"p_ini": 447.490, "p_fim": 494.477, "bio": 0.0225, "tipo_calc": "media"},
    {"semana": 21, "fase": "Engorda 2",  "dias": 147,"p_ini": 494.477, "p_fim": 545.935, "bio": 0.0223, "tipo_calc": "media"},
    {"semana": 22, "fase": "Engorda 2",  "dias": 154,"p_ini": 545.935, "p_fim": 599.437, "bio": 0.0210, "tipo_calc": "media"},
    {"semana": 23, "fase": "Engorda 2",  "dias": 161,"p_ini": 599.437, "p_fim": 653.986, "bio": 0.0195, "tipo_calc": "media"},
    {"semana": 24, "fase": "Engorda 2",  "dias": 168,"p_ini": 653.986, "p_fim": 706.345, "bio": 0.0183, "tipo_calc": "media"},
    {"semana": 25, "fase": "Engorda 2",  "dias": 175,"p_ini": 706.345, "p_fim": 755.789, "bio": 0.0170, "tipo_calc": "media"},
    {"semana": 26, "fase": "Engorda 2",  "dias": 182,"p_ini": 755.789, "p_fim": 802.816, "bio": 0.0160, "tipo_calc": "media"},
    {"semana": 27, "fase": "Engorda 2",  "dias": 189,"p_ini": 802.816, "p_fim": 850.140, "bio": 0.0160, "tipo_calc": "media"},
    {"semana": 28, "fase": "Engorda 3",  "dias": 196,"p_ini": 850.140, "p_fim": 898.688, "bio": 0.0155, "tipo_calc": "media"},
    {"semana": 29, "fase": "Engorda 3",  "dias": 203,"p_ini": 898.688, "p_fim": 949.345, "bio": 0.0153, "tipo_calc": "media"},
    {"semana": 30, "fase": "Engorda 3",  "dias": 210,"p_ini": 949.345, "p_fim": 1001.809,"bio": 0.0150, "tipo_calc": "media"},
    {"semana": 31, "fase": "Engorda 3",  "dias": 217,"p_ini": 1001.809,"p_fim": 1056.434,"bio": 0.0148, "tipo_calc": "media"},
    {"semana": 32, "fase": "Engorda 3",  "dias": 224,"p_ini": 1056.434,"p_fim": 1112.870,"bio": 0.0145, "tipo_calc": "media"},
    {"semana": 33, "fase": "Engorda 3",  "dias": 231,"p_ini": 1112.870,"p_fim": 1171.501,"bio": 0.0143, "tipo_calc": "media"},
    {"semana": 34, "fase": "Engorda 3",  "dias": 238,"p_ini": 1171.501,"p_fim": 1231.925,"bio": 0.0140, "tipo_calc": "media"},
]

# --- INTERFACE LATERAL (INPUTS GERAIS) ---
st.sidebar.image("https://algomix.com.br/wp-content/uploads/2021/08/logo-algomix.png", width=200) # Tentei pegar logo da web, se não carregar, remova
st.sidebar.header("Parâmetros da Simulação")

qtd_peixes = st.sidebar.number_input("Quantidade de Peixes", value=100000, step=1000)
peso_inicial_user = st.sidebar.number_input("Peso Inicial (g) para Simulação", value=0.5)
peso_final_user = st.sidebar.number_input("Peso Final (g) para Simulação", value=850.0)

st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para Equipe Algomix")

# --- CORPO PRINCIPAL (PREÇOS) ---
st.title("🐟 Simulador de Custo - Tilápia")
st.markdown("Insira os valores da **SACA (25kg)** para cada fase:")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Fase Inicial")
    p_bercario1 = st.number_input("Preço Saca - Berçário 1", value=115.41)
    p_bercario2 = st.number_input("Preço Saca - Berçário 2", value=104.60)

with col2:
    st.subheader("Recria")
    p_recria1 = st.number_input("Preço Saca - Recria 1", value=89.76)
    p_recria2 = st.number_input("Preço Saca - Recria 2", value=69.50)

with col3:
    st.subheader("Engorda")
    p_engorda1 = st.number_input("Preço Saca - Engorda 1", value=66.00)
    p_engorda2 = st.number_input("Preço Saca - Engorda 2", value=62.25)
    p_engorda3 = st.number_input("Preço Saca - Engorda 3", value=62.25)

# Mapeamento de Preços por Fase
precos_map = {
    "Berçário 1": p_bercario1,
    "Berçário 2": p_bercario2,
    "Recria 1": p_recria1,
    "Recria 2": p_recria2,
    "Engorda 1": p_engorda1,
    "Engorda 2": p_engorda2,
    "Engorda 3": p_engorda3
}

# --- CÁLCULOS ---
resultados = []
custo_total_acumulado = 0
racao_total_acumulada = 0

for linha in dados_base:
    # Verificação se a semana está dentro do range de peso solicitado pelo cliente
    # A lógica: Se o peso inicial da semana é menor que o peso final desejado 
    # E o peso final da semana é maior que o peso inicial desejado
    dentro_do_range = (linha["p_ini"] < peso_final_user) and (linha["p_fim"] > peso_inicial_user)
    
    if dentro_do_range:
        # 1. Definição do Peso para cálculo de ração (baseado na sua fórmula)
        if linha["tipo_calc"] == "fator":
            # Fórmula Semanas 1-15: PesoInicial + (PesoInicial * Fator)
            peso_base_calculo = linha["p_ini"] + (linha["p_ini"] * linha["fator_ajuste"])
        else:
            # Fórmula Semana 16+: Média (Inicial + Final) / 2
            peso_base_calculo = (linha["p_ini"] + linha["p_fim"]) / 2
        
        # 2. Cálculo Ração Dia (kg) -> (QtdPeixes * PesoBase * %Bio) / 1000
        racao_dia = (qtd_peixes * peso_base_calculo * linha["bio"]) / 1000
        
        # 3. Cálculo Ração Semana (kg)
        racao_semana = racao_dia * 7
        
        # 4. Custos
        preco_saca = precos_map[linha["fase"]]
        preco_kg = preco_saca / 25.0
        custo_semana = racao_semana * preco_kg
        
        # Acumula Totais
        custo_total_acumulado += custo_semana
        racao_total_acumulada += racao_semana
        
        sacas_necessarias = racao_semana / 25.0
        
        resultados.append({
            "Fase": linha["fase"],
            "Semana": f"{linha['semana']}ª",
            "Peso Inicial (g)": linha["p_ini"],
            "Peso Final (g)": linha["p_fim"],
            "Ração/Dia (kg)": round(racao_dia, 1),
            "Total Ração (kg)": round(racao_semana, 1),
            "Sacas": round(sacas_necessarias, 1),
            "Custo (R$)": round(custo_semana, 2)
        })

# --- EXIBIÇÃO DOS RESULTADOS ---
if len(resultados) > 0:
    st.markdown("---")
    st.subheader("📊 Resultado da Simulação")
    
    # Métricas Principais
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"<div class='metric-box'><b>Custo Total</b><br>R$ {custo_total_acumulado:,.2f}</div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-box'><b>Total Ração</b><br>{racao_total_acumulada/1000:,.1f} Ton</div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-box'><b>Total Sacas</b><br>{racao_total_acumulada/25:,.0f} sc</div>", unsafe_allow_html=True)
    if qtd_peixes > 0:
        custo_por_peixe = custo_total_acumulado / qtd_peixes
        m4.markdown(f"<div class='metric-box'><b>Custo/Peixe</b><br>R$ {custo_por_peixe:,.2f}</div>", unsafe_allow_html=True)

    # Tabela Detalhada
    st.write("")
    st.write("### Detalhamento Semana a Semana")
    df = pd.DataFrame(resultados)
    st.dataframe(df, use_container_width=True)
    
else:
    st.warning("Nenhuma semana encontrada para esse intervalo de peso.")
