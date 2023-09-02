from dash import Dash, dcc, html, Input, Output, callback, dash_table,callback_context
import dash_bootstrap_components as dbc
from spotifyTools import spotifyTools
import plotly.express as px

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
spTools = spotifyTools()
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

# Add a CSS class for the table rows
table_row_style = {
    'height': '50px',  # Adjust the height as needed
}

# Add a CSS class for the table cells
table_cell_style = {
    'whiteSpace': 'normal',
    'height': 'auto',
    'backgroundColor': 'lavender',
}

# Use the Spotify green color (#1DB954) as the primary color
spotify_green = "#1DB954"

# Create a custom style for the buttons
button_style = {
    "background-color": spotify_green,
    "color": "white",
    "border": "none",
    "border-radius": "5px",
    "padding": "10px 20px",
    "font-size": "16px",
    "cursor": "pointer",
}

app.layout = html.Div([
    html.H1("Hoon's Spotify Dashboard", style={'textAlign': 'center', 'color': spotify_green}),
    html.Div(children=[   
        dbc.Row([
            html.H6('Please Select One of the Contexts Below', style={'text-align': 'center', 'color': spotify_green}),
        ], align="center"),
        dbc.Row([
            dbc.Col(html.Button('Listening Habits Over 2 Years', id="btn-1", className="btn", style=button_style), width=4, style={'textAlign': 'center'}),
            dbc.Col(html.Button('Listening Habits Over 6 months', id="btn-2", className="btn", style=button_style), width=4, style={'textAlign': 'center'}),
            dbc.Col(html.Button('Listening Habits Over the last month', id="btn-3", className="btn", style=button_style), width=4, style={'textAlign': 'center'}),
        ])
    ], style={'margin-top': '10px', 'margin-bottom': '10px', "border": f"1px solid {spotify_green}"}),
    html.Div([
        dash_table.DataTable(
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        style_data_conditional=style_data_conditional,
        hidden_columns=['popularity', 'id'],
        id='Rankings',
        style_cell=table_cell_style,  # Apply the cell style
        style_header=dict(backgroundColor=spotify_green, color="white"),
        page_size=5,
        sort_action="native",
        style_data=table_row_style,  # Apply the row style
    ),
        dbc.Row([
            dbc.Col(
                html.Div(children=[
                    html.Div(children=[
                        html.H5('Select a song in the table and listen to a Snippet!', style={'color': spotify_green}),
                        html.P(id='songFound'),
                        html.Audio(controls=True, style={'width': '100%'}, id='snippetLink')  # Adjust audio width
                    ], style={"border": f"1px solid {spotify_green}"}),
                    html.Div(children=[
                        html.H5('Below is a Spotify Popularity Index Distribution Histogram', style={'color': spotify_green}),
                        html.P('The Histogram shows the distribution of the Spotify Popularity Index (a score out of 100) of the songs I listen to. \
                            By clicking on any of the Songs in the Table, a vertical line will appear indicating the "spotify popularity index" of that Song.'),
                        dcc.Graph(
                            id='popularityHist',
                            style={'display': 'inline-block', 'width': '100%'},  # Adjust graph width
                        )
                    ], style={"border": f"1px solid {spotify_green}"})
                ]), width=7, style={'textAlign': 'center'}),  # Use width=12 for full width on mobile
            dbc.Col(
                html.Div(children=[
                    html.P(id='albumFound'),
                    html.Img(alt='Album Cover will be displayed here.', id='albumCover', style={'width': '85%', 'height': '85%'})
                ], style={"border": f"1px solid {spotify_green}"}),
                width=5, style={'text-align': 'center'}
            )
        ], align="center")
    ])
])

@callback(  
    Output('Rankings', 'style_data_conditional'),
    Input('Rankings', 'active_cell'))
def update_selected_row_color(active):
    style = style_data_conditional.copy()
    if active:
        # Update only the selected cell's background color
        style.append(
            {
                "if": {"filter_query": "{{id}} = {}".format(active["row_id"])},
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
    fig = px.histogram(spTools.getChosen(), x="popularity", nbins=20,opacity=0.2,labels={
                     "popularity": "Spotify Popularity Index"})
    if active:
        search = spTools.getChosen()[spTools.getChosen()['id']==active['row_id']]['popularity'].values[0]
        fig.add_vline(x=search)
    fig.update_layout(bargap=0.2,yaxis={'visible': False, 'showticklabels': False})
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
def update_album(active):
    if active:
        return 'The Album Cover of the selected Song is shown below'
    else:
        return 'There is no Album Cover 😔'


@app.callback(
    [Output(f"btn-{i}", "className") for i in range(1, 4)],
    [Input(f"btn-{i}", "n_clicks") for i in range(1, 4)],
)
def set_active(*args):
    ctx = callback_context

    if not ctx.triggered or not any(args):
        return ["btn active","btn","btn"]

    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return [
        "btn active" if button_id == f"btn-{i}" else "btn" for i in range(1, 4)
    ]

@app.callback(
    Output('Rankings','data'),
    [Input(f"btn-{i}", "n_clicks") for i in range(1, 4)],
)
def update_figure(*args):
    ctx = callback_context

    if not ctx.triggered or not any(args):
        return spTools.getltRankings().to_dict('records')

    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == 'btn-1':
        spTools.updateChosen('ltr')
        return spTools.getltRankings().to_dict('records')
    elif button_id == 'btn-2':
        spTools.updateChosen('mtr')
        return spTools.getmtRankings().to_dict('records')
    elif button_id == 'btn-3':
        spTools.updateChosen('str')
        return spTools.getstRankings().to_dict('records')

@app.callback(
    Output('Rankings','column'),
    [Input(f"btn-{i}", "n_clicks") for i in range(1, 4)],
)
def update_figure(*args):
    ctx = callback_context

    if not ctx.triggered or not any(args):
        return [{"name": i, "id": i} for i in spTools.getltRankings().columns]

    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == 'btn-1':
        return [{"name": i, "id": i} for i in spTools.getltRankings().columns]
    elif button_id == 'btn-2':
        return [{"name": i, "id": i} for i in spTools.getmtRankings().columns]
    elif button_id == 'btn-3':
        return [{"name": i, "id": i} for i in spTools.getstRankings().columns]


if __name__=="__main__":
    app.run()