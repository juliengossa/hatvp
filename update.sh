#! /bin/bash

# wget https://www.hatvp.fr/livraison/merge/declarations.xml

if ! cmp -s declarations.xml declarations.xml.1
then
  cp declarations.xml.1 declarations/declarations_`date +"%Y%m%d"`.xml
fi

mv declarations.xml.1 declarations.xml

python3 hatpv.py declarations/declarations_2017.xml | tee declarations_2017.csv
python3 hatpv.py declarations/declarations_2021.xml | tee declarations_2021.csv
python3 hatpv.py declarations/declarations_2022.xml | tee declarations_2022.csv
python3 hatpv.py declarations/declarations_2024.xml | tee declarations_2024.csv
