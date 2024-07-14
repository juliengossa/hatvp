# MIT License
#
# Copyright (c) 2023 Julien Gossa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

#!/usr/bin/env python

import json
import os
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
import re
import argparse


patrimoine = [
    #("participationFinanciereDto",'nomSociete',['nombreParts'],'evaluation'),
    ("immeubleDto",'nature',['superficieBati'],'valeurVenale'),
    ("sciDto",'denomination',['capitalDetenu'],'valeur'),
    ("valeursNonEnBourseDto",'denomination',[],'valeurActuelle'),
    ("valeursEnBourseDto",'naturePlacement',[],'valeur'),
    ("assuranceVieDto",'etablissement',[],'valeurRachat'),
    ("comptesBancaireDto",'typeCompte',['etablissement'],'valeur'),
    ("bienDiverDto",'description',[],'valeur'),
    ("vehiculeDto",'nature',[],'valeur'),
    ("fondDto",'denomination',['description'],'valeur'),
    ("autreBienDto",'denomination',['description'],'valeur'),
    ("bienEtrangerDto",'nature',['description'],'valeur'),
    ("passifDto",'nature',['nomCreancier'],'restantDu')
]


def get_soup(file):
    with open(file, "r") as f:
        soup = BeautifulSoup(f.read(),features="xml")
    return soup


def csv_format(s):
    s = str(s).strip().replace(',',' ').replace('\n',' ').lower()
    return re.sub(' +', ' ', s)

def get_childtext(dec,key):
    try:
        return csv_format(dec.findChild(key).text)
    except:
        return "NA"

header_header = ["Nom","Prénom","Date_depot","Version","Type_mandat","Mandat"]
def get_header(dec):
    decl = dec.findChild("declarant")
    return {
        "nom": get_childtext(decl,"nom"),
        "prenom": get_childtext(decl,"prenom"),
        "dateDepot" : get_childtext(dec,"dateDepot").split(' ')[0],
        "version" : get_childtext(dec,"declarationVersion"),
        "type_mandat" : get_childtext(dec,"mandat"),
        "mandat" : get_childtext(dec,"labelDeclaration")
    }

def get_values_sum(dec,section,values):
    p = dec.findChild(section)
    return { section+"_"+v : sum([ int(np.text) for np in p.findAll(v) ]) for v in values }


def get_values(dec,section,values):
    p = dec.findChild(section)
    items = p.findChild('items').findChildren('items')
    return [ { v : i.find(v).text for v in values } for i in items ]

def get_SDV(dec,section,description,details,value):
    if not isinstance(details,list): details = [ details ]
    p = dec.findChild(section)
    try:
        items = p.findChild('items').findChildren('items')
    except Exception as e:
        return []
    return [ {
        'section' : section,
        'description' : get_childtext(i, description),
        'details' : " ".join([ i.find(d).text for d in details ]),
        'valeur' : get_childtext(i,value) } for i in items ]

def print_patrimoine(dec):
    header = get_header(dec)
    for p in patrimoine:
        items = get_SDV(dec,p[0],p[1],p[2],p[3])
        for i in items:
            print(",".join([csv_format(h) for h in header.values()]+[csv_format(v) for v in i.values()]))

def print_patrimoines(file):
    print(",".join(header_header+["Section","Description","Détails","Valeur"]))
    dec = get_soup(file)
    for d in dec.findAll("declaration"):
        print_patrimoine(d)

def main():
    parser = argparse.ArgumentParser(description='Parse les declarations XML de la HATPV')
    parser.add_argument('file', type=str, help='le fichier à parser')
    args = parser.parse_args()

    # dec = get_soup("aoc_interets_20230214.xml")
    # print(get_header(dec))
    # print(get_values_sum(dec,"participationFinanciereDto",['nombreParts','evaluation']))
    # print(get_values(dec,"participationFinanciereDto",['nomSociete','nombreParts','evaluation']))

    #dec = get_soup("aoc_patrimoine_20230714.xml")
    # print_patrimoine(dec)

    print_patrimoines(args.file)

if __name__ == "__main__":
    main()
