import requests
from bs4 import BeautifulSoup

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




# URL da página
url = 'https://www.carpages.ca/'

url_cars = 'https://www.guiadoautomovel.pt/marcashttps://www.guiadoautomovel.pt/marcas'

# Fazer a requisição HTTP
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}

#Acesso a página principal
responseMain = requests.get(url, headers=headers)

#Acesso as marcas de carros
responseCarsList = requests.get(url_cars, headers=headers)

#Lista de marcas de carros

#Verificar se a requisição foi bem-sucedida
if(responseCarsList.status_code == 200):
    soupCars = BeautifulSoup(responseCarsList.content, 'html.parser')
    carsMarks = soupCars.find('div', class_ = 'todas-marcas')
    carMark = carsMarks.find('div', class_ = 'cada-marca').find('h2')
    # carMarks = carsTag.get_text(strip = True)
    print(carMark)

else
    print(f"Erro ao acessar a página: {responseCarsList.status_code}")

# Verificar se a requisição foi bem-sucedida
if responseMain.status_code == 200:
    soupMain = BeautifulSoup(responseMain.content, 'html.parser')

    linksCategory = linksCategory(soupMain) 

    for item in linksCategory:
        pageForCategory = BeautifulSoup(requests.get(item['link'], headers=headers).content, 'html.parser')


    

else:
    print(f"Erro ao acessar a página: {responseMain.status_code}")


