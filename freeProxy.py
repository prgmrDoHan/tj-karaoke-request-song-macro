import requests
from bs4 import BeautifulSoup
import re

def get_proxy_list():
    url = 'https://spys.one/en/socks-proxy-list/'
    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    data = { "xx0":"0e1dddce3adc16f9f1df4d75ac28eac5","xpp" : "4", "xf1" : "0", "xf2" : "0", "xf4" : "0", "xf5" : "2" }
    r = requests.post(url, data=data,headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Result list of IP and Port
    result = []

    # Get pre-defined number combination
    ports = {}
    script = soup.select_one("body > script")
    for row in script.text.split(";"):
        if "^" in row:
            line = row.split("=")
            ports[line[0]] = line[1].split("^")[0]

    # Each rows
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

        result.append((ip + ":" + port, pct))

    # Sort by uptime value
    result.sort(key=lambda element : int(element[1]), reverse=True)

    return result


if __name__ == "__main__":
    proxy_list = get_proxy_list()
    print(proxy_list)
    print(proxy_list[0][0])