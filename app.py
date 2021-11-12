# ## Mission To Mars
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scraper

# Setup Flask App
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraped():
    mars= mongo.db.mars
    data = scraper.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)