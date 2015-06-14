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

"""
This plugin provides a command to look up the approximate geographical
location of hosts using utrace.de's API. Please note that the API only
allows 100 requests per day from the same IP address.
"""

from imp import reload

import supybot

from . import plugin

__version__ = ''
__author__ = supybot.Author('nyuszika7h', 'nyuszika7h', 'nyuszika7h@openmailbox.org')
__contributors__ = {}
__url__ = ''

# In case we're being reloaded.
reload(plugin)

if supybot.world.testing:
    from . import test

Class = plugin.Class
