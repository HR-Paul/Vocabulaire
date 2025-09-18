from typing import cast
import os

import random
#from copy import deepcopy

import json


def get_liste(path:str,name:str):
    #renvoi:list[tuple[str,str]]=[]
    liste:dict[str,list[str]]=json.load(open(path))[name][1]
    res:dict[str,dict[str,int]]={}
    for cle in liste.keys():
        res[cle]={"apparu":0,"réussi":0,"raté":0}
    return liste,res
    #return renvoi

def devinette(tableau,nbrepoints,essais):
    from random import randint
    hasard=essais-1
    choix=randint(0,1)
    if choix==0:
        demande="terme 1"
        réponse="terme 2"
    else:
        demande="terme 2"
        réponse="terme 1"
    essai=input(tableau[hasard][demande]+"\n")
    if essai=="exit":
        return essai,essai
    elif essai==tableau[hasard][réponse]:
        nbrepoints+=1
        print("Bravo ! La réponse était effectivement",tableau[hasard][réponse])
        print("Vous avez",nbrepoints,"points sur",essais,"ce qui vous fait un taux de",(nbrepoints/essais)*100,"% de réussite !")
    elif essai!=tableau[hasard][réponse]:
        print("Vous avez",nbrepoints,"points sur",essais,"ce qui vous fait un taux de",(nbrepoints/essais)*100,"% de réussite !")
        print("La réponse était",tableau[hasard][réponse])
        rectification=""
        while rectification!=tableau[hasard][réponse] and rectification!="exit":
            print("Essaye de le réécrire :")
            rectification=input()
        if rectification=="exit":
            return essai,essai
    print()
    essais+=1
    return nbrepoints,essais

#demande=random.choice(list(tableau.keys()))
def devinette(nbpoints:int,nbessais:int,suite:int,demande:str):
    essai=input(demande+"\n")
    if essai=="exit":
        return nbpoints,nbessais
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
            rectification=input(f"Essaye de réécrire { {True:"la réponse",False:"une des réponses"}[len(tableau[demande])==1] } :\n")
    resultats[demande]["apparu"]+=1
    nbessais+=1
    return nbpoints,nbessais,suite


"""def devinette_aléa(tableau:dict[str,list[str]],nbrepoints:int,nbreessais:int,suite:int,hasard:int=-1):
    if hasard==-1:
        hasard=randint(0,2*(len(tableau)-1))
    if hasard%2==0:
        demande="terme 1"
        réponse="terme 2"
    else:
        demande="terme 2"
        réponse="terme 1"
    hasard=hasard//2
    essai=input(str(tableau.keys()[hasard])+"\n")
    if essai=="exit":
        return tableau,essai,nbreessais,suite,2*hasard
    elif essai==tableau[hasard][réponse]:
        tableau[hasard]["réussi"]+=1
        tableau[hasard]["apparu"]+=1
        nbreessais+=1
        nbrepoints+=1
        suite+=1
        print("Bravo ! La réponse était effectivement",tableau[hasard][réponse])
        if suite>=3:
            print("Incroyable ! Vous êtes sur une série de",suite,"bonnes réponses")
        print("Vous avez",nbrepoints,"points sur",nbreessais,"ce qui vous fait un taux de",(nbrepoints/nbreessais)*100,"% de réussite !")
    elif essai!=tableau[hasard][réponse]:
        suite=0
        tableau[hasard]["raté"]+=1
        tableau[hasard]["apparu"]+=1
        nbreessais+=1
        print("Vous avez",nbrepoints,"points sur",nbreessais,"ce qui vous fait un taux de",(nbrepoints/nbreessais)*100,"% de réussite !")
        print("La réponse était",tableau[hasard][réponse])
        rectification=""
        while rectification!=tableau[hasard][réponse]:
            rectification=input("Essaye de le réécrire :\n")
            if rectification=="exit":
                return tableau,essai,nbreessais,suite,2*hasard
    return tableau,nbrepoints,nbreessais,suite"""
def analyse_résultats(tableau:dict[str,dict[str,int]]):
    resultatstops=maxium(tableau,5)
    print("############################################################")
    print("####################   LES TOPS   ##########################")
    print("############################################################")
    for i in range(len(resultatstops[0])):
        print("Le mot",resultatstops[0][i],"est apparu",tableau[resultatstops[0][i]]["apparu"],"fois.")
    print()
    for i in range(len(resultatstops[1])):
        print("Le mot",resultatstops[1][i],"a été réussi",tableau[resultatstops[1][i]]["réussi"],"fois.")
    print()
    for i in range(len(resultatstops[2])):
        print("Le mot",resultatstops[2][i],"a été râté",tableau[resultatstops[2][i]]["raté"],"fois.")
def maxium(tableau:dict[str,dict[str,int]],tops:int):
    """
    tableau:liste de dictionnaires contenant les mots en allemand en français, leur fréquence d'apparition de réussite et de râté
    tops:nombre de valeur du top voulu
    renvoi:liste de liste de dictionnaires contenant le top 'tops' des mots les plus apparus, les plus réussis et les plus échoués
    renvoi[any]:liste de dictionnaire contenant le top des mots les plus apparus/réussis/échoués en fonction de any
    renvoi[any][any1]:dictionnaire d'un mot allemand ou français avec ses informations
    """
    renvoi=[sorted(tableau,reverse=True,key=lambda dict:tableau[dict]["apparu"]),sorted(tableau,reverse=True,key=lambda dict:tableau[dict]["réussi"]),sorted(tableau,reverse=True,key=lambda dict:tableau[dict]["raté"])]
    for _ in range(len(tableau)-tops):
        del(renvoi[0][tops])
        del(renvoi[1][tops])
        del(renvoi[2][tops])
    return renvoi
def boucle_aléa(tab:dict[str,list[str]]):
    valeur=0
    points=0
    tries=0
    suite=0
    continuer=True
    retour=-1
    while continuer:
        #print(tries)
        continuer1=""
        if retour==-1:
            ensemble=list(devinette_aléa(tab,points,tries,suite))
        else:
            ensemble=list(devinette_aléa(tab,points,tries,suite,retour))
        if len(ensemble)==4:
            tab,valeur,tries,suite,retour=ensemble[0],ensemble[1],ensemble[2],ensemble[3],-1
        else:
            tab,valeur,tries,suite,retour=ensemble[0],ensemble[1],ensemble[2],ensemble[3],ensemble[4]
        if valeur!="exit":
            points=valeur
            retour=-1
        else:
            analyse_résultats(tab)
            while continuer1.lower()!="oui" and continuer1.lower()!="non":
                continuer1=str(input("Voulez-vous continuer le quiz ? (oui ou non)\n"))
            if continuer1.lower()=="non":
                continuer=False
        
    return
def boucle(tab):
    continuer=True
    nbre_essais=1
    points=0
    while continuer and nbre_essais!=len(tab):
        valeur,nbre_essais=devinette(tab,points,nbre_essais)
        if valeur!="exit":
            points=valeur
        else:
            analyse_résultats(tab)
            continuer=""
            while continuer.lower()!="oui" and continuer.lower()!="non":
                continuer=str(input("Voulez-vous continuer le quiz ? (oui ou non)\n"))
            if continuer.lower()=="non":
                continuer=False
    return

suite=0


tableau,resultats=get_liste(os.path.join(os.path.curdir,"listes_vocab.json"),"anglaisG25256S1")
analyse_résultats(resultats)
#boucle(tab)
devinette(0,0,0,"compel")
#boucle_aléa(tab)