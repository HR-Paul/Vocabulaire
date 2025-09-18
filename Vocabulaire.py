import random
from parameters import *
import json


def get_liste():
    #renvoi:list[tuple[str,str]]=[]
    liste:dict[str,list[str]]=json.load(open(path_file_list))[listechoisie]
    res:dict[str,dict[str,int]]={}
    for cle in liste.keys():
        res[cle]={"apparu":0,"réussi":0,"raté":0}
    return liste,res


def devinette(nbpoints:int,nbessais:int,suite:int,demande:str):
    essai=input(demande+"\n")
    if essai=="exit":
        return nbpoints,nbessais,suite
    elif essai in tableau[demande]:
        resultats[demande]["réussi"]+=1
        nbpoints+=1
        suite+=1
        print(f"Vous avez {nbpoints} points sur {nbessais+1} ce qui vous fait un taux de {(nbpoints/(nbessais+1))*100} % de réussite !")
        print("Bravo ! La réponse était effectivement",essai)
        if suite>=3:
            print("Incroyable ! Vous êtes sur une série de",suite,"bonnes réponses")
    else:
        resultats[demande]["raté"]+=1
        suite=0
        print(f"Vous avez {nbpoints} points sur {nbessais+1} ce qui vous fait un taux de {(nbpoints/(nbessais+1))*100} % de réussite !")
        if len(tableau[demande])==0:
            print(f"La réponse était {tableau[demande][0]}")
        else:
            print(f"Vous pouviez répondre {repr(tableau[demande][0])}{"".join(", ou "+repr(tableau[demande][i]) for i in range(1,len(tableau[demande])))}")
        rectification=""
        while rectification not in tableau[demande]:
            rectification=input(f"Essayez de réécrire { {True:"la réponse",False:"une des réponses"}[len(tableau[demande])==1] } :\n")
    resultats[demande]["apparu"]+=1
    nbessais+=1
    return nbpoints,nbessais,suite
def analyse_résultats():
    apparus,reussis,rates=maxium(resultats,5)
    print("############################################################")
    print("####################   LES TOPS   ##########################")
    print("############################################################")
    for i in range(len(apparus)):
        print("Le mot",apparus[i],"est apparu",resultats[apparus[i]]["apparu"],"fois.")
    print()
    for i in range(len(reussis)):
        print("Le mot",reussis[i],"a été réussi",resultats[reussis[i]]["réussi"],"fois.")
    print()
    for i in range(len(rates)):
        print("Le mot",rates[i],"a été râté",resultats[rates[i]]["raté"],"fois.")
def maxium(tableau:dict[str,dict[str,int]],tops:int):
    return sorted(tableau,reverse=True,key=lambda dict:tableau[dict]["apparu"])[:tops],sorted(tableau,reverse=True,key=lambda dict:tableau[dict]["réussi"])[:tops],sorted(tableau,reverse=True,key=lambda dict:tableau[dict]["raté"])[:tops]
def newboucle():
    points=0
    essais=0
    suite=0
    suivant=True
    if len(tableau)==0:
        print("Aucun élément à apprendre")
        return
    while suivant:
        if aléa:
            demande=random.choice(list(tableau.keys()))
        else:
            demande=tuple(tableau.keys())[essais%len(tableau)]
        precessais=essais
        points,essais,suite=devinette(points,essais,suite,demande)
        if precessais==essais:
            analyse_résultats()
            inpsuiv=""
            while inpsuiv.lower()!="oui" and inpsuiv.lower()!="non":
                inpsuiv=str(input("Voulez-vous continuer le quiz ? (oui ou non)\n"))
            if inpsuiv.lower()=="non":
                suivant=False
def add_nouveaux():
    try:
        tableau:dict[str,dict[str,list[str]]]=json.load(open(path_file_list))
    except (json.decoder.JSONDecodeError,FileNotFoundError):
        tableau:dict[str,dict[str,list[str]]]={}
    with open("./nouveaux.txt") as f:
        content:list[str]=f.read().splitlines()
    if len(content)==0:
        if tableau.get(listechoisie)==None:
            tableau[listechoisie]={}
        json.dump(tableau,open(path_file_list,"w"))
        return
    for i in range(len(content)):
        demande,reponse=content[i].split("=")
        if tableau.get(listechoisie)==None:
            tableau[listechoisie]={}
        tableau[listechoisie][demande.strip()]=[val.strip() for val in reponse.split(",")]
    with open("./nouveaux.txt","w") as f:
        f.write("")
    json.dump(tableau,open(path_file_list,"w"))







add_nouveaux()
tableau,resultats=get_liste()


newboucle()
