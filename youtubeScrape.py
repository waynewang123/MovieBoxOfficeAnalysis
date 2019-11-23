import urllib.request
import urllib
import re
import time
from unidecode import unidecode

file = open("movieList.csv","r")
output_file = open("views.csv","w")
line = file.readline()
line = file.readline()


while line:

    # httpHandler = urllib.HTTPHandler(debuglevel=1)
    # httpsHandler = urllib.HTTPSHandler(debuglevel=1)
    # opener = urllib.build_opener(httpHandler, httpsHandler)
    # urllib.install_opener(opener)
    try:
        temp = line.split(",")[2]   # getting movie name
        film_name = re.sub(" ", "+", temp)


        url = "https://www.youtube.com/results?search_query=" + film_name

url = unidecode(url)    # unicode change
        
        req = urllib.request.Request(url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })



        data = urllib.request.urlopen(req).read()
        data = data.decode('UTF-8')
        # print(data)
        # reg = "<li>\S+ views</li>"
        reg = "<li>[\d,]+\sviews</li>"  # using regular expression to find number of views
        pattern = re.compile(reg)
        matcher = re.findall(pattern,data)
        print(matcher)
        max = -1
        # find the largest views in the first page of youtube
        for m in matcher:
            if m == "<li>No views</li>":
                continue
            m = re.sub(',',"",m)
            m = re.sub('<li>',"",m)
            m = re.sub(' views</li>',"",m)
            m = int(m)
            if max < m:
                max = m
            # print(m)

        print(max)
        output_file.write(temp+","+str(max)+"\n")

        line = file.readline()
        print("----sleep 2 second----")
        time.sleep(2)
            
    except urllib.error.HTTPError:
        # if 503, wait until recovery
        print("-----error-----")
        time.sleep(600)

    # break

file.close()
output_file.close()
