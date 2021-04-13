import json

r = {'schedule': ['@start']}
with open('datajs.json', 'w', encoding='utf-8') as file:
    json.dump(r, file)
with open('datajs.json', 'r', encoding='utf-8') as file:
    r = json.load(file)
print(r)