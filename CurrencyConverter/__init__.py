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

"""
This plugin provides currency conversion
through the free JSON API at free.currencyconverterapi.com.
"""

import imp

import supybot

__version__ = ''

__author__ = supybot.Author('nyuszika7h', 'nyuszika7h', 'nyuszika7h@gmail.com')

# This is a dictionary mapping supybot.Author instances
# to lists of contributions.
__contributors__ = {}

__url__ = ''

from . import config, plugin

# In case we're being reloaded.
imp.reload(config)
imp.reload(plugin)
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if supybot.world.testing:
    from . import test

Class = plugin.Class
configure = config.configure


# vim:set tabstop=4 shiftwidth=4 softtabstop=0 expandtab textwidth=79:
