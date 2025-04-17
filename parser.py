from bs4 import BeautifulSoup
import requests as r

url = 'https://www.alenka.ru/catalog/'

res = r.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
products = soup.find_all('div', 's-card')

result = []

for product in products:
    text = product.find('a', 's-card-body-title').text.split(' ')
    category = text[0]
    name = ''
    if 'гр' in text[-1]:
        name = ' '.join(text[1:-2])
    else:
        name = ' '.join(text[1:])
    name = name.replace(',', '')

    price, amount = product.find('span', 's-card-body-price-title-old-current').text.split()
    amount = amount.split('/')[1]
    image = 'https://www.alenka.ru' + product.find('img').attrs['data-src']
    data = {
        'name': name,
        'category': category,
        'price': price,
        'amount': amount,
        'image': image,
    }
    