import requests
from bs4 import BeautifulSoup

def get_recommendLink(
                        song_type,
                        singer,
                        song_title,
                        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
                        timeout=5
                    ):
    url = f'https://www.tjmedia.com/tjsong/song_songRequestEnd_b.asp?dt_code={song_type+"0"}&song={singer}&title={song_title}'
    headers= headers
    timeout=timeout
    res = requests.get(url, headers=headers,timeout=timeout)
    soup = BeautifulSoup(res.content, 'lxml')
    request_code=soup.select("#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(7) > a")[0].get('href').split('(')[1][:-1]
    request_link= f'https://www.tjmedia.com/tjsong/song_songRequestEnd_save.asp?dt_code={song_type+"0"}&song={singer}&title={song_title}&intTotalCount=0&intPageCount=0&intPage=1&mode=4&idx={request_code}'
    return request_link