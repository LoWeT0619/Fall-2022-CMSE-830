
#######################
##                   ##
##  ICA: RBF-NN App  ##
##  CMSE 830         ##
##  12 & 14 Oct 2022 ##
##                   ##
#######################


# import libraries
import streamlit as st
import seaborn as sns
import pandas as pd
import altair as alt
import numpy as np

# get data
df = pd.read_csv('https://raw.githubusercontent.com/LoWeT0619/Fall-2022-CMSE-830/main/PB_data.csv')
# st.write(df)

labels = df.select_dtypes(include=['float64', 'int64']).columns  # feel free to change this
# st.write(labels)


#######################
## streamlit sidebar ##
#######################

st.sidebar.title("""
# Regression
Can you find the best parameters using the sliders?
""")

# allow user to choose which portion of the data to explore
x_axis_choice = st.sidebar.selectbox(
    "x axis",
    labels)
y_axis_choice = st.sidebar.selectbox(
    "y axis",
    labels)

# as the user explores different parts of the data, the
# range of the plots will change; think about how to scale
# the plots and the ranges of the sliders to account for 
# what the user has chosen to explore
min_x = df[x_axis_choice].min(axis=0)
max_x = df[x_axis_choice].max(axis=0)
min_y = df[y_axis_choice].min(axis=0)
max_y = df[y_axis_choice].max(axis=0)


##########
## LINE ##
##########

# we will compare two models: a line and the RBF-NN; this code
# does the line, which is done for you (but, update and change
# as you see fit!)

st.sidebar.write('line: slope and intercept')

s = float((max_y-min_y)/(max_x-min_x))
i = float(min_y-s*min_x)

parameter_list = ['slope', 'intercept']
parameter_input_values = []
parameter_default_values = [s, i]
values = []

# line sliders
# loop over the sliders: this is handy when there are many sliders
# improvement: make the min and max values correspond to what the user selected
for parameter, parameter_df in zip(parameter_list, parameter_default_values):
    values = st.sidebar.slider(label=parameter, key=parameter, value=float(parameter_df),
                               min_value=(float(parameter_df) - 3.0), max_value=(float(parameter_df) + 3.0), step=0.1)
    parameter_input_values.append(values)
 
input_variables = pd.DataFrame([parameter_input_values], columns=parameter_list, dtype=float)

# calculate line
# this uses the slider values to compute our model (a line in this case)
# hint: copy this below and replace the line with the sum of two Gaussians
slope = float(input_variables['slope'].iloc[0])
intercept = float(input_variables['intercept'].iloc[0])

x = np.linspace(min_x, max_x)
line_df = pd.DataFrame({
    'x': x,
    'y': slope*x + intercept})


############
## RBF-NN ##
############

# this is the part you need to write, starting with this starter code
st.sidebar.write('RBF: centers, widths and heights')

c1 = float(min_x)
w1 = float((min_y-max_y*np.exp(-(min_x-max_x)**2))/(1-np.exp(-(max_x-min_x)**2)*np.exp(-(min_x-max_x)**2)))

c2 = float(max_x)
w2 = float((max_y-min_y*np.exp(-(max_x-min_x)**2))/(1-np.exp(-(min_x-max_x)**2)*np.exp(-(max_x-min_x)**2)))

rbf_parameter_list = ['center 1', 'width 1', 'height 1', 'center 2', 'width 2', 'height 2']
rbf_parameter_input_values = []
rbf_parameter_default_values = [c1, w1, '0.0', c2, w2, '0.0']
rbf_values = []

# RBF-NN sliders
# the RBF-NN model has six parameters, so you need six sliders; again, feel
# free to upgrade this as you see fit
for rbf_parameter, rbf_parameter_df in zip(rbf_parameter_list, rbf_parameter_default_values):
 
    rbf_values = st.sidebar.slider(label=rbf_parameter, key=rbf_parameter, value=float(rbf_parameter_df),
                                   min_value=(float(rbf_parameter_df)-100.0), max_value=(float(rbf_parameter_df)+100.0),
                                   step=1.0)
    rbf_parameter_input_values.append(rbf_values)
 
rbf_input_variables = pd.DataFrame([rbf_parameter_input_values], columns=rbf_parameter_list, dtype=float)

# calculate RBF-NN
# this is just a copy of the code above, so it is just another line; replace this
# with a sum over two Gaussians
center1 = float(rbf_input_variables['center 1'].iloc[0])
width1 = float(rbf_input_variables['width 1'].iloc[0])
height1 = float(rbf_input_variables['height 1'].iloc[0])

center2 = float(rbf_input_variables['center 2'].iloc[0])
width2 = float(rbf_input_variables['width 2'].iloc[0])
height2 = float(rbf_input_variables['height 2'].iloc[0])

x = np.linspace(min_x, max_x)
rbf_df = pd.DataFrame({
    'x': x,
    'y': width1*np.exp(-(x-center1)**2/height1**2) + width2*np.exp(-(x-center2)**2/height1**2)})


##############
## plotting ##
##############

# this part is self explanatory; feel free to upgrade this simple
# visualization to something more interesting and useful to the user
linear_reg = alt.Chart(line_df).mark_line().encode(
    x='x',
    y='y',
    color=alt.value("#FFAA00"))

rbf_reg = alt.Chart(rbf_df).mark_line().encode(
    x='x',
    y='y',
    color=alt.value("#00FF00"))

scatter = alt.Chart(df).mark_circle(size=100).encode(
    x=x_axis_choice, y=y_axis_choice, color='preterm_birth:O',
    tooltip=['gestational_age', 'birthweight_sdscore', 'maternal_age',
             'maternal_bmi', 'paternal_age', 'paternal_bmi']).interactive()

scatter + linear_reg + rbf_reg

