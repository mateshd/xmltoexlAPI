from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


import xml.etree.ElementTree as ET
import pandas as pd
import os
# Create your views here.


@api_view(['GET'])
def api_info(request):
    return Response('Hello , Call xml_to_excel_api/ for converting xml files to excel files')

@api_view(['POST'])
@parser_classes([MultiPartParser])
def xml_to_excel(request):
    "get request content "
    file = request.FILES.get('file',None)
    get_vch_type = request.data.get('voucher_type')
    if file:
        """parse xml file to read"""
        tree = ET.parse(file)
        root = tree.getroot()
        tally_msg = root[1].findall('IMPORTDATA/REQUESTDATA/TALLYMESSAGE')
        data_list = []
        for x in tally_msg:
            data = {}
            single_voucher = x.findall('VOUCHER')
            get_attrib = single_voucher[0].attrib
            """checking voucher type is recipet or other depend on request data"""
            if get_attrib.get('VCHTYPE') == get_vch_type:
                voucher = x.findall('.//VOUCHER/*')
                for i in voucher:
                    if (not(i.text and i.text.strip())):
                        data[i.tag] = 'NA'
                    elif 'DATE' in i.tag:
                        date_no = i.text
                        to_date_format = date_no[6:] + '-' + date_no[4:6] + '-' + date_no[0:4]
                        data[i.tag] = to_date_format
                    else:
                        data[i.tag] = i.text
                data_list.append(data)
        """data_list create to write excel file"""
        if data_list:
            data =pd.DataFrame.from_dict(data_list)

            #define cuurrent file path
            os.chdir('../xmltoexlAPI/output')
            dir = os.path.abspath(os.curdir)
            file = 'result.xlsx'
            file_path = os.path.join(dir,file)
            data.to_excel(file_path,index=False)
            return JsonResponse({'status': 'Excel File Created Successfully'},safe=False)
        else:
            return JsonResponse({'status': 'data file not found'},safe=False)        
    else:
        return JsonResponse({'status': 'file not Found'},safe=False)


""""Developed by Matesh Divekar 07-08-2022"""