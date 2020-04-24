import os
import re
import urllib
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup 
import lxml
import win32api
import win32gui
import win32con

def get_img_url(html):
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
    image_path_list = []
    for img_url in img_list:
        image_name = title_list[i].get_text() 
        image_name = re.sub(r'\(.*\)', '', image_name)
        image_name = image_name + '.jpg'
        image_name= image_name.replace(' ', '')
        image_path=os.path.join(file_dir, image_name)
        image_path_list.append(image_path)
        print('Downloading->>>' + image_path)
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(img_url, image_path)
        time.sleep(1)
        i += 1
    return image_path_list

def update_desktop_image(image_path):
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, image_path)

def main():
    try:
        html = getHtml('https://bing.ioliu.cn/ranking')
        # html = getHtml('https://bing.ioliu.cn/') 
        # print(html)
    except:
        print('get html failed!')
        return
    try:
        img_list = get_img_url(html)
    except:
        print('get img_list failed!')
        return
    try:
        title_list = get_img_title(html)
    except:
        print('get title_list failed!')
        return

    image_dir = os.path.abspath('.') + '\\image\\' + datetime.now().strftime('%Y%m%d')
    if os.path.exists(image_dir) is False:
        os.makedirs(image_dir)
        
    try:
        image_path_list = download_image(img_list, title_list, image_dir)
    except:
        print('Downloading->>> ERROR!')
        return    
    print ('Downloading->>> Finish!!')

    update_desktop_image(image_path_list[3])

if __name__ == '__main__':
    main()

