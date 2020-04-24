import os
import re
import urllib
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup  # Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库
import lxml

def get_img_url(html):
    # reg = r'src="(.*?jpg)"'
    soup = BeautifulSoup(html, 'lxml')
    taglist = soup.find_all(name='img')
    img_list = []
    for tag in taglist:
        s = tag['data-progressive']
        img_list.append(s.replace('640x480', '1920x1080'))
    # print(img_list)
    return img_list

def get_img_title(html):
    soup = BeautifulSoup(html, 'lxml')
    title_list = soup.find_all(name='h3')
    # print(title_list)
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

def download_image(img_list, title_list, file_dir):
    opener=urllib.request.build_opener()
    opener.addheaders=[("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36")]
    i = 0
    for img_url in img_list:
        image_name = title_list[i].get_text() 
        image_name = re.sub(r'\(.*\)', '', image_name)
        image_name = image_name + '.jpg'
        image_name= image_name.replace(' ', '')
        work_path=os.path.join(file_dir, image_name)
        print('Downloading->>>' + work_path)
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(img_url, work_path)
        time.sleep(1)
        i += 1
def main():
    # html = getHtml('https://bing.ioliu.cn/ranking') 
    html = getHtml('https://bing.ioliu.cn/') 
    # print(html)
    img_list = get_img_url(html)
    title_list = get_img_title(html)
    image_dir = os.path.abspath('.') + '\\image\\' + datetime.now().strftime('%Y%m%d')
    if os.path.exists(image_dir) is False:
        os.makedirs(image_dir)
    file_dir = image_dir
    
    download_image(img_list, title_list, file_dir)
        
    print ('Downloading->>> Finish!!')


if __name__ == '__main__':
    main()

