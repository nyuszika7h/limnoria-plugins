# Copyright 2017, nyuszika7h <nyuszika7h@gmail.com>
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

import httplib
import math
import re
import time
import traceback

import arrow
import requests

from supybot import callbacks, commands, schedule
from supybot.commands import *

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('CurrencyConverter')
except ImportError:
    # Placeholder that allows to run the plugin
    # on a bot without the i18n module
    _ = lambda x: x


def getPositiveFloat(irc, msg, args, state, type=_('positive floating point number')):
    try:
        f = float(args[0])

        if f <= 0:
            state.errorInvalid(type, args[0])

        state.args.append(float(args[0]))
        del args[0]
    except ValueError:
        state.errorInvalid(type, args[0])


commands.addConverter('positiveFloat', getPositiveFloat)


_CURRENCY_CODE_RE = re.compile(r'(?i)^[a-z]{3}$')

_CURRENCY_CODE_MSG = """
Please refer to the list at
http://www.xe.com/iso4217.php#section2 for valid currency codes.
""".replace('\n', ' ').strip()


class CurrencyConverter(callbacks.Plugin):
    """
    This plugin provides currency conversion
    through the free JSON API at free.currencyconverterapi.com.
    """

    def __init__(self, irc):
        self.__parent = super(CurrencyConverter, self)
        self.__parent.__init__(irc)

        self.irc = irc
        self.cache = {}

    @staticmethod
    def _round(num, precision, fixedRound):
        if fixedRound:
            return round(num, precision)
        else:
            return round(num, max(precision - math.ceil(math.log10(num)), 0))

    def _exchange(self, amount, source, target):
        fq = '_'.join((source, target))
        rq = '_'.join((target, source))

        q = ','.join((fq, rq))

        if (fq in self.cache
                and time.time() < (self.cache[fq]['lastUpdate'] +
                                   self.registryValue('refreshInterval'))):
            return (self.cache[fq]['exchangeRate'] * amount,
                    self.cache[fq]['lastUpdate'])
        else:
            try:
                r = requests.get('https://free.currencyconverterapi.com/api/v6/convert',
                                 params={'q': q,
                                         'compact': 'ultra',
                                         'apiKey': self.registryValue('apiKey')})
                r.raise_for_status()

                data = r.json()

                fwdRate = data[fq]
                revRate = data[rq]

                t = time.time()

                self.cache[fq] = {'exchangeRate': fwdRate,
                                  'lastUpdate': t}

                self.cache[rq] = {'exchangeRate': revRate,
                                  'lastUpdate': t}

                return (fwdRate * amount, None)
            except requests.exceptions.HTTPError:
                status_name = httplib.responses[r.status_code]
                self.irc.error(f'HTTP Error {r.status_code}: {status_name}')
                traceback.print_exc()
            except Exception as e:
                if fq in self.cache:
                    self.irc.error('{0.__class__.__name__}: {0}'.format(e))
                    traceback.print_exc()

                    return (self.cache[fq]['exchangeRate'] * amount,
                            self.cache[fq]['lastUpdate'])
                else:
                    raise

    @wrap([optional('positiveFloat', 1), 'something', optional(('literal', ('in', 'to'))), 'something'])
    def exchange(self, irc, msg, args, amount, source, _, target):
        """[<amount>] <source currency> [in|to] <target currency>

        Converts <amount> of <source currency> to <target currency>
        through the free JSON API at free.currencyconverterapi.com.
        If no amount is specified, it is assumed to be 1
        and the base exchange rate will be returned.
        """

        for currency in (source, target):
            if not _CURRENCY_CODE_RE.search(currency):
                irc.error(('{0!r} is not a valid three-letter currency '
                           'code. ' + _CURRENCY_CODE_MSG).format(currency),
                          Raise=True)

        source = source.upper()
        target = target.upper()

        try:
            (result, cached) = self._exchange(amount, source, target)
        except KeyError:
            irc.error('At least one of the currencies you entered is '
                      'invalid. ' + _CURRENCY_CODE_MSG, Raise=True)

        precision = self.registryValue('precision')
        fixedRound = self.registryValue('fixedRound')

        amount = '{0:,}'.format(self._round(amount, precision, fixedRound))
        result = '{0:,}'.format(self._round(result, precision, fixedRound))

        if not fixedRound:
            amount = re.sub(r'\.0$', '', str(amount))
            result = re.sub(r'\.0$', '', str(result))

        if cached:
            cachedText = ' (cached {0})'.format(arrow.get(cached).humanize())
        else:
            cachedText = ''

        irc.reply('{0} {1} = {2} {3}{4}'.format(
            amount, source, result, target, cachedText))


Class = CurrencyConverter


# vim:set tabstop=4 shiftwidth=4 softtabstop=0 expandtab textwidth=79:
