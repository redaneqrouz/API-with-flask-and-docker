import os 
import pandas as pd 
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns

def header():
    html= '<head></head><body>'
    return html

def read_data_file(file_path, file_name):
    file_data = os.path.join( file_path, file_name)
    data = pd.read_csv(file_data)
    return data
############################ page: basic visual     ###############################################

def gender_distribution( data ):
    "Distribution de gender male / female"
    sns.countplot(x='gender', data=data)
    plt.title('Distribution de gender')
    if not os.path.exists("figures/gender.jpg"):
        plt.savefig("figures/gender.jpg")

def age_histogram( data ):
    "créer un histogram d'age"
    data.hist('age', bins=35);
    plt.title('Distribution d ages');
    plt.xlabel('Age');
    if not os.path.exists("figures/age.jpg"):
        plt.savefig("figures/age.jpg")
    
def population_ville( data ):
    "créer un histogram de population par ville"
    plt.figure( figsize = (10, 6))
    carrier_count = data['city'].value_counts()
    sns.barplot(carrier_count.index, carrier_count.values, alpha=1)
    plt.title('distribution de population par ville')
    plt.ylabel('nombre de femmes/hommes ', fontsize=12)
    plt.xlabel('Villes', fontsize=12)
    if not os.path.exists("figures/ville.jpg"):
        plt.savefig("figures/ville.jpg")
##########################  page: stat_avancee #########################################

def porcentage_par_ville( data ):
    "créer un disque des porcentage des population par ville"
    labels = data['city'].astype('category').cat.categories.tolist()
    counts = data['city'].value_counts()
    sizes = [counts[var_cat] for var_cat in labels]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
    ax1.axis('equal')
    if not os.path.exists("figures/perc_ville.jpg"):
        plt.savefig("figures/perc_ville.jpg")
    
def gender_ville( data ):
    "répartition d hommes / femmes par ville"

    labels = data['city'].astype('category').cat.categories.tolist()
    data_arr = np.asarray( data )
    counts_men = []
    counts_women = []
    for label in labels:
        partial_data = data_arr[data_arr[:,2] == label]
        mean_men = partial_data[partial_data[:,1] == 'm'][:,0].mean()
        mean_women = partial_data[partial_data[:,1] == 'f'][:,0].mean()

        counts_men.append( mean_men )
        counts_women.append( mean_women )

    N = len(counts_men)
    menMeans = np.asarray( counts_men ).reshape((7,)) 
    womenMeans =  np.asarray( counts_women ).reshape((7,)) 
    ind = np.arange(N)     
    width = 0.9       
    plt.figure( figsize = (15,9))

    p1 = plt.bar(ind, menMeans, width )
    p2 = plt.bar(ind, womenMeans, width,
                bottom=menMeans)

    plt.ylabel('Scores')
    plt.title('population par ville et gender')
    plt.xticks(ind, labels)
    plt.yticks(np.arange(0, 120, 10))
    plt.legend((p1[0], p2[0]), ('hommes', 'femmes'))
    if not os.path.exists("figures/gender_ville.jpg"):
        plt.savefig("figures/gender_ville.jpg")
    
def bars_gender_ville( data ):
    labels = data['city'].astype('category').cat.categories.tolist()
    hommes  = []
    femmes = []
    for label in labels:
        partial_data = data[data['city'] == label]
        hommes.append( len( partial_data[data['gender'] == 'm'] ))
        femmes.append( len( partial_data[data['gender'] == 'f'] ))
    label = labels
    plt.figure(figsize=(15, 8))
    ax = plt.subplot(111)
    index = np.arange(len(labels))

    plt.xlabel('champs', fontsize=15)
    plt.ylabel('nombre de femmes / hommes', fontsize=15)
    plt.title('male/female par ville')
    plt.bar(index, hommes, color = 'r', width = 0.2, label='male')  # label='algo sur mon pc'
    plt.bar(index-0.20, femmes, color = 'b', width = 0.2, label='female')
    y_pos = np.arange(len(label))
    plt.xticks(y_pos, label)
    ax.legend()
    if not os.path.exists("figures/bars_gender.jpg"):
        plt.savefig("figures/bars_gender.jpg")
    
################################# page:Demographie ###########################################

def pyramide_ages( data ):
    "plot la difference d'ages entre les deux genders"
    from numpy import arange

    homme = data[ data['gender'] == 'm']['age']
    femme = data[ data['gender'] == 'f']['age']
    
    hommes = []
    femmes = []

    for i in range(101):
        h = len( homme[ homme == i] )
        f = len( femme[ femme == i] )
        hommes.append( h )
        femmes.append( f )
    hommes = np.asarray( hommes )
    femmes = np.asarray( femmes )
    
    somme = hommes - femmes

    fig, ax = plt.subplots(figsize=(8,8))
    ValH = ax.barh(arange(len(hommes)), hommes, 1.0, label="Hommes", color='b', linewidth=0, align='center')
    ValF = ax.barh(arange(len(femmes)), -femmes , 1.0, label="Femmes",
                color='r', linewidth=0, align='center')
    diff, = ax.plot(somme, arange(len(femmes)), 'y', linewidth=2)
    ax.set_title("Pyramide des ages")
    ax.set_ylabel("Ages")
    ax.set_xlabel("Habitants")
    ax.set_ylim([0, 110])
    ax.legend((ValH[0], ValF[0], diff), ('Hommes', 'Femmes', 'différence'))
    if not os.path.exists("figures/pyramide.jpg"):
        plt.savefig("figures/pyramide.jpg")
    
def esperance_vie( data ):
    "afficher la difference entre les esperance de vie chez les deux genders"
    from matplotlib import pyplot as plt

    H = data[ data['gender'] == 'm']['age']
    F = data[ data['gender'] == 'f']['age']
    
    hommes = []
    femmes = []

    for i in range(101):
        h = len( H[ H == i] )
        f = len( F[ F == i] )
        hommes.append( h )
        femmes.append( f )
    hommes = np.asarray( hommes )
    femmes = np.asarray( femmes )
    
    h_f = np.c_[hommes, femmes]
    hf = np.concatenate((h_f, np.zeros((8, 2))), axis=0)
    nb = hf.shape[0]
    esp = np.zeros ((nb,2))
    for t in range(0,nb):
        for i in (0,1):
            if hf[t,i] == 0:
                esp[t,i] = 0
            else:
                somme  = 0.0
                for d in range(1,nb-t):
                    if hf[t+d,i] > 0:
                        somme += d * (hf[t+d,i] - hf[t+d+1,i]) / hf[t,i]
                esp[t,i] = somme
    h = plt.plot(esp)
    plt.legend(h, ["Homme", "Femme"])
    plt.title("Espérance de vie")
    if not os.path.exists("figures/esperance.jpg"):
        plt.savefig("figures/esperance.jpg")
