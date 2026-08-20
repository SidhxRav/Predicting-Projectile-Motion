import streamlit as st
import math as mt
import plotly.graph_objects as go

def Runge_Kutta_4 (accel,velo,dt):
    f1 = accel
    f2 = accel + (dt/2)*f1)
    f3 = accel+(dt/2)*f2
    f4 = accel + (dt)*f3

    return velo + (dt/6)*(f1+2*f2+2*f3+f4)

def calculations_using_velocity_and_angle(v,θ,g, initial_height, variable_starting_height):
    vy = v * mt.sin(θ)
    vx = v * mt.cos(θ)


    discriminant = vy**2 - 2*g*initial_height

    if variable_starting_height:
        t1 = (-vy + mt.sqrt(discriminant))/g
        t2 = (-vy - mt.sqrt(discriminant))/g
        t = max(t1,t2)
        d = vx*t
        s = (-(vy**2))/(2*g) + initial_height
    else:
        t = (2*(-vy))/g
        d = vx*t
        s = (-(vy**2))/(2*g)
    

    return vx, vy, t, d, s
def calculate_trajectory_path(vy, vx, t, dt, g, initial_height):
    independent_t = 0

    x_pos_values = []

    y_pos_values = []

    t_values = []
  
    while independent_t <= t:
        x_pos = vx * independent_t
        y_pos = vy * independent_t + 0.5 * g * (independent_t**2) + initial_height

        x_pos_values.append(x_pos)
        y_pos_values.append(y_pos)
        t_values.append(independent_t)
        independent_t += dt
    return x_pos_values, y_pos_values, t_values
def calculations_with_qudratic_drag(v,theta,g,initial_height,k,dt):
    vx = v * mt.cos(theta)
    vy = v * mt.sin(theta)
    y = initial_height
    x=0
    t=0
    x_pos_values = []
    y_pos_values = []
    t_values = []

    #append initial values
    x_pos_values.append(x)
    y_pos_values.append(y)
    t_values.append(t)
    while y >=0 and t <1000:
        absolute_v = mt.sqrt(vx**2 + vy**2)
        #Calculate the acceleration in the opposite direction to the velocity due to drag
        ax = -k * absolute_v * vx
        ay = g - k * absolute_v * vy
        #Update the values of the velocites
        Runge_Kutta_4(ax,vx,dt)
        Runge_Kutta_4(ay,vy,dt)
        vy += ay * dt
        if vx < 0:
            vx = 0
        #update the position based on velocities
        x += vx*dt
        y += vy*dt  
        t += dt

        x_pos_values.append(x)
        y_pos_values.append(y)
        t_values.append(t)
    return x_pos_values, y_pos_values, t_values
#====================================
#Outputs
def show_outputs(t, g, d, s, k, gravity):
    st.divider()
    st.header("Results")
    col1,col2,col3,col4 = st.columns(4)
# Display Findings
    with col1:
        st.metric("Gravity (m/s²):", f"{g:.2f}")
    with col2:
        st.metric("Time taken to contact the ground (s):", f"{t:.2f}")
    with col3:
        st.metric("Distance travelled horizontally (m):", f"{d:.2f}")
    with col4:
        st.metric("Max height reached (m):", f"{s:.2f}")
    if k > 0:
        st.markdown(r"$k = \dfrac{C_d \rho A}{2m}$")
        st.metric(f"k :", f"{k:.6f}")

    if t < 0.01:
        st.warning ("If numbers appear zero, they are NOT, they are most likely just very small and hence negligable")

    if gravity != "Custom":
        st.write(f"Selected planet/body: **{gravity}**")
#====================================================
#Graphing
def show_graph(x_pos_values, y_pos_values,t_values, θrad, θdeg, initial_height):
    st.header("Trajectory")

    fig = go.Figure()
    
    #Create the trajectory
    fig.add_trace(go.Scatter(x = x_pos_values, y = y_pos_values, mode='lines', line= dict(dash="dot", width= 3),customdata= t_values , hovertemplate= "Distance: %{x:.2f} m<br>" + "Height: %{y:.2f} m<br>" + "Time: %{customdata:.2f} s" ,name= 'Trajectory'))

    #Display angle
    #horizontal reference line
    ref_len = max(x_pos_values) * 0.08
    fig.add_shape(type="line", x0=0, y0=initial_height, x1=ref_len, y1=initial_height, line = dict(width = 2, dash = "dot", color= "red"))

    #vertical reference line
    launch_len = ref_len
    fig.add_shape(type="line", x0=0, y0=initial_height, x1=launch_len * mt.cos(θrad), y1=launch_len* mt.sin(θrad) + initial_height, line = dict(width=2, dash = 'dot', color="red"))

    #set up values for the angle projection
    arc_r = ref_len * 0.6
    arc_x = []
    arc_y = []
    steps = 30

    for i in range(steps+1):
        a = θrad * i /steps
        arc_x.append(arc_r * mt.cos(a))
        arc_y.append(arc_r * mt.sin(a) + initial_height)
    
    #project angle
    fig.add_trace(go.Scatter(x = arc_x, y = arc_y, mode = 'lines', hoverinfo="skip", showlegend=False, line= dict(color="red", dash = 'dot')))

    #Angle annotation
    mid_angle = θrad
    label_r = arc_r * 1.35
    fig.add_annotation(x = label_r * mt.cos(mid_angle) * 2, y = label_r * mt.sin(mid_angle) * 0.5 + initial_height, text=f"θ = {θdeg:.1f}°", showarrow=False)


    
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor = ('rgba(0,0,0,0)'),margin = dict(l=20, r=20, t=20, b=20),xaxis= dict(title='Horizontal Distance (m)', showgrid = False, zeroline= False), showlegend=False, yaxis=dict(scaleanchor="x",scaleratio=1, title= 'Height (m)', showgrid = False))
    st.plotly_chart(fig, use_container_width=True)

def show_comparison_comparison_graph(x_pos_values, y_pos_values,t_values,x_pos_values2, y_pos_values2,t_values2, θrad, θdeg, initial_height):
    st.header("Trajectory")

    fig = go.Figure()
    
    #Create the trajectorys
    fig.add_trace(go.Scatter(x = x_pos_values, y = y_pos_values, mode='lines', line= dict(dash="dot", width= 3, color= "cyan"),customdata= t_values , hovertemplate= "Distance: %{x:.2f} m<br>" + "Height: %{y:.2f} m<br>" + "Time: %{customdata:.2f} s" ,name= 'With Air Resistance'))
    fig.add_trace(go.Scatter(x = x_pos_values2, y = y_pos_values2, mode='lines', line= dict(dash="dot", width= 3, color= "green"),customdata= t_values2 , hovertemplate= "Distance: %{x:.2f} m<br>" + "Height: %{y:.2f} m<br>" + "Time: %{customdata:.2f} s" ,name= 'No Air resistance'))
    #Display angle
    #horizontal reference line
    ref_len = max(x_pos_values) * 0.08
    fig.add_shape(type="line", x0=0, y0=initial_height, x1=ref_len, y1=initial_height, line = dict(width = 2, dash = "dot", color= "red"))

    #vertical reference line
    launch_len = ref_len
    fig.add_shape(type="line", x0=0, y0=initial_height, x1=launch_len * mt.cos(θrad), y1=launch_len* mt.sin(θrad) + initial_height, line = dict(width=2, dash = 'dot', color="red"))

    #set up values for the angle projection
    arc_r = ref_len * 0.6
    arc_x = []
    arc_y = []
    steps = 30

    for i in range(steps+1):
        a = θrad * i /steps
        arc_x.append(arc_r * mt.cos(a))
        arc_y.append(arc_r * mt.sin(a) + initial_height)
    
    #project angle
    fig.add_trace(go.Scatter(x = arc_x, y = arc_y, mode = 'lines', hoverinfo="skip", showlegend=False, line= dict(color="red", dash = 'dot')))

    #Angle annotation
    mid_angle = θrad
    label_r = arc_r * 1.35
    fig.add_annotation(x = label_r * mt.cos(mid_angle) * 2, y = label_r * mt.sin(mid_angle) * 0.5 + initial_height, text=f"θ = {θdeg:.1f}°", showarrow=False)


    
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor = ('rgba(0,0,0,0)'),margin = dict(l=20, r=20, t=20, b=20),xaxis= dict(title='Horizontal Distance (m)', showgrid = False, zeroline= False), showlegend=True, yaxis=dict(scaleanchor="x",scaleratio=1, title= 'Height (m)', showgrid = False))
    st.plotly_chart(fig, use_container_width=True)
#===================================================
