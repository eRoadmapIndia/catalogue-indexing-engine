
from openai import OpenAI
import json
import streamlit as st
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic","lZTCy6LyxmszTk2DPqAV"),
    verify_certs=False,
)

es.ping()
#es.info()

model = SentenceTransformer('all-mpnet-base-v2')

client = OpenAI(api_key="sk-proj-wH2DJ4K3Y4BOtn3oq8SbT3BlbkFJ5OQSILbgNWxu0oMKbJZN")

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
  prompt='''translate the search query into English according to an ecommerce store and reply in json format.{"Product_category":[text],"Max-price":long,"attributes":text,"Similar-categories":[text],"BrandName":[text] , "converted-english_query"="if the querry is other than english language convert it to english language and correctly structure the search"}.  Product categories are : 	Fashion , Grocery,Smartphone,Electronics,Hardware,Fragrance. Do you understand?'''
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

def main():
    st.title("Search Myntra Fashion Products")

    # Input: User enters search query
    search_query = st.text_input("Enter your search query")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = product_search(search_query,client)

            # Display search results
            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['ProductName']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Description: {result['_source']['Description']}")
                        except Exception as e:
                            print(e)
                        try:
                            st.write(f"Description: {result['_source']['Description']}")
                        except Exception as e:
                            print(e)
                        st.divider()
if __name__ == "__main__":
    main()