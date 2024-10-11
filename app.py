import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

                           
# Layout
st.set_page_config(page_title="Obras", layout='wide')
st.markdown("""<h1 style="text-align: center;">DASHBOARD OBRAS - MJ/RO</h1>""",
    unsafe_allow_html=True
)
st.divider()

# Carregar datasets
df_database = pd.read_excel("database.xlsx", sheet_name="database")
df_pagamentos = pd.read_excel("database.xlsx", sheet_name="pagamentos")
df_custom2 = pd.read_excel("database.xlsx", sheet_name="custo_m2")

# Sidebar
obras = df_database['OBRA'].value_counts().index
obras.insert(0, 'Todas')
selectbox_obra = st.sidebar.selectbox('Escolha uma obra:',
    ['Todas'] + df_database['OBRA'].value_counts().index.to_list()
)


# Lógica para mostrar os dados
if selectbox_obra == 'Todas':
    df_selected = df_database
    df_pagamentos = df_pagamentos
else:
    # Filtrando os dados para a obra selecionada
    df_selected = df_database[df_database['OBRA'] == selectbox_obra]
    df_pagamentos = df_pagamentos[df_pagamentos['OBRA'] == selectbox_obra]

# Métricas
valor_orcamento = (df_selected['VALOR ESTIMADO'].sum())
valor_contratado = (df_selected['VALOR CONTRATADO'].sum())
qtd_obras = df_selected['OBRA'].nunique()

c1, c2, c3 = st.columns(3)
style_metric_cards(background_color= 'rainbow')

c1.metric("Total Planejado:", valor_orcamento)
c2.metric("Total Contratado:", valor_contratado)
c3.metric("Quantidade de Obras:", qtd_obras)

# ORÇAMENTOS X CONTRATOS
# col1, col2 = st.columns(2)
# estimado_contratado = df_selected.groupby('OBRA')[['VALOR ESTIMADO', 'VALOR CONTRATADO']].sum().reset_index()
# estimado_contratado = estimado_contratado.melt(id_vars='OBRA', 
#                                                 value_vars=['VALOR ESTIMADO', 'VALOR CONTRATADO'], 
#                                                 var_name='Tipo', 
#                                                 value_name='Valor')
# fig1 = px.bar(estimado_contratado, 
#               x='OBRA', 
#               y='Valor', 
#               color='Tipo', 
#               barmode='group',
#               color_discrete_map={
#                   'VALOR ESTIMADO': 'blue',  # Cor azul para VALOR ESTIMADO
#                   'VALOR CONTRATADO': 'green'  # Cor verde para VALOR CONTRATADO
#               },
#               title='Comparativo de Valores Estimado e Contratado por Obra')
# fig1.update_traces(texttemplate='R$ %{y:,.2f}', textposition='outside')
# for trace in fig1.data:
#     trace.text = [f"R$ {str(v).replace('.', ',').replace(',', '.').replace('.', ',')}" for v in trace.y]
# col1.plotly_chart(fig1)



# Total por medição da obra
total_medicao = df_pagamentos.groupby('MEDIÇÃO')[['PREVISTO', 'REALIZADO']].sum().reset_index()
total_medicao = total_medicao.sort_values(by='MEDIÇÃO', ascending=True)
# Criando o gráfico de área
fig2 = px.area(total_medicao,
                x='MEDIÇÃO',
                y=["PREVISTO", "REALIZADO"],
                title='Total por Medição',)

# Formatação dos rótulos em milhares
fig2.update_yaxes(tickprefix="", ticksuffix="k", tickmode='array',
                  tickvals=[0, 200000, 400000, 600000, 800000],
                  ticktext=["0", "200k", "400k", "600k", "800k"])

# Atualizando os rótulos de texto para aparecerem em milhares
for trace in fig2.data:
    # Atualiza os valores de texto para a forma '350k'
    trace.text = [f"{int(value // 1000)}k" for value in trace.y]
    trace.textposition = 'top center'  # Define a posição do texto

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig2)




# TOTAL POR ETAPA

total_etapa = df_selected.groupby('ETAPA')['VALOR CONTRATADO'].sum().reset_index()
total_etapa = total_etapa.sort_values(by='VALOR CONTRATADO', ascending=True)
fig3 = px.bar(total_etapa, x='VALOR CONTRATADO', y='ETAPA', text_auto=True, height=1000, title='Total por Etapa')
st.plotly_chart(fig3)


df_pagamentos

# Formulário para preenchimento
with st.form(key='formulario_registro'):
    obra = st.selectbox('OBRA:', df_pagamentos['OBRA'].value_counts().index)
    med = st.selectbox('MED:', df_pagamentos['MEDIÇÃO'].value_counts().index)
    valor = st.number_input('VALOR:', min_value=0.0, step=0.01, format="%.2f")

    # Botão de submissão
    submit_button = st.form_submit_button(label='Enviar')

# Exibir os dados preenchidos após o envio
if submit_button:
    st.write("### Dados preenchidos:")
    st.write(f"**OBRA:** {obra}")
    st.write(f"**MED:** {med}")
    st.write(f"**REALIZADO:** R$ {valor:.2f}")


df_custom2
