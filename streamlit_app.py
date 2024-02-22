import streamlit
import pandas
import requests
import snowflake.connector
from urlib.error import URLError

streamlit.title('hello!')

#Import Pandas

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import Requests

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruit_to_show = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruit_show = my_fruit_list.loc[fruit_to_show]

# Display the table on the page.

streamlit.dataframe(fruit_show)

streamlit.header('Fruityvice Fruit Advice')

fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)

#Normalize json data into a table
fruityvice_normalize = pandas.json_normalize(fruityvice_response.json())

#Show output in a table form
streamlit.dataframe(fruityvice_normalize)

streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input('What fruit would you like to add?: ')
streamlit.write('Thanks for adding a fruit to the list')

my_cur.execute("INSERT INTO fruit_load_list VALUES ('FROM STREAMLIT')")

