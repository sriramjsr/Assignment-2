import pandas as pd
import os 
import json
import mysql.connector as sql
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

icon = Image.open("data\ICN.png")

st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   )       
st.sidebar.header(":wave: :green[**Hello! Welcome to the dashboard**]")

mydb = sql.connect(host = "localhost",
                        user = "root",
                        password = "2104030@#",
                        database = "phone_pe"
                        )
cursor = mydb.cursor(buffered = True)


with st.sidebar:
    selected = option_menu("Menu",["Home","Top Charts", "Explore Data", "About"],
                           icons=["house","graph-up-arrow","bar-chart-line","exclamation-circle"],
                           default_index=0,
                           styles={"nav-link":{"font-size": "17.5px","text-align":"left","margin": "-1px","--hover-color": "#6F36AD"},
                                   "nav-link-selected":{"background-color": "#6F36AD"}})

if selected == "Home":
    st.image("data\img.png")
    st.markdown("### :violet[Data Visualization and Exploration]")
    st.markdown("### :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")

    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("##### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("##### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("data\home.png")
    

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from aggree_transaction where year = {Year} and Quater = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        

        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select Districts , sum(Transaction_count) as Count, sum(Transaction_amount) as Total from map_transaction where year = {Year} and Quater = {Quarter} group by Districts order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            cursor.execute(f"select Pincodes, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction where year = {Year} and quater = {Quarter} group by Pincodes order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    # Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        

        # Brands which have total transaction count and the percentage
        with col1:
            st.markdown("### :violet[Brands]")
            cursor.execute(f"select brands, sum(Transaction_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from aggre_users where year = {Year} and quater = {Quarter} group by Brands order by Total_Count desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
            fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="Brand",
                            orientation='h',
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)  


        # State wise app opens and the total registered users
        with col2:
            st.markdown("### :violet[State]")
            cursor.execute(f"select State , sum(RegisteredUsers) as Total_Users, sum(AppOpens) as App_Opens from map_user where year = {Year} and quater = {Quarter} group by State order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','App_Opens'])

            fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['App_Opens'],
                                labels={'Total_Users':'Total_Users'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        # Districts wise total users and their app open

        with col3:
            st.markdown("### :violet[District]")
            cursor.execute(f"select Districts,sum(RegisteredUsers) as Total_Users,sum(AppOpens)  as App_Opens from map_user where year = {Year} and quater = {Quarter} group by Districts order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns = ['Districts', 'Total_Users' , 'App_Opens'])
            df.Total_Users = df.Total_Users.astype(float) 
            fig = px.bar(df,
                            title= 'Top 10',
                            x = 'Total_Users',
                            y = 'Districts',
                            orientation='h',
                            color='App_Opens',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)


        # pincode wise total users from the year and the quarter
        with col4:
            st.markdown("### :violet[Pincodes]")
            cursor.execute(f"select Pincodes,sum(RegisteredUsers) as Total_Users from top_user where year = {Year} and quater = {Quarter} group by Pincodes order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(),columns = ['Pincodes', 'Total_Users'])

            fig = px.pie(df, values =  'Total_Users',
                             names = "Pincodes",
                             title="Top 10",
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    
if selected == "Explore Data":
    st.markdown("## :violet[Explore Data]")
    Year = st.sidebar.slider("**Year**",min_value=2018,max_value=2022)
    Quarter = st.sidebar.slider("**Quarter**",min_value=1,max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)


    if Type == "Transactions":

            with col1:
                st.markdown('### :violet[ALL states Transaction amount]')
                cursor.execute(f'select state, sum(Transaction_amount) as Total_amount from map_transaction where year = {Year} and quater = {Quarter} group by state order by state')
                df = pd.DataFrame(cursor.fetchall(),columns = ['state','Total_amount'])
                df1 = pd.read_csv(r'D:\phone pe\data\Statenames.csv')
                df.state = df1


                fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",

                      featureidkey='properties.ST_NM',
                      locations='state',
                      color='Total_amount',
                      color_continuous_scale='sunset')
                
                
            #fig.update_geos(showland=False, showframe=False)
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)



            with col2:
                st.markdown('### :violet[All states Transactions count]')
                cursor.execute(f'select state,sum(Transaction_count) as Total_Transaction from map_transaction where year = {Year} and quater = {Quarter} group by state')
                df = pd.DataFrame(cursor.fetchall(),columns = ['state','Total_Transaction'])
                df1 = pd.read_csv(r'D:\phone pe\data\Statenames.csv')
                df.state = df1
                


                fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",

                      featureidkey='properties.ST_NM',
                      locations='state',
                      color='Total_Transaction',
                      color_continuous_scale='sunset')
                
                fig.update_geos(fitbounds = "locations", visible = False)
                st.plotly_chart(fig,use_container_width=True)
    

            st.markdown('### :violet[Top payment type]')
            cursor.execute(f'select Transaction_type,sum(Transaction_count)as Total_Transaction,sum(Transaction_amount)as Total_amount from aggree_transaction where year = {Year} and quater = {Quarter} group by Transaction_type')
            df = pd.DataFrame(cursor.fetchall(),columns = ['Transaction_type','Total_Transaction','Total_amount'])

            fig = px.bar(df,
                            title="Transaction Type and Total Transactions",
                            x= "Transaction_type",
                            y = "Total_Transaction",
                            orientation='v',
                            color='Total_amount',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)


            st.markdown('# ')
            
            st.markdown('### :violet[Select any state  you need to know about and in the districts of the state ]')
            state = st.selectbox("state",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
            
            cursor.execute(f"select state,Districts,year,quater,sum(Transaction_count) as Total_count,sum(Transaction_amount)as Total_amount from map_transaction where year = {Year} and quater = {Quarter} and state = '{state}' group by state,Districts,year,quater order by state,Districts")
            df = pd.DataFrame(cursor.fetchall(),columns = ['state','Districts','year','quater','Total_count','Total_amount'])

            fig = px.bar(df,
                         title=state,
                         x= "Districts",
                         y="Total_count",
                         orientation='v',
                         color="Total_amount",
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

    if Type == "Users":
        st.markdown('### :violet[Overall state App Opening frequency]')
        cursor.execute(f'select state,sum(RegisteredUsers) as Total_Users,sum(AppOpens) as TotalTimeAppOpens from map_user where year = {Year} and quater = {Quarter} group by state order by state')
        df = pd.DataFrame(cursor.fetchall(),columns = ['state','Total_Users','TotalTimeAppOpens'])
        df1 = pd.read_csv(r'D:\phone pe\data\Statenames.csv')
        df.state = df1

        fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",

                      featureidkey='properties.ST_NM',
                      locations='state',
                      color='TotalTimeAppOpens',
                      color_continuous_scale='sunset')
                
        fig.update_geos(fitbounds = "locations", visible = False)
        st.plotly_chart(fig,use_container_width=True)

        st.markdown('## :violet[select the state you want to explore about it]')
        state = st.selectbox("state",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        cursor.execute(f'select state,year,quater,Districts,sum(RegisteredUsers) as Total_Users,sum(AppOpens) as TotalTimeAppOpens from map_user where year = {Year} and quater = {Quarter} and state = "{state}" group by state,year,quater,Districts order by state,Districts')
        df = pd.DataFrame(cursor.fetchall(), columns = ['state','year','quater','Districts','Total_Users','TotalTimeAppOpens'])

        fig = px.bar(df,
                     title=state,
                     x="Districts",
                     y="Total_Users",
                     orientation='v',
                     color='TotalTimeAppOpens',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

if selected == "About":
    
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")