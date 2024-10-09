import streamlit as st
import pandas as pd
import random

#To keep settings when swapping pages
for k, v in st.session_state.items():
    st.session_state[k] = v

st.set_page_config(
    layout="wide") 
st.header('Containers')
st.page_link("dateformats.py", label="Home", icon="🏠")
picnics = {'Name': ['Tom', 'nick', 'krish', 'jack'],
                'Age': ['old', 'young', 'old', 'child']}

# Create DataFrame
df = pd.DataFrame(picnics)

def menucheck(menulist,all,uniq):
        
        val = [None]* len(menulist) # this list will store info about which category is selected
        # st.write(val)
        if all:
                for i, cat in enumerate(menulist):
            # create a checkbox for each category
                    # idx = random.randint(1,100000)
                    val[i] = st.checkbox(cat, value=True, key = cat + uniq )# value is the preselect value for first render
                    
        
        else:
                for i, cat in enumerate(menulist):
                    # create a checkbox for each category
                    # idx = random.randint(1, 200000)
                    val[i] = st.checkbox(cat, value=False, key = cat + uniq) # value is the preselect value for first render
        return menulist[val]

def add(a,b):
        c = a+b
        return c 

if st.button('add'):
    result = add(1, 2)
    st.write('result: %s' % result)



col1, col2, col3 = st.columns([1,1,1])
with col1:
    with st.container(border = True, height=320, key ='sss'):
        # st.write("Menu")
        # dx = random.randint(1,100000)
        all = st.checkbox('All', value = True, key ='all') 
        # menulist1 = ['Toffee is great for tooth decay', 
        #             'Chocolate', 'Ice Cream','Lemonade']
        menulist1 = df.Name.unique()
        if all:
           menulist1 = menucheck(menulist1,True, 'one')
           st.write(menulist1) 
        else:
           menulist1 = menucheck(menulist1,False,'one') 
           st.write(menulist1) 

with col2:
        with st.container(border = True, height=320, key = 'ssddffg'):
                    #  st.write("Menu")
                    #  dx = random.randint(1,100000)
                     all2 = st.checkbox('All', value = True, key ='all2') 
                    #  menulist2 = ['Toffee is great for tooth decay', 
                    #              'Chocolate', 'Ice Cream','Lemonade', 'Gobstopper']
                     menulist2 = df.Age.unique()
                     
                     if all2:
                         menulist2 = menucheck(menulist2,True,'two')
                         st.write(menulist2) 
                     else:
                         menulist2 = menucheck(menulist2,False, 'two') 
                         st.write(menulist2)
df = df[df.Name.isin(menulist1) & df.Age.isin(menulist2)]
if df.shape[0]>0:    

     st.write(df)
else:
    st.write("Empty Dataframe")

 
with st.container(border=True, height =50):
   st.write("No of Cases found=",len(df) )
