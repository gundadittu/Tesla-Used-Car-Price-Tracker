import requests
import json 

url_list = [
	"https://www.tesla.com/used/5YJSA1E14GF169821", 
	# "https://www.tesla.com/used/5YJSA1E11GF174829?region=CA&postal=94591&coord=38.1165,-122.2091&redirect=no",
	# "https://www.tesla.com/used/5YJSA1E12HF181290?region=CA&postal=94591&coord=38.1165,-122.2091&redirect=no", 
	# "https://www.tesla.com/used/5YJSA1E18GF156036?region=CA&postal=95131&coord=37.3902956,-121.8961047&redirect=no"
]

def find_first_char_occurrence(str1, ch): 
	for i in range(len(str1)):
		if str1[i] == ch:
			return i

	return None

for url in url_list:
	page = requests.get(url)
	content = page.content
	content = content.decode('utf8')
	print(content)
	
	start_marker =  "\"vehicle\""
	start_index = content.find(start_marker)+10
	
	token_index = content[start_index:].find("\"token\"")
	end_index = start_index + token_index
	
	end_marker =  "}"
	first_oc = find_first_char_occurrence(content[end_index:], end_marker)
	end_index += first_oc if first_oc != None else 0 
	
	inventory_details = content[start_index: end_index]
	inventory_details =""+inventory_details+"}" # properly end dictionary structure

	vehicle_data = json.loads(inventory_details)

	# print(vehicle_data)