import requests as req
import subprocess
import os
import freeProxy as fp

class tjKaraoke:
    def __init__(
                    self,
                    link,
                    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
                    timeout=5
                ):
        self.link = link
        self.headers=headers
        self.timeout=timeout

    def tor(self):
        if os.geteuid() != 0:
            exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

        url= self.link
        headers= self.headers
        timeout= self.timeout

        subprocess.Popen(['systemctl', 'start']+['tor']).wait()
        print('[tor start]')

        while True:
            proxies = {
                'http': "socks5://127.0.0.1:9050",
                'https': "socks5://127.0.0.1:9050",
            }
            
            try:
                res= req.get(
                    url,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout
                )

                if "alert" not in res.text:
                    print("Success")
                else:
                    print("Already Success IP")

            except Exception as e:
                print("raise ERROR ("+str(e)+")")

            subprocess.Popen(['systemctl', 'restart']+['tor']).wait()
            print('[tor reload]')

    def proxy(self):
        url= self.link
        headers= self.headers
        timeout= self.timeout

        proxy_list=fp.get_proxy_list()
        print(proxy_list)

        for i in proxy_list:
            proxies = {
                'http': "socks5://"+i[0],
                'https': "socks5://"+i[0],
            }
            
            try:
                res= req.get(
                    url,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout
                )

                if "alert" not in res.text:
                    print("Success")
                else:
                    print("Already Success IP")

            except Exception as e:
                print("raise ERROR ("+str(e)+")")
        return 1