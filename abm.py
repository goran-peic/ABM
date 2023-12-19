from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from functions import seedActors, RunSimulation, extractInfo, stacked
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter
from bokeh.embed import file_html, components
from bokeh.resources import CDN
from jinja2 import Environment
import re


# env = Environment(extensions=['jinja2.ext.autoescape'])
app = Flask(__name__)
app.config["SECRET_KEY"] = "ITSASECRET"


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "GET":
    return render_template("index.html")
  else:
    terrain_size = int(request.form["terrain_size"])
    grass = int(request.form["grass"])
    sheep = int(request.form["sheep"])
    wolves = int(request.form["wolves"])
    simulation_runs = int(request.form["simulation_runs"])
    grass_reproduction_rate = float(request.form["grass_reproduction_rate"])
    sheep_reproduction_rate = float(request.form["sheep_reproduction_rate"])
    wolf_reproduction_rate = float(request.form["wolf_reproduction_rate"])
    grass_life = int(request.form["grass_life"])
    sheep_life = int(request.form["sheep_life"])
    wolf_life = int(request.form["wolf_life"])

    if simulation_runs > 300:
      too_many_runs = True
      return render_template("index.html", too_many_runs=too_many_runs)

    terrain = pd.DataFrame(0, index=range(terrain_size), columns=list(range(terrain_size)))
    initial_population = seedActors(dataset=terrain, terrain_size=terrain_size, grass=grass, sheep=sheep, wolves=wolves,
                                    grass_reproduction_rate=grass_reproduction_rate, sheep_reproduction_rate=sheep_reproduction_rate,
                                    wolf_reproduction_rate=wolf_reproduction_rate, grass_life=grass_life,
                                    sheep_life=sheep_life, wolf_life=wolf_life)
    del terrain

    initial_info = extractInfo(initial_population)
    dframe = pd.DataFrame(
      {'iter': [1], 'grass_count': initial_info[0], 'sheep_count': initial_info[1], 'wolf_count': initial_info[2]})
    dframe = dframe.loc[:, ['iter', 'grass_count', 'sheep_count', 'wolf_count']]
    dframe = RunSimulation(simulation_runs=simulation_runs, dataset=dframe, initial_population=initial_population,
                           grass_life=grass_life, sheep_life=sheep_life, wolf_life=wolf_life)
    x_iter = dframe.loc[:, 'iter'].values
    y_grass = dframe.loc[:, 'grass_count'].values
    y_sheep = dframe.loc[:, 'sheep_count'].values
    y_wolves = dframe.loc[:, 'wolf_count'].values

    TOOLS = "pan,box_zoom,hover,undo,reset,save"

    ### (1) Population Evolution Plot
    creature_plot = figure(title="Population Evolution (Counts)", tools=TOOLS, width=700, height=350,
                           toolbar_location="above")
    creature_plot.background_fill_color = "#f4f4f4"
    creature_plot.min_border_left = 20
    creature_plot.background_fill_alpha = 0.68
    creature_plot.xaxis.axis_label = "Iteration"; creature_plot.yaxis.axis_label = "Count"
    creature_plot.border_fill_color = "black"; creature_plot.xaxis.axis_label_text_color = \
      creature_plot.yaxis.axis_label_text_color = "white"
    creature_plot.xaxis.major_tick_line_color = creature_plot.xaxis.minor_tick_line_color = \
      creature_plot.yaxis.minor_tick_line_color = creature_plot.yaxis.major_tick_line_color = "white"
    creature_plot.title.text_color = creature_plot.xaxis.major_label_text_color = \
      creature_plot.yaxis.major_label_text_color = "white"
    creature_plot.xaxis.axis_line_color = creature_plot.yaxis.axis_line_color = "white"

    creature_plot.circle(x_iter, y_grass, legend_label="Grass", fill_color="green")
    creature_plot.line(x_iter, y_grass, legend_label="Grass", line_color="green", line_width=2)

    creature_plot.square(x_iter, y_sheep, legend_label="Sheep", fill_color="#ffffff")
    creature_plot.line(x_iter, y_sheep, legend_label="Sheep", line_color="#ffffff", line_width=2)

    creature_plot.triangle(x_iter, y_wolves, legend_label="Wolves", fill_color="red", line_color="red")
    creature_plot.line(x_iter, y_wolves, legend_label="Wolves", line_color="red", line_width=2)

    # creature_plot.legend.background_fill_color = "#e6e6e6"; creature_plot.legend_label.background_fill_alpha = 0.25
    # creature_plot.legend.label_text_font_style = "bold"

    html_text = file_html(creature_plot, CDN, "Population Evolution")
    script_1, div1 = components(creature_plot)
    doc_id = html_text[re.search("docid", html_text).start() + 8: re.search("docid", html_text).start() + 44]
    # element_id = script_1[re.search("elementid", script_1).start() + 12: re.search("elementid", script_1).start() + 48]
    element_id = div1[re.search("div id", div1).start() + 8: re.search("div id", div1).start() + 44]
    #print(script_1)
    print(div)
    print(element_id)
    js_script = html_text[re.search(r"function()", html_text).start() - 8 : re.search("Bokeh.embed.embed_items",
                                                                                      html_text).start() + 61]

    ### (2) Population Stacked Share Plot

    dframe2 = dframe[:]
    dframe2['Grass Share'] = dframe2['grass_count'] / (
    dframe2['grass_count'] + dframe2['sheep_count'] + dframe2['wolf_count'])
    dframe2['Sheep Share'] = dframe2['sheep_count'] / (
    dframe2['grass_count'] + dframe2['sheep_count'] + dframe2['wolf_count'])
    dframe2['Wolf Share'] = dframe2['wolf_count'] / (
    dframe2['grass_count'] + dframe2['sheep_count'] + dframe2['wolf_count'])
    dframe2 = dframe2.loc[:, ['iter', 'Grass Share', 'Sheep Share', 'Wolf Share']]
    categories = ['Grass Share', 'Sheep Share', 'Wolf Share']
    areas = stacked(dframe2, categories)
    colors = list(areas.keys())
    for index, key in enumerate(colors):
      if key == "Grass Share":
        colors[index] = 'green'
      elif key == "Wolf Share":
        colors[index] = 'red'
      else:
        colors[index] = 'white'

    iter2 = np.hstack((dframe2['iter'][::-1], dframe2['iter']))

    TOOLS = "pan,box_zoom,undo,reset,save"
    creature_plot2 = figure(x_range=(1, len(dframe2['iter'])-1), y_range=(0, 1), title="Population Evolution (Shares)",
                            tools=TOOLS, width=700, height=350, toolbar_location="above")
    creature_plot2.grid.minor_grid_line_color = '#eeeeee'

    creature_plot2.patches([iter2] * len(areas), [areas[cat] for cat in categories], color=colors, alpha=1,
                           line_color=None)

    creature_plot2.min_border_left = 20; creature_plot2.min_border_right = 20
    creature_plot2.xaxis.axis_label = "Iteration"
    creature_plot2.yaxis.axis_label = "Share"
    creature_plot2.border_fill_color = "black"
    creature_plot2.xaxis.axis_label_text_color = \
      creature_plot2.yaxis.axis_label_text_color = "white"
    creature_plot2.xaxis.major_tick_line_color = creature_plot2.xaxis.minor_tick_line_color = \
      creature_plot2.yaxis.minor_tick_line_color = creature_plot2.yaxis.major_tick_line_color = "white"
    creature_plot2.title.text_color = creature_plot2.xaxis.major_label_text_color = \
      creature_plot2.yaxis.major_label_text_color = "white"
    creature_plot2.xaxis.axis_line_color = creature_plot2.yaxis.axis_line_color = "white"

    for a, area in enumerate(areas):
      creature_plot2.patch(iter2, areas[area], color=colors[a], alpha=1, line_color=None)

    # creature_plot2.legend_label.background_fill_color = "#e6e6e6"
    # creature_plot2.legend_label.background_fill_alpha = 0.4
    # creature_plot2.legend_label.label_text_font_style = "bold"

    creature_plot2.yaxis[0].formatter = NumeralTickFormatter(format="0%")

    html_text2 = file_html(creature_plot2, CDN, "Population Evolution")
    script_2, div2 = components(creature_plot2)
    doc_id = html_text2[re.search("docid", html_text2).start() + 8: re.search("docid", html_text2).start() + 44]
    # element_id = script_1[re.search("elementid", script_1).start() + 12: re.search("elementid", script_1).start() + 48]
    element_id2 = div2[re.search("div id", div2).start() + 8: re.search("div id", div2).start() + 44]
    js_script2 = html_text2[re.search(r"function()", html_text2).start() - 8 : re.search("Bokeh.embed.embed_items",
                                                                                         html_text2).start() + 61]
    # print(html_text2)
    # print(element_id2)
    plots_created = True
    return render_template('index.html', element_id=element_id, js_script=js_script, plots_created=plots_created,
                           element_id2=element_id2, js_script2=js_script2, terrain_size=terrain_size, grass=grass,
                           sheep=sheep, wolves=wolves, simulation_runs=simulation_runs, grass_reproduction_rate=grass_reproduction_rate,
                           sheep_reproduction_rate=sheep_reproduction_rate, wolf_reproduction_rate=wolf_reproduction_rate,
                           grass_life=grass_life, sheep_life=sheep_life, wolf_life=wolf_life)

if __name__ == "__main__":
  app.run(debug=False)
