import requests
from bs4 import BeautifulSoup

def googling(pesan):
	query = pesan
	pesan=""
	url = 'https://www.google.com/search?q={}&ie=UTF-8'.format(query)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	source=requests.get(url, headers=headers).text
	print(source);input()
	soup = BeautifulSoup(source, 'html.parser')
	try:
		text2 = soup.find("h2",text="Deskripsi").findNext('span')
		pesan += text2.get_text()
		if len(text2.get_text())<40:
			pesan += text2.findNext('span').get_text()+"\n"
			text2 = text2.findNext('span')
		if len(text2.get_text())<40:
			pesan += text2.findNext('span').get_text()+"\n"
			text2 = text2.findNext('span')
		if len(text2.get_text())<40:
			pesan += text2.findNext('span').get_text()+"\n"
			text2 = text2.findNext('span')

		text = soup.find_all("div","rVusze")
		if text!=[]:
			pesan += "\n\n-----Detail-----\n"
			for x in text:
				pesan += x.get_text()+"\n"

		return [pesan],"google"
	except:
		try:
			pesan = soup.find("a","FLP8od").get_text()
			return [pesan],"google"
		except:
			text = soup.find_all("div","ujudUb")
			if len(text)!=0:
				ignore = soup.find("div","ujudUb WRZytc OULBYb").text
				pesan += "Judul: "+soup.find("h2","qrShPb kno-ecr-pt PZPZlf mfMhoc").get_text()+"\nGrup/Penyanyi: "+soup.find("div","wwUB2c PZPZlf").get_text()+"\n\n"
				for x in text:
					if x.text == ignore:
						continue
					for y in x.find_all("span"):
						pesan += y.get_text()+"\n"
					pesan += "\n"
				pesans = [pesan]
				if len(pesan)>=4095:
					pesans = []
					for y in range(4095,0,-1):
						if pesan[y]==" ":
							pesans.append(pesan[:y])
							pesans.append(pesan[y+1:])
							break
				return pesans,"lirik"
			else:
				try:
					text = soup.find("span","aCOpRe").get_text()
					pesan += "Saya tidak begitu mengerti, tapi saya menemukan ini. Semoga membantu ya 🙂\n\n"
					
					if len(text)>0:
						pesan += text
					else:
						pesan += soup.find("span","hgKElc").get_text()
					return [pesan],"google"
				except:
					pesan = "Saya tidak menemukan apapun 😕\n"
					return [pesan],"google"
if __name__ == '__main__':
	googling("hello")