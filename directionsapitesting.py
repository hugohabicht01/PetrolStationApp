import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from pprint import pprint



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


api_key = os.getenv('GOOGLE_API_KEY')


# url = f"https://maps.googleapis.com/maps/api/directions/json?origin=Hanau+Haendelstrasse+Germany&destination=TF107BL+UK&key={api_key}"
url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=Haendelstrasse+Hanau+Germany&destinations=Frankfurt+Vilbeler+Landstrasse+Tankcenter&key={api_key}"

req = requests.get(url)

pprint(req.json())
