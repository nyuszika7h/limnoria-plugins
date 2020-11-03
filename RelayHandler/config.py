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

from supybot import conf, i18n, registry

_ = i18n.PluginInternationalization('RelayHandler')

RelayHandler = conf.registerPlugin('RelayHandler')

conf.registerChannelValue(RelayHandler, 'trustedRelayHostmask',
    registry.String('', _("""Regular expression for the hostmask of the
    relay(s) to trust.""")))
conf.registerChannelValue(RelayHandler, 'relayPrefix',
    registry.String('', _("""Regular expression for the format of messages sent
    by relay to look for. Use (?P<nick>PATTERN) to capture the nick and
    (?P<message>PATTERN) to capture the message. Colors are stripped from the
    message before matching. Due to Python not supporting multiple
    non-conflicting definitions of named groups, this configuration variable
    expects a list of regular expressions separated by spaces. If you need to
    match a literal space character, use \x20 (or \s, which includes other
    whitespace characters).""")))

# vim: set tabstop=4 shiftwidth=4 expandtab textwidth=79:
