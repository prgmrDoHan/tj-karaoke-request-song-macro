import requests
from bs4 import BeautifulSoup
import macro

song_type=str(input("노래 장르를 골라주세요. (Default: 1)\n[1]: 기요 | [2] POP | [3] JPOP | [4] 중국곡\n>> "))
singer=str(input("가수 >> "))
song_title=str(input("노래 제목 >> "))

url = f'https://www.tjmedia.com/tjsong/song_songRequestEnd_b.asp?dt_code={song_type+"0"}&song={singer}&title={song_title}'
headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content, 'lxml')

request_code=soup.select("#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(7) > a")[0].get('href').split('(')[1][:-1]
request_link= f'https://www.tjmedia.com/tjsong/song_songRequestEnd_save.asp?dt_code={song_type+"0"}&song={singer}&title={song_title}&intTotalCount=0&intPageCount=0&intPage=1&mode=4&idx={request_code}'

tjMacro=macro.tjKaraoke(request_link)

howDo= int(input("작동 방법을 선택해주세요.\n[1]: tor을 통한 ip 우회 | [2]: 무료 프록시를 이용한 우회\n>> "))

if howDo == 1:
    tjMacro.tor()
elif howDo == 2:
    tjMacro.proxy()