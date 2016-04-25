import urllib.request as ur
import re
import sys
from bs4 import BeautifulSoup as bs
from subprocess import call

def kpop_lyrics(ly_link, decision):
    file_name = re.search("\/(?:.(?!\/))+$", ly_link).group()[1:-5] + ".txt"

    ly_request = ur.Request(ly_link, headers = {'User-Agent':'Mozilla/5.0'})
    ly_html = ur.urlopen(ly_request).read()

    soup = bs(ly_html, 'lxml')
    song_title = soup.find(attrs = {'itemprop':'itemreviewed'}).text
    yt = soup.find(attrs = {'class':'YOUTUBE-iframe-video'})["src"]
    soup_text = soup.text

    print("[kpop-lyrics-extrator] Title: " + song_title)
    print("[kpop-lyrics-extrator] File name: " + file_name)
    
    korean_or = re.search("HANGUL(.|\n)*ROMANIZATION", soup_text, re.MULTILINE).group()
    english_or = re.search("ENGLISH TRANSLATION(.|\n)*?Title", soup_text, re.MULTILINE).group()
    korean = "\n".join(filter(None, re.split("\n", korean_or)[1:-1])) 
    english = "\n".join(filter(None, re.split("\n", english_or)[1:-1]))
    
    number_of_lines = len(korean.split("\n"))
    number_of_lines1 = len(english.split("\n"))
    
    with open(file_name, "a", encoding = "utf-8") as f:
        f.write(file_name[:-4])
        f.write("\n\n")
        for i in range(number_of_lines1):
            f.write(english.split("\n")[i])
            f.write("\n")
        f.write("\n\n")
        for i in range(number_of_lines):
            f.write(korean.split("\n")[i])
            f.write("\n")
    print("[kpop-lyrics-extrator] Write file: Done.")
    
    if decision == 1:
        print("[kpop-lyrics-extrator] Download audio file by youtube-dl")
        call(["youtube-dl", "--extract-audio", "--audio-format", "mp3", yt])
    
if len(sys.argv) < 2:
    print("[kpop-lyrics-extrator] No url received. Program exit.")
    sys.exit()

if sys.argv[1] == "-m":
    decision = 1
else:
    decision = 0
    
ly_link = sys.argv[-1]

kpop_lyrics(ly_link, decision)