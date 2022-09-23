
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import streamlit as st

data = pd.read_csv("https://raw.githubusercontent.com/LoWeT0619/Fall-2022-CMSE-830/main/data.csv")

features_mean,features_se,features_worst =[],[],[]
for feat in data.columns:
    if "mean" in feat:
        features_mean.append(feat)
    elif "se" in feat:
        features_se.append(feat)
    elif "worst" in feat:
        features_worst.append(feat)

option = st.selectbox(
    'What plot would you like to see?',
    ('kde plot', 'box plot', 'violin plot', 'scatterplot', 'heatmap'))

st.write('You selected:', option)

fig, (ax_kdeplot, ax_boxplot, ax_violinplot, ax_scatterplot, ax_heatmap)  = plt.subplots(
    nrows=5,
    ncols=1,
    figsize=(6, 6))

sns.kdeplot(data=data, x="radius_mean", y="smoothness_mean", ax=ax_kdeplot)
sns.boxplot(data=data,
            x="radius_mean",
            y="diagnosis",
            hue="diagnosis",
            ax=ax_boxplot)
sns.violinplot(data=data,
               x="smoothness_mean",
               y="diagnosis",
               hue="diagnosis",
               ax=ax_violinplot)
sns.scatterplot(data=data, x="radius_mean", y="smoothness_mean", hue="diagnosis", ax=ax_scatterplot)
sns.heatmap(data[features_mean].corr(), annot=True, cmap="PiYG", ax=ax_heatmap)

ax_kdeplot.set_title("kdeplot - radius_mean vs smoothness_mean")
ax_kdeplot.grid(True)
ax_boxplot.set_title("boxplot - radius_mean vs diagnosis")
ax_violinplot.set_title("violinplot - smoothness_mean vs diagnosis")
ax_scatterplot.set_title("scatterplot - radius_mean vs smoothness_mean")
ax_heatmap.set_title("heatmap for each mean")

fig.set_tight_layout(True)

st.pyplot(fig)
