import requests
from bs4 import BeautifulSoup
def narutoboruto(selectt=0):
	url = "https://anoboy.stream/category/boruto-naruto-next-generations/"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	source=requests.get(url, headers=headers).text
	soup = BeautifulSoup(source, 'html.parser')
	hasil = soup.find("div","column-content").find_all("a")[:-5]

	try:
		selectt = int(selectt)
	except Exception as e:
		selectt = 0

	temp = {}
	for x in hasil:
		temp[x["title"].split(" ")[-1]] = [x["href"],x["title"]]

	url = ""
	teks = ""
	if int(hasil[0]["title"].split(" ")[-1])-14<=selectt<=int(hasil[0]["title"].split(" ")[-1]):
		url = temp[str(selectt)][0]
	else:
		teks = f'Hanya bisa melihat 15 episode terbaru({int(hasil[0]["title"].split(" ")[-1])-14}-{int(hasil[0]["title"].split(" ")[-1])})'
		selectt = hasil[0]["title"].split(" ")[-1]
		url = temp[selectt][0]

	source=requests.get(url, headers=headers).text
	soup = BeautifulSoup(source, 'html.parser')
	link = soup.find("video","video-js vjs-default-skin").source["src"]

	return [temp[str(selectt)][1],link,teks]

if __name__ == '__main__':
	print(narutoboruto(189))