import os
import sys
import time
from random import randint
import requests
from bs4 import BeautifulSoup as bs
skipped=[]
checker="post-img-inline lazyload"
numbering=1
names={}
min_time=1
max_time=3
to_skip=['https_prod-cdn.wetransfer.net_packs_media_images_wt-facebook-9db47080.png','https_www.dropbox.com_static_images_spectrum-icons_generated_content_content-folder_dropbox-large.png']
total_size_downloaded=0
min_size_limit=0.25#in MB
max_size_limit=1000000#in MB(i.e approx 1 TB)
chunk_size=100000#in BYTES
flag4=1

def total_page_count(soup):
    try:
        temp = soup.find_all('div', class_='yp-posts-paginate-buttons')
        total_page = int(temp[-1].find_all('a')[-1].get('data-pag'))
    except Exception as e:
        print('HAS 1 PAGE ONLY\n')
        total_page=1
    return total_page

def naming(base_name,names_used):
    if (base_name not in names_used) or (names_used[base_name]==0):
        names_used[base_name]=1
        return base_name
    new_name=str(base_name+'_'+str(names_used[base_name]))
    names_used[base_name]+=1
    return new_name

def extracting_basename(tile):
    try:
        base=tile.find('div',class_='card-content')
        base_name=str((base.find('span',class_="grey-text post-time")).text).strip()
        return base_name
    except Exception as e:
        try:
            base = tile.find('div', class_='card-content np-rd')
            base_name=str((base.find('small',class_="post-time")).text)
            return base_name
        except Exception as e:
            print('extracting basename error:',e)
            print()
            print(tile)
            print()

def calculate_size(link):
    global total_size_downloaded
    siz = requests.head(link)
    siz = float(siz.headers['content-length']) / 1000
    size = (siz / 1000)
    total_size_downloaded+=size
    return size

def sleepy_time():
    sleep_time = randint(min_time,max_time)
    print('\nSLEEPING FOR :', sleep_time, 'SECS\n')
    time.sleep(sleep_time)
    print('-' * 110)

update_message="SEEMS LIKE YOU ALREADY HAVE POSTS OF THIS ARTIST.\nIF YOU WISH TO JUST UPDATE THIS USER'S CONTENT,YOU MAY JUST TO UPDATE IT;\nOR ELSE ALL CONTENT OF THIS USER WILL BE RE-DOWNLOADED,WHICH MIGHT TAKE SOME TIME\n"

def download(name,link,size,base_name,extension,names_used):#yet to remove "name"
    global downloaded,numbering
    try:
        filename=naming(base_name, names_used)+'.'+extension
        if user_option=='u' and os.path.exists(os.path.join(dir_path,filename)):
            flag4=0
            print('MATCHING FILE FOUND.\n')
            print('TOTAL NEW FILES DOWNLOADED: ', downloaded)
            print('TOTAL DATA DOWNLOADED: ', total_size_downloaded, ' MB')
            sys.exit(0)
        image_link = str(link)
        res = requests.get(image_link)
        print('NAME:', filename)
        print('LINK:', image_link)
        print('SIZE:', size,' MB')
        with open(filename,'wb') as playfile:
            for chunk in res.iter_content(chunk_size):
                playfile.write(chunk)
        downloaded += 1
        if user_option=='u':
            u=downloaded
        print("DOWNLOADED FILES: ", downloaded)
        print('-' * 20, ' ' * 20, '-' * 20, ' ' * 20, '-' * 20)
        return 1
    except Exception as e:
        print('\nERROR IN SAVING FILE')
        print(e)
        if base_name in names_used:
            names_used[base_name]-=1
            '''
            print('NAME:', filename)
            print('LINK:', image_link)
            print('SIZE:', size, ' MB')'''
        return 0

def func(site):
    page = requests.get(site).text
    soup = bs(page, 'lxml')
    global downloaded, c
    for tile in soup.find_all('div', class_="col s12 m6"):
        names_used = {}
        base_name = extracting_basename(tile)
        try:
            media = tile.find('div', class_="post-body")#class_="card-reveal"
            flag1 = 0
            for qw in media.find_all('a'):
                try:
                    flag1 = 0
                    # i+=1
                    temp = (qw.get('href'))
                    temp_name = str(temp).split('/')[-1] 
                    link = 'https://data.yiff.party' + temp
                    if len(temp_name) > 5 and 'https_' == temp_name[:6]:
                        print('SKIPPED:', temp_name, '\n', link)
                        skipped.append([temp_name, str(link)])
                        continue

                    extension = str(temp_name.split('.')[-1])  # FINDING EXTENSION OF THE FILE
                    t = ' '.join(qw.img.get('class'))
                    size = calculate_size(link)
                    if t == checker and size>min_size_limit:
                        flag2 = download(temp_name, link, size,base_name,extension,names_used)
                        flag1 = 1
                except Exception as e:
                    continue
            if flag1:
                sleepy_time()
        except Exception as e:
            continue

        flag3 = 0
        try:
            flag2 = 0
            attachments = tile.find('div', class_="card-attachments")
            links = attachments.p
            for link in links.find_all('a'):
                try:
                    flag2 = 0
                    temp_name = link.text
                    if len(temp_name) > 5 and 'https_' == temp_name[:6]:
                        print('SKIPPED:', temp_name, '\n', link)
                        skipped.append([temp_name, str(link)])
                        continue

                    extension = str(temp_name.split('.')[-1])
                    image_link = str(link.get('href'))
                    size = calculate_size(image_link)
                    if size>min_size_limit:
                        flag2 = download(temp_name, image_link, size, base_name, extension, names_used)
                except Exception as e:
                    continue
            if flag2 == 1:
                sleepy_time()

        except Exception as e:
            flag3 = 1
        if flag3:
            try:
                flag2=0
                action = tile.find('div', class_='card-action').a
                link = str(action.get('href'))
                temp_name = str(link.split('/')[-1])
                if len(temp_name) > 5 and 'https_' == temp_name[:6]:
                    print('SKIPPED:', temp_name, '\n', link)
                    skipped.append([temp_name, str(link)])
                    continue

                extension = str(temp_name.split('.')[-1])
                size = calculate_size(link)
                if size>min_size_limit:
                    flag2 = download(temp_name, link, size, base_name, extension, names_used)
            except Exception as e:
                c += 1
                continue
            if flag2 == 1:
                sleepy_time()

def basic_func():
    global current_page
    while current_page<=total_page:
        if total_page > 1:
            print(' ' * 20, 'PAGE NO.:', current_page, '\n')
        site = base_site + '?p=' + str(current_page)
        func(site)
        current_page += 1
        print('+-' * 60)

downloaded=0
c=1
base_dir=os.path.join(os.path.expanduser('~'),'Downloads','YIFF')
base_site=input('ENTER THE URL: ')
page = requests.get(base_site).text
soup = bs(page, 'html.parser')
dir_name=str(soup.find('span',class_="yp-info-name").text).strip()#extracts the name of the  artist
print('FOLDER NAME: ',dir_name)
current_page,total_page=1,total_page_count(soup)
dir_path=os.path.join(base_dir,dir_name)
user_option='d'
if os.path.exists(dir_path):
    os.chdir(dir_path)
    print(update_message)
    user_option=input("PRESS 'U' TO UPDATE;OR 'D' TO DOWNLOAD ALL OVER AGAIN:").lower()
    u=0
else:
    os.makedirs(dir_path)
    os.chdir(dir_path)
basic_func()
if user_option!='u':
    print('\nFINISHED !!!!\n')
    print('TOTAL FILES DOWNLOADED: ', downloaded)
    print('TOTAL DATA DOWNLOADED: ', total_size_downloaded, ' MB')
    print('TOTAL POSTS WITHOUT MEDIA:', c)
    print('SKIPPED LINKS:', len(skipped))
elif user_option=='u' and flag4==1:
    print('UPDATING FINISHED.NO MATCHING OLD FILES HAVE BEEN FOUND')
    print('TOTAL NEW FILES DOWNLOADED: ', downloaded)
    print('TOTAL DATA DOWNLOADED: ', total_size_downloaded, ' MB')
