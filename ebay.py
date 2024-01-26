import requests
import json
import regex as re
from bs4 import BeautifulSoup

def api_request(marke, itemid):
    review_url = f'https://www.ebay.com/fdbk/update_feedback_profile?url=username%3D{marke}%26sort%3DTIME%26filter%3Dfeedback_page%253ARECEIVED_AS_SELLER%252Cperiod%253AAll%252Cimage_filter%253Afalse%26q%3D{itemid}%26page_id%3D1%26limit%3D1000&module=modules%3DFEEDBACK_SUMMARY_V2'

    response = requests.get(review_url)

    if response.status_code == 200:
        # Parse the JSON response
        input_dict = response.json() 
        #rating = []
        outputs = []
        for x in input_dict['modules']['FEEDBACK_SUMMARY_V2']['feedbackView']['feedbackCards']:
            #rating.append(x['feedbackInfo']['rating']['name'])
            text = x['feedbackInfo']['comment']['accessibilityText']
            outputs.append({"review": text.strip()})
        with open("ebay.json", "w") as f:
            json.dump(outputs, f)
        
    else:
        print("API Zugriff fehlgeschlagen")
        print(f'Error: {response.status_code}') 


def noproductpage(url):
    regex = r'https:\/\/www\.ebay\.com\/fdbk\/feedback_profile\/([^?&\/]+).*?q=(\d+)'
    match = re.search(regex, url)
    if match != None:
        marke = match.group(1)
        itemid = match.group(2)
        if marke != None or itemid != None:
            api_request(marke, itemid)
        else:
            print("Not the right page")
    else:
        print('Keine Produktbezogene Seite')

    


def ebay_connect(url, response):
    soup = BeautifulSoup(response.content, 'lxml')
    div = soup.find('div', class_="d-stores-info-categories__container__info__section")
    if div == None:
        noproductpage(url)
        return
    markespan = div.find('span', class_="ux-textspans ux-textspans--BOLD")
    if markespan == None:
        noproductpage(url)
        return
    marke = markespan.text.strip()


    regex = r"itm\/([0-9]+)"
    match = re.search(regex, url)
    itemid = match.group(1)

    if itemid == None:
        noproductpage(url)
        return
 
    api_request(marke, itemid)

def ebay(url):

    header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url, headers = header)

    if response.status_code == 200:
        ebay_connect(url, response)
    else:
        print("Link nicht erreichbar")
        print(f'Error: {response.status_code}')



ebay("https://www.ebay.com/fdbk/feedback_profile/zone_tech_auto?filter=feedback_page%3ARECEIVED_AS_SELLER&q=202072206777&sort=RELEVANCE")

