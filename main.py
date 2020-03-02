import os
import numpy as np

# local importation 
from util import header, read_data_file, gender_distribution, age_histogram, population_ville
from util import porcentage_par_ville, gender_ville, bars_gender_ville
from util import pyramide_ages, esperance_vie

# import flask pour l'interface web
from flask import Flask, render_template, render_template_string, request

# initialiser Flask app
app = Flask(__name__,
            static_url_path='', 
            static_folder='figures',
            template_folder='templates')

# le chemin de de l'api et le code
file_path = os.getcwd() + "/"
file_name = "dataset.csv"

# utiliser la fonction dans util pour importer la data avec pandas 
data = read_data_file(file_path, file_name)
    
@app.route('/')
def home():
    # initialiser les fonctions et créer les plots visuals
    gender_ville ( data )
    population_ville( data )
    age_histogram( data )
    gender_distribution( data )
    
    gender_ville ( data )
    porcentage_par_ville( data )
    bars_gender_ville( data ) 
    
    esperance_vie( data )
    pyramide_ages( data )
    "la page d'acceuil de l'API"
    html = ''
    html += header()
    html += '<h1>API pour naviguer dans des données démographique visualement </h1>'
    html += '<a href="http://localhost:5001/statistic"> Cliquer pour voir les stats</a></br>'
    html += '<a href="http://localhost:5001/basic_visual"> Cliquer pour voir les charts des features basiques</a></br>'
    html += '<a href="http://localhost:5001/stat_avancee"> Cliquer pour voir les charts des statistique  </a></br>'
    html += '<a href="http://localhost:5001/demographie"> Cliquer pour voir les charts démographie </a></br>'
    html += '<a href="http://localhost:5001/form"> Cliquer pour rajouter des champs dans la dataset </a></br>'

    return html

@app.route("/statistic")
def general_statistics():
    "afficher des statistiques sur la data "
    desc = data.describe()
    description = np.asarray( desc )
    # créer la page html correspont a cette page 
    html = ''
    html += header()
    html += '<table><thead><tr><th colspan="2">table de desciption d age</th></tr></thead><tbody>'
    html += "<tr> <td>champs</td> <td>valeurs</td></tr>"
    html += "<tr> <td>total contenus</td> <td>"+str( description[0] ) +"</td></tr>"
    html += "<tr> <td>moyenne des champs </td> <td>"+ str( description[1] )+"</td></tr>"
    html += "<tr> <td>average </td> <td>"+str( description[2] )+"</td></tr>"
    html += "<tr> <td>minimum d'age </td> <td>"+str( description[3] )+"</td></tr>"
    html += "<tr> <td>premier quartile 25%</td> <td>"+str( description[4] )+"</td></tr>"
    html += "<tr> <td>median 50% </td> <td>"+str( description[5] )+"</td></tr>"
    html += "<tr> <td>3eme quartile </td> <td>"+str( description[6] )+"</td></tr>"
    html += "<tr> <td>maximum d'age</td> <td>"+str( description[7] )+"</td></tr>"
    html += "</tbody></table>"
    
    male = data[data['gender'] == 'm']
    female = data[data['gender'] == 'f']
    
    number_of_male = len(male)
    number_of_female = len(female)
    
    html += "hommes: "+str( number_of_male )+" femmes: "+ str( number_of_female ) +"</br>"
    
    male_percent = (number_of_male * 100 ) / (number_of_male + number_of_female) 
    female_percent = (number_of_female * 100) / (number_of_male + number_of_female) 
    
    html += "porcentage des hommes: "+str( male_percent )+"% porcentage des femmes: "+str( female_percent )+"%</br>"
    html += '<a href="http://localhost:5001/" > retourner a la page d accueil </a>'
    html += "</body>"
    return html

@app.route("/basic_visual")
def basic_visual():
    return render_template("basic_visual.html") 

@app.route("/stat_avancee")
def stat_avancee():
    return render_template("stat_avancee.html") 

@app.route("/demographie")
def demographie():
    return render_template("demographie.html") 

@app.route("/form")
def form():
    return render_template("form.html") 



@app.route('/result',methods = ['POST', 'GET'])
def result():
    "traiter la formulaire on remplissant les champs dans une nouvelle base de donnée"
    "et rediriger vers une autre page"
    if request.method == 'POST':
        result = request.form
        form_value = []
        # parcourir les champs et les mettre dans une liste 
        for k, v in result.items():
            form_value.append(v)
        data_temp = data
        # remplir les valeurs dans une base de donnée 
        data_temp.append({'age' : form_value[0] , 'gender' : form_value[1], 'city': form_value[2]} , ignore_index=True)
        # enregitrer la nouvelle base de données avec un nouveau nom 
        data_temp.to_csv(r'new_dataset.csv', index = False)
        return render_template("result.html",result = result)

if __name__ == '__main__':
    app.run(port = 5001, debug = True)
