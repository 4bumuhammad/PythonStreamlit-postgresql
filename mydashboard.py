import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
df = None  # Inisialisasi df di luar blok if

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")

if df is not None:
    col1, col2 = st.columns((2))
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Getting the min and max date 
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

    st.sidebar.header("Choose your filter: ")
    # Create for Region
    region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df["Region"].isin(region)]

    # Create for State
    state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2["State"].isin(state)]

    # Create for City
    city = st.sidebar.multiselect("Pick the City",df3["City"].unique())


    # Filter the data based on Region, State and City

    if not region and not state and not city:
        filtered_df = df
    elif not state and not city:
        filtered_df = df[df["Region"].isin(region)]
    elif not region and not city:
        filtered_df = df[df["State"].isin(state)]
    elif state and city:
        filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
    elif region and city:
        filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
    elif region and state:
        filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
    elif city:
        filtered_df = df3[df3["City"].isin(city)]
    else:
        filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

    category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

    with col1:
        st.subheader("Category wise Sales")
        fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)
