import numpy as np
from dash import Dash, Output,Input, html, dcc
import plotly.express as px
import glob
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import plotly.graph_objects as go

app = Dash(__name__, title="Arctic maps analysis")
server = app.server

l = sorted(glob.glob("./ice_data/*.npy"))
ice_area = np.load("./ice_data_area.npy")

ice_area100 = np.zeros(16)
ice_area50 = np.zeros(16)
years = np.zeros(16)
# years = []
j = 0
sat_maps = []

for file in l:
    img = np.load(file)
    sat_maps.append(np.array(img))
    img[np.isnan(img)] = 0
    ice_area100[j] = np.sum(ice_area[img == 100])
    ice_area50[j] = np.sum(ice_area[img > 50])
    years[j] = int(file[11:15])
    # years.append(file[11:15])
    j = j+1
years= np.sort(years.astype(int))
linear_reg_100 = LinearRegression()
linear_reg_100.fit(years.reshape(-1, 1), ice_area100)
y100_pred = linear_reg_100.predict(years.reshape(-1, 1))
linear_reg_50 = LinearRegression()
linear_reg_50.fit(years.reshape(-1, 1), ice_area50)
y50_pred = linear_reg_50.predict(years.reshape(-1, 1))

app.layout = html.Div([
                                 html.H1("Analysis of Arctic Maps."),
                                 html.H3(["This is a presentation of satellite images of the Arctic Ocean from the year 2003 to 2019."
                                         "This a small subset of the complete satellite data set, with only one map, on the 15th of August, is presented for each year." 
                                        "All the data were downloaded from ",
                                        html.A("here. ", href="https://seaice.uni-bremen.de/data-archive/"),
                                        " The data used in this problem set was collected by two different satellite missions. Involved are the "
                                        "AMSR-E instrument on the Aqua satellite (data from 2002 to 2011) and the AMSR2 instrument on the GCOM-W satellite (data from 2013 to 2019)."
                                        " The data consist of maps of the concentration of ice in the Arctic collected between 2002 and 2019 with the exception of 2012.\n"
                                        "Use the slider to select a year and view the ice map for August 15th of that year."
                                        " There are two figures available: one displays the area where ice concentration is 100%, and the other shows areas where ice concentration is 50% or greater."
                                        " A linear regression model is fit to each figure, the lines that represent the models are shown in red. "
                                        " Hover around the red lines to see more information about the linear fit."]),
            html.Div([
                    dcc.Slider(
                                min=0,
                                max=len(years)-1,
                                value=0,
                                marks={i: str(years[i]) for i in range(len(years))},
                                step=1,
                                id="year_slider"
                                )
                                ]),
            html.Div(
                [dcc.Graph(id="maps_fig", style={"width":"75vh", "height":"75vh"})], style={"position":"absolute", "left":"5%", "width":"55vh", "height":"55vh"}),
            html.Div([dcc.Graph(id = "ice_area100_fig"),
                      dcc.Graph(id="ice_area50_fig")], style={"position":"absolute", "right":"5%", "width":"100vh", "height":"40vh"})]
)

@app.callback(Output("maps_fig", "figure"),
              Input("year_slider","value"))
def update_year(year_index):
    image = sat_maps[year_index]
    fig = px.imshow(image, color_continuous_scale='teal',
                    labels=dict(color="Ice concentration [%]")
                    ,title=f"Arctic map on the 15th of August {years[year_index]}"
    )
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title_font_size = 30, title_font_family = "Bahnschrift",
                      paper_bgcolor="LightSteelBlue")
    return fig

@app.callback(Output("ice_area100_fig", "figure"),
              Input("year_slider", "value"))
def update_year_fig(year_index):
    year = [i for i in years]
    fig_data100 = go.Scatter(x = years, y = ice_area100,name = "Area in km2", mode = "lines + markers",marker= dict(color="blue", size=12))
    fig_fit100 = go.Scatter(x= years, y = y100_pred,
                         hovertext=f"R2 = {r2_score(ice_area100,y100_pred)} , mean_squared_error = {mean_squared_error(ice_area100,y100_pred)}"
                         ,name = "Linear fit", mode = "lines + markers",marker= dict(color="red", size=12))
    figures100 = [fig_data100,fig_fit100]
    fig = go.Figure(data= figures100)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(title ="Years", title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_yaxes(title="Area totally covered by ice [Km2]", title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_layout(title_font_size = 20, title_font_family = "Bahnschrift",
                      paper_bgcolor="LightSteelBlue")
    # fig.add_scatter(x = [years[year_index]],y = [ice_area100[year_index]], mode = "markers",
    #                 marker= dict(color="blue", size=12),name = f'Area totally covered by ice in km2', showlegend=False)
    # fig.add_scatter(x=[years[year_index]], y=[y100_pred[year_index]], mode="markers",
    #                 marker=dict(color="red", size=12), showlegend=False)
    return fig
@app.callback(Output("ice_area50_fig", "figure"),
              Input("year_slider", "value"))
def update_year_fig(year_index):
    year = [i for i in years]
    fig_data50 = go.Scatter(x = years, y = ice_area50,name = "Area in km2", mode = "lines + markers",marker= dict(color="blue", size=12))
    fig_fit50 = go.Scatter(x=years, y=y50_pred,hovertext=f"R2 = {r2_score(ice_area50,y50_pred)} , mean_squared_error = {mean_squared_error(ice_area50,y50_pred)}"
                         ,name = "Linear fit", mode = "lines + markers",marker= dict(color="red", size=12))
    figures50 = [fig_data50, fig_fit50]
    fig = go.Figure(data=figures50)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(title="Years", title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_yaxes( title = "Area where ice concentration is at least 50% [Km2]", title_font_size = 16,title_font_family = "Bahnschrift")
    fig.update_layout(title_font_size = 20, title_font_family = "Bahnschrift",
                      paper_bgcolor="LightSteelBlue")
    # fig.add_scatter(x = [years[year_index]],y = [ice_area50[year_index]], mode = "markers",
    #                 marker= dict(color="blue", size=12), name=f'Area 50% covered by ice in km2',showlegend=False)
    # fig.add_scatter(x=[years[year_index]], y=[y50_pred[year_index]], mode="markers",
    #                 marker=dict(color="red", size=12), showlegend=False)
    return fig
if __name__ == "__main__":
    app.run_server(debug = True)