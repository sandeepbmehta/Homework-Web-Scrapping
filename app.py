from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = mongo.db.mars_collection.find_one()
    return render_template("index.html", mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_collection = mongo.db.mars_collection
    mars_data = scrape_mars.scrape_info()
    mars_collection.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/")

# Route that will trigger the scrape function
@app.route("/hem")
def hemisphere():
    mars_data = mongo.db.mars_collection.find_one()
    #print(mars_data)
    return render_template("Mars-latest-images.html", mars_data=mars_data)

if __name__ == "__main__":
    app.run(debug=True)
