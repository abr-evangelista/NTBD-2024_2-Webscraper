import time
import re
import requests
from bs4 import BeautifulSoup

# URL da página
base_url = 'https://www.carpages.ca/'

# url_cars = 'https://www.guiadoautomovel.pt/marcashttps://www.guiadoautomovel.pt/marcas'

# Fazer a requisição HTTP
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}

#Adiciona Kilometragem a lista de carros especificamente no dicionario
def addMileage(listCars):
    
    for listCar in listCars:
        link = listCar['namelink']

        time.sleep(2)
        itemLink = BeautifulSoup(requests.get(base_url.rstrip('/') + '/' + link.lstrip('/'), headers=headers).content, 'html.parser')


        mileage = itemLink.find('span', title = re.compile('KM'))
        

        if mileage:
            listCar['mileage'] = mileage.text
        else:
            listCar['mileage'] = '0 KM'

#Lista os carros em uma página
def accessPageCars (soup):
    
    cars = soup.find_all(class_ = 't-flex t-gap-6 t-items-start t-p-6')

    listCars = []

    for car in cars:
        nameCar = car.find('h4', class_ = 'hN').find('a').get('title')
        descriptionCar = car.find('h5').get_text(strip=True)
        link =  car.find('h4', class_ = 'hN').find('a').get('href')

        car = {
            'name': nameCar,
            'description': descriptionCar,
            'namelink': link,
            'mileage': ''
        }

        listCars.append(car)
    
    return listCars

def nextPage(soup):
    #Botao da próxima página
    nextPages = soup.find('a', {'title':'Next Page'})
    #Checagem se há próxima página
    if not nextPages:
        return None

    next_url = nextPages.get('href')

    return base_url.rstrip('/') + '/' + next_url.lstrip('/')

#Lista as categorias sendo cada uma delas um objeto
def linksCategory(soup):
        links = soup.find_all(class_='category__link')

        categorys = []

    # Exibir os links
        for link in links:
            nameCategory = link.find('span', class_ = 'category__label').get_text(strip = True)
            href = link.get('href')

            category = {
            'name': nameCategory,
            'link': href
            }
            
            categorys.append(category)

        return categorys






#Acesso a página principal
responseMain = requests.get(base_url, headers=headers)

#Acesso as marcas de carros
# responseCarsList = requests.get(url_cars, headers=headers)

#Lista de marcas de carros

#Verificar se a requisição foi bem-sucedida
# if(responseCarsList.status_code == 200):
#     soupCars = BeautifulSoup(responseCarsList.content, 'html.parser')
#     carMark = soupCars.find('div', class_ = 'cada-marca').find('h2').get_text(strip=True)
#     print(carMark)

# else:
#     print(f"Erro ao acessar a página: {responseCarsList.status_code}")


# Verificar se a requisição foi bem-sucedida
if responseMain.status_code == 200:
    soupMain = BeautifulSoup(responseMain.content, 'html.parser')

    linksCategory = linksCategory(soupMain) 

    for item in linksCategory:
        flag = False

        current_url = item['link']

        

        while True:
            listCarsPages = BeautifulSoup(requests.get(current_url, headers=headers).content, 'html.parser')


            if not flag:
                accessPageCars(listCarsPages)
            
            flag = True

            pageForCategory = BeautifulSoup(requests.get(current_url, headers=headers).content, 'html.parser')

            current_url = nextPage(pageForCategory)

            if not current_url:
                break
            
            listCars =  accessPageCars(listCarsPages)

            addMileage(listCars)

            

else:
    print(f"Erro ao acessar a página: {responseMain.status_code}")


