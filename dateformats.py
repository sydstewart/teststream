from datetime import date , datetime, timedelta
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

st.set_page_config(
    layout="wide",
)


st.header('Dateformats.py')

col1, col2 = st.columns([1,3])

with col1:



            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=Upload data
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file )
                # st.subheader("Data Preview")
                st.write(df)
            
                datecol = st.selectbox(
                    "Select Date ",
                    (list(df.columns)),
                    )
                meascol = st.selectbox(
                    "Select Measure ",
                    (list(df.columns)),
                    )
                freq= st.selectbox( 'Select Frequecy',
                            ('Monthly', 'Weekly', 'Daily'))
with col2:

            df[datecol] = pd.to_datetime(df[datecol], dayfirst = True)

            # st.write('df',df)

            # st.write('YM Date adjusted',df['YM'])
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++Fill in zero months
            if freq== 'Monthly':
                    freq = 'MS'
            elif freq == 'Week':
                    freq = 'W-SUN'
            else: 
                    freq = 'D'

            first_date = df[datecol].min()
            fin_date = df[datecol].max()
          
        
            all_dates = pd.DataFrame({datecol:pd.date_range(start=first_date, end=fin_date,freq=freq)})
            # st.write('all', all_dates)

            df = pd.merge(all_dates, df, how="left", on=datecol).fillna(0)

            #===========================================================================
            df[datecol] = df[datecol].dt.strftime('%Y-%m-%d')
            Date = df[datecol].unique().tolist()

            # ggggst.write('Date', Date)

            max_value = datetime.strptime(max(Date), '%Y-%m-%d')
            min_value = datetime.strptime(min(Date), '%Y-%m-%d')
            value = (min_value, max_value)

            # st.write('Value', value)

            # st.dataframe(data=df)
            # st.column_config.DateColumn(df["YM"], format="YYYY-MM-DD")       
            # df.reset_index(inplace=True) 
            # convert to datetime data type, then grab just the date part (default year first)
            # df['index'] = pd.to_datetime(df['index']).dt.date     

            # st.write(df)

            # min_date = df.index.min()
            # max_date = df.index.max()


            # st.write('Minimum date:', min_value)
            # st.write('Maximum date:', max_value)
            label = 'Month  Range'

            value = (min_value, max_value)
            st.write('value',min_value, max_value )

            Model = st.slider(
                'Date:',
                min_value=min_value,
                max_value=max_value,
                value=value, step= timedelta(weeks =4), format ="YYYY-MM-DD")

            selmin, selmax = Model
            st.write(' From Slider', selmin,selmax)
            selmind = selmin.strftime('%Y-%m-%d')  # datetime to str
            selmaxd = selmax.strftime('%Y-%m-%d')

            # st.write('Selmind:', selmin, selmind)
            # st.write('Selmaxd:', selmax, selmaxd)

            df = df.loc[(df[datecol] >= selmind) & (df[datecol] <= selmaxd)]

            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Plotly Charts
            tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            fig = go.Figure()

            df['Median'] = df[meascol].median()
            df[datecol] = pd.to_datetime(df[datecol])
            # Add traces
            fig.add_trace(go.Scatter(x= df[datecol], y= df[meascol], mode='lines+markers', name= 'Cases'))
            fig.add_trace(go.Scatter(x= df[datecol], y = df['Median'],
                                mode='lines',
                                name='Median'))


    
# st.plotly_chart(fig,use_container_width=True)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=List if Dates

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Tabs   
# st.line_chart(data= df, x= "YM", y="Problem_Cases"     )
with tab1:
    st.header("Run Chart")
    st.plotly_chart(fig,use_container_width=True)
with tab2:
    st.header("Data table")
    st.write(df)

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)