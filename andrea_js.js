callback_select = CustomJS(args=dict(s1=s1, list_s1 = list_s1.copy(), list_s2=list_s2,raw_data = data.to_json(),column_name = column_name, x_values = x_list, columns = data.columns), code="""
// get selected indices and length
const selected_indices = s1.selected.indices;
let length_indices = s1.selected.indices.length;

if (length_indices > 0) {
    // transform raw data
    var data = JSON.parse(raw_data);
    var selected_values = [];

    // reset the selection of all other bar plots
    for (let i = 0; i < list_s1.length; i++) {
            if (list_s1[i] != s1){
                list_s1[i].selected.indices = [];
            }
            // transform the indices to the corresponding x_value
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
    console.log(filtered_rows);
    // for the selected rows, filter the values corresponding updating bar plot
    for (let i = 0; i < list_s1.length; i++){
        if (list_s1[i] != s1){
            var x_value = x_values[i];
            // get the column of target bar plot
            var column_data = data[columns[i]];
            // filter the column
            var final_data = [];
            for (let j = 0; j < filtered_rows.length; j++){
                final_data.push(column_data[filtered_rows[j]]);
            }
            console.log(final_data);
            
            for (let j = 0; j < x_value.length; j++){
                // count the frequency
            }
        }
    }
}

else {
}
""")