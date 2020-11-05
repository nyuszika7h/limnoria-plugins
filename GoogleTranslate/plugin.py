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

import bs4
import requests

from supybot import callbacks, i18n
from supybot.commands import wrap, optional

_ = i18n.PluginInternationalization('GoogleTranslate')


class GoogleTranslate(callbacks.Plugin):
    """
    This plugin lets you use Google Translate without an API key.
    """

    @wrap(['somethingWithoutSpaces', 'somethingWithoutSpaces', 'text'])
    def translate(self, irc, msg, args, source_lang, target_lang, text):
        """<source language> <target language> <text>

        Translates <text> from <source language> to <target language> using Google Translate. Use language codes, e.g. "en" for English and "es" for Spanish. To auto-detect the source language, use "auto".
        """

        r = requests.get('https://translate.google.com/m', params={
            'sl': source_lang,
            'hl': target_lang,
            'q': text
        })

        if not r.ok:
            irc.error(_('HTTP Error %d: %s'), r.status_code, r.reason.title(),
                      Raise=True)

        soup = bs4.BeautifulSoup(r.text)

        result = soup.find('div', class_='t0')

        if not result.text:
            irc.error(_('Nothing returned by Google Translate'), Raise=True)

        irc.reply(result.text)


Class = GoogleTranslate
