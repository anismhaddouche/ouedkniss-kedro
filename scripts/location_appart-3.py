from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
from time import sleep
from random import randint


def load_query(path):
	with open(path) as f:
		return gql(f.read())

def def_var_page(page):
	return {
	  "mediaSize": "LARGE",
	  "q": None,
	  "filter": {
		"categorySlug": "immobilier-location",
		"origin": None,
		"hasPrice": True,
		"fields": [],
		"page": page,
		"count": 1000
	  }
	}

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.ouedkniss.com/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=False)

operationName = "SearchQueryWithoutFilters"

query_last_page = load_query('pagination.graphql')


result_last_page = client.execute(query_last_page,operation_name=operationName,variable_values=def_var_page(1))

lastPage = result_last_page['search']['announcements']['paginatorInfo']['lastPage']

query = load_query('datas.graphql')

i = 1
datas = []
json_file = open("results_2.json", "a")  # append mode

while i <= lastPage:
	
	result = client.execute(query,operation_name=operationName,variable_values=def_var_page(i))
	datas.append(result['search']['announcements']['data'])
	print(">",i,"/",lastPage)
	sleep(randint(1,2))
	
	i=i+1
	
json.dump(datas,json_file)
json_file.close()

