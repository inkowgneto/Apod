import requests
from bs4 import BeautifulSoup
import dateparser
import re
import json

class apod:
    def __init__(self):
        self.all_info = dict

    def get_apod_by_link(self, arch_link):
        page = requests.get(arch_link)
        if page.status_code != 404:
                soup = BeautifulSoup(page.text, 'html.parser')

                #image
                findimage = soup.find('img')
                try:
                    image_link = ('https://apod.nasa.gov/apod/'+findimage.get('src'))
                except AttributeError:
                    image_link = arch_link

                #image date
                find_date = soup.find_all('center')[0]
                find_date = soup.find_all('p')[1]
                try:
                    find_date = find_date.text
                    find_date = find_date.split(' ')
                    find_date = find_date[0:3]
                    year,month,day = find_date
                    combine_format = day+' '+month+' '+year
                    date_of_image =  combine_format.replace('\n','')
                except:
                    date_of_image = ': : :'

                #image title
                try:
                    findtitle = soup.find_all('center')[1]
                    title = findtitle.find_all('b')[0]
                    title = title.text
                except:
                    title = '[]'
                
                #next/prev link
                nextlink = soup.find_all('a')
                list_links = []
                for links in nextlink:
                    links = links.get('href')
                    list_links.append(links)
                try:
                    apod = [item for item in list_links if item.startswith('ap')]
                    apod.reverse()
                    next_day = apod[0]
                    previous_day = apod[1]
                    next_link = ('https://apod.nasa.gov/apod/'+next_day)
                    pre_link = ('https://apod.nasa.gov/apod/'+previous_day)
                except AttributeError:
                    #image next day
                    next1 = soup.find_all('p')[-2]
                    next_link = next1.find_all('a')
                    nextplace = next_link[10].get('href')
                    next_link = ('https://apod.nasa.gov/apod/'+nextplace)
                    #image previous day
                    pre1 = soup.find_all('p')[-2]
                    pre_link = pre1.find_all('a')
                    preplace = pre_link[0].get('href')
                    pre_link = ('https://apod.nasa.gov/apod/'+preplace)

                #image Explanation
                delete = soup.find_all('center')[2]
                delete.decompose()
                para = soup.find_all('p')[2]
                paragraph = para.text
                pattern = re.compile(r'\s+')
                paragraph = re.sub(pattern, ' ', paragraph)
                list2 = {'title' : title, 'date': date_of_image, 'link': image_link, 'explanation': paragraph, 'next': next_link,'pre': pre_link}
                self.all_info = list2
                return list2
        else:
            return None

    def get_apod_by_date(self, date_value):
        verify_date = dateparser.parse(date_value)
        if verify_date is not None:
            date_time = dateparser.parse(date_value ,settings={'DATE_ORDER': 'DMY'})
            date_time = str(date_time)
            date_time = date_time.split(' ')
            date_time = date_time[0]
            year,mon,day = date_time.split('-')
            if int(year)>=1997 and int(year)<=2018:
                combi = year[2:]+mon+day
                arch_link = ('https://apod.nasa.gov/apod/ap'+combi+'.html')
                self.get_apod_by_link(arch_link)
                info = self.all_info
                return info
            else:
                return None           
        else:
            return None

    def get_apod_by_search(self, query):
        url = "https://apod.nasa.gov/cgi-bin/apod/apod_search?tquery="+query
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('body')
        list1 = [] 
        for link in links:
            link = link.find_all('p')
            for linked in link:
                    try:
                        linked = linked.find_all('a')[0]
                        finallink = linked.get('href')
                        list1.append(finallink)
                    except IndexError:
                        if len(list1)>20:
                            list1 = list1[0:20]
                            return list1
        if len(list1)>20:
            list1 = list1[0:20]
        return list1