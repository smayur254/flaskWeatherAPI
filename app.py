from unicodedata import name
import requests
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=60), nullable=False)
    
    
@app.route('/', methods=['GET','POST']) 
def index():
    def ftoc(ftemp):
        return (ftemp-32.0)*(5.0/9.0)

    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
            return redirect(url_for('index'))
        
    if request.method == 'GET':
        cities = City.query.all()
        url = 'http://api.openweathermap.org/data/2.5/weather?q={},&units=imperial&APPID=c050097be0707b395cd6d170871f0b30'
        
        weather_data=[]
        for city in cities:
            response = requests.get(url.format(city.name)).json()
            weather={
                'city': city.name,
                'country': response['sys']['country'],
                'temperature': response['main']['temp'],
                'feels_like': response['main']['feels_like'],
                'temp_max': response['main']['temp_max'],
                'temp_min': response['main']['temp_min'],
                'description': response['weather'][0]['description'],
                }
            weather_data.append(weather)
        return render_template('weather.html', weather_data=weather_data)

if __name__ == ('__main__'):
    app.run(debug=True)
    
    
 