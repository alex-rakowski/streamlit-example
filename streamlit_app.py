from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import py4DSTEM

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
    
    # Define fcc gold structure using manual input of the crystal structure
    pos = [
        [0.0, 0.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.5, 0.0, 0.5],
        [0.5, 0.5, 0.0],
    ]
    atom_num = st.slider("Atom number", 1, 100, 79)
    a = st.slider("A lattice parameter", 0.5, 12.0, 4.08)
    b = st.slider("B lattice parameter", 0.5, 12.0, 4.08)
    c = st.slider("C lattice parameter", 0.5, 12.0, 4.08)
    cell = a,b,c

    crystal = py4DSTEM.process.diffraction.Crystal(
        pos, 
        atom_num, 
        cell)
    # Plot the structure
    fig, _ = crystal.plot_structure(
        zone_axis_lattice=[5,3,1],
        figsize=(4,4),
    returnfig=True)
    st.pyplot(fig)
    
    # Calculate and plot the structure factors

    k_max = st.slider("K Max", 0.5, 10.0, 2.0)  # This is the maximum scattering vector included in the following calculations
    # k_max = 6.0

    crystal.calculate_structure_factors(k_max)

    struc_fig, _ = crystal.plot_structure_factors(
        zone_axis_lattice=[3,2,1], returnfig=True)
    st.pyplot(struc_fig)
    
