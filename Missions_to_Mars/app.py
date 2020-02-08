from flask import Flask, jsonify, render_template
from flask_pymongo import Pymongo
import scrape_mars

app = Flask(__name__)
mongo = Pymongo(app)

@app.route('/')
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_data = mongo.db.mars_data
    mars = scrape_mars.scrape()
    mars_data.update({}, mars, upsert=True)
    return index()

if __name__ == '__main__':
    app.run(debug=True)
