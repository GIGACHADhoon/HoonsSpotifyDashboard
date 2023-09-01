from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from spotifyTools import spotifyTools
import plotly.express as px

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
spTools = spotifyTools()
Rankings = spTools.getRankings()
Snippets = spTools.getSnippets()
Images = spTools.getImages()

style_data_conditional = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgba(150, 180, 225, 0.2)",
        "border": "1px solid blue",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid blue",
    },
]


app.layout = html.Div([
    html.H1("Hoon's Spotify Dashboard", style={'textAlign': 'center'}),
    html.Div([
            dash_table.DataTable(
                         css=[{"selector": ".show-hide", "rule": "display: none"}],
                        style_data_conditional=style_data_conditional,
                        hidden_columns = ['popularity','id'],
                        id='Rankings',
                        columns=[{"name": i, "id": i} 
                                for i in Rankings.columns],
                        data=Rankings.to_dict('records'),
                        style_cell=dict(textAlign='left'),
                        style_header=dict(backgroundColor="paleturquoise"),
                        page_size=5,
                        sort_action="native",
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'backgroundColor':'lavender'},),
            dbc.Row([
                dbc.Col(
                    html.Div(children = [
                        html.Div(children = [
                            html.H5('Select a song in the table and listen to a Snippet!'),
                            html.P(id = 'songFound'),
                            html.Audio(controls=True, style={'align': 'center'}, id ='snippetLink')
                        ], style={"border":"1px black solid"}),
                        html.Div(children = [
                        html.H5('Below is a Popularity Score Distribution Histogram'),
                        html.P('By clicking on any of the Songs in the Table, a vertical line will appear indicating the popularity of that song on the Spotify Platform'),
                        dcc.Graph(
                            id = 'popularityHist',style={'display': 'inline-block'}
                        )
                        ], style={"border":"1px black solid",'height':'25%'})
                    ],style={"text-align": "center",'margin-left':'15px'},),width = 7),
                dbc.Col(
                    html.Div(children = [
                        html.P(id = 'albumFound'),
                        html.Img(alt= 'Album Cover will be displayed here.',id='albumCover',style={'width':'85%','height':'85%'})
                    ], style={"border":"1px black solid",'margin-top':'5%'}),
                    width=5,style={'text-align': 'center','display':'flex','flex-direction':'column','align-items': 'center'}
                )
            ])
        ])
])

@callback(  
Output('Rankings', 'style_data_conditional'),
Input('Rankings', 'active_cell'))
def update_selected_row_color(active):
    style = style_data_conditional.copy()
    if active:
        style.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            },
        )
    return style

@callback(
Output('snippetLink', 'src'),
Input('Rankings', 'active_cell'))
def update_snippet(active):
    if active:
        return Snippets[Snippets['id'] == active['row_id']]['Snippets'].values[0]

@callback(
Output('albumCover', 'src'),
Input('Rankings', 'active_cell'))
def update_image(active):
    if active:
        return Images[Images['id'] == active['row_id']]['imgURL'].values[0]

@callback(
Output('popularityHist', 'figure'),
Input('Rankings', 'active_cell'))
def update_hist(active):
    fig = px.histogram(Rankings, x="popularity", nbins=20,opacity=0.2)
    if active:
        search = Rankings[Rankings['id']==active['row_id']]['popularity'].values[0]
        fig.add_vline(x=search)
    fig.update_layout(bargap=0.2)
    return fig

@callback(
Output('songFound', 'children'),
Input('Rankings', 'active_cell'))
def update_snippet(active):
    #if active and Snippets[Snippets['id'] == active['row_id']]['Snippets'].values[0] != 'None':
    if active and isinstance(Snippets[Snippets['id'] == active['row_id']]['Snippets'].values[0], str):
        return 'Please Turn the volume down close to MINIMUM before clicking play 😉'
    else:
        return 'There is no Snippet Available 😔'

@callback(
Output('albumFound', 'children'),
Input('Rankings', 'active_cell'))
def update_snippet(active):
    if active:
        return 'The Album Cover of the selected Song:'
    else:
        return 'There is no Album Cover 😔'

if __name__=="__main__":
    app.run()