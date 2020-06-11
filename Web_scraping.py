# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 11:46:38 2020

@author: Abdo
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import pymongo
username = 'admin'
password = 'abdolesa123'
mongourl = 'cluster0-md9mu.mongodb.net/test?retryWrites=true&w=majority'
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{mongourl}")
db = client.wuzzef


url = 'https://wuzzuf.net/search/jobs/?q=machine+learning&a=navbl'

job_num = 0
total_job = {}
check = {}
count = 0
while True :

    response = requests.get(url)
    print(response)
    
    data = response.text
    
    soup = BeautifulSoup(data , 'html.parser')
    
    #titles = soup.find_all('h2',{'class':'job-title'})
    
    jobs = soup.find_all('div',{'class':'result-wrp row'})
    
    for job in jobs :
        title = job.find('h2',{'class':'job-title'}).text
        title = title.split()
        title = ' '.join(title)
        companyNamea = job.find('span',{'class':'company-name'})
        companyName = companyNamea.find('span')
        locations = job.find('span',{'class':'location location-desktop'}).text
        detalis = job.find('div',{'class':'job-details'})
        detail = detalis.text
        detail = detail.split()
        detail = ''.join(detail)   
        links = job.find('h2',{'class':'job-title'})
        link = links.find('a').get('href')
        job_num = job_num+1
        job_info = {
                'Title':title,
                'Company_Name':companyName,
                'Location' : locations,
                'Details'  : detail ,
                'Link_Job' : link
                }
        if db.JOB.count_documents({'$or':[{'Title':title},{'Link_job':link}]})==0 :
            _ = db.JOB.insert_one(job_info)
        
            
        #total_job[job_num] = [title,companyName,locations,detail,link]
        
        
        
        #location  = locations.find('span').text 
        #print('title :',title , '\nCompany name : ',companyName,'\nDetails:',detail,'\nlocations:',locations ,'\nlink:',link,'\n-----')

    url_tages = soup.find('ul',{'class':'pagination desktop-pagination hidden-xs'})
    url_tags  = url_tages.find('li',{'class':'hidden-xs'})
    url_tag   = url_tags.find('a').get('href')
    if url_tag :
        url = 'https://wuzzuf.net/search/jobs/?q=machine+learning&a=navbl' + url_tag
        print(url)
        count = count+1
        if count >10:
            break
    else :
        break
    
    
print('total_job :',job_num)
print('\n')
#wuzzef_job = pd.DataFrame.from_dict(total_job,orient='index',columns = ['title','companyName','locations','detail','link'])
#wuzzef_job.to_csv('wuzzef_Machine.csv')