import requests as req
import subprocess
import os
import warnings
import platform

def logging(msg):
    print("[Log]",msg)

class tjKaraoke:
    def __init__(
                    self,
                    links,
                    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
                    timeout=5
                ):
        self.links = links
        self.headers=headers
        self.timeout=timeout

    def tor(self):
        if str(platform.system())!="Linux":
            raise Exception('This feature is only available on Linux.')
            
        if os.geteuid() != 0:
            exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

        headers= self.headers
        timeout= self.timeout

        subprocess.Popen(['systemctl', 'start']+['tor']).wait()
        logging("Start 'tor' to change IP.")

        while True:
            proxies = {
                'http': "socks5://127.0.0.1:9050",
                'https': "socks5://127.0.0.1:9050",
            }
            
            try:
                for url in self.links:
                    res= req.get(
                        url,
                        headers=headers,
                        proxies=proxies,
                        timeout=timeout
                    )

                    if "alert" not in res.text:
                        logging("Successful song recommendation.")
                    else:
                        logging("Changed ip, but it was already recommended.")
            except Exception as e:
                if len(str(e)) > 20:
                    e= e[:20]
                logging(str(e))

            subprocess.Popen(['systemctl', 'restart']+['tor']).wait()
            logging("Stop tor.")

    def proxy(self,proxiesList,proxyType):
        headers= self.headers
        timeout= self.timeout

        for i in proxiesList:
            if proxyType == "HTTP":
                proxies = {
                    'http': "http://"+i[0],
                    'https': "https://"+i[0],
                }
            else:
                proxies = {
                    'http': "socks5://"+i[0],
                    'https': "socks5://"+i[0],
                }
            
            try:
                for url in self.links:
                    res= req.get(
                        url,
                        headers=headers,
                        proxies=proxies,
                        timeout=timeout
                    )

                    if "alert" not in res.text:
                        logging("Successful song recommendation.")
                    else:
                        logging("Changed proxy, but it was already recommended.")
            except Exception as e:
                e=str(e)
                if len(e) > 20:
                    e= e[:20]
                logging(str(e))

        return 1