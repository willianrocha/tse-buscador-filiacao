import requests
import hashlib
from os import makedirs, path, remove
from zipfile import ZipFile
import json
import csv
from shutil import move, rmtree


class GetTSEData(object):
    _root_dir = 'files/'
    _tmp_dir = 'tmp/'

    '''
    Download all the 975 files of every party of every state, including DF
    '''
    def getdata(self, party_list, uf_list,
                rdirectory=_root_dir, tdirectory=_tmp_dir):
        base = 'http://agencia.tse.jus.br/'
        path = 'estatistica/sead/eleitorado/filiados/uf/'
        fname = 'filiados_{0}_{1}.zip'
        new_files = []
        url_complete = base + path + fname
        for party in party_list:
            for uf in uf_list:
                file_name = fname.format(party, uf).lower()
                fn = self.download_file(url_complete.format(party, uf).lower(),
                                        file_name, tdirectory)
                if self.check_file(file_name, rdirectory, tdirectory):
                    self.move_file(file_name, tdirectory, rdirectory)
                    new_files.append(fn)
                else:
                    remove(tdirectory+file_name)
        return new_files

    '''
    Download a single file base on the base url and the file name
    '''
    def download_file(self, url, fname, tdirectory):
        directory = tdirectory
        if not path.exists(directory):
            makedirs(directory)
        filename = directory + fname
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        return filename

    '''
    Create a md5 hash
    '''
    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    '''
    Check if the file was already downloaded
    '''
    def check_file(self, fname, ffrom, fto):
        if path.isfile(ffrom+fname):
            rfile = self.md5(ffrom+fname)
        else:
            return True
        if path.isfile(fto+fname):
            tfile = self.md5(fto+fname)
        else:
            raise FileNotFoundError('No file downloaded: {}'.format(fto+fname))
        if rfile == tfile:
            return False
        else:
            return True

    '''
    Move files from one place to another
    '''
    def move_file(self, fname, ffrom, fto):
        move(ffrom+fname, fto+fname)


class TSEDump(object):
    _root_dir = 'files/'
    _tmp_dir = 'tmp/'

    def filiation_data(self, party_list, uf_list,
                       rdirectory=_root_dir, tdirectory=_tmp_dir):
        fname = 'filiados_{0}_{1}'
        filiados = {}
        for party in party_list:
            for uf in uf_list:
                name = fname.format(party, uf).lower()
                fil = self.open_file(name, uf, party, rdirectory, tdirectory)
                filiados[name] = fil
        return filiados

    def extract_zip(self, fname, tdirectory):
        with ZipFile(fname, 'r') as zip_ref:
            zip_ref.extractall(tdirectory)

    def open_file(self, fname, uf, party, rdirectory, tdirectory):
        csv_fields = ('data_da_extracao', 'hora_da_extracao', 'numero_da_inscricao',
        'nome_do_filiado', 'sigla_do_partido', 'nome_do_partido', 'uf',
        'codigo_do_municipio', 'nome_do_municipio', 'zona_eleitoral',
        'secao_eleitoral', 'data_da_filiacao', 'situacao_do_registro',
        'tipo_do_registro', 'data_do_processamento', 'data_da_desfiliacao',
        'data_do_cancelamento', 'data_da_regularizacao', 'motivo_do_cancelamento')
        csv_directory = '{}/aplic/sead/lista_filiados/uf/'.format(tdirectory)
        csv_file = csv_directory + fname + '.csv'
        zip_name = rdirectory + fname + '.zip'
        collection_name = 'filiation_{}_{}'.format(party, uf).lower()
        if path.isfile(zip_name):  # Check if the original file existis
            self.extract_zip(zip_name, tdirectory)
        else:
            raise FileNotFoundError('No Zip Found: {}'.format(zip_name))
        if path.isfile(csv_file):
            csvfile = open(csv_file, 'r', encoding='iso-8859-1')
            csv_entries = csv.DictReader(csvfile, csv_fields, delimiter=';')
            json_list = []
            for row in csv_entries:
                acpt = json.dumps(row)
                json_list.append(json.loads(acpt))
        else:
            raise FileNotFoundError('No CSV Found: {}'.format(csvfile))
        rmtree(tdirectory)
        return json_list
