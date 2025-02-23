import requests
from bs4 import BeautifulSoup

# URL da página
url = 'https://www.carpages.ca/'

# Fazer a requisição HTTP
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar todas as tags <a>
    links = soup.find_all(class_='category__link')

    # Criar uma lista com os href dos links
    hrefs = [link.get('href') for link in links if link.get('href')]

    # Exibir os links
    for href in hrefs:
        soup_body_style = BeautifulSoup(requests.get(href).content, 'html.parser')
        print(soup_body_style)

else:
    print(f"Erro ao acessar a página: {response.status_code}")