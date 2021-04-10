import requests
from bs4 import BeautifulSoup
def lirik(kunci):
	url = f"https://www.google.com/search?q=Lirik {kunci}&ie=UTF-8"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	source = requests.get(url, headers=headers)
	soup = BeautifulSoup(source.text,"html.parser")
	lyric = soup.find("div",{"class":"hwc"})
	judul = soup.find("div",{"class":"kCrYT"})
	return judul.text,lyric.text
	
if __name__ == '__main__':
	result = lirik("koyo ngene rasane wong nandang kangen")
	print(result[0])
	print(result[1])