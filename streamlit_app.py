# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: My Parents Healthy New Diner :cup_with_straw:")
st.write("Select the fruits that you want in your smoothie")
#st.write("""Replace this example with your own code!**And if you're new to Streamlit,** check out our easy-to-follow guides at [docs.streamlit.io](https://docs.streamlit.io). """ '\n' "This is my first time writing using StreamLit to create a web application")

##option = st.selectbox(
  ##  'What is your favourite fruit?',
    ##('Apple', 'Banana', 'Orange', 'Avacado', 'Strawberry', 'Mango'))

##st.write('Your favourite fruit is :', option)

title = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be : ', title)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert Snowpark dataframe to  a Pandas Dataframe so we can use the LOC funtion
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect(
    'Choost upto 5 fruits:'
    ,my_dataframe
    ,max_selections = 5
    
   )

#The phrase:
# if ingredients_list:
#actually means...
#if ingredients_list is not null: then do everything below this line that is indented.

if ingredients_list:
  ingredients_string = ''
  name_on_order = title
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '

    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    
    st.subheader(fruit_chosen + 'Nutritional Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
    fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)


  st.write(ingredients_string)
    
  my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

  st.write(my_insert_stmt)
  time_to_insert = st.button('Submit Order')

  if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success("""Your Smoothie is ordered,""" + name_on_order + """!""", icon="✅")
        
