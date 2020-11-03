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

import re

from supybot import callbacks, commands, i18n, ircmsgs, ircutils

_ = i18n.PluginInternationalization('RelayHandler')


class RelayHandler(callbacks.Plugin):
    """
    This plugin handles commands from authorized relays.
    """

    def __init__(self, irc):
        self.__parent = super(RelayHandler, self)
        self.__parent.__init__(irc)

    def inFilter(self, irc, msg):
        if msg.prefix.endswith('!relayhandler@relayhandler'):
            # Don't parse our own injected messages
            return msg

        if msg.command != "PRIVMSG":
            # Don't parse non-PRIVMSGs
            return msg

        channel = msg.args[0]

        if not irc.isChannel(channel):
            return msg

        trustedRelayHostmask = re.compile(self.registryValue('trustedRelayHostmask', channel))
        relayPrefixes = self.registryValue('relayPrefix', channel).split()
        if not trustedRelayHostmask:
            self.log.debug('No authorized relays configured for %s',
                           channel)

        m = None

        for relayPrefix in relayPrefixes:
            m = re.match(relayPrefix, ircutils.stripFormatting(msg.args[1]))

            if m is not None:
                break

        if m is None:
            self.log.debug('Message does not match relay pattern')
            return msg

        nick = re.sub(r'\s', '', ircutils.stripFormatting(m.group('nick')))
        message = m.group('message')

        assert(nick is not None)
        assert(message is not None)

        if not re.match(trustedRelayHostmask, msg.prefix):
            self.log.debug('Ignored message from unauthorized relay %s to '
                           '%s: %r', msg.prefix, channel, msg.args[1])
            return msg

        msg.args = (channel, message)

        self.log.debug('Handling relay message from %s in %s (relay: %s): %r',
                       nick, channel, msg.prefix, message)

        prefix = '@%s!%s@relayhandler' % (nick, nick)

        return ircmsgs.IrcMsg(prefix=prefix,
                              command='PRIVMSG',
                              args=(channel, message))


Class = RelayHandler


# vim: set tabstop=4 shiftwidth=4 expandtab textwidth=79:
