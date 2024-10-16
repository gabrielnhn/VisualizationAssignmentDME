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
def create_bar_plot(data_original, clean = True):
    
    output_plots_dict = {}
    output_plots = []
    columns = data.columns.tolist()
    for column in columns:
        # replace '?' by NAN values
        column_data = data[column].replace("?", np.nan).dropna()
        # print(column_data)
        # numerical columns
        if pd.api.types.is_numeric_dtype(column_data):
            sorted_counts = column_data.value_counts().sort_index()
            index = sorted_counts.index.tolist()
            counts = sorted_counts.values.tolist()  
            # print(index[0:30],counts[0:30])
        #categorical columns
        else:
            print(column_data)
            column_data = column_data.apply(lambda sal: sal.strip('.'))

            categories = column_data.value_counts().index.tolist()
            
            counts = column_data.value_counts().values.tolist()
            # print(categories[0:30],counts[0:30])

        if pd.api.types.is_numeric_dtype(column_data):
            frequency_plot = {'x_values': index, 'y_values': counts}
            p = figure(height=600, width=600, title=column.title(), toolbar_location=None, tools="pan,wheel_zoom,box_zoom,reset,tap")
            p.xaxis.formatter = NumeralTickFormatter(format="0,0")
        else:
            frequency_plot = {'x_values': categories, 'y_values': counts}
            p = figure(x_range=categories,height=600, width=600, title=column.title(), toolbar_location=None, tools="pan,wheel_zoom,box_zoom,reset,tap")


        source = ColumnDataSource(frequency_plot)
        p.vbar(x='x_values', top='y_values', width=0.5, source=source, line_color='lightblue', fill_color='lightblue', line_width=2.5)
        # Add hover tool to display values on hover
        hover = HoverTool()
        hover.tooltips = [(column.title(), "@x_values"), ("Count", "@y_values")]
        p.add_tools(hover)


        # Format the y-axis with commas as well
        # p.yaxis.formatter = NumeralTickFormatter(format="0,0",use_scientific = False)
        p.xaxis.major_label_orientation = 1.0

        output_plots_dict[column] = p, source
        output_plots.append(p)
        # show(p)

    print(output_plots)
    return output_plots, output_plots_dict


from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, TapTool, CustomJS
from bokeh.layouts import gridplot
from bokeh.io import output_notebook

# output_notebook()

# Example Data
import pandas as pd
import numpy as np

# data = pd.DataFrame({
#     'Education': np.random.choice(['Bachelors', 'Masters', 'PhD'], size=10),
#     'Income': np.random.choice(['<=50K', '>50K'], size=10),
#     'Age': np.random.randint(18, 21, size=10)
# })

# glob_dict = {}
# for column in data.columns:
#     test = data[column].value_counts()
#     index = test.index.tolist()
#     counts = test.values.tolist()
#     dict_education = dict(x_values=index, y_values=counts)
#     source_education = ColumnDataSource(dict_education)
#     glob_dict[column] = dict_education
# print(glob_dict)

# test = data['Education'].value_counts()
# index = test.index.tolist()
# counts = test.values.tolist()
# counts_divided = (test.values/3).tolist()

# test = data['Age'].value_counts()
# index_age = test.index.tolist()
# counts_age = test.values.tolist()

# # dict_education = dict(x_values=index, y_values=counts)
# dict_education = dict(x_values=index, y_values=counts)
# dict_education_divided = dict(x_values=index, y_values=counts_divided)
# # print(dict_education)

# source_education = ColumnDataSource(dict_education)
# source_education_divided = ColumnDataSource(dict_education_divided)

# # print(source_education)


# views = {}
# views_dict = {}
# for id, item in enumerate(zip(index, counts)):
# # for id, item in enumerate(zip(index_age, counts_age)):
#     x, y = item

#     # views[id] = ColumnDataSource(dataframe_result)
#     views_dict[id] = dict(x_values=[x], y_values=[y])
#     views[id] = ColumnDataSource(dict(x_values=[x], y_values=[y]))





# cur_view = ColumnDataSource(dict())
# cur_fraction = ColumnDataSource(dict())
# empty = ColumnDataSource(dict())

# # source_income = original_income_data

# # Create the first plot (Education Bar Chart)
# p1 = figure(x_range=index, height=400, width=600, title="Source", toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset,tap")
# p1.vbar(x='x_values', top='y_values', width=0.5, source=source_education, line_color='lightblue', fill_color='lightblue', line_width=2.5)
# p1.vbar(x='x_values', top='y_values', width=0.5, source=cur_fraction, line_color='red', fill_color='red', line_width=2.5)

# # Create the second plot (Income Bar Chart)
# p2 = figure(x_range=index, height=400, width=600, title="View", toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset")
# p2.vbar(x='x_values', top='y_values', width=0.5, source=cur_view, line_color='lightblue', fill_color='lightblue', line_width=2.5)

# p3 = figure(x_range=index, height=400, width=600, title="Source", toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset,tap")
# p3.vbar(x='x_values', top='y_values', width=0.5, source=source_education, line_color='lightblue', fill_color='lightblue', line_width=2.5)


# # Add hover tools to both plots
# hover1 = HoverTool()
# hover1.tooltips = [("Education", "@x_values"), ("Count", "@y_values")]
# p1.add_tools(hover1)

# hover2 = HoverTool()
# hover2.tooltips = [("Income", "@x_values"), ("Count", "@y_values")]
# p2.add_tools(hover2)

# JavaScript callback for selection and deselection
# callback = CustomJS(args=dict(source_education=source_education, source_income=source_income, data=data), code="""
#     var indices = source_education.selected.indices;
#     console.log("Hello world!");
#     // If a bar is selected
#     if (indices.length > 0) {
#         var selected_index = indices[0];  // Get the first selected index
#         var selected_education = source_education.data['x_values'][selected_index];
        
#         // Filter the data to update the Income plot
#         var filtered_data = data.filter(row => row['Education'] === selected_education);
#         console.log(filtered_data);
#         console.log(data);

#     }
# """)

callback_code = """
    console.log("Callback call");
    var indices = source_education.selected.indices;

    if (indices.length > 0) {
        var index = indices[0];
        cur_view.data = views.get(index).data;
        cur_fraction.data = source_education_divided.data;
        cur_fraction.selected.indices = indices;

    }
    else
    {
        console.log("ASSERT FAILED");
        cur_fraction.data = empty.data;
    }
    //console.log(source_education.selected.indices.length);
    //console.log("views");
    //console.log(views);
    //console.log("index");
    //console.log(index);
    //console.log("divided");
    //console.log(source_education_divided);
"""

# callback = CustomJS(args=dict(cur_view=cur_view, views=views,
#                                                       source_education=source_education,
#                                                       source_education_divided=source_education_divided,
#                                                       cur_fraction=cur_fraction,
#                                                       empty=empty), code=callback_code)

# Add the callback to the first plot
# p1.select(type=TapTool).callback =  callback
# p1.select(type=TapTool).js_on_change("indices", callback)


# source_education.selected.js_on_change("indices", callback)

class custom_callbacks:
    def __init__(self, feature =None, source=None, figure=None):
        self.feature = feature
        self.source = source
        self.figure = figure

    def default_function(self, attr, old, new):
        # print(f"CALLBACK FOR {self.param.__name__}")
        print("\t")
        # print(attr, new)
        # print()
        if new:
            index = new[0]
            pass
        else:
            index = None

        print(f"CALLBACK in feature `{self.feature}`, {self.source} IN PLOT {self.figure}, INDEX {index}")
            # cur_view.data = views[new[0]].data
            # cur_view.data = views_dict[new[0]]



grid_list, plot_dict = create_bar_plot(data)



for column, (plot, source) in plot_dict.items():
    source.selected.on_change("indices", custom_callbacks(column, source, plot).default_function)



# source_education.selected.on_change("indices", python_callback)
# source_education.selected.on_change("indices", custom_callbacks(source_education, p1).default_function)


# p3.select(type=TapTool).callback = python_callback


# Display the plots in a grid
# grid = gridplot([[p1, p2], [p3]])
grid = gridplot(arrange_plots_in_grid(grid_list))

# grid = grid_list[0]
# show(grid)
curdoc().add_root(grid)

