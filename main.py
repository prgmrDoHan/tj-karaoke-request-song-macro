import json

import modules.tjKoraoke as tj
import modules.freeProxy as fp
import modules.macro as macro

links= []
def logging(msg):
    print("[Log]",msg)

with open('setting.macro.json') as f:
    settings = json.load(f)

for song in settings['songsToRecommend']:
    links.append(tj.get_recommendLink(
        str(song['songType']),
        str(song['singer']),
        str(song['songTitle'])
    ))

tjMacro = macro.tjKaraoke(links)

if settings['howDo'] == "proxy":
    freeProxy = fp.proxies(
        str(settings['proxyType'])
    )
    proxies = freeProxy.get_list()
    logging("Start MACRO.")
    tjMacro.proxy(proxies)
elif settings['howDo'] == "tor":
    logging("Start MACRO.")
    tjMacro.tor()
elif settings['howDo'] == "all":
    freeProxy = fp.proxies(
        str(settings['proxyType'])
    )
    proxies = freeProxy.get_list()
    logging("Proxies Count:"+str(len(proxies)))
    print(proxies)
    # logging("Start MACRO.")
    # tjMacro.proxy(proxies,str(settings['proxyType']))
    # tjMacro.tor()