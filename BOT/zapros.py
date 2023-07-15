import requests
import json


def get_zapros(zap):  #<--Делаем API запрос и получаем новости по нужной нам теме
    final_list = []
    r = requests.get(f'https://newsdata.io/api/1/news?apikey=pub_25992e01855fd3cb256b98155755687b9e1b6&country=ru&category={zap}')
    text = json.loads(r.content)
    for i, z in text.items():
        if isinstance(z, list):
            for s in z:
                if s['link'] is not final_list:
                    final_list.append(s['link'])

    return final_list


def category(cat):  #<-- Переводим нашу категорию в тему для API
    if cat == 'government_agencies':
        return 'science'
    if cat == 'judicial':
        return 'science'
    if cat == 'financial_sphere':
        return 'business'
    if cat == 'trade':
        return 'business'
    if cat == 'crime':
        return 'politics'
    if cat == 'production':
        return 'top'
    if cat == 'transportation':
        return 'science'
    if cat == 'checked':
        return 'politics'
    if cat == 'bankruptcy':
        return 'business'
    if cat == 'rating':
        return 'top'
    if cat == 'standart':
        return 'top'
    if cat == 'social':
        return 'science'
    if cat == 'service':
        return 'food'
    if cat == 'deal':
        return 'business'
    if cat == 'investments':
        return 'business'
    if cat == 'ptoject':
        return 'business'
    if cat == 'risk':
        return 'business'
    if cat == 'organization_structure':
        return 'business'
    if cat == 'license':
        return 'politics'
    if cat == 'sanctions':
        return 'politics'
    if cat == 'bank':
        return 'business'
    if cat == 'CP':
        return 'science'
    if cat == 'sport':
        return 'sports'
    if cat == 'medicine':
        return 'health'
    if cat == 'culture':
        return 'entertainment'
    if cat == 'honor':
        return 'top'
    if cat == 'family':
        return 'tourism'
    if cat == 'science':
        return 'science'
    if cat == 'top':
        return 'world'
    if cat == 'weather':
        return 'science'
    if cat == 'education':
        return 'science'
    if cat == 'metallurgy':
        return 'business'
    if cat == 'internet':
        return 'top'
    if cat == 'chemical':
        return 'science'
    if cat == 'gold':
        return 'science'
    if cat == 'agriculture':
        return 'top'
    if cat == 'food':
        return 'top'
    if cat == 'paper':
        return 'environment'
    if cat == 'cloth':
        return 'top'
    if cat == 'construction':
        return 'business'
    if cat == 'resources':
        return 'business'
