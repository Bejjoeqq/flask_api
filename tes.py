from flask import Flask, render_template, url_for,json,make_response,jsonify
from flask_restful import Api, Resource
from data import cari_nama,detail
from scrape import lirik

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/api")
def menu():
	return render_template("menu.html")

class Cari_mahasiswa(Resource):
	def get(self,name):
		resultdata = {
	        "status" : 200,
	        "message" : "",
	        "result" : []
	        }
		nim,nama = cari_nama(name)
		if nim and nama:
			resultdata["message"] = "success"
			for x in range(len(nim)):
				resultdata["result"].append({
					"nim" : nim[x],
					"nama" : nama[x]
					})
		else:
			resultdata = {
		        "status" : 404,
		        "message" : "not found"
		        }
		return jsonify(**resultdata)

class Detail_mahasiswa(Resource):
	def get(self,name):
		try:
			resultdata = detail(name,False)
		except:
			resultdata = {
		        "status" : 404,
		        "message" : "not found"
		        }
		return jsonify(**resultdata)

class Detail_mahasiswa_full(Resource):
	def get(self,name):
		try:
			resultdata = detail(name)
		except:
			resultdata = {
		        "status" : 404,
		        "message" : "not found"
		        }
		return jsonify(**resultdata)

class Lirik_google(Resource):
	def get(self,name):
		try:
			resultdata = {
		        "status" : 200,
		        "message" : "success",
		        "result" : {
			        "judul" : "",
			        "lirik" : ""
			        }
		        }
			lagu = lirik(name)
			resultdata["result"]["judul"] = lagu[0]
			resultdata["result"]["lirik"] = lagu[1]
		except:
			resultdata = {
		        "status" : 404,
		        "message" : "not found"
		        }
		return jsonify(**resultdata)

api.add_resource(Cari_mahasiswa,"/api/carimhs/<string:name>")
api.add_resource(Detail_mahasiswa,"/api/detailmhs/<string:name>")
api.add_resource(Detail_mahasiswa_full,"/api/detailmhs/<string:name>/full")
api.add_resource(Lirik_google,"/api/lirik/<string:name>")

if __name__ == '__main__':
	app.run()