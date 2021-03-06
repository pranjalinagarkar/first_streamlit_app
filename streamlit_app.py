import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

#create the function
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

#new section to bring new fruityvice response
streamlit.header('FruityVice advise!')
try:
   fruit_choice = streamlit.text_input("What fruit would you like information about? ",'apple')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

#dont run anything past here while we troubleshoot
#streamlit.stop()

streamlit.header("View our Fruit List - Add your favourites ")
#snowflake related function
def get_fruit_load_list():
   with  my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()

#add button to load fruit list
if streamlit.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)

#Allow end user to add fruit to the list
def insert_row_snowflake(new_fruit):
   with  my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
      return "Thanks for adding " + new_fruit
   
add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('AddFruitToTheList'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_row_snowflake(add_my_fruit)
   my_cnx.close()
   streamlit.text(back_from_function)
#streamlit.write("Thanks for adding ",add_my_fruit)

