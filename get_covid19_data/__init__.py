#import essential framework
from flask import Flask
from flask_restful import Resource, Api
import requests
import pandas as pd
from bs4 import BeautifulSoup

def request_data():
    url = "https://www.worldometers.info/coronavirus/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find(name = 'table', attrs = {'id': 'main_table_countries_today'})
    df = pd.read_html(str(table))[0]
    df.columns = ['country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases', 'serious_or_critical', 'total_cases_per_1m_population', 'deaths_per_1m_population', 'total_tests', 'tests_per_1m_population']
    df['country'] = df['country'].str.lower()
    df['country'] = df['country'].str.replace(" ", "_")
    df.set_index('country', inplace=True)
    return df.to_dict(orient='index')

#create an instance of flask
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'Ravi' : 'Vandita', 'test':'done'}
class CountryStats(Resource):
    def get(self, countryname):
        data = request_data()
        if countryname == 'all':
            return data
        else:
            return data[countryname]

api.add_resource(HelloWorld, '/')
api.add_resource(CountryStats, '/countrystats/<countryname>')

if __name__ == '__main__':
    app.run(debug=True)