import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# CONFIGURACIÓN
# -------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# -------------------------
# CARGAR DATOS
# -------------------------

df = pd.read_csv("Datos_Salida_Extraccion/saber11_limpio.csv")

estrato_col = "fami_estratovivienda"

print(f"dimensiones data frame",{df.shape})

score_options = [
    "punt_global",
    "punt_matematicas",
    "punt_lectura_critica",
    "punt_c_naturales",
    "punt_sociales_ciudadanas",
    "punt_ingles",
]

estratos_orden = sorted(df[estrato_col].dropna().unique())

# -------------------------
# DISEÑO DEL DASHBOARD
# -------------------------

app.layout = html.Div([
    
    html.H2("Dashboard Pruebas Saber 11 - Atlántico"),

    dcc.Tabs(
        id = "tabs",
        children = [

        dcc.Tab(label="Estrato Socioeconómico", value = "tab-estrato", children=[
            
            html.Br(),
            html.H2("Análisis por Nivel Socioeconómico"),

            #SECCIÓN 1 : Brechas por Estrato

            html.Div([
                html.H3("1. Brechas en Resultados", style={"margin": "0"}),
                html.P(
                    "Comparación del desempeño según estrato socioeconómico.",
                    style={"marginTop": "5px"}
                ),
                dcc.Dropdown(
                    id="score-col-estrato",
                    options=[{"label": c, "value": c} for c in score_options],
                    value="punt_global",
                    clearable=False,
                ),
                dcc.RadioItems(
                    id="tipo-grafico-estrato",
                    options=[
                        {"label": "Boxplot", "value": "box"},
                        {"label": "Violin", "value": "violin"},
                    ],
                    value="box",
                    inline=True,
                    style={"marginTop": "15px"}
                ),
                dcc.Loading(
                    id="loading-estrato",
                    type="circle",  # puedes usar "default", "circle", "dot"
                    children=html.Div(id="contenido-estrato")
                )
            ],
            style={
                "backgroundColor": "#F5F7FA",
                "padding": "15px 20px",
                "borderRadius": "8px",
                "borderLeft": "6px solid #6C63FF",
                "marginBottom": "25px"
            }),

            #SECCIÓN 2: Evolución resultados en el tiempo por Estrato
            html.Div([

                html.H3("2. Evolución del Desempeño en el Tiempo", style={"margin": "0"}),

                html.P(
                    "Análisis de la evolución del puntaje global por estrato a lo largo del tiempo.",
                    style={"marginTop": "5px"}
                ),

                html.Br(),

                dcc.Loading(
                    type="circle",
                    children=html.Div(id="contenido-tiempo")
                )

            ],
            style={
                "backgroundColor": "#F5F7FA",
                "padding": "25px",
                "borderRadius": "10px",
                "borderLeft": "6px solid #6C63FF",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
                "marginBottom": "40px"
            })

            

        ]),

        dcc.Tab(label="Jornada Académica", value = "tab-jornada", children=[
            
            html.Br(),
            html.H3("Diferencias Resultados por Jornada"),
            
            html.Div([
            html.H3("3. Diferencias en Resultados por Jornada Académica"),
            html.P("Comparación del desempeño según jornada académica."),
            dcc.Dropdown(
                id="score-col-jornada",
                options=[{"label": c, "value": c} for c in score_options],
                value="punt_global",
                clearable=False,
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="contenido-jornada")
            )
        ],
        style={
            "backgroundColor": "#F5F7FA",
            "padding": "25px",
            "borderRadius": "10px",
            "borderLeft": "6px solid #6C63FF",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
            "marginBottom": "40px"
        })

        ]),

    ])

])

#Sección 1: Brechas por Estrato
@app.callback(
    Output("contenido-estrato", "children"),
    Input("score-col-estrato", "value"),
    Input("tipo-grafico-estrato", "value"),
)
def update_estrato(score_col, tipo_grafico):    

    # KPIs
    # -----------------------------
    # Filtrar grupos correctamente
    bajo = df[df["fami_estratovivienda"].isin([1, 2])].copy()
    alto = df[df["fami_estratovivienda"].isin([5, 6])].copy()

    # Eliminar posibles valores faltantes en el puntaje seleccionado
    bajo = bajo.dropna(subset=[score_col])
    alto = alto.dropna(subset=[score_col])

    # Calcular medias
    bajo_mean = bajo[score_col].mean()
    alto_mean = alto[score_col].mean()

    # Calcular brecha
    brecha_abs = alto_mean - bajo_mean
    brecha_pct = (brecha_abs / bajo_mean) * 100 if bajo_mean != 0 else 0


    kpis = html.Div([
        html.Div([
            html.H6("Media Estrato Bajo (1–2)"),
            html.H4(f"{bajo_mean:.1f} pts")
        ], style={"width": "30%"}),

        html.Div([
            html.H6("Media Estrato Alto (5–6)"),
            html.H4(f"{alto_mean:.1f} pts")
        ], style={"width": "30%"}),

        html.Div([
            html.H6("Brecha"),
            html.H4(f"{brecha_abs:.1f} pts"),
            html.P(f"{brecha_pct:.1f}%")
        ], style={"width": "30%"})
    ],
    style={
        "display": "flex",
        "justifyContent": "space-between",
        "marginBottom": "25px"
    })

    # GRÁFICO DINÁMICO
    # -----------------------------

    # Orden correcto de categorías
    orden_estratos = [
        "Sin Estrato",
        "Estrato 1",
        "Estrato 2",
        "Estrato 3",
        "Estrato 4",
        "Estrato 5",
        "Estrato 6",
    ]


    if tipo_grafico == "box":
        fig = px.box(
            df,
            x="fami_estratovivienda",
            y=score_col,
            category_orders={"fami_estratovivienda": orden_estratos},
            points=False,
            labels={
                "fami_estratovivienda": "Estrato",
                score_col: "Puntaje"
            }
        )

        fig.update_traces(boxmean=True)

    else:
        fig = px.violin(
            df,
            x="fami_estratovivienda",
            y=score_col,
            category_orders={"fami_estratovivienda": orden_estratos},
            points=False,
            labels={
                "fami_estratovivienda": "Estrato",
                score_col: "Puntaje"
            }
        )

    fig.update_layout(
        template="simple_white",
        title=f"{score_col} por Estrato Socioeconómico"
    )

    graph = dcc.Graph(figure=fig)

    # HISTOGRAMA
    # -----------------------------
    colores_estrato = {
    1.0: "#3B5BDB",
    2.0: "#C92A2A",
    3.0: "#2B8A3E",
    4.0: "#5F3DC4",
    5.0: "#D9480F",
    6.0: "#0B7285"
    }

    fig_hist = px.histogram(
        df,
        x=score_col,
        color="fami_estratovivienda",
        nbins=40,
        histnorm="probability density", #Normalizar como densidad, comparar distribuciones con tamaños distintos
        opacity=0.55,
        barmode="overlay",
        color_discrete_map= colores_estrato,
        labels={
            "fami_estratovivienda": "Estrato",
            score_col: "Puntaje"
        },
        title=f"Distribución de {score_col} por Estrato"
    )

    fig_hist.update_layout(
        template="simple_white",
        legend_title="Estrato (clic para ocultar/mostrar)",
        yaxis_title="Probabilidad"
    )

    fig_hist.update_traces(marker_line_width=0)

    graph_hist = dcc.Graph(figure=fig_hist)

    # CONCLUSIÓN
    # -----------------------------

    conclusion = html.Div([
        html.H5("Conclusión"),
        html.P(
            f"Se evidencia una brecha significativa en {score_col}. "
            f"Los estudiantes de estratos altos (5–6) obtienen en promedio "
            f"{brecha_abs:.1f} puntos más que los de estratos bajos (1–2), "
            f"lo que representa una diferencia aproximada del {brecha_pct:.1f}%."
        )
    ], style={"marginTop": "20px"})

    # RETURN FINAL
    # -----------------------------

    return html.Div([
        kpis,
        graph,
        graph_hist,
        conclusion
    ])

#Sección 2: Evolución resultados en el tiempo por Estrato
@app.callback(
    Output("contenido-tiempo", "children"),
    Input("tabs", "value")
)
def update_tiempo(estratos_seleccionados):

    import plotly.express as px

    #Grafica del tiempo
    #-----------------------
    promedios = (
        df.groupby(["periodo", "fami_estratovivienda"])["punt_global"]
        .mean()
        .reset_index()
    )

    #Periodo como categoría (para que no salga “k” y no se pegue)
    promedios["periodo"] = promedios["periodo"].astype(str)

    # Ordenar periodos
    orden_periodos = sorted(promedios["periodo"].unique())
    promedios["periodo"] = pd.Categorical(promedios["periodo"], categories=orden_periodos, ordered=True)

    # 3) Línea (leyenda = “checkboxes”)
    colores_estrato = {
    1.0: "#3B5BDB",
    2.0: "#C92A2A",
    3.0: "#2B8A3E",
    4.0: "#5F3DC4",
    5.0: "#D9480F",
    6.0: "#0B7285"
    }
    fig = px.line(
        promedios.sort_values("periodo"),
        x="periodo",
        y="punt_global",
        color="fami_estratovivienda",
        category_orders={"periodo": orden_periodos},
        color_discrete_map=colores_estrato,
        markers=True,
        labels={
            "periodo": "Periodo",
            "punt_global": "Puntaje Global",
            "fami_estratovivienda": "Estrato"
        },
        title="Evolución del Puntaje Promedio por Estrato"
    )

    fig.update_layout(
        template="simple_white",
        legend_title="Estrato (clic para ocultar/mostrar)",
        legend=dict(orientation="v", x=1.02, y=1),
        xaxis=dict(type="category")  # clave
    )
    fig.update_traces(line=dict(width=3))

    graph_line = dcc.Graph(figure=fig)

    # Heatmap (todos los estratos)
    # -----------------------

    # Crear tabla pivote
    tabla_pivot = (
        df.groupby(["fami_estratovivienda", "periodo"])["punt_global"]
        .mean()
        .reset_index()
        .pivot(index="fami_estratovivienda", columns="periodo", values="punt_global")
    )
    tabla_pivot = tabla_pivot.sort_index(axis=1)

    fig_heat = go.Figure(data=go.Heatmap(
        z=tabla_pivot.values,
        x=tabla_pivot.columns.astype(str),
        y=tabla_pivot.index.astype(str),
        colorscale=[
            [0.0, "#E3F2FD"],   # azul muy claro
            [0.25, "#A2BCEA"],  # azul medio
            [0.5, "#5C6BC0"],   # azul-violeta
            [0.75, "#7E57C2"],  # morado medio
            [1.0, "#4527A0"]    # morado oscuro
        ],
        colorbar=dict(title="Puntaje"),
        text=tabla_pivot.round(1).values,
        texttemplate="%{text}",
        textfont={"size": 10},
    ))

    fig_heat.update_layout(
        title="Mapa de Calor - Puntaje Promedio Global por Estrato y Periodo",
        xaxis_title="Periodo",
        yaxis_title="Estrato",
        template="simple_white"
    )
    graph_heat = dcc.Graph(figure=fig_heat)

    # Métrica: Variación total 2014–2024
    # -------------------------------------

    primer = promedios.sort_values("periodo").iloc[0]["punt_global"]
    ultimo = promedios.sort_values("periodo").iloc[-1]["punt_global"]

    variacion_abs = ultimo - primer
    variacion_pct = (variacion_abs / primer) * 100 if primer != 0 else 0

    metrica = html.Table([
        html.Thead(
            html.Tr([
                html.Th("Indicador", style={"backgroundColor": "#0F0B5CF0", "color": "white", "padding": "10px"}),
                html.Th("Valor", style={"backgroundColor": "#0F0B5CF0", "color": "white", "padding": "10px"})
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Td("Variación Absoluta 2014–2024", style={"padding": "10px"}),
                html.Td(f"{variacion_abs:.1f} pts", style={"padding": "10px"})
            ]),
            html.Tr([
                html.Td("Variación Porcentual 2014–2024", style={"padding": "10px"}),
                html.Td(f"{variacion_pct:.1f}%", style={"padding": "10px"})
            ])
        ])
    ],
    style={
        "width": "60%",
        "margin": "0 auto",
        "marginBottom": "25px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"
    })

    #Conclusión
    #-----------------------------------

    conclusion = html.Div([
    html.H5("Conclusión"),
    html.P(
        "Aunque el puntaje promedio presenta fluctuaciones a lo largo del tiempo, "
        "los estratos altos (4–6) mantienen consistentemente mejores resultados que "
        "los estratos bajos (1–2). Las caídas observadas alrededor de 2018 y 2020 "
        "afectan a todos los grupos, pero no modifican de manera sustancial la "
        "brecha estructural entre ellos."
    ) ], style={"marginTop": "25px"})


    # Retorno final

    return html.Div([
        metrica,
        graph_line,
        html.Br(),
        graph_heat, 
        html.Br(),
        conclusion
    ])

#sección 3: RESULTADOS POR JORNADA
@app.callback(
    Output("contenido-jornada", "children"),
    Input("score-col-jornada", "value")
)
def update_jornada(score_col):

    orden_jornada = [
    "COMPLETA",
    "UNICA",
    "MAÑANA",
    "TARDE",
    "SABATINA",
    "NOCHE"
    ]

    # COLORES FIJOS (mismos para todos los gráficos)
    colores_jornada = {
        "COMPLETA": "#3B5BDB",  # azul
        "UNICA": "#C92A2A",     # rojo
        "MAÑANA": "#2B8A3E",    # verde
        "TARDE": "#5F3DC4",     # morado
        "SABATINA": "#D9480F",  # naranja
        "NOCHE": "#0B7285"      # azul claro
    }

    # -----------------------------
    # KPIs
    # -----------------------------
    resumen = (
        df.groupby("cole_jornada")[score_col]
        .agg(["count","mean","median","std"])
        .reset_index()
    )

    max_mean = resumen["mean"].max()
    min_mean = resumen["mean"].min()

    jornada_max = resumen.loc[resumen["mean"].idxmax(), "cole_jornada"]
    jornada_min = resumen.loc[resumen["mean"].idxmin(), "cole_jornada"]

    brecha_abs = max_mean - min_mean
    brecha_pct = (brecha_abs / min_mean) * 100 if min_mean != 0 else 0

    kpis = html.Div([
        html.Div([
            html.H6("Mayor Promedio"),
            html.H4(f"{jornada_max}"),
            html.P(f"{max_mean:.1f} pts")
        ], style={"width":"30%"}),

        html.Div([
            html.H6("Menor Promedio"),
            html.H4(f"{jornada_min}"),
            html.P(f"{min_mean:.1f} pts")
        ], style={"width":"30%"}),

        html.Div([
            html.H6("Brecha"),
            html.H4(f"{brecha_abs:.1f} pts"),
            html.P(f"{brecha_pct:.1f}%")
        ], style={"width":"30%"})
    ],
    style={
        "display":"flex",
        "justifyContent":"space-between",
        "marginBottom":"25px"
    })

    # -----------------------------
    # BOX PLOT
    # -----------------------------
    fig_box = px.box(
        df,
        x="cole_jornada",
        y=score_col,
        category_orders={"cole_jornada (click para ocultar/mostrar)": orden_jornada},
        color="cole_jornada",
        color_discrete_map=colores_jornada,
        template="simple_white",
        title=f"{score_col} por Jornada Académica"
    )
    fig_box.update_traces(boxmean=True)


    graph_box = dcc.Graph(figure=fig_box)

    # -----------------------------
    # GRÁFICO DE BARRAS (medias)
    # -----------------------------
    resumen = df.groupby("cole_jornada")["punt_global"].mean().reset_index()
    resumen["cole_jornada"] = pd.Categorical(
    resumen["cole_jornada"],
    categories=orden_jornada,
    ordered=True
    )

    resumen = resumen.sort_values("cole_jornada")

    fig_bar = px.bar(
        resumen,
        x="cole_jornada",
        y="punt_global",
        category_orders={"cole_jornada (click para ocultar/mostrar)": orden_jornada},
        color="cole_jornada",
        color_discrete_map=colores_jornada,
        template="simple_white",
        title="Promedio por Jornada"
    )
    
    graph_bar = dcc.Graph(figure=fig_bar)


    # -----------------------------
    # CONCLUSIÓN
    # -----------------------------
    conclusion = html.Div([
        html.H5("Conclusión"),
        html.P(
            "Se evidencian diferencias significativas en el desempeño según la jornada académica. "
            "Las jornadas con mayor promedio superan ampliamente a las de menor desempeño, "
            "lo que sugiere posibles diferencias estructurales asociadas al contexto educativo."
        )
    ], style={"marginTop":"20px"})

    return html.Div([
        kpis,
        graph_box,
        html.Br(),
        graph_bar,
        html.Br(),
        conclusion
    ])

if __name__ == "__main__":
    app.run(debug=True, port=8051)