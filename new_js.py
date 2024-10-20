# We do the basic setup here.
# Do not (!) change this cell! All changes will be reset during grading!

# numpy and pandas
import numpy as np
import pandas as pd

# We import a range of bokeh functionality that will likely be needed already
# if you need more, import it at the top of the corresponding cell
from bokeh.plotting import figure, gridplot, show
from bokeh.transform import factor_cmap, linear_cmap
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, BasicTicker, PrintfTickFormatter, CustomJS, Select, axes
from bokeh.models.annotations import Label
from bokeh.io import output_notebook, curdoc

# output_notebook() # activate Bokeh output to Jupyter notebook

# You can use this to calculate the density plot in Assignment V.3
from scipy.stats import gaussian_kde

# We load the adult data  (https://archive.ics.uci.edu/dataset/2/adult) as in previous assignments (note, we keep the headers, to use them in the pandas dataframe)
# Note: we do not change ? values to nan, but rather keep them as ? so they will be shown in the visualizations
data = pd.read_csv("datasets/Visualization/adult_all.csv")

data.head()

# Sample DataFrame
# data = {
#     'class': ['A', 'A', 'B', 'B', 'C'],
#     'age': [10, 20, 30, 25, 15],
#     'income': [3, 7, 5, 2, 8]
# }

# data = pd.DataFrame(data)

# from here its ready to be copied into notebook
import math
import json
from bokeh.models.widgets import Div
from bokeh.layouts import column as bokeh_column
from bokeh.layouts import grid


def arrange_plots_in_grid(plot_list, num_cols=4):
    num_rows = math.ceil(len(plot_list) / num_cols)
    grid = []
    for i in range(num_rows):
        row = plot_list[i * num_cols:(i + 1) * num_cols]
        while len(row) < num_cols:
            row.append(None)
        grid.append(row)
    return grid
    
glob_dict = {}
x_list = []
# Define a function to create individual bar plots for categorical and numerical columns
def create_bar_plot(data, clean = True):
    TOOLS="pan,box_zoom,tap, hover"
    list_plot = []
    list_source = []
    columns = data.columns.tolist()
    for column in columns:
        TOOLTIPS=[(column.title(), "@x_values"), ("Count", "@y_values")]
        # replace '?' by NAN values
        column_data = data[column].replace("?", np.nan).dropna()
        # numerical columns
        if pd.api.types.is_numeric_dtype(column_data):
            sorted_counts = column_data.value_counts().sort_index()
            index = sorted_counts.index.tolist()
            counts = sorted_counts.values.tolist()  
            glob_dict[column] = dict(x_values=index, y_values=counts)
            list_source.append(dict(x_values=index, y_values=counts))
            x_list.append(index)
        #categorical columns
        else:
            categories = column_data.value_counts().index.tolist()
            counts = column_data.value_counts().values.tolist()
            glob_dict[column] = dict(x_values=categories, y_values=counts)
            list_source.append((dict(x_values=categories, y_values=counts)))
            x_list.append(categories)
        if pd.api.types.is_numeric_dtype(column_data):
            frequency_plot = {'x_values': index, 'y_values': counts}
            p = figure(height=600, width=600, title=column,
                       toolbar_location="above", tools=TOOLS, tooltips=TOOLTIPS)
            p.xaxis.formatter = NumeralTickFormatter(format="0,0")
        else:
            frequency_plot = {'x_values': categories, 'y_values': counts}
            p = figure(x_range=categories,height=600, width=600, title=column,
                       toolbar_location="above", tools=TOOLS, tooltips=TOOLTIPS)
        list_plot.append(p)
    return list_plot,list_source
    
print("Creating original plots...", end="")
list_plot,list_source = create_bar_plot(data)
print(" Done.")


print("Adjusting column data sources...", end="")
index = 0
list_source_full = []
list_source_subset = []
for p,source in zip(list_plot,list_source):
    source_full = ColumnDataSource(source)
    source_full.name = p.title.text
    list_source_full.append(source_full)

    new_source = dict(x_values = source['x_values'],y_values=[0 for i in source['y_values'] ])
    source_subset = ColumnDataSource(new_source)
    list_source_subset.append(source_subset)
    p.vbar(x='x_values', top='y_values', width=0.5, source=source_full, line_color='lightblue', fill_color='lightblue', line_width=2.5)
    p.vbar(x='x_values', top='y_values', width=0.5, source=source_subset, line_color='orange', fill_color='orange', line_width=2.5)
    # # Add hover tool to display values on hover
    # hover = HoverTool()
    # hover.tooltips = [(data.columns[index], "@x_values"), ("Count", "@y_values")]
    # p.add_tools(hover)
    # Add the TapTool and link it to the callback
    # Format the y-axis with commas as well
    p.xaxis.major_label_orientation = 1.0

print(" Done.")

# data_json = data.to_json()

data_cds = ColumnDataSource(data)

javascript_code = """

function getSourceFull(array, name) {
    //array.forEach(function return_if_match(source)
    for(let k = 0; k < array.length; k++)
    {
        let source = array[k];
        if (source.name === name)
            return source;
    }
}

// get selected indices and length
let source_full = getSourceFull(list_source_full, column_name);
const selected_indices = source_full.selected.indices;
let length_indices = selected_indices.length;

if (length_indices > 0) {
    list_titles.forEach((title) => title.text = "Loading...");
}

setTimeout(function() { // timeout so browser doesnt get stuck doing the calculations

    

    if (length_indices > 0) {

        list_titles.forEach((title) => title.text = "Loading...");
        var data = raw_data.data;
        var selected_values = [];
        
        // get x_value
        for (let i = 0; i < list_source_full.length; i++) {
            if (list_source_full[i].name == column_name){
                var x_value = x_values[i];
                for (let j = 0; j < length_indices; j++){
                    selected_values.push(x_value[selected_indices[j]]);
                }
            }
        }

        var column_data = data[column_name];
        var filtered_rows = [];
        // for the column data calculate the rows corresponding to selected x_values
        for (const [index, value] of Object.entries(column_data)) {
            if (Object.values(selected_values).indexOf(value) > -1) {
                filtered_rows.push(parseInt(index));
            }
        }

        // for the selected rows, filter the values corresponding updating bar plot
        for (let i = 0; i < list_source_full.length; i++){
            var x_value = x_values[i];
            // get the column of target bar plot
            var column_data = data[columns[i]];
            // filter the column
            var final_data = [];
            for (let j = 0; j < filtered_rows.length; j++){
                final_data.push(column_data[filtered_rows[j]]);
            }
            var new_y_values = [];
            for (let j = 0; j < x_value.length; j++){
                new_y_values.push(final_data.filter(x => x==x_value[j]).length);
            }
            list_source_subset[i].data.y_values = new_y_values;
            list_source_subset[i].change.emit();
            let title = columns[i]
            if (selected_values.length > 0)
            {
                title += " (when "+column_name+"="+selected_values+")";
            }
            list_titles[i].text = title;
            list_titles[i].change.emit();
            //console.log(title);


        }

        // reset the selection of all other bar plots
        for (let i = 0; i < list_source_full.length; i++)
        {
            //if (list_source_full[i] != source_full){
            if (list_source_full[i].name != column_name){
                list_source_full[i].selected.indices = [];
                list_source_subset[i].selected.indices = [];
            }
        }
    
    }
    else {
    // unselecting
        //console.log("UNSELECTED");
        // check if no source is selected
        //console.log(list_source_full.map((source) => source.selected.indices.length))
        if ( list_source_full.every((source) => source.selected.indices.length === 0) )
        {
            console.log("every empty. reset.");
            for (let i = 0; i < list_source_subset.length; i++){
                var x_value = x_values[i];
                var new_y_values = [];
                for (let j = 0; j < x_value.length; j++){
                    new_y_values.push(0);
                }
                list_source_subset[i].data.y_values = new_y_values;
                list_source_subset[i].change.emit();
                list_titles[i].text = columns[i];
                list_titles[i].change.emit();

            }
        }
    }
}, 100); // end timeout
"""

print("Setting callbacks...", end="")

# list_source_full_copy = list_source_full.copy()
list_titles = [plot.title for plot in list_plot]
index = 0
for source_full in list_source_full:
    column_name = data.columns[index]

    args=dict(column_name = column_name,
             list_source_full = list_source_full.copy(),
                list_source_subset=list_source_subset,raw_data = data_cds,
                x_values = x_list, columns = data.columns, list_titles=list_titles,)

    callback_select = CustomJS(args=args, code=javascript_code)

    source_full.selected.js_on_change('indices', callback_select)
    # source_full.js_on_change('selected.indices', callback_select)
    index = index + 1
print(" Done.")




# test_plot = create_grid(list_plot)

print("Arranging plot grid...", end="")
test_plot = arrange_plots_in_grid(list_plot, num_cols=2)
test_plot = grid(test_plot)

HTML = """
    <h1>Instructions:</h1>
    <h2>1:Choose one of the plots;</h2>
    <h2>2:Click on one of the bars;</h2>
    <h2>3:Wait a few moments...</h2>
    <h2>4:The selected subset of the data should be plotted in comparison to all the data!</h2>
"""
div = Div(text=HTML,width=900, height=300)

plot = bokeh_column(div, test_plot)

print(" Done.")
print("Building Bokeh App...")
curdoc().add_root(plot)
# show(plot)

