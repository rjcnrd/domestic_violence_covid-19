# Visualising domestic violence in the UK and impacts of covid-19

In several European countries, lockdown measures are implemented following the covid-19 outbreak in Spring 2020. In several countries, an increase in domestic violence has been reported following this new living situation. This project aims at increasing information about the increase in domestic violence towards women since the lockdown to raise public attention and action to the subject.

This project is a first draft of our work around gender inequality during the COVID. It has a structure with tabs and is using a fake data set randomly generated.
Since we changed the structure and we want to represent real data, we are creating a new repo for this project. Please look for gender_inequality_covid-19.

### Setup

After cloning the repo, create a virtual environment & start the app following the steps below.

#### Create environment
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Launch the dash app
```
python3 app.py
```
Open http://127.0.0.1:8050/ in your browser to see the app.

#### Update the environment
```
pip3 freeze>requirements.txt
```

#### Deploy the app on Heroku :

Make sure you have master up to date, then :

```
git push heroku master
```
Link can be found : https://dash-app-gender-violence.herokuapp.com

## Built With

* [Plotly/Dash](https://plotly.com/dash/) 
## Authors

Amélie Meurer and Roberta Conrad

## License

This project is licensed under the MIT License.
