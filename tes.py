from flask import Flask, render_template, url_for
from flask_restful import Api, Resource
from auto import googling #error
from boruto import narutoboruto

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/api")
def menu():
	return render_template("menu.html")

class Googlers(Resource):
	def get(self,name):
		hasil = googling(name)
		return {"data":hasil}

class Boruto(Resource):
	def get(self,name):
		hasil = narutoboruto(name)
		return {"data":hasil}
		
api.add_resource(Googlers,"/api/google/<string:name>")
api.add_resource(Boruto,"/api/boruto/<string:name>")

if __name__ == '__main__':
	app.run()