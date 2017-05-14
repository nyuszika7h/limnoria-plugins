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

from supybot import conf, registry

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('CurrencyConverter')
except:
    # Placeholder that allows to run the plugin
    # on a bot without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot-wizard to configure this module.
    # 'advanced' is a bool that specifies whether the user identified
    # themself as an advanced user or not.  You should effect your
    # configuration by manipulating the registry as appropriate.

    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('CurrencyConverter', True)


CurrencyConverter = conf.registerPlugin('CurrencyConverter')

# This is where your configuration variables (if any) should go. For example:
# conf.registerGlobalValue(CurrencyConverter, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))
conf.registerChannelValue(CurrencyConverter, 'precision',
    registry.Integer(3, _("""Determines the number of significant figures
    (or decimal points if 'fixedRound' is True) to round the output to.
    Note that numbers which have no digits after the decimal point are never
    further rounded.""")))
conf.registerChannelValue(CurrencyConverter, 'fixedRound',
    registry.Boolean(False, _("""Determines whether the output should be
    rounded to a fixed number of decimal places specified by 'precision'
    rather than significant figures.""")))


# vim:set tabstop=4 shiftwidth=4 softtabstop=0 expandtab textwidth=79:
