"""
Reader for the http://entilocali.opencontent.it/
"""

import datetime
import posixpath
import urlparse

import requests

from datacat.readers import BaseReader
from datacat.schema import DATE_FORMAT


def urljoin(base, *parts):
    """A mix between urlparse.urljoin() and posixpath.join()"""
    return urlparse.urljoin(base, posixpath.join(*parts))


class TrentoEntiLocaliReader(BaseReader):
    default_conf = {
        'url': 'http://entilocali.opencontent.it/',
    }

    @property
    def od_api_url(self):
        return urlparse.urljoin(self.conf['url'], '/api/opendata/v1/')

    def _list_datasets(self):
        url = urlparse.urljoin(self.od_api_url, 'dataset')
        response = requests.get(url)
        assert response.ok
        return response.json()

    def _get_dataset(self, dataset_id):
        url = urljoin(self.od_api_url, 'dataset', dataset_id)
        response = requests.get(url)
        assert response.ok
        return response.json()

    def _normalize_dataset(self, dataset):

        def date_to_iso(dt):
            dtm = datetime.datetime.fromtimestamp(float(dt))
            return dtm.strftime(DATE_FORMAT)

        return {
            '_id': dataset['id'],
            '_type': 'dataset',
            'title': dataset['title'],
            'description': dataset.get('notes'),
            'author': {
                'name': dataset.get('author'),
                'email': dataset.get('author_email'),
            },
            'maintainer': {
                'name': dataset.get('maintainer'),
                'email': dataset.get('maintainer_email'),
            },
            'category': dataset.get('categories'),
            'license': dataset.get('license_id'),
            'temporal_coverage': [
                date_to_iso(dataset.get('from_time')),
                date_to_iso(dataset.get('to_time')),
            ],
            'landing_page': dataset.get('url'),

            # The filter(bool, ...) is to exclude empty strings
            'tags': filter(bool, [
                t.strip()
                for t in dataset.get('tags', '').split(',')
            ]),

            'distribution': [
                self._normalize_distribution(d)
                for d in dataset['resources']
            ],
        }

    def _normalize_distribution(self, distribution):
        return {
            # '_id': ...
            '_type': 'distribution',
            'title': distribution['name'],
            'description': distribution.get('description'),
            'extra': {
                'resource_type': distribution.get('resource_type'),
                'format': distribution.get('format'),
                'media_type': distribution.get('mimetype'),
                'byte_size': distribution.get('size'),
                'download_url': distribution.get('url'),
            },
        }

    def crawl_data(self):
        for dataset_id in self._list_datasets():
            dataset = self._get_dataset(dataset_id)
            yield self._normalize_dataset(dataset)
