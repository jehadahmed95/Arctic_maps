import numpy as np
from dash import Dash, Output,Input, html, dcc
import plotly.express as px
import glob


l = glob.glob("./ice_data/*.npy")
ice_area = np.load("./ice_data_area.npy")


ice_area100 = np.zeros(16)
ice_area50 = np.zeros(16)
ice_mean = np.zeros(16)
years = np.zeros(16)
j = 0
sat_maps = []

for file in l:
    img = np.load(file)
    sat_maps.append(np.array(img))
    img[np.isnan(img)] = 0
    ice_area100[j] = np.sum(ice_area[img == 100])
    ice_area50[j] = np.sum(ice_area[img > 50])
    ice_mean[j] = np.mean(img)
    years[j] = int(file[11:15])
    j = j+1

years= years.astype(int)


app = Dash(__name__, title="Arctic maps analysis")
server = app.server
# , external_stylesheets=[dbc.themes.CYBORG]
app.layout = html.Div( children=[html.H1("Analysis of Arctic Maps."),
                                 html.H3(["This is a presentation of satellite images of the Arctic Ocean from the year 2003 to 2019."
                                        "This a small subset of the complete satellite data set, with only one map, on the 15th of August, is presented for each year." 
                                        "All the data were downloaded from ", html.A("here. ", href="https://seaice.uni-bremen.de/data-archive/"),
                                        " The data used in this problem set was collected by two different satellite missions. Involved are the "
                                        "AMSR-E instrument on the Aqua satellite (data from 2002 to 2011) and the AMSR2 instrument on the GCOM-W satellite (data from 2013 to 2019)."
                                        " The data consist of maps of the concentration of ice in the Arctic collected between 2002 and 2019 with the exception of 2012.\n"


                                        ]),
                                 html.H3("Use the slider to select a year and view the ice map for August 15th of that year."
                                        " There are two figures available: one displays the area where ice concentration is 100%, and the other shows areas where ice concentration is 50% or greater."
                                         " A linear regression model is fit to each figure, the lines that represent the models are shown in grey. "
                                         " Hover around the grey lines to see more information about the linear fit."


                                          ),
                                          # " In addition to the area where ice concentration is 100% and smaller or equal to 50% as a function of the year. ",
                                 # dcc.Dropdown(options = [{"label":year, "value":year} for year in years]),
                                 html.Div([dcc.Slider(
                                            min=0,
                                            max=len(years)-1,
                                            # min= years[0],
                                            # max= years[-1],
                                            value=0,
                                            marks={i: str(years[i]) for i in range(len(years))},
                                            step=1,
                                            id="year_slider"
                                            )], style={"width":"60%"})
                                 ,
                                 dcc.Graph(id="maps_fig", style = {'width': '75vh', 'height': '75vh',"position":"abolute", "top":"10vh"}),
                                 html.Div([html.H2(id = "total_area")]),
                                 # dcc.Graph(id = "total_area_fig")
                                 dcc.Graph(id = "ice_area100_fig", style = {'width': '100vh', 'height': '40vh',
                                                                            "position": "absolute", "top":"30vh", "right":"20vh"}),
                                 dcc.Graph(id="ice_area50_fig", style = {'width': '100vh', 'height': '40vh',
                                                                            "position": "absolute", "top":"70vh", "right":"20vh"}),
                                 # dcc.Graph(id="ice_mean_fig", style={'width': '80vh', 'height': '30vh',
                                 #                                        "position": "absolute", "top": "80vh",
                                 #                                        "right": "45vh"})
                                ]
                    )
@app.callback(Output("maps_fig", "figure"),
              Input("year_slider","value")
              )
def update_year(year_index):
    image = sat_maps[year_index]
    fig = px.imshow(image, color_continuous_scale='teal',
                    labels=dict(color="Ice concentration [%]")
                    ,title=f"Arctic map on the 15th of August {years[year_index]}"
                    # ,color_continuous_label='Continent',
                    # color_continuous_label_font=dict(size=16)
    )
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title_font_size = 30, title_font_family = "Bahnschrift",
                      paper_bgcolor="LightSteelBlue")
    # fig.update_layout(coloraxis_colorbar= dict(tickvals = [""], ticktext=[""]))
    return fig

# @app.callback(Output("total_area", "children"),
#               Input("year_slider","value")
#               )
# def update_year_ice100(year_index):
#     image = ice_area100[year_index]
#     year = [i for i in years]
#     # fig = px.imshow(image)
#     # fig.update_layout(coloraxis_colorbar= dict(tickvals = [""], ticktext=[""]))
#     n = 0
#     # for i in years:
#     return f"Area totally covered by ice in {year[year_index]} is {ice_area100[year_index]:,.2f} squared km"
        # n = n+1
@app.callback(Output("ice_area100_fig", "figure"),
              Input("year_slider", "value"))
def update_year_fig(year_index):
    year = [i for i in years]
    # fig, ax = plt.subplots()
    fig = px.scatter(x = years, y = ice_area100,
                     trendline='ols',trendline_scope="overall",
                     trendline_color_override="grey",
                     title = "Area totally covered by ice in squared kilometer")

    fig.update_xaxes(title ="Years", title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_yaxes(title="Area totally covered by ice [Km2]", title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_layout(title_font_size = 20, title_font_family = "Bahnschrift",
                      paper_bgcolor="LightSteelBlue")
    # fig.show()
    #
    # fig = px.line(x = years, y = pred_area100)
    # fig.add_scatter(trendline = "ols")

    fig.add_scatter(x = [years[year_index]],y = [ice_area100[year_index]], mode = "markers",
                    marker= dict(color="blue", size=12),name = f'Area totally covered by ice in km2', showlegend=True)
    return fig
@app.callback(Output("ice_area50_fig", "figure"),
              Input("year_slider", "value"))
def update_year_fig(year_index):
    year = [i for i in years]
    # fig, ax = plt.subplots()
    fig = px.scatter(x = years, y = ice_area50, title = "Area with at least 50% of ice concentration in squared kilometer",
                     trendline='ols',trendline_scope="overall",
                     trendline_color_override="grey")
    fig.update_xaxes(title="Years", title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_yaxes(title=r'Area where ice coverage > 50% [Km2]', title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_layout(title_font_size = 20, title_font_family = "Bahnschrift",
                      paper_bgcolor="LightSteelBlue")
    fig.add_scatter(x = [years[year_index]],y = [ice_area50[year_index]], mode = "markers",
                    marker= dict(color="blue", size=12), name=f'Area 50% covered by ice in km2',showlegend=True)
    return fig
# @app.callback(Output("ice_mean_fig", "figure"),
#               Input("year_slider", "value"))
# def update_year_fig(year_index):
#     year = [i for i in years]
#     # fig, ax = plt.subplots()
#     fig = px.line(x = years, y = ice_mean, title = "Mean value of ice concentration")
#     fig.add_scatter(x = [years[year_index]],y = [ice_mean[year_index]], mode = "markers",
#                     marker= dict(color="blue", size=12), name="",  showlegend=False)
#     return fig

if __name__ == "__main__":
    app.run_server(debug = True)







