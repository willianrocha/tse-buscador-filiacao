import zipfile
import urllib.request as urllib2

all_states_in_br = [
	"ac", "al", "am", "ap", "ba", "ce", "df", "es", "go",
	"ma", "mg", "ms", "mt", "pa", "pb", "pe", "pi", "pr",
	"rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to"
]

all_political_parties = [
 	"dem", "novo", "pen", "pc_do_b", "pcb", "pco", "pdt", "phs",
 	"pmdb", "pmb", "pmn", "pp", "ppl", "pps", "pr", "prb", "pros",
 	"prp", "prtb", "psb", "psc", "psd", "psdb", "psdc", "psl", "psol",
 	"pstu", "pt", "pt_do_b", "ptb", "ptc", "ptn", "pv", "rede", "sd"
]

def download_all_zips():
	for x in all_states_in_br:
		for y in all_political_parties:
			url_zip_location = "http://agencia.tse.jus.br/estatistica/sead/eleitorado/filiados/uf/filiados_{}_{}.zip".format(y, x)
			print(url_zip_location)
			file_name = url_zip_location.split('/')[-1]
			u = urllib2.urlopen(url_zip_location)
			f = open('./zips/{}'.format(file_name), 'wb')
			meta = u.info()
			file_size_dl = 0
			block_sz = 8192
			while True:
			    buffer = u.read(block_sz)
			    if not buffer:
			        break

			    file_size_dl += len(buffer)
			    f.write(buffer)
			    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100)
			    status = status + chr(8)*(len(status)+1)
			    print(status)
			f.close()
			print_info('./zips/{}'.format(file_name))

def print_info(archive_name):
    with zipfile.ZipFile(archive_name,"r") as zip_ref:
    	zip_ref.extractall("./extracts")

download_all_zips()





























