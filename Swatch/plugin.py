# Copyright 2014-2015, nyuszika7h <nyuszika7h@gmail.com>
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

import time as time_

import arrow

from supybot import callbacks, conf
from supybot.commands import optional, wrap


class Swatch(callbacks.Plugin):
    """
    This plugin provides commands to convert from and to Swatch Internet
    Time, also known as beat time.
    """

    @wrap([optional('float')])
    def beats(self, irc, msg, args, seconds):
        """[<seconds>]

        Returns the current Swatch Internet Time.  If <seconds> is
        specified, it's interpreted as an offset in seconds from
        midnight UTC+1. For example, "beats [seconds 17h 30m]" returns
        the Swatch Internet Time for 17:30 UTC+1.
        """

        now = arrow.now('UTC+1')

        if seconds is None:
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            seconds = (now - midnight).seconds

        # Wrap around
        seconds %= 86400

        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        irc.reply('%d' % int((seconds + (minutes * 60) +
                             (hours * 3600)) / 86.4))

    @wrap([optional('channel'), optional('nonInt'), 'float'])
    def time(self, irc, msg, args, channel, fmt, beats):
        """[<format>] <beats>

        Returns the current time represented by <beats> in <format>, or
        if <format> is not given, uses the configurable format for the
        current channel.
        """

        if not fmt:
            if channel:
                fmt = conf.get(conf.supybot.reply.format.time, channel)
            else:
                fmt = conf.supybot.reply.format.get('time')

        midnight = arrow.now('UTC+1').replace(hour=0, minute=0, second=0, microsecond=0)
        seconds = float(midnight.strftime('%s')) + (beats * 86.4)

        irc.reply(time_.strftime(fmt, time_.localtime(seconds)))


Class = Swatch
