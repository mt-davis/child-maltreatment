import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import folium
from streamlit_folium import st_folium

def create_line_chart(data, x_col, y_col, title, color="#3498db", point=True):
    """Create an interactive line chart using Altair."""
    chart = alt.Chart(data).mark_line(point=point).encode(
        x=alt.X(f"{x_col}:O", title=x_col),
        y=alt.Y(f"{y_col}:Q", title=y_col),
        tooltip=[x_col, y_col]
    ).properties(
        title=title
    ).interactive()
    
    if color:
        chart = chart.configure_mark(color=color)
    
    return chart

def create_multi_line_chart(data, x_col, y_cols, title, colors=None):
    """Create a multi-line chart with multiple y variables."""
    if not colors:
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
    
    # Melt the dataframe to get it in the right format for Altair
    id_vars = [x_col]
    melted_df = pd.melt(data, id_vars=id_vars, value_vars=y_cols, 
                        var_name='Metric', value_name='Value')
    
    # Create the chart
    chart = alt.Chart(melted_df).mark_line(point=True).encode(
        x=alt.X(f"{x_col}:O", title=x_col),
        y=alt.Y("Value:Q", title="Value"),
        color=alt.Color("Metric:N", scale=alt.Scale(range=colors[:len(y_cols)])),
        tooltip=[x_col, "Metric", "Value"]
    ).properties(
        title=title
    ).interactive()
    
    return chart

def create_bar_chart(data, x_col, y_col, title, color="#3498db", sort=True):
    """Create an interactive bar chart using Altair."""
    if sort:
        sort_order = alt.SortField(field=y_col, order="descending")
    else:
        sort_order = None
    
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f"{x_col}:N", title=x_col, sort=sort_order),
        y=alt.Y(f"{y_col}:Q", title=y_col),
        tooltip=[x_col, y_col]
    ).properties(
        title=title
    ).interactive()
    
    if color:
        chart = chart.configure_mark(color=color)
    
    return chart

def create_stacked_bar_chart(data, x_col, y_col, color_col, title):
    """Create a stacked bar chart."""
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f"{x_col}:N", title=x_col),
        y=alt.Y(f"{y_col}:Q", title=y_col),
        color=alt.Color(f"{color_col}:N"),
        tooltip=[x_col, y_col, color_col]
    ).properties(
        title=title
    ).interactive()
    
    return chart

def create_heatmap(data, x_col, y_col, value_col, title):
    """Create a heatmap using Altair."""
    chart = alt.Chart(data).mark_rect().encode(
        x=alt.X(f"{x_col}:O", title=x_col),
        y=alt.Y(f"{y_col}:O", title=y_col),
        color=alt.Color(f"{value_col}:Q", scale=alt.Scale(scheme="blues")),
        tooltip=[x_col, y_col, value_col]
    ).properties(
        title=title
    ).interactive()
    
    return chart

def create_pie_chart(data, names_col, values_col, title):
    """Create a pie chart using Matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(data[values_col], labels=data[names_col], autopct='%1.1f%%', 
           startangle=90, shadow=False)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(title)
    
    return fig

def create_donut_chart(data, names_col, values_col, title, center_text=None):
    """Create a donut chart using Matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create a color palette
    colors = plt.cm.Blues(np.linspace(0.2, 0.7, len(data)))
    
    # Draw the pie chart
    wedges, texts, autotexts = ax.pie(
        data[values_col], 
        labels=data[names_col], 
        autopct='%1.1f%%',
        colors=colors,
        wedgeprops=dict(width=0.5, edgecolor='w'),
        textprops=dict(color="black")
    )
    
    # Add a circle at the center to turn the pie chart into a donut
    centre_circle = plt.Circle((0, 0), 0.35, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Add text in the center if provided
    if center_text:
        ax.text(0, 0, center_text, ha='center', va='center', fontsize=12)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    plt.title(title)
    
    return fig

def create_choropleth_map(data, state_col, value_col, title, colorscale="Blues"):
    """Create a US state choropleth map using Folium."""
    # Initialize the map centered on US
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    
    # Add the choropleth layer
    folium.Choropleth(
        geo_data="https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json",
        name="choropleth",
        data=data,
        columns=[state_col, value_col],
        key_on="feature.properties.name",
        fill_color=colorscale,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=value_col
    ).add_to(m)
    
    # Add tooltips
    folium.LayerControl().add_to(m)
    
    return m

def create_interactive_map(df, lat_col, lon_col, popup_cols, title, zoom_start=4):
    """Create an interactive map with markers and popups."""
    # Initialize the map centered on data points
    mean_lat = df[lat_col].mean()
    mean_lon = df[lon_col].mean()
    m = folium.Map(location=[mean_lat, mean_lon], zoom_start=zoom_start)
    
    # Add markers with popups
    for idx, row in df.iterrows():
        lat = row[lat_col]
        lon = row[lon_col]
        
        # Create popup content from specified columns
        popup_content = "<strong>{}:</strong>".format(row.get('State', 'Location'))
        for col in popup_cols:
            if col in row:
                popup_content += "<br>{}: {}".format(col, row[col])
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(m)
    
    return m

def create_area_chart(data, x_col, y_col, title, color="#3498db"):
    """Create an area chart using Altair."""
    chart = alt.Chart(data).mark_area(
        line={'color': color},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color=color, offset=0),
                   alt.GradientStop(color='white', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        x=alt.X(f"{x_col}:O", title=x_col),
        y=alt.Y(f"{y_col}:Q", title=y_col),
        tooltip=[x_col, y_col]
    ).properties(
        title=title
    ).interactive()
    
    return chart

def create_stacked_area_chart(data, x_col, y_cols, color_col, title):
    """Create a stacked area chart for multiple metrics."""
    # Melt the dataframe for Altair
    id_vars = [x_col]
    melted_df = pd.melt(data, id_vars=id_vars, value_vars=y_cols, 
                       var_name=color_col, value_name='Value')
    
    # Create the chart
    chart = alt.Chart(melted_df).mark_area().encode(
        x=alt.X(f"{x_col}:O", title=x_col),
        y=alt.Y("Value:Q", title="Value", stack=True),
        color=alt.Color(f"{color_col}:N"),
        tooltip=[x_col, color_col, "Value"]
    ).properties(
        title=title
    ).interactive()
    
    return chart

def create_bubble_chart(data, x_col, y_col, size_col, color_col, title):
    """Create a bubble chart with Altair."""
    chart = alt.Chart(data).mark_circle(opacity=0.7).encode(
        x=alt.X(f"{x_col}:Q", title=x_col),
        y=alt.Y(f"{y_col}:Q", title=y_col),
        size=alt.Size(f"{size_col}:Q", scale=alt.Scale(range=[100, 2000])),
        color=alt.Color(f"{color_col}:N"),
        tooltip=[x_col, y_col, size_col, color_col]
    ).properties(
        title=title
    ).interactive()
    
    return chart

def create_gauges(value, max_value, title, color_scheme="blues"):
    """Create a gauge visualization."""
    # Calculate percentage
    pct = (value / max_value) * 100
    
    # Create gauge figure with Matplotlib
    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(polar=True))
    
    # Customize colors based on value
    if color_scheme == "blues":
        color = plt.cm.Blues(pct / 100)
    elif color_scheme == "reds":
        color = plt.cm.Reds(pct / 100)
    elif color_scheme == "greens":
        color = plt.cm.Greens(pct / 100)
    else:
        color = plt.cm.Blues(pct / 100)
    
    # Background ring (empty part)
    ax.barh(0, 100, height=0.6, color="lightgray", alpha=0.3)
    
    # Value ring
    ax.barh(0, pct, height=0.6, color=color)
    
    # Set the compass points
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2])
    ax.set_xticklabels(['0%', '25%', '50%', '75%'])
    
    # Remove y-axis ticks
    ax.set_yticks([])
    
    # Set limits and aspect ratio
    ax.set_ylim(-1.5, 1.5)
    ax.set_title(title)
    
    # Add value text in center
    ax.text(0, -0.8, f"{value}/{max_value}\n({pct:.1f}%)", ha="center", va="center", fontsize=12)
    
    # Set the circumference to only show the top half
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    
    return fig

def create_comparison_chart(data, category_col, value_col, compare_col, title):
    """
    Create a chart comparing two groups of data.
    For example, comparing victim rates across different demographics.
    """
    # Sort the data based on the value column
    sorted_data = data.sort_values(by=value_col)
    
    chart = alt.Chart(sorted_data).mark_bar().encode(
        x=alt.X(f"{value_col}:Q", title=value_col),
        y=alt.Y(f"{category_col}:N", title=category_col, sort="-x"),
        color=alt.Color(f"{compare_col}:N"),
        tooltip=[category_col, value_col, compare_col]
    ).properties(
        title=title
    ).interactive()
    
    return chart

def create_waffle_chart(value, max_value, title, rows=10, cols=10, icon="▣"):
    """Create a waffle chart to visually represent proportions."""
    # Calculate how many squares to fill
    total_squares = rows * cols
    filled_squares = int(round(total_squares * (value / max_value)))
    
    # Create HTML for the waffle chart
    waffle_html = f"<h4>{title}: {value}/{max_value} ({value/max_value:.1%})</h4>"
    waffle_html += "<div style='display: grid; grid-template-columns: repeat({}, 1fr); gap: 2px; width: 100%;'>".format(cols)
    
    for i in range(total_squares):
        if i < filled_squares:
            # Filled square
            waffle_html += f"<div style='aspect-ratio: 1; background-color: #3498db; display: flex; align-items: center; justify-content: center; color: white;'>{icon}</div>"
        else:
            # Empty square
            waffle_html += f"<div style='aspect-ratio: 1; background-color: #eaecee; display: flex; align-items: center; justify-content: center; color: #bdc3c7;'>{icon}</div>"
    
    waffle_html += "</div>"
    
    return waffle_html