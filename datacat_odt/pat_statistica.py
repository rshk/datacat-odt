"""
Reader for the http://www.statistica.provincia.tn.it API
"""

import requests

from datacat.readers import BaseReader


class PatStatisticaReader(BaseReader):
    """
    Statistica provinciale
    """

    default_conf = {
        'url': 'http://www.statweb.provincia.tn.it/IndicatoriStrutturali/'
               'exp.aspx?list=i&fmt=json',
    }

    def _list_datasets(self):
        response = requests.get(self.conf['url'])
        assert response.ok
        for item in response['IndicatoriStrutturali']:
            yield item['URL']

    def crawl_data(self):
        pass


class PatStatisticaSubproReader(BaseReader):
    """
    Statistica Sub-provinciale
    """

    default_conf = {
        'url': 'http://www.statweb.provincia.tn.it/INDICATORISTRUTTURALISubPro'
               '/exp.aspx?list=i&fmt=json',
    }

    def _list_datasets(self):
        already_followed = set()
        response = requests.get(self.conf['url'])
        assert response.ok
        for item in response['Lista indicatori strutturali SP']:
            if item['URLIndicatoreD'] not in already_followed:
                already_followed.add(item['URLIndicatoreD'])
                yield item['URLIndicatoreD']

            ## Follow links to sub-tables
            for url in item['URLTabDenMD'], item['URLTabNumMD']:
                if url in already_followed:
                    continue
                already_followed.add(url)
                resp = requests.get(url)
                assert resp.ok
                data = resp.json()
                assert len(data.keys()) == 1
                url_tabd = data[data.keys()[0]]['URLTabD']
                if url_tabd not in already_followed:
                    already_followed.add(url_tabd)
                    yield url_tabd

            resp = requests.get()
            assert resp.ok
            data = resp.json()
            assert len(data.keys()) == 1
            yield data['URLTabD']

            # note: we have URLTabDenMD and URLTabNumMD too, indicating
            # the denominator and numerator tables respectively.

    def crawl_data(self):
        pass
