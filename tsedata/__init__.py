from __future__ import absolute_import

from .tsedata import GetTSEData, TSEDump


class TSE:
    def __init__(self):
        _party_list = ['DEM', 'NOVO', 'PCB', 'PCO', 'PC_do_B', 'PDT', 'PEN',
        'PHS', 'PMB', 'PMDB', 'PMN', 'PP', 'PPL', 'PPS', 'PR',
        'PRB', 'PROS', 'PRP', 'PRTB', 'PSB', 'PSC', 'PSD', 'PSDB',
        'PSDC', 'PSL', 'PSOL', 'PSTU', 'PT', 'PTB', 'PTC', 'PTN',
        'PT_do_B', 'PV', 'REDE', 'SD']
        _uf_list = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
        'MA', 'MT', 'MS', 'MG', 'PR', 'PB', 'PA', 'PE', 'PI', 'RJ',
        'RN', 'RS', 'RO', 'RR', 'SC', 'SE', 'SP', 'TO']
        self._party_list = _party_list
        self._uf_list = _uf_list

    def download(self, partido=None, estado=None):
        if partido is None:
            partido = self._party_list
        if estado is None:
            estado = self._uf_list
        list_files = GetTSEData().getdata(party_list=partido,
                                          uf_list=estado)
        return list_files

    def extract(self, partido=None, estado=None):
        if partido is None:
            partido = self._party_list
        if estado is None:
            estado = self._uf_list
        filiados = TSEDump().filiation_data(party_list=partido,
                                            uf_list=estado)
        return filiados
