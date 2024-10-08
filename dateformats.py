from datetime import date , datetime, timedelta
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

#To keep settings when swapping pages
for k, v in st.session_state.items():
    st.session_state[k] = v
    
st.set_page_config(
    layout="wide",
)


st.header('Run Charts')
st.page_link("dateformats.py", label="Home", icon="🏠")
st.page_link("pages/cont.py", label="Filtering by Checkboxes", icon="1️⃣")
# st.page_link("pages/modelchecks.py", label="Test Filtering of Cases", icon="2️⃣", disabled=False)
col1, col2 = st.columns([1,3])

with col1:
     
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
                df = pd.read_csv(uploaded_file )
                # st.subheader("Data Preview")
                st.write(df.head(3))
                

            
                datecol = st.selectbox(
                    "Select Date ",
                    (list(df.columns)),index=None,placeholder ="Choose a date column",
                    )
                meascol = st.selectbox(
                    "Select Measure ",
                    (list(df.columns)),index=None, placeholder="Select a Measure...",
                    )
                freq = st.selectbox( 
                    "Select Frequency",
                    ('Monthly', 'Weekly', 'Daily'),index= None, placeholder ="Select a Time Interval..",
                    )
        if uploaded_file is not None: 
            if datecol != None and meascol != None and freq != None: 
                # st.write(df[datecol])

                if freq== 'Monthly':
                        freq = 'MS'
                elif freq == 'Week':
                        freq = 'W-SUN'
                else: 
                        freq = 'D'

                df[datecol] = pd.to_datetime(df[datecol], dayfirst = True)
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

                label = 'Month  Range'

                value = (min_value, max_value)
                # st.write('value',min_value, max_value )
                
with col2:                
    if uploaded_file is not None: 
        if datecol != None and meascol != None and freq != None:  
               
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
                
                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                
                fig = go.Figure()

                df['Median'] = df[meascol].median()
                df[datecol] = pd.to_datetime(df[datecol])
                # Add traces
                fig.add_trace(go.Scatter(x= df[datecol], y= df[meascol], mode='lines+markers', name= 'Cases'))
                fig.add_trace(go.Scatter(x= df[datecol], y = df['Median'],
                                    mode='lines',
                                    name='Median'))


            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=List if Dates
                tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
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
