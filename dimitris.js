const selected_indices = source_all.selected.indices;

    // Clear comparison data for all plots
    for (const key in plot_dict) {{
        plot_dict[key].source_compare.data = {{x_values: [], y_values: []}};
    }}

    if (selected_indices.length === 0) {{
        // If no selection, return early
        for (const key in plot_dict) {{
            plot_dict[key].source_compare.change.emit();
        }}
        return;
    }}

    const index = selected_indices[0]; // Get the first selected index
    const attribute = source_all.data['x_values'][index]; // Get the selected attribute

    // Initialize new y_values for each plot in plot_dict
    for (const key in plot_dict) {{
        const new_y_values = {{x_values: [], y_values: []}};
        const categories = plot_dict[key].source_all.data['x_values'];
        const all_data = glob_dict[key]; // Access the glob_dict data

        // Calculate the new counts based on the selected attribute
        for (let i = 0; i < all_data.y_values.length; i++) {{
            if (all_data.x_values[i] === attribute) {{
                const category = all_data.x_values[i]; // Assuming the same column for comparison
                const idx = new_y_values['x_values'].indexOf(category);
                if (idx === -1) {{
                    new_y_values['x_values'].push(category);
                    new_y_values['y_values'].push(1);
                }} else {{
                    new_y_values['y_values'][idx] += 1;
                }}
            }}
        }}

        // Update the comparison source with the new data
        plot_dict[key].source_compare.data = new_y_values;
        plot_dict[key].source_compare.change.emit(); // Notify changes
    }}