# fruta =['Morando','leon','sadler','sadler','asheley' ]
# print(fruta)

# frutas = {'Morando':'rosa','leon':'roxo','sadler':'misto','sadler':'branco','asheley':'white' }

# for chave,valor in frutas.items():
#     print(chave)
#     print(valor)
import urllib.request, json

url = 'https://api.themoviedb.org/3/movie/550?api_key=0e7423b403e951fb10ace6e5b54d06c9'

resposta = urllib.request.urlopen(url)

print(resposta)

dados = resposta.read()

jsondata = json.loads(dados)

print(jsondata['production_countries'])
