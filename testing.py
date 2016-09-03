import pandas as pd
from functions import seedActors, RunSimulation, extractInfo, stacked
from bokeh.plotting import figure, show
import numpy as np
from bokeh.palettes import brewer

from bokeh.charts import Scatter
from bokeh.embed import file_html
from bokeh.resources import CDN
from jinja2 import Environment
import re, requests



terrain_size = 15
grass = 70
sheep = 60
wolves = 50
simulation_runs = 100

grass_reproduction_rate = 0.5
sheep_reproduction_rate = 0.3
wolf_reproduction_rate = 0.2
grass_life = 10
sheep_life = 20
wolf_life = 25

#    print(request.form["runsim"])
#    if request.form["runsim"] is None: return render_template("index.html")
#    else:

terrain = pd.DataFrame(0, index=range(terrain_size), columns=list(range(terrain_size)))
initial_population = seedActors(dataset=terrain, terrain_size=terrain_size, grass=grass, sheep=sheep, wolves=wolves,
                                grass_reproduction_rate=grass_reproduction_rate, sheep_reproduction_rate=sheep_reproduction_rate,
                                wolf_reproduction_rate=wolf_reproduction_rate, grass_life=grass_life,
                                sheep_life=sheep_life, wolf_life=wolf_life)
del terrain

initial_info = extractInfo(initial_population)
dframe = pd.DataFrame(
  {'iter': [1], 'grass_count': initial_info[0], 'sheep_count': initial_info[1], 'wolf_count': initial_info[2]})
dframe = dframe.ix[:, ['iter', 'grass_count', 'sheep_count', 'wolf_count']]
dframe = RunSimulation(simulation_runs=simulation_runs, dataset=dframe, initial_population=initial_population)
x_iter = dframe.ix[:, 'iter'].values
y_grass = dframe.ix[:, 'grass_count'].values;
y_sheep = dframe.ix[:, 'sheep_count'].values;
y_wolves = dframe.ix[:, 'wolf_count'].values

TOOLS = "pan,wheel_zoom,hover,undo,reset,save"

### (1) Population Evolution Plot
creature_plot = figure(title="Population Evolution", tools=TOOLS, width=700, height=350,
                       responsive=True, toolbar_location="above")
creature_plot.background_fill_color = "#f4f4f4"
creature_plot.min_border_left = 20
creature_plot.background_fill_alpha = 0.82
creature_plot.xaxis.axis_label = "Iteration"; creature_plot.yaxis.axis_label = "Count"
creature_plot.border_fill_color = "black"; creature_plot.xaxis.axis_label_text_color = \
  creature_plot.yaxis.axis_label_text_color = "white"
creature_plot.xaxis.major_tick_line_color = creature_plot.xaxis.minor_tick_line_color = \
  creature_plot.yaxis.minor_tick_line_color = creature_plot.yaxis.major_tick_line_color = "white"
creature_plot.title.text_color = creature_plot.xaxis.major_label_text_color = creature_plot.yaxis.major_label_text_color = "white"
creature_plot.xaxis.axis_line_color = creature_plot.yaxis.axis_line_color = "white"

creature_plot.circle(x_iter, y_grass, legend="Grass", fill_color="green")
creature_plot.line(x_iter, y_grass, legend="Grass", line_color="green")

creature_plot.square(x_iter, y_sheep, legend="Sheep", fill_color="blue")
creature_plot.line(x_iter, y_sheep, legend="Sheep", line_dash=(4, 4), line_color="blue", line_width=2)

creature_plot.triangle(x_iter, y_wolves, legend="Wolves", fill_color="red", line_color="red")
creature_plot.line(x_iter, y_wolves, legend="Wolves", line_color="red")

# show(creature_plot)

### (2) Population Stacked Share Plot

dframe2 = dframe[:]
dframe2['Grass Share'] = dframe2['grass_count'] / (
dframe2['grass_count'] + dframe2['sheep_count'] + dframe2['wolf_count'])
dframe2['Sheep Share'] = dframe2['sheep_count'] / (
dframe2['grass_count'] + dframe2['sheep_count'] + dframe2['wolf_count'])
dframe2['Wolf Share'] = dframe2['wolf_count'] / (
dframe2['grass_count'] + dframe2['sheep_count'] + dframe2['wolf_count'])
dframe2 = dframe2.ix[:, ['iter', 'Grass Share', 'Sheep Share', 'Wolf Share']]
categories = ['Grass Share', 'Sheep Share', 'Wolf Share']

areas = stacked(dframe2, categories)
colors = list(areas.keys())
for index, key in enumerate(colors):
  if key == "Grass Share": colors[index] = 'green'
  elif key == "Wolf Share": colors[index] = 'red'
  else: colors[index] = 'white'
print(colors)

iter2 = np.hstack((dframe2['iter'][::-1], dframe2['iter']))

TOOLS = "pan,box_zoom,undo,reset,save"
creature_plot2 = figure(x_range=(1, simulation_runs), y_range=(0, 1), title="Population Evolution (Shares)", tools=TOOLS,
                        width=700, height=350, responsive=True, toolbar_location="above")
# creature_plot2.grid.minor_grid_line_color = '#eeeeee'

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
creature_plot2.title.text_color = creature_plot2.xaxis.major_label_text_color = creature_plot2.yaxis.major_label_text_color = "white"
creature_plot2.xaxis.axis_line_color = creature_plot2.yaxis.axis_line_color = "white"

for a, area in enumerate(areas):
  creature_plot2.patch(iter2, areas[area], color=colors[a], legend=area, alpha=1, line_color=None)

creature_plot2.legend.background_fill_color = "#e6e6e6";
creature_plot2.legend.background_fill_alpha = 0.4
creature_plot2.legend.label_text_font_style = "bold"

show(creature_plot2)

'''

N = 20 # iterations
categories = ['y' + str(x) for x in range(10)] # three species
data = {}
data['x'] = np.arange(N)
for cat in categories:
    data[cat] = np.random.randint(10, 100, size=N)

df = pd.DataFrame(data)
df = df.set_index(['x'])

def stacked(df, categories):
    areas = dict()
    last = np.zeros(len(df[categories[0]]))
    for cat in categories:
        next = last + df[cat]
        areas[cat] = np.hstack((last[::-1], next))
        last = next
    return areas

areas = stacked(df, categories)

print(areas)

colors = brewer["Spectral"][len(areas)]

x2 = np.hstack((data['x'][::-1], data['x']))

print(x2)

p = figure(x_range=(0, 19), y_range=(0, 800))
p.grid.minor_grid_line_color = '#eeeeee'

print([x2] * len(areas))
print("###")
print([areas[cat] for cat in categories])

p.patches([x2] * len(areas), [areas[cat] for cat in categories],
          color=colors, alpha=0.8, line_color=None)

show(p)

'''













### (3) Initial Scatter Plot
# Need to write an ExtractData function to get spatial data from the final pop.
# initial_scatter = Scatter(title="Population Evolution", tools=TOOLS, width=700, height=350,
#                       responsive=True, toolbar_location="above")
# p = Scatter(df, x='mpg', y='hp', color='cyl', title="HP vs MPG (shaded by CYL)",
#            xlabel="Miles Per Gallon", ylabel="Horsepower")

### ANALYSES
# (1) Show initial and final distributions. Use histograms instead of pie charts. Maybe stacked?
# (2) Plotting the position information on the tile board.
# (3) Under what conditions do we see stable (non-extinction) patterns persist?
