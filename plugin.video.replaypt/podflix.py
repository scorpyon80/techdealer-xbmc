#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,HTMLParser
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.replaypt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

podflix_url = 'http://podflix.com.br/'
##################################################

def listar_categorias():
	try:
		codigo_fonte = abrir_url(podflix_url+'beta/?podcastsList=all')
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match = re.findall('<div id="post.*?" class="postlist">.*?<a href="(.+?)">.*?<img.*?src="(.+?)".*?></a>.*?<h1 class="posttitle">(.+?)</h1>.*?</div><!-- post -->', codigo_fonte, re.DOTALL)
		for url, iconimage, name in match:
			addDir(name,url,449,iconimage)
		
def listar_episodios(url):
    try:
		codigo_fonte = abrir_url(url)
    except:
		codigo_fonte = ''
    if codigo_fonte:
		match = re.findall('<div id="post.*?".*?>.*?<img.*?src="(.+?)".*?></a>.*?<h2 class="posttitle"><a href="(.+?)" rel="bookmark">\n(.+?)</a></h2>.*?</div><!-- post -->', codigo_fonte, re.DOTALL)
		for iconimage, url, name in match:
			try:
				name = name.decode('utf-8').encode('utf-8')
			except:
				try:
					name = name.decode("latin-1").encode("utf-8")
				except:
					continue
			addDir(name,url,450,iconimage,False)	
		next_page = re.search('<div class="nav-previous"><a href="(.+?)" ><span class="meta-nav">&larr;</span> Older posts</a></div>', codigo_fonte)
		if next_page != None:
				addDir('[B]<< Anterior[/B]',next_page.group(1),449,addonfolder+artfolder+'podflix.png')

def procurar_fontes(url,name,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Replay PT', 'Resolvendo o podcast...')
	progress.update(0)
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if progress.iscanceled():
			sys.exit(0)
	progress.update(100)
	progress.close()
	if codigo_fonte:
		podcast_file = re.search("<a href='([^'\"<>]+?)' TARGET='_blank'><img src='/lib/images/post/zip.jpg' alt='Zip' height='50px' width='50px'></a>", codigo_fonte)
		if podcast_file:
			listitem = xbmcgui.ListItem(label=name, iconImage=str(iconimage), thumbnailImage=str(iconimage), path=url)
			listitem.setProperty('IsPlayable', 'true')
			try:
				xbmc.Player().play(item=podcast_file.group(1), listitem=listitem)
			except:
				pass
	else:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Replay PT', 'Podcast não encontrado...')
						
############################################################################################################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDir(name,url,mode,iconimage,pasta=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
        return ok
        
############################################################################################################
          
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
      
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "Iconimage: "+str(iconimage)