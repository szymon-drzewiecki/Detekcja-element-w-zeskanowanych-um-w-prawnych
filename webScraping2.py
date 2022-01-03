from bs4 import BeautifulSoup
from requests import get
import time
import random
def searchForACompanyName(ListOfNumbers):
    #accesing the home page for anti-crawling
    time.sleep(5.4)
    URL = 'https://krs-pobierz.pl'
    page = get(URL)

    listOfNames = []
    listOfRegon = []
    listOfNIP = []
    
    for number in ListOfNumbers:
        randomTime = random.randint(4,15)
        time.sleep(randomTime)
        URL = 'https://krs-pobierz.pl/szukaj?q={}'.format(number)
        page = get(URL)
        bs = BeautifulSoup(page.content, 'html.parser')
        isNIPokay = bs.find('section', attrs = {'class':'details darkerBg'})
        if isNIPokay != None:
            nameTextBracket = isNIPokay.find('div', attrs = {'class':'col-xs-12'})
            listOfNames.append(nameTextBracket.find('h1').get_text().strip())
        else:
            print("Nieprawidłowy numer NIP")
    return listOfNames



def searchForACompanyInfo(ListOfNumbers):
    #accesing the home page for anti-crawling
    time.sleep(1.5)
    URL = 'https://aleo.com/pl/'
    page = get(URL)

    listOfNames = []
    listOfNIPS = []
    listOfREGONS = []
    
    for number in ListOfNumbers:
        randomTime = random.randint(2,4)
        time.sleep(randomTime)
        URL = 'https://aleo.com/pl/firmy?phrase={}&showAuthorityPlate=true'.format(number)
        page = get(URL)
        bs = BeautifulSoup(page.content, 'html.parser')
        isNIPokay = bs.find('table', attrs = {'class':'table_system_components table_system_components_rwd'})
        if isNIPokay != None:
            nameTextBracket = isNIPokay.find('h3', attrs = {'class':'title'})
            listOfNames.append(nameTextBracket.find('a').get_text().strip())
            numbersBracket = isNIPokay.find('div', attrs = {'class':'table_item_registry_identifiers'})
            NIPbracket = numbersBracket.find('div', attrs = {'class':'company_tax_identifier'})
            REGONbracket = numbersBracket.find('div', attrs = {'class':'company_economy_reg_identifier'})
            listOfNIPS.append(NIPbracket.find('strong').get_text().strip())
            listOfREGONS.append(REGONbracket.find('strong').get_text().strip())
        else:
            print("Nieprawidłowy numer NIP/REGON/KRS")
            return False
    return listOfNames, listOfNIPS, listOfREGONS