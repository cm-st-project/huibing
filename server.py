from flask import Flask,  request, redirect, url_for, render_template
from flask_cors import CORS
app = Flask(__name__, template_folder='static/template', static_folder='static')
import utils
import glob
import json


CORS(app)

@app.route('/')
def home():
    return render_template('intro.html', filename='dollar-gill-tVmvyJ5tEco-unsplash.jpg')

@app.route('/search', methods=['POST'])
def search():
    print(request.get_json()['joints'])
    filename = utils.search2(request.get_json()['joints'])
    return json.dumps(filename)

@app.route('/pictures', methods=['GET'])
def fetch_pictures():
    files = glob.glob('static/pictures/*jpg')
    # print(files)
    return json.dumps(files)

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='pictures/' + filename), code=301)

@app.route("/Allpictures")
def pictures():
    return render_template("pictures.html")

@app.route('/aboutus')
def about_us():
    return render_template("aboutus.html")

@app.route('/charity')
def charity():
    return render_template("charity.html")

@app.route('/searchPage', methods=['GET'])
def searchPage():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
