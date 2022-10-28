
import pandas as pd  #pip install pandas openpyxl
import plotly.express as  px #  pip install plotly-express
import streamlit as st # pip install streamlit

# page title and icon
st.set_page_config( page_title='Sales Dashboard',
                    page_icon=':bar_chart:',
                    layout='wide',

)

@st.cache
def get_data_from_excel():
# read excel file
    df= pd.read_excel(
        io= 'supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        # how many rows it needs to skip
        skiprows= 3,
        # whitch columns you wante to use
        usecols='B:R',
        nrows=1000,
    )

    # add hour column to dataframe
    df['hour']= pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df


df = get_data_from_excel()
# df.to_csv('exemple.csv')

# *****sideBar***************
st.sidebar.header("Please Filter Here :")

# create multiselect city
city = st.sidebar.multiselect(
    "Select the city:",
    options=df['City'].unique(),
    default=df['City'].unique(),
)

#  create multiselct customer type
customer_type = st.sidebar.multiselect(
    "Select the Customer type:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique(),
)

# create multiselect gender
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique(),
)
#  query : filter data with city, customer_type and gender column
df_selection= df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# ***** MainPage********
#  title of main page 



st.title(':bar_chart: Sales Dashboard')
st.markdown('##')

# claculate KPI's 
try:
    total_sales = int(df_selection['Total'].sum())
    # round , 1 get one number after comma
    average_rating = round(df_selection['Rating'].mean(), 1)
    # a result of 6.9 would display as seven starts,for instance
    star_rating=':star:'* int(round(average_rating, 0))
    average_sales_by_transaction = round(df_selection["Total"].mean(), 2)

except Exception:
        print('no data selected')


left_column, middle_column, right_column =st.columns(3)
try:

    with left_column:
        st.subheader('Total Sales:')
        st.subheader(f'US $ {total_sales:,}')
        

    with middle_column:
        st.subheader('Average Sales Per Transaction:')
        st.subheader(f'US $ {average_sales_by_transaction}')  
        

    with right_column:
        st.subheader('Average Rating:')
        st.subheader(f'US $ {average_rating} {star_rating}')


except Exception:
        print('no data selected')
       
   
# to separate KPI's 
st.markdown("------") 

# sales by product line [BAR CHART]

sales_by_production_line =(
    # calculate total
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by= "Total")
)

fig_product_sales = px.bar(
    sales_by_production_line,
    x= 'Total',
    y= sales_by_production_line.index,
    orientation='h',
    title="<b>Sales By Product Line </b>",
    color_discrete_sequence= ['#0083BB'] * len(sales_by_production_line),
    template="plotly_white",
    
)

fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid =False))
)

# to visualization of chart
# st.plotly_chart(fig_product_sales)

#  calculate sales by hours 

sales_by_hour = df_selection.groupby(by =['hour']).sum()[['Total']]

fig_hourly_sales = px.bar(
    sales_by_hour,
    x= sales_by_hour.index,
    y= 'Total',
    title="<b>Sales By Hour </b>",
    color_discrete_sequence= ['#0083BB'] * len(sales_by_hour),
    template="plotly_white",
    
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode ='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid =False)),
)

left_column , right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width= True)
right_column.plotly_chart(fig_hourly_sales, use_container_width= True)

hide_st_style ="""
                <style>
                #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                header {visibility : hidden;}
                </style>
            """
st.markdown(hide_st_style,unsafe_allow_html=True)