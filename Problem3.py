import requests as req
from lxml import html
import json

def parseOrg(str, dict):
    '''Parses the first column and extracts organisation name'''
    str=str.strip()
    str=str.replace(':','')
    info=str.split('-')
    dict['office_name']=info[0]

def parseOrgAddress(str, dict):
    '''Parses the organisation address and extracts address, city, state and zip'''
    str=str.strip()
    address=str.split('\n')
    street=address[0].strip()
    dict['office_address']=street
    cityInfo=address[-1].strip()
    if ',' in cityInfo:
        city=cityInfo.split(',')[0]
        dict['office_city']=city
        state=cityInfo.split(',')[1].strip()
        state=state.split(' ')[0]
        zip=cityInfo.split(',')[1].strip().split(' ')[1]
        dict['office_state']=state
        dict['office_zip']=zip
    else:   #last row of the extracted data breaks the preset pattern for address nomenclature
        dataList=cityInfo.split(' ')
        cityName=''
        for i in range(len(dataList)-2):
            cityName+=dataList[i]+' '
        dict['office_city']=cityName[:-1]
        dict['office_state']=dataList[2]
        dict['office_zip']=dataList[-1]

    #print(list(str))


def parseMail(str,dict):
    '''Parses the organisations mailing address and extracts address, city, state and zip'''
    str=str.strip()
    address=str.split('\n')
    val=address[0].strip()
    if 'P.O.' in val:
        dict['mail_pobox']=val
        dict['mail_address']=None
    else:
        dict['mail_pobox']=None
        dict['mail_address']=val

    cityInfo=address[-1].strip()
    if ',' in cityInfo:
        city=cityInfo.split(',')[0]
        dict['mail_city']=city
        state=cityInfo.split(',')[1].strip()
        state=state.split(' ')[0]
        zip=cityInfo.split(',')[1].strip().split(' ')[1]
        dict['mail_state']=state
        dict['mail_zip']=zip
    else:   #last row of the extracted data breaks the preset pattern for address nomenclature
        dataList=cityInfo.split(' ')
        cityName=''
        for i in range(len(dataList)-2):
            cityName+=dataList[i]+' '
        dict['mail_city']=cityName[:-1]
        dict['mail_state']=dataList[2]
        dict['mail_zip']=dataList[-1]


def parseContact(str,dict):
    '''Extracts contact information '''
    str=str.strip()
    if str is None or len(str)==0:
        dict['mail_phone']=None
    else:
        str=str.replace(' ','').replace('\n',' ')       # first value contains two phone numbers, this parse is for that specifically
        dict['mail_phone']=str

def parseEmail(str, dict):
    '''Extracts the email id if present'''
    str=str.strip()
    if str is None or len(str)==0:
        dict['office_link']=None
    else:
        dict['office_link']=str


def parse(data):
    '''Helper function to parse table data. Uses supporting helper functions to parse data depending on the type and returns a dict object for the table row'''
    cells=data.xpath('td')
    dict={}
    parseOrg(cells[0].text_content(),dict)
    parseOrgAddress(cells[1].text_content(),dict)
    parseMail(cells[2].text_content(),dict)
    parseContact(cells[3].text_content(),dict)
    parseEmail(cells[4].text_content(),dict)

    return dict




def fetch():
    '''Fetches data from the html file using requests and parses the every table row using a helper function parse'''

    result=[]
    resp=req.get("https://dot.ca.gov/contact-us")
    root=html.fromstring(resp.content)
    rows=root.xpath('//*[@id="main-content"]/div/main/div[1]/div[1]/table//tr')


    for i,data in enumerate(rows):
        if i==0:
            continue
        else:
            result.append(parse(data))
    jsonObj=json.dumps(result)
    return jsonObj



if __name__=="__main__":
    print(fetch())

