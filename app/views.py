from django.shortcuts import redirect, render
from django.http import HttpResponse , HttpResponseRedirect, response
from django.template import loader
from requests.api import request
from .forms import LoginForm
import requests
import re
from django.contrib.auth import logout as django_logout

#from django.template import Context, Template



def index(request):
    
    if 'login_data'   in request.session:
        #print (request.session.items())
        return redirect("/registry")
    else: 
        #print (request.session.items())
        if request.method == 'POST':
            form = LoginForm(request.POST)
            #print (form)
            if form.is_valid():
                request.session['login_data'] = request.POST
                return HttpResponseRedirect('registry')
        else:
            
            form = LoginForm()
    
    return render(request, 'login.html' ,{'form': form})


def logout(request):
    django_logout(request) 
    return redirect("/")


def list_of_image(url, username, password):
    api = "/v2/_catalog"
    url = url
    username = username
    password = password
    r = requests.get(url+api, verify=False ,auth=(username, password ))
    
    return r

def list_of_tag(url, username, password ,imagename):
    api = "/tags/list"
    url = url
    username = username
    password = password
    imagename = imagename
    r = requests.get(url+"/v2/"+imagename+api,verify=False ,auth=(username, password ))
    return r

def registry(request ):
    if 'login_data'  not in request.session:
        return redirect("/")
    else:
        login_data = request.session.get('login_data')
        dockerurl = login_data['dockerRegistyUrl']
        username = login_data['dockerRegistyUsername']
        password = login_data['dockerRegistyPassword']
        response = list_of_image(dockerurl , username , password )
        if response.status_code == 200:
            return render(request, 'registry.html' , {'response':response.json()} )
        else:
            try: 
                response.raise_for_status()
            except requests.exceptions.HTTPError as e: 
                re = e
                django_logout(request)
                return render(request, 'login.html' , {'error_message' : re} )


def get_Sha(url, username, password ,imagename , tags):
    api = "/manifests/"
    url = url
    username = username
    password = password
    imagename = imagename
    headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
    r = requests.get(url+"/v2/"+imagename+api+tags,headers=headers ,verify=False , auth=(username, password ))
    return r.headers



def get_name_list_image_tag(image_describe , dockerurl , username , password , imagename):

            image_describe= image_describe
            # print name and list of iamge tag
            for k , v in image_describe.items():
                if k == 'name':
                    name = v
                elif k == 'tags':
                    tempTags = v

            # print tags in describe            
            if tempTags  == None:
                url = dockerurl.replace("https://","")
                context = {
                "name": name,
                "tags": "empty" ,
                "url" : url,
                }
                return context
            else:
                tags ={}
                for tag in tempTags:
                    tempSha = re.search(r"\bsha256:\w+", str(get_Sha(dockerurl , username , password , imagename, tag))) 
                    if tempTags  == None:
                        tags["empty"] = tempSha.group()
                    else:
                            tags[tag] = tempSha.group()

                url = dockerurl.replace("https://","")
                context = {
                "name": name,
                "tags": tags ,
                "url" : url,
                }
                return context


def taglist(request):
        imagename = request.GET['id']
        login_data = request.session.get('login_data')
        dockerurl = login_data['dockerRegistyUrl']
        username = login_data['dockerRegistyUsername']
        password = login_data['dockerRegistyPassword']
        if request.method == 'POST':
            if 'deleteimage' in request.POST:
                tag = (request.POST.getlist('deleteimage'))
                delete_image(dockerurl, username, password ,imagename , str(tag[0]))

            image_describe = list_of_tag(dockerurl , username , password , imagename).json()
            # pass image_descibe to 
            context = get_name_list_image_tag(image_describe , dockerurl , username , password , imagename)
            return render(request, 'listImage.html' , context)
        else:
            imagename = request.GET['id']
            image_describe = list_of_tag(dockerurl , username , password , imagename).json()
            # pass image_descibe to 
            context = get_name_list_image_tag(image_describe , dockerurl , username , password , imagename)
            return render(request, 'listImage.html' , context)


def delete_image(url, username, password ,imagename , tag):
    api = "/manifests/"
    url = url
    username = username
    password = password
    imagename = imagename
    headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
    r = requests.delete(url+"/v2/"+imagename+api+tag,headers=headers,verify=False ,auth=(username, password ))
