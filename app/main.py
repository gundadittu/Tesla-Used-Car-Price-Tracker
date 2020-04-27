from lxml import html
import requests
from datetime import datetime
import json 
import smtplib
from flask import Flask
from flask import render_template
from flask import request
# https://www.tesla.com/inventory/used/ms?AUTOPILOT=AUTOPILOT&Year=2016,2017&arrangeby=plh&zip=95131

def convert_vehicle_data_list_to_string(lst): 
	new_lst = []
	for item in lst: 
		new_item = ''.join([str(x)+": "+str(item[x])+'\n' for x in item])
		new_lst.append(new_item)

	return new_lst

def send_email(data, title):
	gmail_user = 'gundadittu@gmail.com'
	gmail_password = 'ctygkhaeeifltnbj'
	data = convert_vehicle_data_list_to_string(data)
	email_text = " \n||||||||||||||||||||||||||| \n\n".join(data)

	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	# start TLS for security 
	s.starttls() 
	# Authentication 
	s.login(gmail_user, gmail_password) 
	# message to be sent 
	message = 'Subject: {}\n\n{}'.format(title, email_text)
	# sending the mail 
	s.sendmail(gmail_user, gmail_user, message) 
	# terminating the session 
	s.quit()

def find_first_char_occurrence(str1, ch): 
	for i in range(len(str1)):
		if str1[i] == ch:
			return i

	return None

def parse_car_profiles(url_list):
	data = [] 
	for url in url_list:
		try:  
			page = requests.get(url)
			content = page.content

			start_marker =  "\"vehicle\""
			start_index = content.find(start_marker)

			token_index = content[start_index:].find("\"token\"")
			end_index = start_index + token_index

			end_marker =  "}"
			first_oc = find_first_char_occurrence(content[end_index:], end_marker)
			end_index += first_oc if first_oc != None else 0 

			inventory_details = content[start_index: end_index]
			inventory_details ="{"+inventory_details+"} }" # properly end dictionary structure

			json_inventory_details = json.loads(inventory_details)
			vehicle_data = json_inventory_details["vehicle"]

			price = vehicle_data["InventoryPrice"]
			mileage = vehicle_data["Odometer"]
			color = vehicle_data["PAINT"]
			history = vehicle_data["VehicleHistory"]
			year = vehicle_data["Year"]
			autopilot = ", ".join(vehicle_data["AUTOPILOT"])
			vin = vehicle_data["VIN"]
			battery = ", ".join(vehicle_data["BATTERY"])

			accessed_date_time = datetime.now().strftime("%I:%M%p on %B %d, %Y")
			item = { 
				"price": price, 
				"mileage": mileage, 
				"color": color, 
				"history": history, 
				"year": year, 
				"autopilot": autopilot, 
				"vin": vin, 
				"battery": battery,
				"url": url, 
				"dateTime": accessed_date_time
			}
			data.append(item)
		except e: 
			print("Error with "+ url)
			print(e)
			continue 

	return data 


curr_url_list = [
	"https://www.tesla.com/used/5YJSA1E14GF169821", 
	"https://www.tesla.com/used/5YJSA1E11GF174829?region=CA&postal=94591&coord=38.1165,-122.2091&redirect=no",
	"https://www.tesla.com/used/5YJSA1E12HF181290?region=CA&postal=94591&coord=38.1165,-122.2091&redirect=no"
]

app = Flask(__name__)

@app.route("/")
def execute_watchlist_update():
    results = parse_car_profiles(curr_url_list)
	send_email(results, "TESLA CPO Watchlist - "+str(len(results))+" items")
    return "Executed Watchlist Update"

if __name__ == "__main__":
    app.run()
