from curses.ascii import isupper
from dataclasses import replace
import requests
from bs4 import BeautifulSoup
import re
import warnings
import modules.jsUnpacker as jsUnpacker

def changeNum(source):
    num=["Zero","One","Two","Three","Four","Five","Six","Seven","Eight","Nine"]
    for i in range(len(num)):
        source = source.replace(num[i], str(i))
    return source

class proxies:
    def __init__(
                    self,
                    type,
                    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
                    timeout=5
                ):
        self.proxyType=type
        self.headers=headers
        self.timeout=timeout

    def get_list(self):
        url = 'https://spys.one/asia-proxy/'
        headers= self.headers
        timeout = self.timeout
        data = {
            "xpp" : "5",
            "tldc" : "0",
            "xf1" : "0",
            "xf2" : "0",
            "xf5" : "2"
        }
        if self.proxyType == "HTTP":
            data = {
                "xpp" : "5",
                "tldc" : "0",
                "xf1" : "0",
                "xf2" : "1",
                "xf5" : "1"
            }
        elif self.proxyType != "SOCKS":
            warnings.warn("Unknown 'proxyType'",SyntaxWarning)
                   
        r = requests.post(url, data=data,headers=headers,timeout=timeout)
        soup = BeautifulSoup(r.content, 'lxml')
        result = []

        ports = {}
        script = soup.select_one("body > script")

        unpackedScript = jsUnpacker.unpack(str(script.text.replace(r"\u005e", "^")))

        for row in unpackedScript.split(";"):
            if "^" in row:
                line = row.split("=")
                ports[line[0]] = line[1].split("^")[0]

        trs = soup.select("tr[onmouseover]")
        for tr in trs:
            e_ip = tr.select_one("font.spy14")
            ip = ""

            # Get port number
            e_port = tr.select_one("script")
            port = ""
            if e_port is not None:
                re_port = re.compile(r'\(([a-zA-Z0-9]+)\^[a-zA-Z0-9]+\)')
                match = re_port.findall(e_port.text)
                for item in match:
                    port = port + ports[item]
            else:
                continue
            
            # port to Num
            changedPort = changeNum(port)

            # Get ip number
            if e_ip is not None:
                for item in e_ip.findAll('script'):
                    item.extract()
                ip = e_ip.text
            else:
                continue

            # Get uptime value (%)
            tds = tr.select("td")
            is_skip = False
            for td in tds:
                e_pct = td.select_one("font > acronym")
                if e_pct is not None:
                    pct = re.sub('([0-9]+)%.*', r'\1', e_pct.text)
                    if not pct.isdigit():
                        is_skip = True
                else:
                    continue
            if is_skip:
                continue

            result.append((ip + ":" + changedPort, pct))

        # Sort by uptime value
        result.sort(key=lambda element : int(element[1]), reverse=True)

        return result