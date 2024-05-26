import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import IndexMapping

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic","lZTCy6LyxmszTk2DPqAV"),
    verify_certs=False,
)
es.ping()
es.info()

model = SentenceTransformer('all-mpnet-base-v2')

class catalogue():
    def __init__(self,ElasticsearchObject,TransformerModel,IndexMapping):
        self.es=ElasticsearchObject
        self.model=TransformerModel
        self.IndexMapping=IndexMapping
    def get_embedding(text):
        text = text.replace("\n", " ")
        return self.model.encode(text)
    def catalogue_input(self):
        def fashion(self,inputpath,outputpath):
            df=pd.read_csv(inputpath)
            df.dropna(inplace=True)
            df.shape
            df.head()
            df["search"]=df['ProductName']+df['Description']
            df.head(1)
            df['searchvector']= df['search'].apply(lambda x : self.model.encode(x))
            df.head(2)
            df.to_csv(outputpath)
            self.es.indices.create(index="fashion", mappings=self.IndexMapping.Fashion)
        def grocery(self,inputpath,outputpath):
            df=pd.read_csv(inputpath)
            df.dropna(inplace=True)
            df.shape
            df.head()
            df["search"]=df['ProductName']+df['Description']
            df.head(1)
            df['searchvector']= df['search'].apply(lambda x : self.model.encode(x))
            df.head(2)
            df.to_csv(outputpath)
            self.es.indices.create(index="grocery", mappings=self.IndexMapping.Grocery)
        def fragrance(self,inputpath,outputpath):
            df=pd.read_excel(inputpath)
            df.dropna(inplace=True)
            df.shape
            df.head()
            df["search"]=df['name']+df['description']
            df.head(1)
            df['searchvector']= df['search'].apply(lambda x : self.model.encode(x))
            df.head(2)
            df.to_csv(outputpath)
            self.es.indices.create(index="fragrance", mappings=self.IndexMapping.Fragrance)
        def electronics(self,inputpath,outputpath):
            df=pd.read_csv(inputpath)
            df.dropna(inplace=True)
            df.shape
            df.head()
            df["search"]=df['name']
            df.head(1)
            df['searchvector']= df['search'].apply(lambda x : self.model.encode(x))
            df.head(2)
            df.to_csv(outputpath)
            self.es.indices.create(index="electronics", mappings=self.IndexMapping.Electronics )
        def hardware(self,inputpath,outputpath):
            df=pd.read_csv(inputpath)
            df.dropna(inplace=True)
            df.shape
            df.head()
            df["search"]=df['Name']+df['Description']
            df.head(1)
            df['searchvector']= df['search'].apply(lambda x : self.model.encode(x))
            df.head(2)
            df.to_csv(outputpath)
            self.es.indices.create(index="hardware", mappings=self.IndexMapping.Hardware )
        def smartphones(self,inputpath,outputpath):
            df=pd.read_csv(inputpath)
            df.dropna(inplace=True)
            df.shape
            df.head()
            df["search"]=df['title']+df['highlights']
            df.head(1)
            df['searchvector']= df['search'].apply(lambda x : self.model.encode(x))
            df.head(2)
            df.to_csv(outputpath)
            self.es.indices.create(index="smartphones", mappings=self.IndexMapping.Smartphones )

                    