import snowflake.connector as sf
from snowflake.connector import DictCursor
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

conn = sf.connect(
    user='PRAS29',
    password='Prasdream@2023',
    account='RYQHXXK-FN69582',
    warehouse='COMPUTE_WH',
    database='CODING_CHALLENGE',
    schema='PUBLIC',
    role='ACCOUNTADMIN'
    )

cur=conn.cursor(DictCursor)

query = 'SELECT * FROM BOOK_STORE'
cur.execute(query)
data_fetch=cur.fetchall()
df=pd.DataFrame(data_fetch)
#print(df.head())
#print(df.columns)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.header("Filters:")

# Add a multiselect for "RATING"
rating = st.sidebar.multiselect(
    "RATING",
    options=sorted(df["RATING"].unique()),
    default=sorted(df["RATING"].unique())
)

# Add a price range slider to the sidebar
price_range = st.sidebar.slider('Price Range (€)',
                                min_value=df['PRICE_IN_EUROS'].min(),
                                max_value=df['PRICE_IN_EUROS'].max(),
                                value=(df['PRICE_IN_EUROS'].min(), df['PRICE_IN_EUROS'].max()))

# Add a radio button for "AVAILABILITY"
availability = st.sidebar.radio(
    "AVAILABILITY",
    options=["In stock", "Out of stock"],
    index=0  # Default selection (0 for "In stock", 1 for "Out of stock")
)

# Filter the DataFrame based on user selections
df = df[
    (df["RATING"].isin(rating)) &
    (df['PRICE_IN_EUROS'] >= price_range[0]) &
    (df['PRICE_IN_EUROS'] <= price_range[1]) &
    (df['AVAILABILITY'] == availability)
]

# Function to create KPIs
def display_kpis():
    st.subheader("Key Performance Indicators")

    col1,col2,col3,col4=st.columns(4)

    # Number of books with 4+ rating
    with col1:
        cost_of_inventory = df['PRICE_IN_EUROS'].sum()
        # st.markdown(
        #     f"<div style='border:1px solid #d3d3d3; padding: 10px; border-radius: 10px; margin-right: 10px; display: inline-block;'>"
        #     f"<p style='font-size: 18px; margin: 0;'>Cost of Inventory:</p>"
        #     f"<p style='font-size: 24px; font-weight: bold; margin: 0;'>€{cost_of_inventory}</p>"
        #     f"</div>", unsafe_allow_html=True
        # )
        st.markdown(
        f"<div style='border:1px solid #d3d3d3; padding: 10px; border-radius: 10px; margin-right: 10px; display: inline-block; text-align: center;'>"
        f"<p style='font-size: 15px; margin: 0;'>Cost of Inventory:</p>"
        f"<p style='font-size: 24px; font-weight: bold; margin: 0; line-height: 1.5;'>€{cost_of_inventory}</p>"
        f"</div>", unsafe_allow_html=True)

    # Average price of books
    with col2:
        avg_price = df['PRICE_IN_EUROS'].mean()
        st.markdown(
            f"<div style='border:1px solid #d3d3d3; padding: 10px; border-radius: 10px; margin-right: 10px; display: inline-block;text-align: center;'>"
            f"<p style='font-size: 15px; margin: 0;'>Avg. price of books:</p>"
            f"<p style='font-size: 24px; font-weight: bold; margin: 0;'>€{avg_price:.2f}</p>"
            f"</div>", unsafe_allow_html=True
        )

    # Average rating of books
    with col3:
        avg_rating = df['RATING'].mean()
        st.markdown(
            f"<div style='border:1px solid #d3d3d3; padding: 10px; border-radius: 10px; margin-right: 10px; display: inline-block;text-align: center;'>"
            f"<p style='font-size: 15px; margin: 0;'>Avg. rating of books:</p>"
            f"<p style='font-size: 24px; font-weight: bold; margin: 0;'>{avg_rating:.2f}</p>"
            f"</div>", unsafe_allow_html=True
        )

    # Percentage of books available
    with col4:
        num_of_books = df.shape[0]
        st.markdown(
            f"<div style='border:1px solid #d3d3d3; padding: 10px; border-radius: 10px; display: inline-block;text-align: center;'>"
            f"<p style='font-size: 15px; margin: 0;'>No. of Books:</p>"
            f"<p style='font-size: 24px; font-weight: bold; margin: 0;'>{num_of_books}</p>"
            f"</div>", unsafe_allow_html=True
        )

def display_table():
    st.subheader("Top rated books in the price range")
    top_10_books = df.sort_values(by=['RATING'], ascending=[False]).head(10)
    st.table(top_10_books[['BOOK_TITLE', 'PRICE_IN_EUROS', 'RATING', 'AVAILABILITY']])


# Function to create histogram
def display_histogram():

    # Histogram of price
    col1, col2 = st.columns(2)

    fig1 = px.histogram(df, x='PRICE_IN_EUROS', nbins=5, labels={'PRICE_IN_EUROS': 'Price(€)'}, title='Distribution of Prices')
    fig1.update_traces(marker=dict(color=px.colors.sequential.Plasma))
    fig1.update_layout(bargap=0.1)
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(df,names='RATING',title='Distribution of Rating',labels={'RATING': 'Rating'},)
    col2.plotly_chart(fig2, use_container_width=True)

# Function to create scatter plot
def display_scatter_plot():
    st.subheader("Price and Rating relationship")

    # Scatter plot
    plt.figure(figsize=(7, 5))
    sns.scatterplot(x='PRICE_IN_EUROS', y='RATING', data=df, hue='AVAILABILITY', palette='viridis')
    st.pyplot()

# colT1,colT2 = st.columns(10)
# with colT2:
#     st.title("Bookstore Dashboard")
st.markdown("<h1 style='text-align: center; color: blue;'>The Bookstore</h1>", unsafe_allow_html=True)

# Display KPIs
display_kpis()

st.markdown("---")

display_table()
# Display histograms
display_histogram()

# Display scatter plot
display_scatter_plot()
