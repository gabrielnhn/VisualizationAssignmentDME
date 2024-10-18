# We do the basic setup here.
# Do not (!) change this cell! All changes will be reset during grading!

# numpy and pandas
import numpy as np
import pandas as pd
from bokeh.io import curdoc

# We import a range of bokeh functionality that will likely be needed already
# if you need more, import it at the top of the corresponding cell
from bokeh.plotting import figure, gridplot, show
from bokeh.layouts import column, grid
from bokeh.layouts import column as bokeh_column
from bokeh.transform import factor_cmap, linear_cmap
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, BasicTicker, PrintfTickFormatter, CustomJS, Select, axes
from bokeh.models.annotations import Label
from bokeh.io import output_notebook
# output_notebook() # activate Bokeh output to Jupyter notebook

# You can use this to calculate the density plot in Assignment V.3
from scipy.stats import gaussian_kde
from bokeh.layouts import gridplot
import math

# We load the adult data  (https://archive.ics.uci.edu/dataset/2/adult) as in previous assignments (note, we keep the headers, to use them in the pandas dataframe)
# Note: we do not change ? values to nan, but rather keep them as ? so they will be shown in the visualizations
data = pd.read_csv("datasets/Visualization/adult_all.csv")

data.head()

def arrange_plots_in_grid(plot_list, num_cols=4):
    # Calculate the number of rows required
    num_rows = math.ceil(len(plot_list) / num_cols)
    
    # Create the grid by adding plots row-wise (each row contains up to 4 plots)
    grid = []
    for i in range(num_rows):
        row = plot_list[i * num_cols:(i + 1) * num_cols]  # Get plots for the current row
        # If there are fewer than 4 plots in the last row, append None to fill the empty spaces
        while len(row) < num_cols:
            row.append(None)
        grid.append(row)
    
    return grid

###############################
# VIS1 COPY
#global dict whatever
glob_dict = {}



def create_bar_plot(data_original, clean = True):
    
    TOOLS="pan,box_zoom,tap, hover"
    output_plots_dict = {}
    output_plots = []
    columns = data.columns.tolist()
    for column in columns:
        TOOLTIPS=[(column.title(), "@x_values"), ("Count", "@y_values")]
        # replace '?' by NAN values
        column_data = data[column].replace("?", np.nan).dropna()
        if pd.api.types.is_numeric_dtype(column_data):
            sorted_counts = column_data.value_counts().sort_index()
            index = sorted_counts.index.tolist()
            counts = sorted_counts.values.tolist()  
            glob_dict[column] = dict(x_values=index, y_values=counts)
        #categorical columns
        else:
            # print(column_data)
            column_data = column_data.apply(lambda sal: sal.strip('.'))

            categories = column_data.value_counts().index.tolist()
            
            counts = column_data.value_counts().values.tolist()
            glob_dict[column] = dict(x_values=categories, y_values=counts)

        if pd.api.types.is_numeric_dtype(column_data):
            frequency_plot = {'x_values': index, 'y_values': counts}
            p = figure(height=600, width=600, title=column.title(), toolbar_location=None, tools=TOOLS, tooltips=TOOLTIPS)
            p.xaxis.formatter = NumeralTickFormatter(format="0,0")
        else:
            frequency_plot = {'x_values': categories, 'y_values': counts}
            p = figure(x_range=categories,height=600, width=600, title=column.title(), toolbar_location=None, tools=TOOLS, tooltips=TOOLTIPS)

        source = ColumnDataSource(frequency_plot)
        compare = ColumnDataSource({})
        p.vbar(x='x_values', top='y_values', width=0.5, source=source, line_color='lightgreen', fill_color='lightgreen', line_width=2.5)
        p.vbar(x='x_values', top='y_values', width=0.5, source=compare, line_color='orange', fill_color='orange', line_width=2.5)
        p.xaxis.major_label_orientation = 1.0

        output_plots_dict[column] = {}

        output_plots_dict[column]["plot"] = p
        output_plots_dict[column]["source_all"] = source
        output_plots_dict[column]["source_compare"] = compare
        output_plots.append(p)
        # show(p)

    return output_plots, output_plots_dict


def function_all_p(data,column_name,index):
    local_dictionary = {}
    attribute = glob_dict[column_name]['x_values'][index]
    # select all the columns except the column_name
    for key in glob_dict:
        # get x_values for all other columns
        x_values = glob_dict[key]['x_values']
        # count the new y_values
        column_data = data[data[column_name] == attribute][key]
        index = column_data.value_counts().index.tolist()
        counts = column_data.value_counts().values.tolist()
        new_y_values = []
        for x in x_values:
            if x in index:
                new_y_values.append(counts[index.index(x)])
            else:
                new_y_values.append(0)
        local_dictionary[key] = dict(x_values=x_values, y_values=new_y_values)
    return local_dictionary

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, TapTool, CustomJS
from bokeh.models.widgets.markups import Div
from bokeh.layouts import gridplot
from bokeh.io import output_notebook

# output_notebook()

import pandas as pd
import numpy as np


class custom_callbacks:
    def __init__(self, feature =None, source=None, figure=None):
        self.feature = feature
        self.source = source
        self.figure = figure

    def update_all_plots(self):
        new = self.new
        if new:

            index = new[0]
            new_values = function_all_p(data, self.feature, index)
            for column, new_source in new_values.items():

                plot_dict[column]["source_compare"].data = new_source
                plot_dict[column]["source_compare"].selected.indices = []

            for column in plot_dict:
                plot_dict[column]["plot"].title.text = column.title() + \
                    f" ({self.feature}={plot_dict[self.feature]["source_compare"].data["x_values"][index]})"

        else:
            index = None
            for column in plot_dict:
                plot_dict[column]["source_compare"].data = {}
                plot_dict[column]["plot"].title.text = column.title()


    def default_function(self, attr, old, new):
        self.new = new

        print("\t")
        for column in plot_dict:
            plot_dict[column]["plot"].title.text = "Loading..."
        curdoc().add_next_tick_callback(self.update_all_plots)


grid_list, plot_dict = create_bar_plot(data)

for column, d in plot_dict.items():
    d["source_all"].selected.on_change("indices", custom_callbacks(column, d["source_all"], d["plot"]).default_function)


grid = gridplot(arrange_plots_in_grid(grid_list, num_cols=3))


HTML = """
        <h1>Instructions:</h1>
        <h2>1:Choose one of the plots;</h2>
        <h2>2:Click on one of the bars;</h2>
        <h2>3:Wait a few moments...</h2>
        <h2>4:The selected subset of the data should be plotted in comparison to all the data!</h2>
"""
div = Div(text=HTML,
width=900, height=200)


curdoc().add_root(bokeh_column(div, grid))

