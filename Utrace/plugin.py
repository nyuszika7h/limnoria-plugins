# Copyright 2013-2015, nyuszika7h <nyuszika7h@openmailbox.org>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import bs4
import requests

from supybot import callbacks, i18n
from supybot.commands import wrap

_ = i18n.PluginInternationalization('Utrace')


def _trim(s):
    result = []

    for line in s.splitlines():
        stripped = line.strip()

        if stripped:
            result.append(stripped)

    return '\n'.join(result)


class Utrace(callbacks.Plugin):
    """
    This plugin provides a command to look up the approximate geographical
    location of hosts using utrace.de's API. Please note that the API only
    allows 100 requests per day from the same IP address.
    """

    @wrap(['somethingWithoutSpaces'])
    def utrace(self, irc, msg, args, address):
        """<address>

        Looks up <address> using utrace.de's API.
        """

        self.log.info(_('Looking up %s on utrace.de'), address)

        r = requests.get('http://xml.utrace.de', params={'query': address},
                         allow_redirects=False)

        if not r.ok:
            irc.error(_('HTTP Error %d: %s'), r.status_code, r.reason.title(),
                      Raise=True)

        if 'location' in r.headers:
            irc.error(_('Received redirect to %s. This most likely means you'
                        'exceeded the query limit.') % r.headers['location'])

        soup = bs4.BeautifulSoup(r.text)

        if getattr(soup, 'results', None) is None:
            irc.error(_('Invalid response: %r'), soup, Raise=True)

        result = soup.results.result

        if not result.text:
            irc.error(_('Empty response'), Raise=True)

        info = {
            'ip': result.ip.text,
            'host': result.host.text,
            'isp': result.isp.text,
            'org': result.org.text,
            'region': result.region.text,
            'countrycode': result.countrycode.text,
            'location': [],
            'latitude': result.latitude.text,
            'longitude': result.longitude.text,
            'queries': result.queries.text
        }

        if info['region']:
            info['location'].append(info['region'])
        if info['countrycode']:
            info['location'].append(info['countrycode'])

        info['location'] = ', '.join(info['location'])

        for (key, value) in info.items():
            if not value:
                info[key] = '(none)'

        self.log.info(_('Utrace: %d out of 100 queries used'), info['queries'])

        irc.reply(_trim("""
            IP: %(ip)s
            Host: %(host)s
            ISP: %(isp)s
            Organization: %(org)s
            Location: %(location)s
            Latitude: %(latitude)s
            Longitude: %(longitude)s
            Queries: %(queries)s/100
        """).replace('\n', ' | ') % info)


Class = Utrace
