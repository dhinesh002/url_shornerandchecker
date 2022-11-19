from flask import Flask, render_template, request
import pyshorteners
import validators
import requests
import datetime

now = datetime.datetime.now()
#print(now.year)
year = now.year

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html',year=year)


@app.route('/check', methods=['POST'])
def check():
    web_address = request.form['URL']
    valid = validators.url(web_address)
    if valid == True and len(web_address) > 30:
        short = pyshorteners.Shortener()
        shorten_url = short.tinyurl.short(web_address)
        return render_template('output.html', output_url=shorten_url, year=year)

    elif valid == True and len(web_address) < 30:
        return render_template('small.html')
    else:
        return render_template('error.html')


@app.route('/security', methods=['POST'])
def security():
    global web_name, web_status, child_reputaion, child_confidence, reputaion, confidence, name, name_confidence, track, track_confidence, service, services
    api = "https://wot-web-risk-and-safe-browsing.p.rapidapi.com/targets"
    web_address = request.form['URL']
    if 'http' in web_address:
        new_url = web_address.split('/')
        queries = (new_url[2])
        querystring = {"t": queries}
        headers = {
            "X-RapidAPI-Key": "4aae66a013mshc0f15b50e2472e3p1dcc27jsn39280417afac",
            "X-RapidAPI-Host": "wot-web-risk-and-safe-browsing.p.rapidapi.com"
        }
        response = requests.request("GET", api, headers=headers, params=querystring)
        try:
            security = response.json()
            web_name = security[0]['target']
            web_status = security[0]['safety']['status']
            child_reputaion = security[0]['childSafety']['reputations']
            child_confidence = security[0]['childSafety']['confidence']
            reputaion = security[0]['safety']['reputations']
            confidence = security[0]['safety']['confidence']
            name = security[0]['categories'][0]['name']
            name_confidence = security[0]['categories'][0]['confidence']
            track = security[0]['categories'][1]['name']
            track_confidence = security[0]['categories'][1]['confidence']
            services = security[0]['categories'][3]['name']
        except IndexError:
            pass
        except KeyError:
            return render_template('error.html')
        return render_template('security.html', name=web_name, status=web_status, child_r=child_reputaion,
                               child_c=child_confidence, reputaion=reputaion, confidence=confidence,
                               trust=name, trust_c=name_confidence, track=track, track_c=track_confidence,
                               Service=services, year=year)


if __name__ == '__main__':
    app.run(debug=True)
