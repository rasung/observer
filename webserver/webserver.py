from flask import Flask, render_template
import pymongo
import pandas as pd

app = Flask(__name__)

# mongodb setting
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydb"]
mycol = mydb["mycollection"]

@app.route('/')
def hello():

	res = {}
	mydoc = mycol.find({'type' : 'rank'})
	for x in mydoc:
  		res = pd.DataFrame(x['data'])
  		print(res.to_html())


	return render_template("home.html", message="Hello Flask!");

if __name__ == '__main__':
    app.run()