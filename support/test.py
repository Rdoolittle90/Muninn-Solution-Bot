import requests

request = requests.get(url="https://finder.cstone.space/FPSArmors?type=Arms")

content = request.content

print(content)