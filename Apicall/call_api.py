"""call api from this python script"""

import requests
import json



def xml_to_api():

    input_file = "input.xml"
    data = {
        'voucher_type': 'Receipt'
    }

    headers = {"Content-Type": "multipart/form-data"}
    
    url = 'http://127.0.0.1:8000/xml_to_excel_api'
    with open(input_file) as xml:
        file_obj = {'file': xml}
        response = requests.post(url,files=file_obj,data=data)
        print(response.text)
    
xml_to_api()


""""Developed by Matesh Divekar 07-08-2022"""