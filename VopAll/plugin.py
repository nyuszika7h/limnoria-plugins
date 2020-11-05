# Copyright 2016, nyuszika7h <nyuszika7h@gmail.com>
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

from supybot import callbacks, i18n, ircmsgs
from supybot.commands import getopts, wrap

_ = i18n.PluginInternationalization('VopAll')


class VopAll(callbacks.Plugin):
    """
    This plugin provides commands to (de)voice or (de)op everyone in a channel.
    """


    def _split_modes(self, users):
        users = list(users)

        while users:
            batch = users[:4]
            users = users[4:]
            yield batch


    @wrap(['op', 'channel'])
    def voiceall(self, irc, msg, args, channel):
        """[<channel>]

        Voices everyone in the channel. <channel> is only necessary
        if the message isn't sent in the channel itself.
        """

        chanstate = irc.state.channels[channel]
        users = [user for user in chanstate.users if not chanstate.isVoice(user)]

        for batch in self._split_modes(users):
            irc.queueMsg(ircmsgs.voices(channel, batch))

    @wrap(['op', 'channel'])
    def devoiceall(self, irc, msg, args, channel):
        """[<channel>]

        Devoices everyone in the channel. <channel> is only necessary
        if the message isn't sent in the channel itself.
        """

        chanstate = irc.state.channels[channel]
        users = [user for user in chanstate.users if chanstate.isVoice(user)]

        for batch in self._split_modes(users):
            irc.queueMsg(ircmsgs.devoices(channel, batch))

    @wrap(['op', 'channel'])
    def opall(self, irc, msg, args, channel):
        """[<channel>]

        Ops everyone in the channel. <channel> is only necessary
        if the message isn't sent in the channel itself.
        """

        chanstate = irc.state.channels[channel]
        users = [user for user in chanstate.users if not chanstate.isOp(user)]

        for batch in self._split_modes(users):
            irc.queueMsg(ircmsgs.ops(channel, batch))

    @wrap([getopts({'include-self': ''}), 'op', 'channel'])
    def deopall(self, irc, msg, args, include_self, channel):
        """[--include-self] [<channel>]

        Deops everyone in the channel. Unless --include-self is given,
        the bot won't deop itself. <channel> is only necessary
        if the message isn't sent in the channel itself.
        """

        chanstate = irc.state.channels[channel]
        users = [user for user in chanstate.users if chanstate.isOp(user)]

        if irc.nick in users and not include_self:
            users.remove(irc.nick)

        for batch in self._split_modes(users):
            irc.queueMsg(ircmsgs.deops(channel, batch))


Class = VopAll
