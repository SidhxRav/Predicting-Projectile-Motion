# Imports
import math as mt
import streamlit as st
from Utilities import calculations_using_velocity_and_angle,calculate_trajectory_path,calculations_with_qudratic_drag,show_outputs,show_graph,show_comparison_comparison_graph
# General Setup
st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>Predicting the trajectory of a projectile</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: grey;'>An interactive physics simulator by Sidh Raval :D</p>",
    unsafe_allow_html=True
)
#=====================
#Left side Inputs

initial_height = 0


with st.sidebar:
    st.header('Options')
    input_mode = st.radio('Input type?', ['Slider','Manual'], horizontal= True)
    col1,col2 = st.columns(2)
    with col1:
        variable_starting_height = st.toggle("Elevation?")
    with col2:
        drag_or_not = st.toggle("Air Resistance?")
    
    dt=0.001
    if drag_or_not:
        simple_or_complex_drag = st.selectbox("Options for Air resistance", ["Simple", "Advanced"])
        if drag_or_not and simple_or_complex_drag == "Advanced":
            object_preset = st.selectbox("Object type", 
                [
                "Custom",
                "Sphere (ball)",
                "Cylinder", 
                "Streamlined body",
                "Flat plate"
                ])
    else:
        simple_or_complex_drag = None
    
    gravity = st.selectbox("What Planet would you like to simulate?",['Earth', "Mars", 'Moon', 'Custom'])
    if gravity == 'Earth':
        g = -9.8
    elif gravity == "Moon":
        g = -1.62
    elif gravity == "Mars":
        g = -3.71
    else:
        g = st.number_input("Custom gravity (m/s²)", max_value= 0.0, value=-9.8, step=0.1)

    air_density = {
        "Earth": 1.225,
        "Moon":0.0,
        "Mars":0.02,
        'Custom': None,
    }
    if gravity == 'Custom':
        rho  = st.number_input("Custom air density (kg/m³)", min_value=0.0, max_value=100.0, value=1.225, step= 0.01)
    else:
        rho = air_density[gravity]
        st.markdown(f"$\\rho$ = **{rho}**")
    with st.form("Projectile_Inputs"):
        if input_mode == 'Slider':
            v = st.slider("Velocity (m/s)", 0.5, 200.0, 10.0, 0.5)
            if variable_starting_height:
                θdeg = st.slider("Angle made with surface (°)", -89.9, 89.9, 0.1, 0.1)
            else:
                θdeg = st.slider("Angle made with surface (°)", 0.1, 89.9, 0.1, 0.1)
            #Initial height Sliders
            if variable_starting_height:
                initial_height = st.slider("Elevation (m)", 0.5, 500.0, 10.0, 0.5)
            else: initial_height = 0
            #K value slider
            if drag_or_not and simple_or_complex_drag == "Simple":
                k = st.slider("Air resistance Constant", 0.0001, 0.05, 0.0003, 0.0001, format="%.4f")
            elif drag_or_not and simple_or_complex_drag == "Advanced":
                cd_presets = {
                    "Sphere (ball)": 0.47,
                    "Cylinder": 1.0,
                    "Streamlined body": 0.04,
                    "Flat plate": 1.28,
                    "Custom": None,
                }
                area_presets = {
                    "Sphere (ball)": 0.045,
                    "Cylinder": 0.03,
                    "Streamlined body": 0.01,
                    "Flat plate": 0.08,
                    "Custom": 0.045
                }
                sa = st.slider("Cross sectional area (m²)",0.001, 1.0, area_presets[object_preset], 0.001)

                mass_presets = {
                    "Sphere (ball)": 0.45,
                    "Cylinder": 1.4,
                    "Streamlined body": 2.5,
                    "Flat plate": 0.8,
                    "Custom": 0.45
                }

                m = st.slider("Mass (kg)", 0.1, 10.0, mass_presets[object_preset], 0.1)

                if object_preset == 'Custom':
                    Cd = st.slider("Drag coefficient", 0.01, 2.0, 0.47, 0.01)
                else:
                    Cd = cd_presets[object_preset]
                    st.markdown(f"$C_d$ = **{Cd}**")
                
                k = (Cd * rho * sa) / (2 * m)
                

        elif input_mode == 'Manual':
            v = st.number_input("Velocity (m/s)", min_value= 0.5, max_value= 200.0, value= 10.0, step= 0.5)
            if variable_starting_height:
                θdeg = st.number_input("Angle made with surface (°)", min_value= -89.9, max_value= 89.9, value= 0.1, step=0.1)
            else:
                θdeg = st.number_input("Angle made with surface (°)", min_value= 0.1, max_value= 89.9, value= 0.1, step=0.1)
            if variable_starting_height:
                initial_height = st.number_input("Elevation (m)", min_value=0.5, max_value=500.0, value= 10.0, step = 0.5)
            else: initial_height = 0
            #K value number input
            if drag_or_not and simple_or_complex_drag == "Simple":
                k = st.number_input("Air resistance Constant", min_value=0.0001, max_value=0.05, value=0.0001, step= 0.0001, format="%.4f")
            elif drag_or_not and simple_or_complex_drag == "Advanced":
                cd_presets = {
                    "Sphere (ball)": 0.47,
                    "Cylinder": 1.0,
                    "Streamlined body": 0.04,
                    "Flat plate": 1.28,
                    "Custom": None,
                }
                area_presets = {
                    "Sphere (ball)": 0.045,
                    "Cylinder": 0.03,
                    "Streamlined body": 0.01,
                    "Flat plate": 0.08,
                    "Custom": 0.045
                }
                sa = st.number_input("Cross sectional area (m²)",min_value=0.001, max_value=1.0, value=area_presets[object_preset], step=0.001)

                mass_presets = {
                    "Sphere (ball)": 0.45,
                    "Cylinder": 1.4,
                    "Streamlined body": 2.5,
                    "Flat plate": 0.8,
                    "Custom": 0.45
                }

                m = st.number_input("Mass (kg)", min_value=0.1, max_value=10.0, value=mass_presets[object_preset], step=0.1)

                if object_preset == 'Custom':
                    Cd = st.number_input("Drag coefficient", min_value=0.01, max_value=2.0, value=0.47, step=0.01)
                else:
                    Cd = cd_presets[object_preset]
                    st.markdown(f"$C_d$ = **{Cd}**")
                
                k = (Cd * rho * sa) / (2 * m)
                        
        calculate = st.form_submit_button("Calculate")
    if drag_or_not:
        compare_drag = st.checkbox("Compare quadratic, linear and no drag")
    else:
        compare_drag = False



θrad = mt.radians(θdeg)
#=====================          
# Run Rest of Program
if calculate:
    if drag_or_not:
        vx, vy, t_normal, _, _ = calculations_using_velocity_and_angle(v,θrad,g, initial_height, variable_starting_height)
        x_pos_values_normal, y_pos_values_normal, t_values_normal = calculate_trajectory_path(vy, vx, t_normal, dt, g, initial_height)
        x_pos_values_quad, y_pos_values_quad, t_values_quad= calculations_with_qudratic_drag(v,θrad,g, initial_height, k, dt)
        d = max(x_pos_values_quad)
        s = max(y_pos_values_quad)
        t_quad = max(t_values_quad)
        if compare_drag:
            show_comparison_comparison_graph(x_pos_values_quad,y_pos_values_quad,t_values_quad,x_pos_values_normal,y_pos_values_normal,t_values_normal,θrad,θdeg, initial_height)
        else:
            show_graph(x_pos_values_quad, y_pos_values_quad, t_values_quad,θrad,θdeg, initial_height)
        show_outputs(t_quad,g,d,s,k,gravity)
    else:
        vx,vy,t,d,s = calculations_using_velocity_and_angle(v,θrad,g, initial_height, variable_starting_height)
        x_pos_values, y_pos_values, t_values = calculate_trajectory_path(vy, vx, t, dt, g, initial_height)
        show_graph(x_pos_values, y_pos_values, t_values,θrad,θdeg, initial_height)
        show_outputs(t,g,d,s,0, gravity)
        


