import streamlit
import pandas as pd

streamlit.title('My Parent\'s New Healthy Diner')

streamlit.header('🐸Breakfast Menu')
streamlit.text('🥚Boiled Egg')
streamlit.text('🍀Spinach')
streamlit.text('🥑Avocado')

streamlit.header('🍇:banana:Make your own smoothie:cherries::apple:')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#lets put a pickist so that user can add fruits as per his/her wish.
fruits_selected = streamlit.multiselect("Pick some fruits : ",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#new section to bring new fruityvice response
streamlit.header('FruityVice advise')

fruit_choice = streamlit.text_input("What fruit would you like information about? ",'apple')
streamlit.write("The user entered : ",fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

from snowflake import connector
