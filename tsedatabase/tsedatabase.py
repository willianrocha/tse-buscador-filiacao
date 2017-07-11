# -*- coding: UTF-8 -*-
from zipfile import ZipFile
from os import path
import json
import csv
from shutil import move, rmtree
from pymongo import MongoClient
import pymongo

db_conn = MongoClient('localhost', 27017)
col_filiation = db_conn['tse-filiation']
post_filiation = col_filiation['filiation']

uf_list = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
    'PR','PB','PA','PE','PI','RJ','RN','RS','RO','RR','SC','SE','SP','TO']
party_list = ['DEM', 'NOVO', 'PCB', 'PCO', 'PC_do_B', 'PDT', 'PEN', 'PHS',
    'PMB', 'PMDB', 'PMN', 'PP', 'PPL', 'PPS', 'PR', 'PRB', 'PROS', 'PRP',
    'PRTB', 'PSB', 'PSC', 'PSD', 'PSDB', 'PSDC', 'PSL', 'PSOL', 'PSTU', 'PT',
    'PTB', 'PTC', 'PTN', 'PT_do_B', 'PV', 'REDE', 'SD']

csv_fields = ('data_da_extracao', 'hora_da_extracao', 'numero_da_inscricao',
    'nome_do_filiado', 'sigla_do_partido', 'nome_do_partido', 'uf',
    'codigo_do_municipio', 'nome_do_municipio', 'zona_eleitoral',
    'secao_eleitoral', 'data_da_filiacao', 'situacao_do_registro',
    'tipo_do_registro', 'data_do_processamento', 'data_da_desfiliacao',
    'data_do_cancelamento', 'data_da_regularizacao', 'motivo_do_cancelamento')

def extract_zip(fname):
    with ZipFile(fname,'r') as zip_ref:
    	zip_ref.extractall('./files/tmp')

def open_file(fname,uf,party):
    rdirectory = './files/'
    csv_directory = 'tmp/aplic/sead/lista_filiados/uf/'
    csv_file = rdirectory + csv_directory + fname + '.csv'
    zip_name = rdirectory + fname + '.zip'
    collection_name = 'filiation_{}_{}'.format(party,uf).lower()
    count = 0
    if path.isfile(zip_name): # Check if the original file existis
        extract_zip(zip_name)
    else:
        print('No Zip Found')
    if path.isfile(csv_file):
        csvfile = open(csv_file, 'r', encoding='iso-8859-1')
        csv_entries = csv.DictReader(csvfile, csv_fields, delimiter=';')
        json_list = []
        for row in csv_entries:
            count += 1
            acpt = json.dumps(row)
            json_list.append(json.loads(acpt))
        col_filiation[collection_name].insert_many(json_list)
    else:
        print('No CSV Found')
    print('{0} Entries: {1}'.format(collection_name, count))
    rmtree(rdirectory+'tmp/')

def upload_data():
    fname = 'filiados_{0}_{1}'
    for party in party_list:
        for uf in uf_list:
            name = fname.format(party,uf).lower()
            open_file(name,uf,party)

upload_data()
