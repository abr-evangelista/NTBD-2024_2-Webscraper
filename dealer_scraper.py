import json
import re
import requests
from bs4 import BeautifulSoup

dealerCount = 1

# URL da página
base_url = 'https://www.carpages.ca/'

# Fazer a requisição HTTP
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}

#Lista os dealers em uma página
def accessPageDealer (soup):
    
    dealers = soup.find_all(class_ = re.compile(r"^media media--1-5 soft push-none.*"))

    listDealers = []

    for dealer in dealers:
        link = dealer.find('a').get('href')

        global dealerCount
        print(str(dealerCount) + ": " + base_url.rstrip('/') + '/' + link.lstrip('/'))
        dealerCount += 1
        try:
            response = requests.get(base_url.rstrip('/') + '/' + link.lstrip('/'), headers=headers)
        
        
            if (response.url != base_url.rstrip('/') + '/' + link.lstrip('/')):
                continue
            dealerPage = BeautifulSoup(response.content, 'html.parser')

            #dealerPage.find('div', class_ = "main-container").find(class_ = "t-col-span-full laptop:t-col-span-4 print:t-hidden")

            nameDealer = dealerPage.find('div', class_ = "main-container").find(class_ = "t-col-span-full laptop:t-col-span-4 print:t-hidden").find(class_ = 'hgroup push-half-top').find('h1', class_ = 'hN gamma weight-heavy').get_text(strip=True)
            if dealerPage.find('div', class_ = "main-container").find(class_ = "t-col-span-full laptop:t-col-span-4 print:t-hidden").find(id_ = 'bfh-widget'):
                bfh = True
            else:
                bfh = False
            local = dealerPage.find('div', class_ = "main-container").find(class_ = "t-col-span-full laptop:t-col-span-4 print:t-hidden").find(class_ = 'hN epsilon').find('span', class_ = 'push-quarter-left').get_text(strip=True)

            dealer = {
                'name': nameDealer,
                'localization': local,
                'bfh': bfh
            }

            listDealers.append(dealer)
        except Exception as e:
            print(f"An error occurred: {e}. Checking other dealers")
            continue
    
    return listDealers

def nextPage(soup):
    #Botao da próxima página
    nextPages = soup.find('a', {'title':'Next Page'})
    #Checagem se há próxima página
    if not nextPages:
        return None

    next_url = nextPages.get('href')

    return base_url.rstrip('/') + '/' + next_url.lstrip('/')


#Acesso a página principal
responseMain = requests.get(base_url.rstrip('/') + '/' + "search/", headers=headers)

# Verificar se a requisição foi bem-sucedida
if responseMain.status_code == 200:

    current_url = base_url.rstrip('/') + "/dealer/search/"
    listDealers = []

    while dealerCount < 50:
        listDealerPages = BeautifulSoup(requests.get(current_url, headers=headers).content, 'html.parser')

        listDealers.append(accessPageDealer(listDealerPages))

        print(current_url)

        current_url = nextPage(listDealerPages)

        if not current_url:
            break

    print("over!")    

    with open("rawdealerdata.json", "w") as file:
        json.dump(listDealers, file)

else:
    print(f"Erro ao acessar a página: {responseMain.status_code}")


