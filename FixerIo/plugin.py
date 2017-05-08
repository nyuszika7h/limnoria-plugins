# Copyright 2017, nyuszika7h <nyuszika7h@openmailbox.org>
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

import json
import re
from types import SimpleNamespace

import requests

from supybot import callbacks, commands, i18n, schedule
from supybot.commands import optional, wrap

_ = i18n.PluginInternationalization('FixerIo')


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


def s(x):
    return re.sub(r"\s+", " ", x).strip()


class FixerIo(callbacks.Plugin):
    """
    This plugin provides currency conversion through Fixer.io's free JSON API.
    """

    def __init__(self, irc):
        self.__parent = super(FixerIo, self)
        self.__parent.__init__(irc)

        if 'FixerIoUpdate' in schedule.schedule.events:
            # Remove the event in case it still exists
            # (e.g. if the plugin died uncleanly due to an error)
            schedule.removeEvent('FixerIoUpdate')

        # Update the exchange rates every day
        schedule.addPeriodicEvent(
            self._update, 86400, name='FixerIoUpdate', now=True)

    def die(self):
        schedule.removeEvent('FixerIoUpdate')

    def _update(self):
        self.log.info('Updating exchange rates from Fixer.io')
        r = requests.get('https://api.fixer.io/latest')
        self.data = SimpleNamespace(**r.json())

    def _exchangeRate(self, source, target):
        if source == target:
            return 1
        elif source == self.data.base:
            return self.data.rates[target]
        elif target == self.data.base:
            return 1 / self.data.rates[source]
        else:
            return self.data.rates[target] / self.data.rates[source]

    @wrap([optional('positiveFloat', 1), 'something', 'to', 'something'])
    def exchange(self, irc, msg, args, amount, source, target):
        """[<amount>] <source currency> [to] <target currency>

        Converts <amount> of <source currency> to <target currency> through
        Fixer.io's free JSON API. If no amount is specified, it is assumed to
        be 1 and the base exchange rate will be returned.
        """

        source = source.upper()
        target = target.upper()

        err = None

        if (source not in self.data.rates) and (target not in self.data.rates):
            err = "Unknown currencies: %r and %r. " % (source, target)

        try:
            result = amount * self._exchangeRate(source, target)
        except KeyError as e:
            if not err:
                err = "Unknown currency: %r. " % e.args[0]

            err += s("""Please use three-letter (ISO 4217) currency codes
listed on the European Central Bank's website (https://v.gd/ecbcurrencies).
Other currencies are not currently supported by this plugin.""")

            irc.error(err, Raise=True)

        irc.reply('%.2f %s = %.2f %s (as of %s)' % (
            amount, source, result, target, self.data.date))

    @wrap([('checkCapability', 'admin')])
    def update(self, irc, msg, args):
        """takes no arguments

        Updates the exchange rates from Fixer.io manually. There is normally no
        need to do this as they are automatically updated every day. Requires
        admin capability to avoid abuse.
        """

        self._update()
        irc.replySuccess()


Class = FixerIo
