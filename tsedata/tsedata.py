import requests
import hashlib
from os import makedirs, path, remove
from shutil import move

uf_list = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG", \
    "PR","PB","PA","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"]
party_list = [ "PMDB", "PT", "PSDB", "PP", "PDT", "PTB", "DEM", "PR", "PSB", \
    "PPS", "PSC", "PCdoB", "PRB", "PV", "PSD", "PRP", "PSL", "PMN", "PHS", \
    "PTC", "PTdoB", "PSDC", "SD", "PTN", "PRTB", "PSOL", "PROS", "PEN", "PPL", \
    "PMB", "PSTU", "REDE", "PCB", "NOVO", "PCO"]

'''
Download all the 975 files of every party of every state, including DF
'''
def getdata( \
    url='http://agencia.tse.jus.br/estatistica/sead/eleitorado/filiados/uf/'):
    fname = "filiados_{0}_{1}.zip"
    url_complete = url + fname
    rdirectory = "files/"
    tdirectory = "files/tmp/"
    for party in party_list:
        for uf in uf_list:
            file_name = fname.format(party,uf).lower()
            print(url_complete.format(party,uf).lower())
            download_file(url_complete.format(party,uf).lower(), file_name)
            if not check_file(file_name,rdirectory,tdirectory):
                move_file(file_name,tdirectory,rdirectory)
            else:
                remove(tdirectory+file_name)

'''
Download a single file base on the base url and the file name
'''
def download_file(url, fname):
    directory = "files/tmp/"
    if not path.exists(directory):
        makedirs(directory)
    filename = directory + fname
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return filename

'''
Create a md5 hash
Stack Overflow questions/3431825
'''
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

'''
Check if the file was already downloaded
Problaly useless
'''
def check_file(fname,ffrom,fto):
    if path.isfile(ffrom+fname): # Check if the original file existis
        rfile = md5(ffrom+fname)
    else:
        return False
    if path.isfile(fto+fname): # check the new file
        tfile = md5(fto+fname)
    else:
        print("check_file: No file downloaded")
    if rfile == tfile:
        return False
    else:
        return True

'''
Move files from one place to another
'''
def move_file(fname, ffrom, fto):
    move(ffrom+fname,fto+fname)

getdata()
