#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 2014 Techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,os,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time
import json
h = HTMLParser.HTMLParser()


addon_id = 'plugin.video.footazo'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
addonFanart = os.path.join(addonfolder,'fanart.jpg')

footazo_url = 'http://www.footazo.com/'

################################################## 

#MENUS############################################

def MENU():
	addDir('+ Recentes',footazo_url,1,'')
	addDir('Pesquisar',footazo_url,2,'')
	addDir('Humor',footazo_url+'videos/humor/',1,'')
	addDir('Bizarro',footazo_url+'videos/bizarro/',1,'')
	addDir('Quase!',footazo_url+'videos/quase/',1,'')
	addDir('Wow!',footazo_url+'videos/wow/',1,'')
	addDir('Ouch!',footazo_url+'videos/ouch/',1,'')
	addDir('Entrevistas',footazo_url+'videos/entrevistas/',1,'')
	addDir('Belas',footazo_url+'videos/belas/',1,'')
	addDir('Outros',footazo_url+'videos/outros/',1,'')

###################################################################################
#FUNCOES

def Listar_Videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<div class="indexpost">.*?<div class="posttitle"><a.*?href="(.+?)".*?>(.+?)</a></div>.*?<div class="datalineleft">(.+?)  \|.*?<div class="postimage">.*?<img.*?src="(.+?)".*?>',re.DOTALL).findall(codigo_fonte)
	for link, name, data, iconimage in match:
		addLink('[COLOR yellow]'+data+'[/COLOR] - '+name,link,4,iconimage)
	match = re.search("<span class='current'>.*?</span><a href='(.+?)' class='page larger'>(.+?)</a>",codigo_fonte)
	if match:
		addDir('[COLOR blue]Página '+match.group(2)+' >>[/COLOR]',match.group(1),1,'')

def Pesquisar(url):
	if url==footazo_url:
		addDir('[B]Pesquisar novamente...[/B]',footazo_url,2,'')
		keyb = xbmc.Keyboard('', 'Pesquisar por...')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='':
				sys.exit(0)
			search=urllib.quote(search)
			url = url + '?s=' + search
		else:
			sys.exit(0)
	codigo_fonte = abrir_url(url)
	match = re.compile('<div class="indexpost">.*?<div class="posttitle"><a.*?href="(.+?)".*?>(.+?)</a></div>.*?<div class="datalineleft">(.+?)  \|.*?<div class="postimage">.*?<img.*?src="(.+?)".*?>',re.DOTALL).findall(codigo_fonte)
	for link, name, data, iconimage in match:
		addLink('[COLOR yellow]'+data+'[/COLOR] - '+name,link,4,iconimage)
	match = re.search("<span class='current'>.*?</span><a href='(.+?)' class='page larger'>(.+?)</a>",codigo_fonte)
	if match:
		addDir('[COLOR blue]Página '+match.group(2)+' >>[/COLOR]',match.group(1),2,'')

def Descricao(url,name):
	progress = xbmcgui.DialogProgress()
	progress.create('Footazo', 'Carregando a descrição e comentários...')
	progress.update(0)
	codigo_fonte = abrir_url(url)
	post_content = re.search('<div class="postcontentsingle">(.+?)<div style="float:left;">', codigo_fonte, re.DOTALL)
	if post_content:
		post_content = cleanhtml(post_content.group(1))
	else:
		post_content = 'Post sem conteúdo'
	comments = ''
	codigo_fonte = abrir_url('https://graph.facebook.com/comments/?ids='+url)
	decoded_data = json.loads(codigo_fonte)
	if len(decoded_data[url]['comments']['data'])>0:
		for x in range(0, len(decoded_data[url]['comments']['data'])):
			facebook_name = decoded_data[url]['comments']['data'][x]['from']['name'].encode('utf-8')
			facebook_like_count = str(decoded_data[url]['comments']['data'][x]['like_count'])
			facebook_message = decoded_data[url]['comments']['data'][x]['message'].encode('utf-8')
			if facebook_message.endswith('\n'):
				facebook_message = facebook_message[:-1]
			comments = comments+'[COLOR blue]'+facebook_name+'[/COLOR] disse: [I]('+facebook_like_count+' likes)[/I]\n'+facebook_message+'\n\n'
			codigo_fonte_2 = abrir_url('https://graph.facebook.com/'+decoded_data[url]['comments']['data'][x]['id']+'/comments/')
			decoded_data_2 = json.loads(codigo_fonte_2)
			if len(decoded_data_2['data'])>0:
				for x in range(0, len(decoded_data_2['data'])):
					facebook_name_reply = decoded_data_2['data'][x]['from']['name'].encode('utf-8')
					facebook_like_count_reply = str(decoded_data_2['data'][x]['like_count'])
					facebook_message_reply = decoded_data_2['data'][x]['message'].encode('utf-8')
					if facebook_message_reply.endswith('\n'):
						facebook_message_reply = facebook_message_reply[:-1]
					comments = comments+'[COLOR orange][B]»»[/B][/COLOR] Resposta de [COLOR orange]'+facebook_name_reply+'[/COLOR] a [COLOR blue]'+facebook_name+'[/COLOR]: [I]('+facebook_like_count_reply+' likes)[/I]\n'+facebook_message_reply+'\n\n'
	if comments == '':
		comments = '[COLOR red]Sem comentários.[/COLOR]\n\n'
	if progress.iscanceled():
		sys.exit(0)
	progress.update(100)
	progress.close()
	xbmc.executebuiltin("ActivateWindow(10147)")
	window = xbmcgui.Window(10147)
	xbmc.sleep(100)
	window.getControl(1).setLabel( "%s - %s" % (name,'Footazo',))
	window.getControl(5).setText('[COLOR green][B]Descrição:[/B][/COLOR]\n'+post_content+'\n\n[COLOR green][B]Comentários:[/B][/COLOR]\n'+comments+'Você poderá também deixar o seu comentário visitando:\n[I]'+url+'[/I]\n a partir do seu browser.')

def Procurar_fontes(url,name,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Footazo', 'Procurando fonte...')
	progress.update(0)
	if progress.iscanceled():
		sys.exit(0)
	playlist = xbmc.PlayList(1)
	playlist.clear()
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		html_source_trunk = re.findall('<iframe(.*?)</iframe>', codigo_fonte, re.DOTALL)
		for trunk in html_source_trunk:
			try:
				iframe = re.compile('src=["\'](.+?)["\']').findall(trunk)[0]
			except:
				iframe = ''
			if iframe:
				if iframe.find('youtube') > -1:
					resolver_iframe = youtube_resolver(iframe)
					if resolver_iframe != 'youtube_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('dailymotion') > -1:
					resolver_iframe = daily_resolver(iframe)
					if resolver_iframe != 'daily_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('vimeo.com') > -1:
					resolver_iframe = vimeo_resolver(iframe)
					if resolver_iframe != 'vimeo_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('vk.com') > -1:
					resolver_iframe = vkcom_resolver(iframe)
					if resolver_iframe != 'vkcom_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('facebook.com/video/embed') > -1:
					resolver_iframe = facebook_resolver(iframe)
					if resolver_iframe != 'facebook_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('rutube.ru') > -1:
					resolver_iframe = rutube_resolver(iframe)
					if resolver_iframe != 'rutube_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('videa.hu') > -1:
					resolver_iframe = videa_resolver(iframe)
					if resolver_iframe != 'videa_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('videos.sapo.pt') > -1:
					resolver_iframe = sapo_resolver(iframe)
					if resolver_iframe != 'sapo_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('vine.co') > -1:
					resolver_iframe = vine_resolver(iframe)
					if resolver_iframe != 'vine_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('alkislarlayasiyorum.com') > -1:
					resolver_iframe = alkislarlayasiyorum_resolver(iframe)
					if resolver_iframe != 'alkislarlayasiyorum_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('videolog.tv') > -1:
					resolver_iframe = videologtv_resolver(iframe)
					if resolver_iframe != 'videologtv_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('zideo.nl') > -1:
					resolver_iframe = zideonl_resolver(iframe)
					if resolver_iframe != 'videologtv_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('liveleak.com/ll_embed') > -1:
					resolver_iframe = liveleak_resolver(iframe)
					if resolver_iframe != 'liveleak_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
				elif iframe.find('v.kiwi.kz/v2/') > -1:
					resolver_iframe = kiwikz_resolver(iframe)
					if resolver_iframe != 'kiwikz_nao resolvido':
						playlist.add(resolver_iframe,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		#playwire embed player
		html_playwire_embed = re.findall('<script.*?type\="text/javascript".*?src\=".*?cdn\.playwire\.com/bolt/js/embed\.min\.js".*?data\-publisher-id\="(.+?)".*?data\-video\-id\="(.+?)".*?>', codigo_fonte)
		for data_publisher, video_id in html_playwire_embed:
			try:
				codigo_fonte_2 = abrir_url('http://cdn.playwire.com/v2/'+data_publisher+'/config/'+video_id+'.json')
			except:
				continue
			decoded_data = json.loads(codigo_fonte_2)
			if decoded_data['src'].endswith('.f4m'):
				try:
					codigo_fonte_3 = abrir_url(decoded_data['src'])
				except:
					continue
				match = re.search("<baseURL>(.+?)</baseURL>.*?url\=\"(.+?)\"",codigo_fonte_3)
				if match:
					playlist.add(match.group(1)+' playPath='+match.group(2),xbmcgui.ListItem(name, thumbnailImage=iconimage))
			else:
				playlist.add(decoded_data['src'],xbmcgui.ListItem(name, thumbnailImage=iconimage))
		#youtube embed em flash
		match = re.compile('<embed src=".*?youtube.com/v/([^?"]+).*?"').findall(codigo_fonte)
		if match:
			for youtube_id in match:
				playlist.add('plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		#longtailvideo.com resolver
		match=re.compile("<embed.*?flashvars=\"file=([^&\"]+).*?\".*?src=\"http://player.longtailvideo.com/player5.2.swf\".*?>").findall(codigo_fonte)
		if match:
			for link in match:
				playlist.add(link,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		#player.mais.uol.com.br
		match=re.compile('<embed.*?src="http://player.mais.uol.com.br/embed_v2.swf\?.*?mediaId=([^&"]+).*?".*?>').findall(codigo_fonte)
		if match:
			for mediaid in match:
				codigo_fonte_2 = abrir_url('http://mais.uol.com.br/apiuol/player/media.js?p=undefined&mediaId='+mediaid+'&action=showPlayer&types=V')
				match_2 = re.search('"formats": \[{.*?"url":"(.+?)".*?}', codigo_fonte_2)
				if match_2:
					dummy=abrir_url('http://mais.uol.com.br/crossdomain.xml')
					dummy=abrir_url('http://mais.uol.com.br/notifyMediaView?t=v&v=2&mediaId='+mediaid)
					playlist.add(match_2.group(1)+'?ver=0&start=0&r='+urllib.quote_plus('http://player.mais.uol.com.br/embed_v2.swf?mediaId='+mediaid+'&tv=0')+'|referer=http://player.mais.uol.com.br/embed_v2.swf?mediaId='+mediaid,xbmcgui.ListItem(name, thumbnailImage=iconimage))
		#player.ooyala.com não suportado - total 2 videos
		#meta.ua não suportado - total 1 video
		#wat.tv não suportado - total 1 video
		progress.update(100)
		progress.close()
		if len(playlist) == 0:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('Footazo', 'Nenhuma fonte suportada encontrada...')
		else:
			try:
				xbmc.Player().play(playlist)		
			except:
				pass

def youtube_resolver(url):
	match = re.compile('.*?youtube.com/embed/([^?"]+).*?').findall(url)
	if match:
		return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])
	else: return 'youtube_nao resolvido'
    
def daily_resolver(url):
    if url.find('syndication') > -1: match = re.compile('/embed/video/(.+?)\?syndication').findall(url)
    else: match = re.compile('/embed/video/(.*)').findall(url)
    if match:
        return 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + str(match[0])
    else: return 'daily_nao resolvido'
	
def vimeo_resolver(url):
    match = re.compile('/([0-9]+)').findall(url)
    if match:
        return 'plugin://plugin.video.vimeo/?action=play_video&videoid=' + str(match[0])
    else: return 'vimeo_nao resolvido'
	
def vkcom_resolver(url):
	match = re.compile('http://vk.com/video_ext.php\?oid=([\d]+?)&.*?id=([\d]+?)&.*?hash=([A-Za-z0-9]+).*?').findall(url)
	if match != None:
		for oid, id, hash in match:
			codigo_fonte_2 = abrir_url('http://vk.com/video_ext.php?oid=' + oid + '&id=' + id + '&hash=' + hash)
			match_2 = re.search('url1080=(.+?).1080.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.1080.mp4'
			match_2 = re.search('url720=(.+?).720.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.720.mp4'
			match_2 = re.search('url480=(.+?).480.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.480.mp4'
			match_2 = re.search('url360=(.+?).360.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.360.mp4'
			match_2 = re.search('url240=(.+?).240.mp4', codigo_fonte_2)
			if match_2 != None:
				return match_2.group(1)+'.240.mp4'
			return 'vkcom_nao resolvido'
	else:
		return 'vkcom_nao resolvido'

def facebook_resolver(url):
	try:
		result = abrir_url(url)
		url = re.compile('"params","(.+?)"').findall(result)[0]
		url = re.sub(r'\\(.)', r'\1', urllib.unquote_plus(url.decode('unicode_escape')))
		url = re.compile('_src":"(.+?)"').findall(url)[0]
		return url
	except:
		return 'facebook_nao resolvido'

def rutube_resolver(url):
	try:
		url = url.split("/")[-1].split("?")[0]
		codigo_fonte = abrir_url('http://rutube.ru/api/play/trackinfo/'+url+'/?format=json')
		return json.loads(codigo_fonte)['video_balancer']['m3u8']
	except:
		return 'rutube_nao resolvido'

def videa_resolver(url):
	try:
		url = url.rsplit("v=", 1)[-1].rsplit("-", 1)[-1]
		url = 'http://videa.hu/flvplayer_get_video_xml.php?v='+url
		result = abrir_url(url)
		url = re.compile('video_url="(.+?)"').findall(result)[0]
		return url
	except:
		return 'videa_nao resolvido'

def sapo_resolver(url):
	try:
		id = url.split("file=")[-1].split("sapo.pt/")[-1].split("/")[0]
		url = '%s/%s' % ('http://videos.sapo.pt', id)
		result = abrir_url(url)
		match = re.search('<meta property="og:video" content="http://imgs.sapo.pt/sapovideo/swf/flvplayer-sapo.swf\?file=(.+?)/mov.+?"/>', result)
		if match != None:
			tmp_url = match.group(1) + '/mov'
			req = urllib2.Request(tmp_url)
			res = urllib2.urlopen(req)
			url = res.geturl()
			return url
		else:
			return 'sapo_nao resolvido'
	except:
		return 'sapo_nao resolvido'

def vine_resolver(url):
	try:
		codigo_fonte = abrir_url(url)
		match = re.search("var videoUrl = '(.+?)';", codigo_fonte)
		if match:
			return match.group(1)
		else:
			return 'vine_nao resolvido'
	except:
		return 'vine_nao resolvido'

def alkislarlayasiyorum_resolver(url):
	try:
		url = url.split("/")[-1].split("?")[0]
		codigo_fonte = abrir_url('http://alkislarlayasiyorum.com/api/playerJson/ay_embed/'+url)
		return json.loads(codigo_fonte)['streamurl']
	except:
		return 'alkislarlayasiyorum_nao resolvido'

def videologtv_resolver(url):
	try:
		url = url.split("id_video=")[-1].split("?")[0]
		codigo_fonte = abrir_url('http://api.videolog.tv/video/'+url+'.json')
		return json.loads(codigo_fonte)['video']['url_mp4']
	except:
		return 'videologtv_nao resolvido'

def zideonl_resolver(url):
	try:
		url = url.split("playzideo=")[-1].split("?")[0]
		codigo_fonte = abrir_url('http://www.zideo.nl/player/iframe?playzideo='+url)
		match = re.search('<div.*?id="videoFile".*?>(.+?)</div>', codigo_fonte)
		if match:
			return match.group(1)
		else:
			return 'vine_nao resolvido'
	except:
		return 'videologtv_nao resolvido'

def liveleak_resolver(url):
	try:
		codigo_fonte = abrir_url(url)
		match = re.search('file: "(.+?)",', codigo_fonte)
		if match:
			return match.group(1)
		else:
			return 'liveleak_nao resolvido'
	except:
		return 'liveleak_nao resolvido'

def kiwikz_resolver(url):
	try:
		codigo_fonte = abrir_url(url)
		return urllib.unquote(re.compile('&url=(.+?)&poster').findall(codigo_fonte)[0])
	except:
		return 'kiwikz_nao resolvido'

###################################################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,mode,iconimage):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty("Fanart_Image", addonFanart)
	liz.addContextMenuItems( [("Ver descrição e comentários", 'RunPlugin(plugin://'+addon_id+'/?mode=3&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+')')] )
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
	return ok
	
def addDir(name,url,mode,iconimage,folder=True):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty("Fanart_Image", addonFanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)

def cleanhtml(raw_html):
	cleanr =re.compile('<.*?>')
	cleantext = re.sub(cleanr,'', raw_html)
	cleantext = re.sub('\s+',' ',cleantext)
	return cleantext

############################################################################################################
#                                               GET PARAMS                                                 #
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


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)




###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################


if mode==None: MENU()
elif mode==1: Listar_Videos(url)
elif mode==2: Pesquisar(url)
elif mode==3: Descricao(url,name)
elif mode==4: Procurar_fontes(url,name,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))