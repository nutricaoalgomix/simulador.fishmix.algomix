# --- CÁLCULOS (CORRIGIDO: Nomes das colunas no Dicionário) ---
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
        
        # Encontra o produto selecionado para exibir na tabela
        produto_fase = st.session_state[f"select_{linha['fase']}"]
        
        resultados.append({
            "Fase": linha["fase"],
            "Produto": produto_fase,
            "Semana": f"{linha['semana']}ª",
            "Peso Inicial (g)": linha["p_ini"],
            "Peso Final (g)": linha["p_fim"],
            # NOVOS NOMES SOLICITADOS (As chaves do dicionário)
            "Ração/Semana (kg)": round(racao_semana, 1),
            "Ração/Semana (sacas de 25kg)": round(sacas_necessarias, 1),
            "Custo/Semana (R$)": round(custo_semana, 2)
        })

# --- EXIBIÇÃO DOS RESULTADOS ---
if len(resultados) > 0:
    st.markdown("---")
    st.subheader("📊 Resultado da Simulação")
    # ... (Métricas Principais continuam aqui) ...

    # Tabela Detalhada (LINHA CORRIGIDA: As chaves da lista devem ser iguais às do dicionário 'resultados')
    st.write("### Detalhamento Semana a Semana")
    df = pd.DataFrame(resultados)
    
    # Esta linha foi corrigida para usar as novas chaves:
    st.table(df[['Fase', 'Produto', 'Semana', 'Peso Inicial (g)', 'Peso Final (g)', 'Ração/Semana (kg)', 'Ração/Semana (sacas de 25kg)', 'Custo/Semana (R$)']])
    
    st.markdown("---")
    
    # ... (Instruções de Impressão e Créditos continuam aqui) ...
