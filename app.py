import streamlit as st
import pandas as pd
import math

# --- CONFIGURAÇÃO E CSS (Otimizado para impressão e esconder sidebar) ---
st.set_page_config(page_title="Simulador Algomix", layout="wide")

st.markdown("""
    <style>
    /* Otimização para Impressão */
    @media print {
        /* Esconde a barra lateral (Sidebar) para liberar espaço) */
        [data-testid="stSidebar"] {
            display: none !important; 
            visibility: hidden;
            width: 0px !important;
        }
        /* Força o conteúdo principal a ocupar a largura total, removendo margens */
        .main {
            padding: 0px !important; 
            margin: 0px !important; 
            width: 100% !important;
            max-width: 100% !important;
        }
        /* Esconde elementos de menu e outros itens desnecessários */
        header, footer, [data-testid="stToolbar"] { visibility: hidden !important; }

    }
    .metric-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #003366; }
    .stApp > header { visibility: hidden; }
    h1 { margin-top: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS FIXOS DA TABELA (SEU SEGREDO INDUSTRIAL - MANTIDO) ---
# ... (O array 'dados_base' de 34 semanas permanece igual ao código anterior) ...
dados_base = [
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

# --- MAPEAMENTO DE OPÇÕES DE RAÇÃO (NOVO) ---
# Usando preços médios sugeridos para preenchimento inicial
OPCOES_RACAO = {
    "Berçário 1": {
        "FISHMIX EVOLUTION INICIAL 45% PÓ": 4.62, 
        "FISHMIX EVOLUTION PRE-INICIAL 58% PÓ": 5.00 
    },
    "Berçário 2": {
        "FISHMIX EVOLUTION INICIAL 42% EXT 1,4-1,7MM": 4.18
    },
    "Recria 1": {
        "FISHMIX EVOLUTION INICIAL 42% EXT 2-3MM": 3.59, 
        "FISHMIX PLUS INICIAL 33% EXT 2-3MM": 3.40
    },
    "Recria 2": {
        "FISHMIX EVOLUTION 35% EXT 3-4MM": 2.78
    },
    "Engorda 1": {
        "FISHMIX EVOLUTION 30% EXT 4-6MM": 2.64, 
        "FISHMIX EVOLUTION 32% EXT 4-6MM": 2.75, 
        "FISHMIX PLUS 31% EXT 4-6MM": 2.55
    },
    "Engorda 2": {
        "FISHMIX ENGORDA 28% EXT 6-8MM": 2.49, 
        "FISHMIX ENGORDA 28% EXT 8-10MM": 2.49, 
        "FISHMIX EVOLUTION 30% EXT 6-8MM": 2.55, 
        "FISHMIX EVOLUTION 32% EXT 6-8MM": 2.65, 
        "FISHMIX PLUS 31% EXT 6-8MM": 2.45, 
        "FISHMIX PLUS 31% EXT 8-10MM": 2.45, 
        "FISHMIX PLUS ENGORDA 33% EXT 6-8MM": 2.60
    },
    "Engorda 3": {
        "FISHMIX ENGORDA 28% EXT 6-8MM": 2.49, 
        "FISHMIX ENGORDA 28% EXT 8-10MM": 2.49, 
        "FISHMIX EVOLUTION 30% EXT 6-8MM": 2.55, 
        "FISHMIX EVOLUTION 32% EXT 6-8MM": 2.65, 
        "FISHMIX PLUS 31% EXT 6-8MM": 2.45, 
        "FISHMIX PLUS 31% EXT 8-10MM": 2.45, 
        "FISHMIX PLUS ENGORDA 33% EXT 6-8MM": 2.60
    },
}

# --- INTERFACE LATERAL (MANTIDO) ---
st.sidebar.image("https://www.algomix.com.br/images/img_logo.webp", width=200) 
st.sidebar.header("Parâmetros da Simulação")
qtd_peixes = st.sidebar.number_input("Quantidade de Peixes", value=100000, step=1000)
peso_inicial_user = st.sidebar.number_input("Peso Inicial (g) para Simulação", value=0.5)
peso_final_user = st.sidebar.number_input("Peso Final (g) para Simulação", value=1000.0)

st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para Equipe Algomix")

# --- CORPO PRINCIPAL (LOGO, TÍTULO e PREÇOS) ---
st.image("https://www.algomix.com.br/images/img_logo.webp", width=300)
st.title("SIMULADOR FISHMIX ALGOMIX")

st.markdown("Selecione o produto e ajuste o **Preço por KG de Ração** para cada fase:")

col1, col2, col3 = st.columns(3)
precos_kg_map = {}

# FUNÇÃO PARA CRIAR A CAIXA DE SELEÇÃO E O INPUT DE PREÇO
def criar_input_fase(col, fase_nome):
    with col:
        st.subheader(fase_nome)
        opcoes = list(OPCOES_RACAO[fase_nome].keys())
        produto_selecionado = st.selectbox(
            f"Produto em {fase_nome}", 
            opcoes, 
            key=f"select_{fase_nome}"
        )
        preco_sugerido = OPCOES_RACAO[fase_nome][produto_selecionado]
        
        preco_input = st.number_input(
            f"Preço por Kg - {fase_nome}", 
            value=preco_sugerido, 
            format="%.2f",
            key=f"price_{fase_nome}"
        )
        # Associa o preço final do input ao mapeamento global de preços
        precos_kg_map[fase_nome] = preco_input
        st.markdown("---")

# CRIAÇÃO DOS CAMPOS POR COLUNA
criar_input_fase(col1, "Berçário 1")
criar_input_fase(col1, "Berçário 2")

criar_input_fase(col2, "Recria 1")
criar_input_fase(col2, "Recria 2")

criar_input_fase(col3, "Engorda 1")
criar_input_fase(col3, "Engorda 2")
criar_input_fase(col3, "Engorda 3")


# --- CÁLCULOS (MANTIDO) ---
resultados = []
custo_total_acumulado = 0
racao_total_acumulada = 0
KG_SACA = 25.0

for linha in dados_base:
    dentro_do_range = (linha["p_ini"] < peso_final_user) and (linha["p_fim"] > peso_inicial_user)
    
    if dentro_do_range:
        # Lógica de cálculo (Peso Base)
        if linha["tipo_calc"] == "fator":
            peso_base_calculo = linha["p_ini"] + (linha["p_ini"] * linha["fator_ajuste"])
        else:
            peso_base_calculo = (linha["p_ini"] + linha["p_fim"]) / 2
        
        # Cálculo Ração Dia e Semana
        racao_dia = (qtd_peixes * peso_base_calculo * linha["bio"]) / 1000
        racao_semana = racao_dia * 7
        
        # Custos (Usa o preço do mapeamento atualizado pelo input do usuário)
        preco_kg = precos_kg_map[linha["fase"]]
        custo_semana = racao_semana * preco_kg
        
        custo_total_acumulado += custo_semana
        racao_total_acumulada += racao_semana
        
        sacas_necessarias = racao_semana / KG_SACA
        
        # Encontra o produto selecionado para exibir na tabela (NOVO)
        produto_fase = st.session_state[f"select_{linha['fase']}"]
        
        resultados.append({
            "Fase": linha["fase"],
            "Produto": produto_fase, # NOVO: Nome do produto selecionado
            "Semana": f"{linha['semana']}ª",
            "Peso Inicial (g)": linha["p_ini"],
            "Peso Final (g)": linha["p_fim"],
            "Ração/Dia (kg)": round(racao_dia, 1),
            "Ração/Semana (kg)": round(racao_semana, 1),
            "Ração/Semana (sacas de 25kg)": round(sacas_necessarias, 1),
            "Custo/Semana (R$)": round(custo_semana, 2)
        })

# --- EXIBIÇÃO DOS RESULTADOS ---
if len(resultados) > 0:
    st.markdown("---")
    st.subheader("📊 Resultado da Simulação")
    
    # Métricas Principais (MANTIDO)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"<div class='metric-box'><b>Custo Total</b><br>R$ {custo_total_acumulado:,.2f}</div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-box'><b>Total Ração</b><br>{racao_total_acumulada/1000:,.1f} Ton</div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-box'><b>Total Sacas ({int(KG_SACA)}kg)</b><br>{math.ceil(racao_total_acumulada/KG_SACA):,.0f} sc</div>", unsafe_allow_html=True) # Ajustei para arredondar sacas para cima
    
    if qtd_peixes > 0:
        custo_por_peixe = custo_total_acumulado / qtd_peixes
        m4.markdown(f"<div class='metric-box'><b>Custo/Peixe</b><br>R$ {custo_por_peixe:,.2f}</div>", unsafe_allow_html=True)

    # Tabela Detalhada (Otimizada para impressão)
    st.write("")
    st.write("### Detalhamento Semana a Semana")
    df = pd.DataFrame(resultados)
    
    # Otimização da Tabela para Impressão
    st.table(df[['Fase', 'Produto', 'Semana', 'Peso Inicial (g)', 'Peso Final (g)', 'Ração/Semana (kg)', 'Ração/Semana (sacas de 25kg)', 'Custo/Semana (R$)']])
    
# ... (código antes da dica de impressão) ...
    
    st.markdown("---")
    
    # 5. Instruções de Impressão (AGORA MAIS CLARAS)
    st.warning("""
    ⚠️ **Dica de Impressão/PDF:** 1. **NÃO use Ctrl+P!** Clique nos **três pontos (⋮)** no canto superior direito do seu navegador e selecione **Imprimir**.
    2. No menu de impressão, escolha **Salvar como PDF** e defina o **Layout** como **Paisagem**.
    3. Em **Mais definições** (ou Escala), ajuste o valor para **70%** ou **65%** para garantir que todo o conteúdo caiba em uma única página.
    """)
    
else:
# ... (restante do código) ...
    st.warning("Nenhuma semana encontrada para esse intervalo de peso.")
    
st.markdown("---")

# 3. Créditos do Desenvolvedor (MANTIDO)
st.markdown("""
    **Desenvolvido por:** **DEONIR BLOEMER** *Médico Veterinário CRMV PR 11906*
    """)
