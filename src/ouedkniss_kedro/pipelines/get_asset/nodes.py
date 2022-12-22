"""
This is a boilerplate pipeline 'get_asset'
 using Kedro 0.18.4
"""

import pandas as pd 


def get_commune(x : list):
    #x = list_to_dict(x)
    try :
        commune = x[0]['name']
    except: 
        commune = None
    return commune


def get_wilaya(x : list):
    #x = list_to_dict(x)
    try :
        wilaya = x[0]['region']['name']
    except: 
        wilaya = None
    return wilaya


def get_medias(column:pd.Series) -> pd.Series:
    """
    In this dataset medias means urls of the annoucements. We create a new column containing a list of avaible urls
    """
    media_all= []
    for index,_ in column.items():
        media_raw = []
        for _, media in enumerate(column.loc[index]):
            try : 
                media_raw.append(media['mediaUrl'])
            except:
                media_raw.append(None)
        media_all.append(media_raw)   
    return pd.Series(media_all)


def get_specs(column : pd.Series) -> pd.DataFrame : 
    """
    Extract the following specification from the column "specs" :
        location_duree, superficie,	pieces,	asset-in-a-promotional-site	property-specifications,	papers,	etages	sale-by-real-estate-agent,	property-payment-conditions
    """

    specs_all = [] 
    # Loop on all rows
    for index,_ in column.items():
        specs_raw = {}
        for i, spec in enumerate(column.loc[index]):
            label = spec["specification"]['codename']
            try: 
                value = spec["value"]
                if len(value) == 1:
                    value = value[0]
            except :
                value = None
             #TODO: améliorer la prise en charge str(value)   
            specs_raw[label] = str(value)
        specs_all.append(specs_raw)
    return pd.DataFrame(specs_all)


def get_asset(data) -> pd.DataFrame:
    """Preprocesses the data of announcements.

    Args:
        data: Raw data.
    Returns:
        asset : Intermediate data
       
    """
    # Convert Data, which is a list of lists, into one flatten list 
    asset = pd.DataFrame([item for sublist in data for item in sublist]) 

    # Get id 
    idx = asset["id"]
    # Get slug 
    slug = asset["slug"]
    # Get description 
    description =  asset["description"]
    # Get if the announcement is from store or not
    isFromStore = asset["isFromStore"]
    # Get the number of like 
    likeCount = asset["likeCount"]
    # Convert 'createdAt' to a Datetime format 
    createdAt = pd.to_datetime(asset['createdAt'])
    #Convert each raw of 'category', which is a dict (eg : {"name": "Appartement"}), to a sting  (eg :"Appartement")
    category = asset["category"].apply(lambda x :x["name"])
    #Get the commune 
    commune = asset["cities"].apply(lambda x : get_commune(x)).rename("commune")
    #Get the wilaya
    wilaya = asset["cities"].apply(lambda x : get_wilaya(x)).rename("wilaya")
    #Get the Store name 
    store = asset["store"].apply(lambda x : x.get('slug') if x != None else None)
    # Convert PriceType to a categorical data 
    priceType = asset["priceType"]
    # Get the price in million
    price = asset["price"]
    # Get the Unit price 
    priceUnit = asset["priceUnit"]
    # Get medias (urls)
    medias = get_medias(asset["medias"])
    # Get some specification in a DataFrame
    specs = get_specs(asset["specs"])
    specs["medias"] = medias
    # Create the outout DataFrame
    df_1 = pd.DataFrame([idx,category,slug,description,price,priceType,priceUnit,wilaya,commune,createdAt,likeCount,isFromStore]).T
    # Convert some variable 
    df_1["priceType"] = df_1["priceType"].astype("category")
    df_1["priceUnit"] = df_1["priceUnit"].astype("category")

    return df_1.join(specs)