from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO

def Listesm(request):
    
    urlphone = 'https://www.jumia.com.tn/smartphones/'
    prixmax = request.GET.get('prixmax')
    pg = request.GET.get('page')
    category = request.GET.get('cat')
    urlCat = 'https://www.jumia.com.tn/smartphones/'
    if prixmax == None:
        prixmax = ''
    if pg == None:
        pg = '1'
    if category != None:    
     urlphone+=category+'/'    
    else:
        category='' 
    urlphone = urlphone+'?page='+pg+'&price=0-'+prixmax

    Pgs = []
    cats = []
    telephones = []
    
    
    try:
     response = requests.get(urlphone)
     responseForCat = requests.get(urlCat)
    except:
        return render(request,'404page.html')
        
    try:
     urlphone = BeautifulSoup(response.content, 'html.parser')
     lescat = BeautifulSoup(responseForCat.content, 'html.parser')
    except:
        return render(request,'404page.html')
    try:
      pg = urlphone.find('div', {'class': 'pg-w -ptm -pbxl'})
    except:
       pg==None
        
    if pg != None:
        pages = pg.find_all('a', {'class': 'pg'})
        
        for p in pages:
            if p.text.isdigit():
            
             Pgs.append(p.text)
        
     
    cat= lescat.find('div', {'class': '-phs -pvxs -df -d-co -h-168 -oya -sc'})
    if cat != None:
     for c in cat:
        
        cats.append(c.text)
  
    
    phone = urlphone.find_all('article', {'class': 'prd _fb col c-prd'})
    nbs=0
    if urlphone.find('p', {'class': '-gy5 -phs'}) != None:
     nbs= urlphone.find('p', {'class': '-gy5 -phs'}).text.split(" ")[0]
     nbs= int(nbs)
    else:
        nbs=0
    
    for p in phone :
     tel = {}   
     nom = p.find('h3', {'class': 'name'}).text
     tel['nom'] = nom
     img = p.find('img', {'class': 'img'}).get('data-src')
     tel['image'] = img
     link = p.find('a', {'class': 'core'}).get('href')
     tel['link'] = link
     prix = p.find('div', {'class': 'prc'}).text
     tel['prix'] = prix   
    
     telephones.append(tel)
    template = loader.get_template('listesm.html')
    context = {
        'phones': telephones,
        'Pgs': Pgs,
        'category': category,
        'max': max,
        'nbs':nbs,
        'Cats':cats,
    }
    return HttpResponse(template.render(context, request))


def consultersm(request,nom):
    urlsingelphone = 'https://www.jumia.com.tn/'+nom
    response = requests.get(urlsingelphone)
    soup = BeautifulSoup(response.content, 'html.parser')
    p = soup.find('section', {'class': 'col12 -df -d-co'})
    
    prix = p.find('span', {'class': '-b -ltr -tal -fs24'}).text

    nom = p.find('h1', {'class': '-fs20 -pts -pbxs'}).text
    img  = p.find('img', {'class': '-fw -fh'}).get('data-src')
    
    
    template = loader.get_template('csmart.html')
    context = {
        'nom': nom, 
        'img': img,
        'prix': prix,
    }
    return HttpResponse(template.render(context, request))