import requests
#python library to pull data out of html and xml
from bs4 import BeautifulSoup

website_based_url = 'http://news.omy.sg/'
url_arr = []
fx = open('crawed_page_with_url.txt', 'w',encoding="utf8")

def link_spider(max_pages):
    page = 0

    while page < max_pages:
        url = 'http://news.omy.sg/News/Local%20News/'+str(page) +'/0/'
        source_code = requests.get(url)
        plain_text = source_code.text

        #get all the html and text
        soup = BeautifulSoup(plain_text,"html.parser")


        #show the specific identifier for the thing you want to show, for eg, title
        #loop all the code and look for <a> with class title
        #print(source_code)
        for link in soup.findAll('a',{'class':'title'}):
            href = link.get('href')
            title = link.string
            escape_duplicate(link.get('href'),'main')
            print(title)
            fx.write(str(title) + '\n')

            get_single_item_data(href)
        page += 1

    fx.close()

#go into indivisual page to get extra info
def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'html.parser')

    for info in soup.findAll('div',{'class':'caption'}):
        image_caption = info.text
        print(image_caption)
        fx.write(str(image_caption)+'\n')

    for link in soup.findAll('a'):
        escape_duplicate(link.get('href'))

#only print out url that never show before
def escape_duplicate(url,mainsub='sub'):
    #if the url is shortcut url, add the based url in
    if not ('http://' or 'https://') in str(url) :
        url = str(website_based_url) + str(url)

    #if url not exists in the list, add to file
    if(url not in url_arr):
        url_arr.append(url)
        if(mainsub=='sub'):
            print('   ' +str(url))
            fx.write('    ')
        else:
            print(str(url))

        fx.write(str(url)+'\n')


link_spider(1)