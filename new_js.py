# We do the basic setup here.
# Do not (!) change this cell! All changes will be reset during grading!

# numpy and pandas
import numpy as np
import pandas as pd
import math

# We import a range of bokeh functionality that will likely be needed already
# if you need more, import it at the top of the corresponding cell
from bokeh.plotting import figure, gridplot, show
from bokeh.layouts import grid
from bokeh.layouts import column as bokeh_column
from bokeh.transform import factor_cmap, linear_cmap
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, BasicTicker, PrintfTickFormatter, CustomJS, Select, axes
from bokeh.models.widgets import Div
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
    list_plot = []
    list_source = []
    columns = data.columns.tolist()
    for column in columns:
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
            p = figure(height=600, width=600, title=column.title(), toolbar_location="above", tools="tap,pan,wheel_zoom,box_zoom,reset")
            p.xaxis.formatter = NumeralTickFormatter(format="0,0")
        else:
            frequency_plot = {'x_values': categories, 'y_values': counts}
            p = figure(x_range=categories,height=600, width=600, title=column.title(), toolbar_location="above", tools="tap,pan,wheel_zoom,box_zoom,reset")
        list_plot.append(p)
    return list_plot,list_source
    
list_plot,list_source = create_bar_plot(data)
# print(data.columns)
# print(glob_dict)
# print(x_list)
# print(data)

index = 0
list_source_full = []
list_source_subset = []
for p,source in zip(list_plot,list_source):
    new_source = dict(x_values = source['x_values'],y_values=[0 for i in source['y_values'] ])
    source_full = ColumnDataSource(source)
    list_source_full.append(source_full)
    source_subset = ColumnDataSource(new_source)
    list_source_subset.append(source_subset)
    p.vbar(x='x_values', top='y_values', width=0.5, source=source_full, line_color='lightblue', fill_color='lightblue', line_width=2.5)
    p.vbar(x='x_values', top='y_values', width=0.5, source=source_subset, line_color='lightgreen', fill_color='lightgreen', line_width=2.5)
    # # Add hover tool to display values on hover
    hover = HoverTool()
    hover.tooltips = [(data.columns[index], "@x_values"), ("Count", "@y_values")]
    p.add_tools(hover)
    # Add the TapTool and link it to the callback
    # Format the y-axis with commas as well
    p.xaxis.major_label_orientation = 1.0

index = 0
data_json = data.to_json()


for source_full in list_source_full:
    column_name = data.columns[index]
    list_titles = [plot.title for plot in list_plot]
    callback_select = CustomJS(args=dict(source_full=source_full, list_source_full = list_source_full.copy(),
                                         list_source_subset=list_source_subset,raw_data = data_json,
                                         column_name = column_name, x_values = x_list, columns = data.columns,
                                         list_titles=list_titles), code="""
        
    list_titles.forEach((title) => title.text = "Loading...");

    setTimeout(function() { // timeout so browser doesnt get stuck doing the calculations

        // keep titles dynamic while stuff is loading
        //let dots = 0;  // Counter to track how many dots have been added
        //const maxDots = 3;  // Maximum number of dots
        //const intervalId = setInterval(function() {
        //    dots = (dots + 1) % (maxDots + 1);  // Cycle between 0 to maxDots
        //    //plotTitle.innerText = "Loading" + ".".repeat(dots);  // Update title with dots
        //    list_titles.forEach((title) => title.text = "Loading" + ".".repeat(dots));
        //}, 10);  // Update every 100ms    


        // get selected indices and length
        const selected_indices = source_full.selected.indices;
        let length_indices = source_full.selected.indices.length;
        if (length_indices > 0) {
            // transform raw data
            var data = JSON.parse(raw_data);
            console.log(data);
            var selected_values = [];
            
             // reset the selection of all other bar plots
            for (let i = 0; i < list_source_full.length; i++) {
                if (list_source_full[i] != source_full){
                //#     //# list_source_full[i].selected.indices = [];
                //#     //# list_source_subset[i].selected.indices = [];
                }
                // transform the indices to the corresponding x_values
                else{
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
            // titles are updating, stop loading stuff
            //clearInterval(intervalId);

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
                list_titles[i].text = columns[i]+" (when "+column_name+"="+selected_values+")";

                // update title
                //console.log(columns);

            }

            // reset the selection of all other bar plots
            for (let i = 0; i < list_source_full.length; i++) {
                if (list_source_full[i] != source_full){
                    list_source_full[i].selected.indices = [];
                    list_source_subset[i].selected.indices = [];
                }
                // transform the indices to the corresponding x_values
                else{
                    var x_value = x_values[i];
                    for (let j = 0; j < length_indices; j++){
                        selected_values.push(x_value[selected_indices[j]]);
                    }
                }
            }
        }
        
        else {
        // unselecting
            console.log("UNSELECTED");
            // check if no source is selected
            console.log(list_source_full.map((source) => source.selected.indices.length))
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
                }
            }


        }
    }, 100); // end timeout


    // restore names
    //# let original_list_titles_text = list_titles.map((title) => title.text); 
    //# list_titles.forEach((title) => title.text = "Loading");
    //# for(let i = 0; i < list_titles.length; i++)
    //# {
    //#     list_titles[i].text = original_list_titles_text[i] + " when
    //# }
    """)
    source_full.selected.js_on_change('indices', callback_select)
    index = index + 1


# test_plot = create_grid(list_plot)
test_plot = arrange_plots_in_grid(list_plot)
test_plot = grid(test_plot)

HTML = """
        <h1>Instructions:</h1>
        <h2>1:Choose one of the plots;</h2>
        <h2>2:Click on one of the bars;</h2>
        <h2>3:Wait a few moments...</h2>
        <h2>4:The selected subset of the data should be plotted in comparison to all the data!</h2>
"""
div = Div(text=HTML,
width=900, height=300)

plot = bokeh_column(div, test_plot)

# show(test_plot)
curdoc().add_root(plot)
