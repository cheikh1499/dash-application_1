
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from dash import Dash
from dash import dash_table
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#manipulation des données
#mettre une colonne raport entre nombre de mort et nombre de cas
# data recuperation  et traitement----------------------------------
data = pd.read_csv("data/reported_numbers.csv")
#Nous avons epurer les donnes en supprimer les ligne de "No.of cases" et de "No.of death" n'ayant pas de valeur
df= data.dropna()
cas=df["No. of cases"]
nbre_death=df["No. of deaths"]
#nous avons creer un autre dataframe afin de supprimer les valeurs dont le nombre de desces est superieur au nbre de cas
df2=df.drop(df[cas<nbre_death].index)
#1-Ajouter une nouvelle colonne calculant le rapport entre les nombre de morts sur le
#nombre de cas
#notre colonne s'appelle proportion
proportion= df2["No. of deaths"]/df["No. of cases"]
#metons proportion dans notre dataframe
df2.insert(5,"proportion",proportion,True)
#remplacons nos "NaN" par des 0
df2["proportion"]=df2["proportion"].fillna(0)
whoregion=df2["WHO Region"]
#total cas
data_cas=data['No. of cases'].sum()
df_cas= pd.DataFrame({'somme': [data_cas]})

#total nombre de mort
data_mort=data['No. of deaths'].sum()
df_mort= pd.DataFrame({'somme': [data_mort]})
#top 10 pays avec le plus de cas de malaria
df3=data[["Country","No. of cases","No. of deaths"]].groupby("Country").sum().reset_index()
top10PlusCas=df3.sort_values(by=["No. of cases"],ascending=False).head(10)
figPCas=px.bar(top10PlusCas,x="No. of cases",y="Country",orientation='h')

#top 10 pays avec le plus de mort de malaria
top10PlusMort=df3.sort_values(by=["No. of deaths"],ascending=False).head(10)
figPMort=px.bar(top10PlusMort,x="No. of deaths",y="Country",orientation='h')

#TOP 10 PAYS AVEC MOINS DE CAS
top10MoinsCas=df3.sort_values(by=["No. of cases"]).head(10)
figMCas=px.bar(top10PlusCas,x="No. of cases",y="Country",orientation='h')

#top 10 pays avec moins de mort
top10MoinsMort=df3.sort_values(by=["No. of deaths"]).head(10)
figMMort=px.bar(top10PlusMort,x="No. of deaths",y="Country",orientation='h')

#nombre de cas par region en diagramme en camenbert
nbreCasParRegion=data[["WHO Region","No. of cases"]].groupby("WHO Region").sum().reset_index()
figRMort=px.pie(nbreCasParRegion,values="No. of cases",names="WHO Region")

#nombre de mort  par region en diagramme en camenbert
nbreMortParRegion=data[["WHO Region","No. of deaths"]].groupby("WHO Region").sum().reset_index()
figRCas=px.pie(nbreMortParRegion,values="No. of deaths",names="WHO Region")
#courbe 
courbe=data[["Year","No. of cases","No. of deaths"]].groupby("Year").sum()
rapport=courbe["No. of deaths"]/courbe["No. of cases"]
courbe.insert(2,"rapport",rapport,True)
figCourbe=px.line(courbe)

#debut de notre application
app= Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.layout= html.Div([
    #premier ligne contenant le titre
    dbc.Row([
        html.H1("Dashbord  Examen de visualisation")
    ],className="titre"),
    #deuxieme ligne contenant les filtrage
    dbc.Row([
        dbc.Col([
           region_:= dcc.Dropdown( 
                className= "filtred",
                id="region",
                placeholder="Region",
                options=[{"label":x,"value":x} for x in data["WHO Region"].unique()]
            )
            ]),
        dbc.Col([
            pays_:=dcc.Dropdown( 
                className= "filtred",
                id="pays",
                placeholder="pays",
                options=[{"label":x,"value":x} for x in data["Country"].unique()]
            )

            ]),
        dbc.Col([
           annee_:= dcc.Dropdown( 
                className= "filtred",
                id="annee",
                placeholder="Annee",
                options=[{"label":x,"value":x} for x in data["Year"].unique()]
            )
            ])

    ],id="filtrage"),
    dbc.Row([
        dbc.Col([
            html.H3(children="table des donnees avec rapport",
            style={"text-align":"center"}),
            table_data:=dash_table.DataTable(
                id='table-data',
                 style_data={
                     'whiteSpace': 'normal',
                     'height': 'auto',
                },
                data=df2.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df2.columns],
                page_size=10,
            )
            
        ],id="table")
        
    ],className="titre3"),
    dbc.Row([
        dbc.Col([
            html.H3(children="Nombre total de cas",
            style={"text-align":"center"}),
            table_cas:=dash_table.DataTable(
                id='table-data1',
                 style_data={
                     'whiteSpace': 'normal',
                     'height': 'auto',
                },
                data=df_cas.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df_cas.columns],
                page_size=10,
            )
        ]),
        dbc.Col([
            html.H3(children="Nombre de mort",
            style={"text-align":"center"}),
            table_mort:=dash_table.DataTable(
                id='table-data2',
                 style_data={
                     'whiteSpace': 'normal',
                     'height': 'auto',
                },
                data=df_mort.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df_mort.columns],
                page_size=10,
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(children="Top 10 pays avec le plus de cas",
            style={"text-align":"center"}),
            graphe_Pcas:=dcc.Graph(figure=figPCas)
        ]),
        dbc.Col([
            html.H3(children="Top 10 pays avec le plus de cas",
            style={"text-align":"center"}),
            graphe_Pmort:=dcc.Graph(figure=figPMort)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(children="Top 10 pays avec moins de cas",
            style={"text-align":"center"}),
            graphe_Mcas:=dcc.Graph(figure=figMCas)
        ]),
        dbc.Col([
            html.H3(children="Top 10 pays avec moins de mort",
            style={"text-align":"center"}),
            graphe_Mmort:=dcc.Graph(figure=figMMort)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(children=" nombre de cas par region ",
            style={"text-align":"center"}),
            graphe_Rcas:=dcc.Graph(figure=figRCas)
        ]),
        dbc.Col([
            html.H3(children="nombre de mort par region ",
            style={"text-align":"center"}),
            graphe_Rmort:=dcc.Graph(figure=figRMort)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(children="courbe d'evolution ",
            style={"text-align":"center"}),
            graphe_courbe:=dcc.Graph(figure=figCourbe)
        ]),
]),
])

@app.callback(
    Output(table_data,"data"),
    Output(table_cas,"data"),
    Output(table_mort,"data"),
    Output(graphe_Pcas,"figure"),
    Output(graphe_Pmort,"figure"),
    Output(graphe_Mcas,"figure"),
    Output(graphe_Mmort,"figure"),
    Output(graphe_Rcas,"figure"),
    Output(graphe_Rmort,"figure"),
    Output(graphe_courbe,"figure"),

    Input(region_,"value"),
    Input(pays_,"value"),
    Input(annee_,"value")
)

def update_table(region_,pays_,annee_):
    region=list(set(df2["WHO Region"].values))
    pays=list(set(df2["Country"].values))
    annee=list(set(df2["Year"].values))
    if region_ is not None:
        region=[region_]
    if pays_ is not None:
        pays=[pays_]
    if annee_ is not None:
        annee=[annee_]
    #propotion
    df_table=df2[(df2["Year"].isin(annee)) & (df2["Country"].isin(pays)) & (df2["WHO Region"].isin(region))]
    #total cas
    data_cas=data.loc[(data["Year"].isin(annee)) & (data["Country"].isin(pays)) & (data["WHO Region"].isin(region)),"No. of cases"].sum()
    df_cas = pd.DataFrame({'somme': [data_cas]})
    #total mort
    data_mort=data.loc[(data["Year"].isin(annee)) & (data["Country"].isin(pays)) & (data["WHO Region"].isin(region)),"No. of deaths"].sum()
    df_mort = pd.DataFrame({'somme': [data_mort]})
    #top10plusCas
    topPaysCas= data[(data["Year"].isin(annee))  & (df2["WHO Region"].isin(region))].groupby("Country")["No. of cases"].sum().reset_index()
    top10PlusCas=topPaysCas.sort_values(by=["No. of cases"],ascending=False).head(10)
    figPlusCas=px.bar(top10PlusCas,x="No. of cases",y="Country",orientation='h')
    #top10plusMort
    topPaysMort= data[(data["Year"].isin(annee))  & (df2["WHO Region"].isin(region))].groupby("Country")["No. of deaths"].sum().reset_index()
    top10PlusMort=topPaysMort.sort_values(by=["No. of deaths"],ascending=False).head(10)
    figPlusMort=px.bar(top10PlusMort,x="No. of deaths",y="Country",orientation='h')
    #top10MoinsCas
    topPaysCas= data[(data["Year"].isin(annee))  & (df2["WHO Region"].isin(region))].groupby("Country")["No. of cases"].sum().reset_index()
    top10MoinsCas=topPaysCas.sort_values(by=["No. of cases"]).head(10)
    figMoinsCas=px.bar(top10MoinsCas,x="No. of cases",y="Country",orientation='h')
    #top10MoinsMort
    topPaysMort= data[(data["Year"].isin(annee))  & (df2["WHO Region"].isin(region))].groupby("Country")["No. of deaths"].sum().reset_index()
    top10MoinsMort=topPaysMort.sort_values(by=["No. of deaths"]).head(10)
    figMoinsMort=px.bar(top10MoinsMort,x="No. of deaths",y="Country",orientation='h')
    #nombre de cas par region en diagramme en camenbert
    nbreCasParRegion=data[(data["Year"].isin(annee)) & (data["Country"].isin(pays))].groupby("WHO Region")["No. of cases"].sum().reset_index()
    figRMort=px.pie(nbreCasParRegion,values="No. of cases",names="WHO Region")
    #nombre de mort  par region en diagramme en camenbert
    nbreMortParRegion=data[(data["Year"].isin(annee)) & (data["Country"].isin(pays))].groupby("WHO Region")["No. of deaths"].sum().reset_index()
    figRCas=px.pie(nbreMortParRegion,values="No. of deaths",names="WHO Region")
    #courbe nombre cas, nombre de mort , et le rapport en fonction de l'annee
    courbe=data[(data["Country"].isin(pays)) & (data["WHO Region"].isin(region))].groupby("Year")[["No. of cases","No. of deaths",]].sum()
    rapport=courbe["No. of deaths"]/courbe["No. of cases"]
    courbe.insert(2,"rapport",rapport,True)
    print(courbe)
    figCourbe=px.line(courbe)

    return df_table.to_dict('records'),df_cas.to_dict('records'),df_mort.to_dict('records'),figPlusCas,figPlusMort,figMoinsCas,figMoinsMort,figRMort,figRCas,figCourbe



if __name__ == '__main__':
    app.run_server(debug=True)
