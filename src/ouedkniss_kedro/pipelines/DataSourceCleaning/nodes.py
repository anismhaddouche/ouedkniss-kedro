"""
This is a boilerplate pipeline 'DataSourceCleaning'
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
    id = asset["id"]
    # Get slug 
    slug = asset["slug"]
    # Get description 
    description =  asset["description"]
    # Get if the announcement is from store or not
    isFromStore = asset["isFromStore"]
    # Get the number of like 
    likeCount = asset["likeCount"]
    # Convert 'createdAt' to a Datetime format 
    createdAt = asset["createdAt"] 
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
    asset = pd.DataFrame([id,category,slug,description,price,priceType,priceUnit,wilaya,commune,createdAt,likeCount,isFromStore]).T

    # Convert some variables  dtypes
    # TODO : create a function that convert asset
    asset =  asset.join(specs)

    asset["priceType"] = asset["priceType"].astype("category")
    asset["priceUnit"] = asset["priceUnit"].astype("category")
    asset["id"] = asset["id"].astype('int')
    asset["category"] = asset["category"].astype("category")
    asset['createdAt'] = pd.to_datetime(asset['createdAt'])
    asset["slug"] = asset["slug"].astype("string")
    asset["wilaya"] = asset["wilaya"].astype("category")
    asset["commune"] = asset["commune"].astype("category")
    asset["location_duree"] = asset["location_duree"].str.extract('(\\d)').astype('Int64')
    asset["superficie"] = asset["superficie"].str.extract('(\\d+)').astype('Int64')
    asset["pieces"] = asset["pieces"].str.extract('(\\d{1,2})').astype('Int64')
    asset["asset-in-a-promotional-site"]=asset["asset-in-a-promotional-site"].astype('bool')
    #TODO  : convert 'property-specifications' and 'papers'
    return asset



def cleaning(asset) -> pd.DataFrame : 
    """
    Clean asset data 
    """
    asset_cleaned = asset
    return asset_cleaned

    #   df = pd.DataFrame([id,category,slug,description,price,priceType,priceUnit,wilaya,commune,createdAt,likeCount,isFromStore]).T

    # # Convert some variables  dtypes
    # # TODO : create a function that convert asset
    # asset =  df.join(specs)

    # df["priceType"] = df["priceType"].astype("category")
    # df["priceUnit"] = df["priceUnit"].astype("category")
    # df["id"] = df["id"].astype('int')
    # df["category"] = df["category"].astype("category")
    # df['createdAt'] = pd.to_datetime(df['createdAt'])
    # df["slug"] = df["slug"].astype("string")
    # df["wilaya"] = df["wilaya"].astype("category")
    # df["commune"] = df["commune"].astype("category")
    # df["location_duree"] = df["location_duree"].str.extract('(\\d)').astype('Int64')

    # # Concatenate the two dataframes df and spec
    # return asset