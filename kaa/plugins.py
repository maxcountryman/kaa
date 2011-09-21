from kaa import bot
from kaa.utilities import bitly, unescape

import json
import urllib
import urlparse

import requests

@bot.command('.')
@bot.command
def usage(context):
    plugin = context.args
    if plugin:
        for p in bot.config['PLUGINS']:
            if plugin == p['hook']:
                response = []
                for func in p['funcs']:
                    response += [func.__doc__]
                return ', '.join(response)
    else:
        p = [p['hook'] for p in bot.config['PLUGINS']]
        p = ', '.join(p)
        return 'Plugins currently loaded: ' + p

@bot.command('e')
@bot.command
def erlang(context):
    '''erlang interpreter: .e <expression>'''
    expression = context.args
    base_url = 'http://www.tryerlang.org/api/evaluate'
    query = requests.post(base_url, data={'expression': expression}).content
    result = json.loads(query)['result']
    return result

@bot.command('p')
@bot.command
def python(context):
    '''python interpreter: .p <expression>'''
    query = urllib.quote(context.args)
    url = 'http://eval.appspot.com/eval?statement={0}'.format(query)
    response = requests.get(url)
    
    if not response.ok:
        return 'Error: {0}'.format(response.status_code)
    else:
        response = response.read()
    
    if response.startswith('Traceback (most recent call last):'):
            response = response.splitlines()[-1]
            return response
    else:
        return response[:500]

@bot.command('g')
@bot.command
def google(context):
    '''google search: .g <query>'''
    url = urlparse.urlunsplit(
            (
                'http', 
                'ajax.googleapis.com', 
                '/ajax/services/search/web', 
                'v=1.0&q={0}'.format(context.args), 
                None,
                )
            )
    
    response = urllib.urlopen(url)
    response = json.loads(response.read())['responseData']['results']
    
    if not response:
        error = 'Request error: no results'
        return error
    else:
        url = urllib.unquote(response[0]['url'])
        if 'www.youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=', 1)[-1]
            return get_youtube_description(video_id)
        url = bitly.shorten(longurl=url)['url']
        title = unescape(response[0]['titleNoFormatting'])
        response = title + ' - ' + url 
        return response

