# -*- coding: UTF-8 -*-
from zipfile import ZipFile
from os import path
import json
import csv
from shutil import move, rmtree

uf_list = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG", \
    "PR","PB","PA","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"]
party_list = [ "PMDB", "PT", "PSDB", "PP", "PDT", "PTB", "DEM", "PR", "PSB", \
    "PPS", "PSC", "PCdoB", "PRB", "PV", "PSD", "PRP", "PSL", "PMN", "PHS", \
    "PTC", "PTdoB", "PSDC", "SD", "PTN", "PRTB", "PSOL", "PROS", "PEN", "PPL", \
    "PMB", "PSTU", "REDE", "PCB", "NOVO", "PCO"]

csv_fields = ('DATA DA EXTRACAO', 'HORA DA EXTRACAO','NUMERO DA INSCRICAO',
 'NOME DO FILIADO', 'SIGLA DO PARTIDO', 'NOME DO PARTIDO', 'UF',
 'CODIGO DO MUNICIPIO', 'NOME DO MUNICIPIO', 'ZONA ELEITORAL',
 'SECAO ELEITORAL', 'DATA DA FILIACAO', 'SITUACAO DO REGISTRO',
 'TIPO DO REGISTRO', 'DATA DO PROCESSAMENTO', 'DATA DA DESFILIACAO',
 'DATA DO CANCELAMENTO', 'DATA DA REGULARIZACAO', 'MOTIVO DO CANCELAMENTO')

def extract_zip(fname):
    with ZipFile(fname,"r") as zip_ref:
    	zip_ref.extractall("./files/tmp")

def open_file(fname):
    rdirectory = "./files/"
    csv_directory = "tmp/aplic/sead/lista_filiados/uf/"
    csv_file = rdirectory + csv_directory + fname + ".csv"
    zip_name = rdirectory + fname + ".zip"
    # json_file = open(fname+".json","w")
    print(fname)
    if path.isfile(zip_name): # Check if the original file existis
        extract_zip(zip_name)
    else:
        print("No Zip Found")
    if path.isfile(csv_file): # Check if the original file existis
        csvfile = open(csv_file, 'r')
        csv_entries = csv.DictReader(csvfile,csv_fields,delimiter=';')
        for row in csv_entries:
            # TODO insert in database
            print json.dumps(row, encoding='iso-8859-1')
    else:
        print("No CSV Found")
    rmtree(rdirectory+"tmp/")

def upload_data():
    fname = "filiados_{0}_{1}"
    for party in party_list:
        for uf in uf_list:
            name = fname.format(party,uf).lower()
            open_file(name)

upload_data()
