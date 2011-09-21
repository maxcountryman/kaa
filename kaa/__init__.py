#from __future__ import absolute_import
from irctk import Bot

bot = Bot()
bot.config.from_pyfile('settings.cfg')

import kaa.plugins
