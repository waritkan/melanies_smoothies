# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the Fruits you want in your custom smoothie.
  """
)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your Smoothie will be:", name_on_order )

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients :',
    my_dataframe,
    max_selections=5
)

if ingredient_list :
    
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        test_list = ['Apples', 'Blueberries', 'Jack fruit', 'Raspberries', 'Strawberries']

        if fruit_chosen in test_list :
          if fruit_chosen == 'Apples':
            fruit_chosen = 'Apple'
          elif fruit_chosen == 'Blueberries':
            fruit_chosen = 'Blueberry'
          elif fruit_chosen == 'Jack fruit':
            fruit_chosen = 'Jackfruit'
          elif fruit_chosen == 'Raspberries':
            fruit_chosen = 'Raspberry'
          else:
            fruit_chosen = 'Strawberry'
                  
        ingredients_string += fruit_chosen+ ' '
        st.subheader(fruit_chosen + ' Nutrution Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # st.write(ingredient_string)   

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered!, {name_on_order}', icon="✅")
        st.stop()



