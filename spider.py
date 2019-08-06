import os
import re
import urllib
import requests
import time
from bs4 import BeautifulSoup  # Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库

def get_img_url(html):
    reg = r'src="(.*?jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    print(imglist)
    return imglist

def get_img_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_list = soup.find_all(name='h3')
    
    #title_list = soup.find_all(name='div',attrs={"class":"description"})
    # print('\n\n')
    # print(title_list)
    # print('\n\n')
    # print(title_list[0].get_text())
    return title_list

def getHtml(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    response  = requests.get(url, headers = headers)
    html = response.text
    html_file = open('tmp.html', mode='w', encoding='utf-8')
    html_file.write(html)
    html_file.close()
    return html

def main():
    # html = getHtml('https://bing.ioliu.cn/ranking') 
    html = getHtml('https://bing.ioliu.cn/') 
    # print(html)
    i = 0
    imglist = get_img_url(html)
    title_list = get_img_title(html)
    file_dir = os.path.abspath('./image') 
    opener=urllib.request.build_opener()
    opener.addheaders=[("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36")]
    for imgurl in imglist:
        image_name = title_list[i].get_text() 
        image_name = re.sub(r'\(.*\)', '', image_name)
        image_name = image_name + '.jpg'
        image_name= image_name.replace(' ', '')
        work_path=os.path.join(file_dir, image_name) 
        print ('downloading->>>' + work_path)
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgurl, work_path)
        time.sleep(1)
        i += 1
    
    print ('finish!')


if __name__ == '__main__':
    main()

