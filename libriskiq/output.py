#!/usr/bin/env python
__author__ = 'RiskIQ Research'
__version__ = '0.1-ALPHA'
import json


class GenericOutput(object):
    def __init__(self, results):
        api_results = []
        if type(results) is list:
            for api_result in results:
                if 'records' in api_result:
                    r = api_result.pop('records')
                    api_results.extend(r)
                else:
                    api_results.append(api_result)
        elif type(results) is dict:
            if 'records' in results:
                api_results = results['records']
            else:
                api_results = [api_results]
        self._results = api_results

    def _format_header(self, header_content):
        char_len = 80
        return '-- %s ' % header_content + '-' * (char_len-len(header_content))

    @property
    def results(self):
        return self._results

    @property
    def csv(self):
        raise NotImplemented('CSV Output Not Implemented')

    @property
    def json(self):
        return json.dumps(self._results, indent=4, separators=(',', ': '))

    @property
    def count(self):
        return list(self._results)

    @property
    def text(self):
        return str(self._results)

    @property
    def count(self):
        return len(self._results)


class PassiveDNS(GenericOutput):
    @property
    def text(self):
        r = list()
        for record in self._results:
            r.append(self._format_header(record['name']))
            r.append('Times Seen: %s' % record['count'])
            r.append('Record Type: %s' % record['rrtype'])
            r.append('Record First Seen: %s' % record['firstSeen'])
            r.append('Record Last Seen: %s' % record['lastSeen'])
            r.append('Record Responses: %s' % '\n                  '.join(record['data']))
        return '\n'.join(r)

    @property
    def csv(self):
        return


class BlacklistIncident(GenericOutput):

    @property
    def text(self):
        return repr(self._results)


class BlacklistEntry(GenericOutput):

    @property
    def text(self):
        r = list()
        for record in self._results:
            r.append(self._format_header(record['hostname']))
            r.append('Match URL: %s' % record['url'])
            r.append('Alexa Rank: %s' % record['rank'])
            r.append('Match Type: %s' % record['matchType'])
            r.append('Description: %s' % record['description'])
            r.append('Score: %s' % record['score'])
            if 'entries' in record:
                e = []
                entries = record['entries']
                for entry in entries:
                    if 'type' in entry:
                        e.append('-- %s' % entry.pop('type'))
                        for k, v in entry.items():
                            e.append('%s: %s' % (k, v))
                entries = "\n         ".join(e)
                r.append('Entries: %s' % entries)
            attributes = [i.capitalize() for i in ['malware', 'phishing', 'spam'] if record[i]]
            r.append('Flags: %s' % ", ".join(attributes))
        return "\n".join(r)