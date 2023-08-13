import streamlit

streamlit.title("My Mom`s new healthy diner");

streamlit.header('Breakfast favourites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
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

#This is for the fruitvice api
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice=streamlit.text_input('Provide fruit name', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

import requests
fruitvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

#fruitvice_response=requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruitvice_response)
#streamlit.text(fruitvice_response.json())

fruitvice_normalize = pandas.json_normalize(fruitvice_response.json())
streamlit.dataframe(fruitvice_normalize)

#snowflake connectors
import snowflake.connector

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
