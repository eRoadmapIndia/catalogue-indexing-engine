from openai import OpenAI
import json
import streamlit as st
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from PIL import Image
import os
import uuid
import base64
from PIL import Image
import io
import requests
ELASTIC_PASSWORD = "QzA59iR1XznhHVrCFioX0not"

# Found in the 'Manage Deployment' page
CLOUD_ID = "ONDC_Catalogue_indexing_Engine:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmNGM1MzEwYWVmZWY0NzBjODM4MjVlMjk0Mjg5ZDBmNyRlNDM1ZGZhNDllM2U0MGRjYjYwZjgzODhmZjQwYjU4YQ=="

es = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


es.ping()
#es.info()

model = SentenceTransformer('all-mpnet-base-v2')

client = OpenAI(api_key="sk-proj-wH2DJ4K3Y4BOtn3oq8SbT3BlbkFJ5OQSILbgNWxu0oMKbJZN")




# OpenAI API Key
api_key = "sk-proj-wH2DJ4K3Y4BOtn3oq8SbT3BlbkFJ5OQSILbgNWxu0oMKbJZN"

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

def fashion_search(input_keyword):
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field" : "searchvector",
        "query_vector" : vector_of_input_keyword,
        "k" : 10,
        "num_candidates" : 500, 
    }

    res = es.knn_search(index="fashion", knn=query , source=["ProductName","Description","Price (INR)"])
    print(res["hits"]["hits"])
    return res["hits"]["hits"]
def grocery_search(input_keyword):
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field" : "searchvector",
        "query_vector" : vector_of_input_keyword,
        "k" : 10,
        "num_candidates" : 500, 
    }

    res = es.knn_search(index="grocery", knn=query , source=["Name","Quantity","DiscountedPrice","imageurl"])
    print(res["hits"]["hits"])
    return res["hits"]["hits"]
def electronics_search(input_keyword):
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field" : "searchvector",
        "query_vector" : vector_of_input_keyword,
        "k" : 10,
        "num_candidates" : 500, 
    }

    res = es.knn_search(index="electronics", knn=query , source=["name","main_category","discount_price","image"])
    print(res["hits"]["hits"])
    return res["hits"]["hits"]
def smartphone_search(input_keyword):
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field" : "searchvector",
        "query_vector" : vector_of_input_keyword,
        "k" : 10,
        "num_candidates" : 500, 
    }

    res = es.knn_search(index="smartphone", knn=query , source=["title","brand","highlights","selling_price"])
    print(res["hits"]["hits"])
    return res["hits"]["hits"]
def fragrance_search(input_keyword):
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field" : "searchvector",
        "query_vector" : vector_of_input_keyword,
        "k" : 10,
        "num_candidates" : 500, 
    }

    res = es.knn_search(index="fragrance", knn=query , source=["name","description","price","image1"])
    print(res["hits"]["hits"])
    return res["hits"]["hits"]
def hardware_search(input_keyword):
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field" : "searchvector",
        "query_vector" : vector_of_input_keyword,
        "k" : 10,
        "num_candidates" : 500, 
    }

    res = es.knn_search(index="hardware", knn=query , source=["Name","Short description","Sale price","Images"])
    print(res["hits"]["hits"])
    return res["hits"]["hits"]

def inference_text(query,client):
  prompt='''translate the search query into English according to an ecommerce store and reply in json format.{"Product_category":[text],"Max-price":long,"Min-price":long,attributes":text,"Similar-categories":[text],"BrandName":[text] , "converted-english_query"="if the querry is other than english language convert it to english language and correctly structure the search"}.  Product categories are : 	Fashion , Grocery,Smartphone,Electronics,Hardware,Fragrance. Do you understand?'''
  response = client.chat.completions.create(
  model="gpt-4o",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": query}
  ]
)
  result=json.loads(response.choices[0].message.content)
  print(result)
  return result
def product_search(query,client):
    result=inference_text(query,client)
    print("\n\n\n ",result)
    if 'Fashion' in result['Product_category'] :
        return fashion_search(result['converted-english_query'])
    elif 'Grocery' in result['Product_category'] :
        return grocery_search(result['converted-english_query'])
    elif 'Smartphone' in result['Product_category'] :
        return smartphone_search(result['converted-english_query'])
    elif 'Electronics' in result['Product_category'] :
        return electronics_search(result['converted-english_query'])
    elif 'Hardware' in result['Product_category']:
        return hardware_search(result['converted-english_query'])
    elif 'Fragrance' in result['Product_category'] :
        return fragrance_search(result['converted-english_query'])
    else:
        print("Something Went Wrong ! Enter a better Querry")

def format_fashion_products(input_list):
    formatted_list = []
    for idx, item in enumerate(input_list, start=1):
        formatted_product = {
            "image": "https://via.placeholder.com/150",
            "ProductName": item['_source']['ProductName'],
            #"Description": item['_source']['Description'],
            "Price (INR)": item['_source']['Price (INR)']
        }
        formatted_list.append(formatted_product)
    return formatted_list
def format_grocery_products(input_list):
    formatted_list = []
    for idx, item in enumerate(input_list, start=1):
        formatted_product = {
            "imageurl": item['_source']['imageurl'],
            "Name": item['_source']['Name'],
            "Quantity": item['_source']['Quantity'],
            "DiscountedPrice": item['_source']['DiscountedPrice']
        }
        formatted_list.append(formatted_product)
    return formatted_list
def format_fragrance_products(input_list):
    formatted_list = []
    for idx, item in enumerate(input_list, start=1):
        formatted_product = {
            "image1": item['_source']['image1'],
            "name": item['_source']['name'],
            #"description": item['_source']['description'],
            "price": item['_source']['price']
        }
        formatted_list.append(formatted_product)
    return formatted_list
def format_hardware_products(input_list):
    formatted_list = []
    for idx, item in enumerate(input_list, start=1):
        formatted_product = {
            "Images": item['_source']['Images'].split(',')[0],
            "Name": item['_source']['Name'],
            #"Short description": item['_source']['Short description'],
            "Sale price": item['_source']['Sale price']
        }
        formatted_list.append(formatted_product)
    return formatted_list
def format_electronics_products(input_list):
    formatted_list = []
    for idx, item in enumerate(input_list, start=1):
        formatted_product = {
            "image": item['_source']['image'],
            "name": item['_source']['name'],
            "main_category": item['_source']['main_category'],
            "discount_price": item['_source']['discount_price']
        }
        formatted_list.append(formatted_product)
    return formatted_list


# main function to perform text search based on search querry and search
def Elasticsearch_products(search_query,client):
                search_products  = product_search(str(search_query),client)
                if search_products[0]!=None:
                    if search_products[0]['_index']=='fashion':
                        print("\n\n"+"Hurray! searching fashion")
                        filtered_products=format_fashion_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_fashion_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='grocery':
                        print("\n\n"+"Hurray! searching Grocery")
                        filtered_products=format_grocery_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_grocery_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='fragrance':
                        print("\n\n"+"Hurray! searching Fragrance")
                        filtered_products=format_fragrance_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_fragrance_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='hardware':
                        print("\n\n"+"Hurray! searching hardware")
                        filtered_products=format_hardware_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_hardware_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='electronics':
                        print("\n\n"+"Hurray! searching Electronics")
                        filtered_products=format_electronics_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_electronics_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                else:
                    st.write("Sorry We do not sell these products")



def main():
         # Sample data for products
        products = [
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 1", "Description": "Description 1", "Price (INR)": 10},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 2", "Description": "Description 2", "Price (INR)": 20},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 3", "Description": "Description 3", "Price (INR)": 30},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 4", "Description": "Description 4", "Price (INR)": 40},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 5", "Description": "Description 5", "Price (INR)": 50},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 6", "Description": "Description 6", "Price (INR)": 60},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 7", "Description": "Description 7", "Price (INR)": 70},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 8", "Description": "Description 8", "Price (INR)": 80},
            {"image": "https://via.placeholder.com/150", "ProductName": "Product 9", "Description": "Description 9", "Price (INR)": 100},
        ]

        # Function to display product
        def display_fashion_product(product):
            st.image("https://via.placeholder.com/150", width=200, use_column_width=False)
            st.markdown(f"**{product['ProductName']}**")
            #st.markdown(f"*{product['Description']}*")
            st.markdown(f"<span style='color:red;'>₹{product['Price (INR)']}</span>", unsafe_allow_html=True)
        def display_grocery_product(product):
            st.image(product['imageurl'], width=200, use_column_width=False)
            st.markdown(f"**{product['Name']}**")
            st.markdown(f"*{product['Quantity']}*")
            st.markdown(f"<span style='color:red;'>₹{product['DiscountedPrice']}</span>", unsafe_allow_html=True)
        def display_fragrance_product(product):
            st.image(product['image1'], width=200, use_column_width=False)
            st.markdown(f"**{product['name']}**")
            #st.markdown(f"*{product['description']}*")
            st.markdown(f"<span style='color:red;'>₹{product['price']}</span>", unsafe_allow_html=True)
        def display_hardware_product(product):
            st.image(product['Images'].split(',')[0], width=200, use_column_width=False)
            st.markdown(f"**{product['Name']}**")
            #st.markdown(f"*{product['Short description']}*")
            st.markdown(f"<span style='color:red;'>₹{product['Sale price']}</span>", unsafe_allow_html=True)
        def display_electronics_product(product):
            st.image(product['image'], width=200, use_column_width=False)
            st.markdown(f"**{product['name']}**")
            st.markdown(f"*{product['main_category']}*")
            st.markdown(f"<span style='color:red;'>₹{product['discount_price']}</span>", unsafe_allow_html=True)

        def Elasticsearch_products(search_query,client):
                search_products  = product_search(str(search_query),client)
                if search_products[0]!=None:
                    if search_products[0]['_index']=='fashion':
                        print("\n\n"+"Hurray! searching fashion")
                        filtered_products=format_fashion_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_fashion_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='grocery':
                        print("\n\n"+"Hurray! searching Grocery")
                        filtered_products=format_grocery_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_grocery_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='fragrance':
                        print("\n\n"+"Hurray! searching Fragrance")
                        filtered_products=format_fragrance_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_fragrance_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='hardware':
                        print("\n\n"+"Hurray! searching hardware")
                        filtered_products=format_hardware_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_hardware_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                    elif search_products[0]['_index']=='electronics':
                        print("\n\n"+"Hurray! searching Electronics")
                        filtered_products=format_electronics_products(search_products)
                        # Create a 3x3 grid
                        cols = st.columns(3)
                        num_products = len(filtered_products)

                        for idx, product in enumerate(filtered_products):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                display_electronics_product(product)

                        if not filtered_products:
                            st.write("No products found.")
                else:
                    st.write("Sorry We do not sell these products")

        def image_text(headers,image_base64):
                payload = {
                    "model": "gpt-4o",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Write a search query to search on an ecommerce store according to this image"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 300
                }

                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                
                if response.status_code == 200:
                    response_data = response.json()
                    st.write(response_data['choices'][0]['message']['content'])
                    return response_data['choices'][0]['message']['content']
                else:
                    st.error("API request failed. Please check the request and try again.")
        # Streamlit layout

        
        st.title("Search on ONDC Products Network")

        # Sidebar for Price (INR) information
        
        min_price = 0
        max_price = "1000+"

        st.sidebar.image(r"https://eroadmap.in/wp-content/uploads/2023/06/cropped-WhatsApp-Image-2023-06-13-at-11.46.171.jpg",use_column_width=True)
        st.sidebar.header("Price Information")
        st.sidebar.text(f"Minimum Price: ₹{min_price}")
        st.sidebar.text(f"Maximum Price: ₹{max_price}")

        # Search bar with mic and camera icons
        search_query = st.text_input("Search for products")
        col1,col2= st.columns([2,10])
        with col1:
            search_button = st.button("Search")
        with col2:
            uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            # You can now use the uploaded image for further processing
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            Elasticsearch_products(image_text(headers,image_base64),client)  # Calling the image_text function

        # Filter products based on search query when search button is clicked
        filtered_products = products
        if search_button:
            Elasticsearch_products(search_query,client)

if __name__ == "__main__":
    main()