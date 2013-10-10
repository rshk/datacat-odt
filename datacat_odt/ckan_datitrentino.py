"""
Custom Ckan source for the customized Ckan 1.8 running
on dati.trentino.it
"""

from datacat.readers.ckan import CkanClient18, CKANReader


class CkanDatiTrentinoClient(CkanClient18):
    def normalize_dataset(self, dataset):
        new = super(CkanDatiTrentinoClient, self
                    ).normalize_dataset(dataset)
        return new

    def normalize_distribution(self, distribution):
        new = super(CkanDatiTrentinoClient, self
                    ).normalize_distribution(distribution)
        return new

    def normalize_organization(self, organization):
        new = super(CkanDatiTrentinoClient, self
                    ).normalize_organization(organization)
        return new


class CkanDatiTrentinoReader(CKANReader):
    def _get_ckan_client(self):
        if (1, 8) >= self.conf['ckan_version'] < (2, ):
            return CkanDatiTrentinoClient(**self.conf)
        return super(CkanDatiTrentinoReader, self)._get_ckan_client()
