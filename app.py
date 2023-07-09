# The main libraries , which we will be using
import streamlit as st # App Chalta hai...
import pandas as pd # Charts
import plotly.express as px # Plotting


st.set_page_config(
                    page_title='Sales Dashboard', #Sabse Upar
                    page_icon=':bar_chart:', #Bar Char ICON
                    layout="wide",
                    initial_sidebar_state="auto",
)

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
            io = 'supermarket_sales.xlsx',
            engine = 'openpyxl',
            sheet_name = 'Sales',
            skiprows=3,
            usecols='B:R',
            nrows = 1000,
    )
    #Date Time:
    df['hour'] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

#SideBar
st.sidebar.header("Filter Options Here:")

city = st.sidebar.multiselect(
    "Select the City:",
    options = df["City"].unique(),
    default = df["City"].unique(),
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options = df["Customer_type"].unique(),
    default = df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options = df["Gender"].unique(),
    default = df["Gender"].unique(),
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


st.title(":bar_chart: Sales Dashboard")
st.markdown("##") #Separate the KPI's


# Totalling KPI'S

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US ${total_sales:,}")

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sale per Transaction:")
    st.subheader(f"US ${average_sale_by_transaction}")

st.markdown("---")


sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083BB"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)



#Sales by Hour

sales_by_hour = df_selection.groupby(by="hour").sum()[["Total"]]

fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title = "<b>Sales by hour</b>",
    color_discrete_sequence=["#0083BB"] * len(sales_by_hour),
    template = "plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis = dict(tickmode = "linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False))
)

left_column_1,right_column_1 = st.columns(2)
left_column_1.plotly_chart(fig_hourly_sales,use_container_width=True)
right_column_1.plotly_chart(fig_product_sales,use_container_width=True)



# type_to_gross_income = (
#     df_selection.groupby(by=["Customer_type"]).sum()[["gross margin percentage"]].sort_values(by="gross margin percentage")
# )

# fig_type_income = px.line(
#     type_to_gross_income,
#     x = type_to_gross_income.index,
#     y = "gross margin percentage",
#     title="Customer Type vs Gross Percentage",
#     color_discrete_sequence=["#0083BB"] * len(type_to_gross_income),
#     template="plotly-white",
# )

# ll_column = st.column(1)
# ll_column.plotly_chart(fig_type_income)

# Default Options are cleared for better styling
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

