Grocery={
    "properties":{
        "pid":{
            "type":"text"
        },
        "Name": {
            "type": "text"
        },
        "Brand": {
            "type":"text"
        },
        "Price":{
            "type" : "long"
        },
        "DiscountedPrice":{
            "type" : "long"
        },
        "imageurl":{
            "type": "text"
        },
        "Quantity":{
            "type": "text"
        },
        "Category":{
            "type": "text"
        },
        "SubCategory":{
                "type": "text"
        } ,
        "search":{
            "type": "text"
        },
        "searchvector":{
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "l2_norm"
        }
    }
}
Fashion ={
    "properties":{
        "ProductID":{
            "type":"long"
        },
        "ProductName":{
            "type":"text"
        },
        "ProductBrand":{
            "type":"text"
        },
        "Gender":{
            "type":"text"
        },
        "Price (INR)":{
            "type":"long"
        },
        "NumImages":{
            "type":"long"
        },
        "Description":{
            "type":"text"
        },
        "PrimaryColor":{
            "type":"text"
        },
        "search":{
            "type":"text"
        },
        "DescriptionVector":{
            "type":"dense_vector",
            "dims": 768,
            "index":True,
            "similarity": "l2_norm"
        }

    }
}
Electronics={
    "properties":{
        "pid":{
            "type":"text"
        },
        "name":{
            "type":"text"
        },
        "main_category":{
            "type": "text"
        },
        "sub_category":{
            "type":"text"
        },
        "image":{
            "type":"text"
        },
        "discount_price":{
            "type":"long"
        },
        "actual_price":{
            "type":"long"
        },
        "search":{
            "type":"text"
        },
        "searchvector":{
            "type":"dense_vector",
            "dims":768,
            "index":True,
            "similarity":"l2_norm"
        }
    }
}
Smartphones={
    "properties":{
        "pid":{
            "type":"text"
        },
        "title":{
            "type":"text"
        },
        "ram":{
            "type":"text"
        },
        "brand":{
            "type":"text"
        },
        "product_id":{
            "type":"text"
        },
        "highlights":{
            "type":"text"
        },
        "selling_price":{
            "type":"long"
        },
        "original_price":{
            "type":"long"
        },
        "search":{
            "type":"text"
        },
        "searchvector":{
            "type":"dense_vector",
            "dims":768,
            "index":True,
            "similarity":"l2_norm"
        }
    }
}
Fragrance={
    "properties":{
        "pid":{
            "type":"text"
        },
        "name":{
            "type":"text"
        },
        "description":{
            "type":"text"
        },
        "price":{
            "type":"long"
        },
        "compare_price":{
            "type":"text"
        },
        "categories":{
            "type":"text"
        },
        "weight":{
            "type":"long"
        },
        "image1":{
            "type":"text"
        },
        "brand_name":{
            "type":"text"
        },
        "search":{
            "type":"text"
        },
        "searchvector":{
            "type":"dense_vector",
            "dims":768,
            "index":True,
            "similarity":"l2_norm"
        }
    }
}
Hardware={
    "properties":
    {
        "ID":{
            "type":"long"
        },
        "Name":{
            "type":"text"
        },
        "Short description":{
            "type":"text"
        },
        "Description":{
            "type":"text"
        },
        "Sale price":{
            "type":"long"
        },
        "Regular price":{
            "type": "long"
        },
        "Categories":{
            "type": "text"
        },
        "Tags":{
            "type":"text"
        },
        "images":{
            "type":"text"
        },
        "search":{
            "type":"text"
        },
        "searchvector":{
            "type":"dense_vector",
            "dims":768,
            "index":True,
            "similarity":"l2_norm"
        }
    }
}