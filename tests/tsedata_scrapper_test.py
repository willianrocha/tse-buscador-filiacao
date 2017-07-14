import unittest
from os import remove, rmdir
from mockito import when, mock

import requests
from tsedata.tsedata import GetTSEData

class TSEDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tse = GetTSEData()
        cls.file_test =  'tests/files/filiados_pcb_rr.zip'
        cls.file_test_tmp = 'tests/tmp/'

    @classmethod
    def tearDownClass(cls):
        remove(cls.file_test)
        rmdir(cls.file_test_tmp)

    def test_tse_url_path(cls):
        url = 'http://agencia.tse.jus.br'
        path = '/estatistica/sead/eleitorado/filiados/uf/'
        fname = 'filiados_pcb_rr.zip'
        full_path = '{}{}{}'.format(url, path, fname)

        tse_path = requests.get(full_path)
        assert tse_path.ok == True

    def test_download_files(cls):
        url = 'http://agencia.tse.jus.br'
        path = '/estatistica/sead/eleitorado/filiados/uf/'
        fname = 'filiados_pcb_rr.zip'
        full_path = '{}{}{}'.format(url, path, fname)
        tdir = 'tests/tmp/'
        path_to_tse = GetTSEData()
        path_to_tse_mock = '{}{}'.format(tdir, fname)
        when(path_to_tse) \
            .download_file(full_path, fname, tdir) \
            .thenReturn(path_to_tse_mock)

        assert cls.tse.download_file(full_path, fname, tdir) \
               == path_to_tse.download_file(full_path, fname, tdir)

    def test_gettsedata_getdata_new(cls):
       p = ['pcb']
       u = ['rr']
       rdirectory_test = 'tests/files/'
       tdirectory_test = 'tests/tmp/'
       getdata_mock = GetTSEData()
       when(getdata_mock) \
            .getdata(p, u, rdirectory_test, tdirectory_test) \
            .thenReturn(['tests/tmp/filiados_pcb_rr.zip'])

       assert cls.tse.getdata(p, u, rdirectory_test, tdirectory_test) \
              == getdata_mock.getdata(p, u, rdirectory_test, tdirectory_test)
