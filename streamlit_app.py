#the below imports are placed one-after-the-other after testing all the things
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom`s new healthy diner");

streamlit.header('Breakfast favourites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

#multiselect pick list
#streamlit.multiselect("pick some fruits",list(my_fruit_list.index),['Avocado','Strawberries'])
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

fruits_selected = streamlit.multiselect("Pick some fruits",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

#to show
streamlit.dataframe(fruits_to_show)

#this is for function
def get_fruitvice_data(this_fruit_choice):
  fruitvice_response=requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruitvice_normalize = pandas.json_normalize(fruitvice_response.json())
  return fruitvice_normalize

#This is for the fruitvice api
streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice=streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    #fruitvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #fruitvice_normalize = pandas.json_normalize(fruitvice_response.json())
    #streamlit.dataframe(fruitvice_normalize)  
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function) 
    
except URLError as e:
    streamlit.error()
  
#streamlit.write('The user entered', fruit_choice)




#fruitvice_response=requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruitvice_response)
#streamlit.text(fruitvice_response.json())



#-------the stop is written after the below lines are tested
streamlit.stop()
#snowflake connectors


my_conn = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_conn.cursor()
#my_cur.execute("select current_user(),current_account(),current_region()")
my_cur.execute("select * from fruit_load_list")
#my_data = my_cur.fetchone()--fetch one row
my_data = my_cur.fetchall()
streamlit.header("Sample list from fruit_load_list table:")
streamlit.dataframe(my_data)

#small exercise----------------------

streamlit.text("What fruit would you like to add?")
var=streamlit.text_input('')
streamlit.write('The fruit name you entered is',var)

#small exercise-2--------------------
my_cur.execute("insert into fruit_load_list values('test-streamlit app')");


