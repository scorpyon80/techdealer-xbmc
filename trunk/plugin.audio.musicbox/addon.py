#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 2014 Techdealer

##############LIBRARIES TO IMPORT AND SETTINGS####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,datetime,os,xbmcvfs
import json
import random
import hashlib
import cookielib
h = HTMLParser.HTMLParser()

import SimpleDownloader as downloader
downloader = downloader.SimpleDownloader()
from random import randint

addon_id = 'plugin.audio.musicbox'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
translation = selfAddon.getLocalizedString
datapath = xbmc.translatePath('special://profile/addon_data/%s' % addon_id ).decode("utf-8")

default_vk_token = '9baa01b7b841f1a05a0fef48d26e9b74ead40f78757fb369f1417c22653fdcb376efa1f81ffe56cadae22'

def translate(text):
	return translation(text).encode('utf-8')
	  
###################################################################################
#MAIN MENU

def Main_menu():
	if bool(selfAddon.getSetting('vk_email')=="") ^ bool(selfAddon.getSetting('vk_password')==""):
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30865))
		selfAddon.setSetting('vk_token','')
		xbmcaddon.Addon(addon_id).openSettings()
		return
	elif selfAddon.getSetting('vk_email')=="" and selfAddon.getSetting('vk_password')=="":
		if selfAddon.getSetting('vk_token')!=default_vk_token:
			selfAddon.setSetting('vk_token',default_vk_token)
	else:
		try:
			#login in vk.com - login in account
			cookies = cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
			response = opener.open('https://login.vk.com/?act=login&email='+selfAddon.getSetting('vk_email')+'&pass='+selfAddon.getSetting('vk_password')+'&expire=&vk=')
			#login in vk.com - get the token
			request2=urllib2.Request('https://oauth.vk.com/authorize?client_id=2648691&scope=audio,offline&redirect_uri=http://oauth.vk.com/blank.html&display=touch&response_type=token')
			cookies.add_cookie_header(request2)
			response2 = opener.open(request2)
			selfAddon.setSetting('vk_token',re.search('access_token=(.+?)&', response2.geturl()).group(1))
			notification(translate(30860),translate(30864),'4000',addonfolder+artfolder+'notif_vk.png')
		except:
			try:
				#if the previous step fail, maybe is necessary give permissions to the application (if used by 1st time), lets try...
				request2=urllib2.Request(re.search('<form method="post" action="(.+?)">', response2.read()).group(1),{})
				request2.add_header('Referer', 'https://oauth.vk.com/authorize?client_id=2648691&scope=audio,offline&redirect_uri=http://oauth.vk.com/blank.html&display=touch&response_type=token')
				cookies.add_cookie_header(request2)
				response2 = opener.open(request2)
				selfAddon.setSetting('vk_token',re.search('access_token=(.+?)&', response2.geturl()).group(1))
				notification(translate(30860),translate(30864),'4000',addonfolder+artfolder+'notif_vk.png')
			except:
				#if the previous step fail, the account provided is invalid
				dialog = xbmcgui.Dialog()
				ok = dialog.ok(translate(30400),translate(30866))
				xbmcaddon.Addon(addon_id).openSettings()
				return
	#check if token is valid
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q=eminem&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	if 'error' in decoded_data:
		dialog = xbmcgui.Dialog()
		try: ok = dialog.ok(translate(30400),translate(30867)+str(decoded_data['error']['error_msg']))
		except: ok = dialog.ok(translate(30400),translate(30867)+str(decoded_data['error']))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		addDir(translate(30401),'1',1,addonfolder+artfolder+'recomended.png')
		addDir(translate(30402),'1',2,addonfolder+artfolder+'digster.png')
		if selfAddon.getSetting('hide_soundtrack')=="false": addDir(translate(30403),'1',7,addonfolder+artfolder+'atflick.png')
		addDir(translate(30404),'1',11,addonfolder+artfolder+'8tracks.png')
		addDir(translate(30405),'1',13,addonfolder+artfolder+'charts.png')
		addDir(translate(30406),'1',25,addonfolder+artfolder+'search.png')
		addDir(translate(30407),'1',38,addonfolder+artfolder+'mymusic.png')
		addDir(translate(30408),'',41,addonfolder+artfolder+'favorites.png')
		addDir(translate(30409),'',45,addonfolder+artfolder+'userspace.png')
		addDir(translate(30410),'',49,addonfolder+artfolder+'configs.png',False)

###################################################################################
#RECOMENDATIONS

def Recomendations(url):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=chart.getTopTracks&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['tracks']['track'])):
		artist = decoded_data['tracks']['track'][x]['artist']['name'].encode("utf8")
		track_name = decoded_data['tracks']['track'][x]['name'].encode("utf8")
		try: iconimage = decoded_data['tracks']['track'][x]['image'][3]['#text'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
	total_pages = decoded_data['tracks']['@attr']['totalPages']
	if int(url)<int(total_pages): addDir(translate(30411),str(int(url)+1),1,addonfolder+artfolder+'next.png')

###################################################################################
#DIGSTER	

def Digster_menu():
	addDir('[COLOR blue][B]'+translate(30109)+':[/B][/COLOR] '+['Adria','Australia','Austria','Belgium','Denmark','Estonia','Finland','France','Germany','Latvia','Lithuania','Mexico','Netherlands','New Zeland','Norway','Poland','Portugal','Romania','Spain','Sweden','Switzerland','United Kingdom','USA'][int(selfAddon.getSetting('digster_country'))],'',2,'',False)
	addDir(translate(30425),'',3,'')
	addDir(translate(30426),'genre',4,'')
	addDir(translate(30427),'mood',4,'')
	addDir(translate(30428),'suitable',4,'')

def Digster_sections():
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/sections')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['sections'])):
		slug = decoded_data['sections'][x]['slug'].encode("utf8")
		title = decoded_data['sections'][x]['name'].encode("utf8")
		addDir(title,'1',5,'',search_query = '&section='+slug)

def Digster_categories(url):
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/taxonomies/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['taxonomy'])):
		slug = decoded_data['taxonomy'][x]['slug'].encode("utf8")
		title = decoded_data['taxonomy'][x]['title'].encode("utf8").replace("&amp;", "&")
		addDir(title,'1',5,'',search_query = '&'+url+'='+slug)

def List_digster_playlists(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists?posts_per_page='+str(items_per_page)+'&paged='+str(url)+search_query)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['playlists'])):
		slug = decoded_data['playlists'][x]['slug'].encode("utf8")
		title = decoded_data['playlists'][x]['title'].encode("utf8")
		try: iconimage = decoded_data['playlists'][x]['image']['large'][0].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir(title,slug,6,iconimage,country = selfAddon.getSetting('digster_country'),type='playlist')
	#check if next page exist
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists?posts_per_page='+str(items_per_page)+'&paged='+str(int(url)+1)+search_query)
	decoded_data = json.loads(codigo_fonte)
	if len(decoded_data['playlists'])>0: addDir(translate(30411),str(int(url)+1),5,addonfolder+artfolder+'next.png',search_query = search_query)

def List_digster_tracks(url,country):
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(country)]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['playlist']['tracks'])):
		if len(decoded_data['playlist']['tracks'][x]['artists'])==1: artist = decoded_data['playlist']['tracks'][x]['artists'][0].encode("utf8")
		elif len(decoded_data['playlist']['tracks'][x]['artists'])==2: artist = decoded_data['playlist']['tracks'][x]['artists'][0].encode("utf8")+' feat. '+decoded_data['playlist']['tracks'][x]['artists'][1].encode("utf8")
		elif len(decoded_data['playlist']['tracks'][x]['artists'])>2:
			artist = ''
			for y in range(0, len(decoded_data['playlist']['tracks'][x]['artists'])): artist = artist+decoded_data['playlist']['tracks'][x]['artists'][y].encode("utf8")+' & '
			artist = artist[:-3] # remove last ' & '
		track_name = decoded_data['playlist']['tracks'][x]['title'].encode("utf8")
		iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)

###################################################################################
#ATFLICK SOUNDTRACK

def Atflick_menu():
	addDir(translate(30450),'0',8,'',playlist_id = 'featured')
	addDir(translate(30451),'0',8,'',playlist_id = 'newlyadded')
	addDir(translate(30452),'0',8,'',playlist_id = 'genre/all')
	addDir(translate(30453),'0',8,'',playlist_id = 'genre/comedy')
	addDir(translate(30454),'0',8,'',playlist_id = 'genre/romance')
	addDir(translate(30455),'0',8,'',playlist_id = 'genre/action')
	addDir(translate(30456),'0',8,'',playlist_id = 'genre/family')
	addDir(translate(30457),'0',8,'',playlist_id = 'Science%20Fiction')

def List_atflick_movies(url,playlist_id):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	if playlist_id == 'featured':
		codigo_fonte = abrir_url('http://ast.vionlabs.com/api/featured/6')[3:]+']]}'
		decoded_data = json.loads(codigo_fonte)
		for x in range(0, len(decoded_data['movies'])):
			try:
				name = str(decoded_data['movies'][x][0]['name']).encode("utf8")
				movie_id = str(decoded_data['movies'][x][0]['id'])
				try: iconimage = decoded_data['movies'][x][0]['posters'][1]['poster_link'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(name,movie_id,9,iconimage,type='soundtrack')
			except: pass
	else:
		codigo_fonte = abrir_url('http://ast.vionlabs.com/api/'+playlist_id+'/'+str(items_per_page)+'/'+url)
		decoded_data = json.loads(codigo_fonte)
		for x in range(0, len(decoded_data['movies'])):
			try:
				name = decoded_data['movies'][x]['name'].encode("utf8")
				movie_id = str(decoded_data['movies'][x]['id'])
				try: iconimage = decoded_data['movies'][x]['posters'][1]['poster_link'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(name,movie_id,9,iconimage,type='soundtrack')
			except: pass
		#check if next page exist
		if int(url)<int(decoded_data['pages']): addDir(translate(30411),str(int(url)+1),8,addonfolder+artfolder+'next.png',playlist_id = playlist_id)

def List_atflick_albums(url):
	codigo_fonte = abrir_url('http://ast.vionlabs.com/api/detail/movie/'+url)
	decoded_data = json.loads(codigo_fonte)
	if len(decoded_data['movie'][0]['albums'])==1:
		album = decoded_data['movie'][0]['albums'][0]['album_name'].encode("utf8")
		album_id = decoded_data['movie'][0]['albums'][0]['album_id'].encode("utf8")
		#try: iconimage = decoded_data['movies'][0]['posters'][1]['poster_link'].encode("utf8")
		#except: iconimage = addonfolder+artfolder+'no_cover.png
		List_atflick_tracks(album_id)
	else:
		albums = []
		albums_id = []
		for x in range(0, len(decoded_data['movie'][0]['albums'])):
			albums.append(decoded_data['movie'][0]['albums'][x]['album_name'].encode("utf8"))
			albums_id.append(decoded_data['movie'][0]['albums'][x]['album_id'].encode("utf8"))
			#try: iconimage = decoded_data['movies'][x]['posters'][1]['poster_link'].encode("utf8")
			#except: iconimage = addonfolder+artfolder+'no_cover.png'
		if albums and albums_id:
			album_id = xbmcgui.Dialog().select(translate(30458), albums)
			if album_id != -1: List_atflick_tracks(albums_id[album_id])
			else: sys.exit(0)

def List_atflick_tracks(url):
	codigo_fonte = abrir_url('https://api.spotify.com/v1/albums/'+url+'/tracks')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['items'])):
		artist = decoded_data['items'][x]['artists'][0]['name'].encode("utf8")
		track_name = decoded_data['items'][x]['name'].encode("utf8")
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,addonfolder+artfolder+'no_cover.png',search_query = artist+' '+track_name)

###################################################################################
#8TRACKS

def Eighttracks_menu():
	addDir(translate(30475),'1',12,'',search_query = 'all:popular')
	addDir(translate(30476),'1',12,'',search_query = 'collection:staff-picks')
	addDir(translate(30477),'1',12,'',search_query = 'collection:featured')
	addDir(translate(30478),'1',12,'',search_query = 'all:hot')
	addDir(translate(30479),'1',12,'',search_query = 'all:recent')

def List_8tracks_suggestions(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://8tracks.com/mix_sets/'+search_query+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['mixes'])):
		username = decoded_data['mixes'][x]['user']['login'].encode("utf8")
		playlist_name = decoded_data['mixes'][x]['name'].encode("utf8")
		tracks_count = str(decoded_data['mixes'][x]['tracks_count'])
		playlist_id = str(decoded_data['mixes'][x]['id'])
		try: iconimage = decoded_data['mixes'][x]['cover_urls']['max200'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',33,iconimage,playlist_id = playlist_id,type='playlist')
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30411),str(int(url)+1),12,addonfolder+artfolder+'next.png',search_query = search_query)
		
###################################################################################
#CHARTS

def Top_charts_menu():
	addDir(translate(30522),'1',14,'')
	addDir(translate(30500),'1',15,'')
	addDir(translate(30501),'1',16,'')
	addDir(translate(30502),'1',20,'',playlist_id = 'all')
	addDir(translate(30503),'1',20,'',playlist_id = 'classics')
	addDir(translate(30504),'1',21,'')
	addDir(translate(30505),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-100')
	addDir(translate(30506),'1',24,'',playlist_id = 'http://www.billboard.com/rss/charts/billboard-200')
	addDir(translate(30507),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-songs')
	addDir(translate(30508),'1',24,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-albums')
	addDir(translate(30509),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/pop-songs')
	addDir(translate(30510),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/country-songs')
	addDir(translate(30511),'1',24,'',playlist_id = 'http://www.billboard.com/rss/charts/country-albums')
	addDir(translate(30512),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-songs')
	addDir(translate(30513),'1',24,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-albums')
	addDir(translate(30514),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-songs')
	addDir(translate(30515),'1',24,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-albums')
	addDir(translate(30516),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-r-and-b-hip-hop-airplay')
	addDir(translate(30517),'1',24,'',playlist_id = 'http://www.billboard.com/rss/charts/dance-electronic-albums')
	addDir(translate(30518),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-songs')
	addDir(translate(30519),'1',24,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-albums')

def Vkcom_popular(url):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	index = ((int(url)-1)*items_per_page)
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.getPopular.json?only_eng=1&count='+str(items_per_page)+'&offset='+str(index)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['response'])):
		artist = decoded_data['response'][x]['artist'].encode("utf8").replace("&amp;", "&")
		track_name = decoded_data['response'][x]['title'].encode("utf8")
		link = decoded_data['response'][x]['url'].encode("utf8")
		item_id = str(decoded_data['response'][x]['owner_id'])+'_'+str(decoded_data['response'][x]['aid'])
		addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,item_id = item_id,manualsearch = False,type = 'song')
	#check if next page exist
	try:
		codigo_fonte = codigo_fonte = abrir_url('https://api.vk.com/method/audio.getPopular.json?only_eng=1&count='+str(items_per_page)+'&offset='+str((int(url)*items_per_page))+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		if len(decoded_data['response'])>0:
			addDir(translate(30411),str(int(url)+1),14,addonfolder+artfolder+'next.png')
	except: pass

def Itunes_countries_menu(mode):
	country_name = ["Albania","Algeria","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Botswana","Brazil","British Virgin Islands","Brunei Darussalam","Bulgaria","Burkina Faso","Cambodia","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo, Republic of the","Costa Rica","Croatia","Cyprus","Czech Republic","Denmark","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Fiji","Finland","France","Gambia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea-Bissau","Guyana","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Korea, Republic Of","Kuwait","Kyrgyzstan","Lao, People's Democratic Republic","Latvia","Lebanon","Liberia","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Mauritania","Mauritius","Mexico","Micronesia, Federated States of","Moldova","Mongolia","Montserrat","Mozambique","Namibia","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Saudi Arabia","Senegal","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","South Africa","Spain","Sri Lanka","St. Kitts and Nevis","St. Lucia","St. Vincent and The Grenadines","Suriname","Swaziland","Sweden","Switzerland","São Tomé and Príncipe","Taiwan","Tajikistan","Tanzania","Thailand","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Venezuela","Vietnam","Yemen","Zimbabwe"]
	country_code = ["al","dz","ao","ai","ag","ar","am","au","at","az","bs","bh","bb","by","be","bz","bj","bm","bt","bo","bw","br","vg","bn","bg","bf","kh","ca","cv","ky","td","cl","cn","co","cg","cr","hr","cy","cz","dk","dm","do","ec","eg","sv","ee","fj","fi","fr","gm","de","gh","gr","gd","gt","gw","gy","hn","hk","hu","is","in","id","ie","ir","it","jm","jp","jo","kz","ke","kr","kw","kg","la","lv","lb","lr","lt","lu","mo","mk","mg","mw","my","ml","mt","mr","mu","mx","fm","md","mn","ms","mz","na","np","nl","nz","ni","ne","ng","no","om","pk","pw","pa","pg","py","pe","ph","pl","pt","qa","ro","ru","sa","sn","sc","sl","sg","sk","si","sb","za","es","lk","kn","lc","vc","sr","sz","se","ch","st","tw","tj","tz","th","tt","tn","tr","tm","tc","ug","ua","ae","gb","us","uy","uz","ve","vn","ye","zw"]
	for x in range(0, len(country_name)):
		if country_code[x] not in ["al","dz","ao","bj","bt","td","cn","cg","gy","is","jm","kr","kw","lr","mk","mg","mw","ml","mr","ms","pk","pw","sn","sc","sl","sb","lc","vc","sr","st","tz","tn","tc","uy","ye"]: #Countries without music store
			if mode==15: addDir(country_name[x],'1',17,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])
			elif mode==16: addDir(country_name[x],'1',18,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])

def Itunes_track_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topsongs/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	total_items = len(decoded_data['feed']['entry'])
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		try:
			artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
			track_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
			try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
		except: pass
	if int(int(url)*items_per_page)<total_items: addDir(translate(30411),str(int(url)+1),17,addonfolder+artfolder+'next.png',country = country)

def Itunes_album_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topalbums/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	total_items = len(decoded_data['feed']['entry'])
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		try:
			artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
			album_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
			id = decoded_data['feed']['entry'][x]['id']['attributes']['im:id'].encode("utf8")
			try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,id,19,iconimage,album = album_name,artist = artist,country = country,type = 'album')
		except: pass
	if int(int(url)*items_per_page)<total_items: addDir(translate(30411),str(int(url)+1),18,addonfolder+artfolder+'next.png',country = country)

def Itunes_list_album_tracks(url,album,country):
	#api documentation: https://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.html
	codigo_fonte = abrir_url('https://itunes.apple.com/lookup?id='+url+'&country='+country+'&entity=song&limit=200')
	decoded_data = json.loads(codigo_fonte)
	try:
		if int(decoded_data['resultCount'])>0:
			for x in range(1, len(decoded_data['results'])):
				artist = decoded_data['results'][x]['artistName'].encode("utf8")
				track_name = decoded_data['results'][x]['trackName'].encode("utf8")
				try: iconimage = decoded_data['results'][x]['artworkUrl100'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
	except: pass

def Beatport_top100(url,playlist_id):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://mobile.beatport.com/home/top-100/'+playlist_id+'?layout=false&perPage='+str(items_per_page)+'&page='+url)
	match = re.findall('<img.*?class="cover-art".+?src="(.+?)".*?>.*?<span class="txt metadata title">(.+?)</span>.*?<span class="txt metadata title">(.+?)</span>.*?<span class="txt metadata nowrap">(.+?)</span>', codigo_fonte, re.DOTALL)
	for iconimage, title1, title2, artist in match:
		try:
			title1 = title1.strip()
			title2 = title2.strip()
			track_number = re.search('^([\d]+)\.',title1).group(1)
			track_name = re.search('[\d]+\.\s*(.+)',title1).group(1)+' '+title2
			artist = artist.strip()
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
		except: pass
	if track_number and int(track_number)<100: addDir(translate(30411),str(int(url)+1),20,addonfolder+artfolder+'next.png',playlist_id = playlist_id)

def Officialcharts_uk(url,mode,playlist_id):
	if playlist_id==None or playlist_id=='':
		options_name = ['Singles','Albums','Singles Update','Albums Update','Dance Singles','Dance Albums','Indie Singles','Indie Albums','RnB Singles','RnB Albums','Rock Singles','Rock Albums','Compilations Albums']
		options_mode = [21,22,21,22,21,22,21,22,21,22,21,22,22]
		options_playlist_id = ['http://www.bbc.co.uk/radio1/chart/singles','http://www.bbc.co.uk/radio1/chart/albums','http://www.bbc.co.uk/radio1/chart/updatesingles','http://www.bbc.co.uk/radio1/chart/updatealbums','http://www.bbc.co.uk/radio1/chart/dancesingles','http://www.bbc.co.uk/radio1/chart/dancealbums','http://www.bbc.co.uk/radio1/chart/indiesingles','http://www.bbc.co.uk/radio1/chart/indiealbums','http://www.bbc.co.uk/radio1/chart/rnbsingles','http://www.bbc.co.uk/radio1/chart/rnbalbums','http://www.bbc.co.uk/radio1/chart/rocksingles','http://www.bbc.co.uk/radio1/chart/rockalbums','http://www.bbc.co.uk/radio1/chart/compilations']
		id = xbmcgui.Dialog().select(translate(30520), options_name)
		if id != -1:
			mode = options_mode[id]
			playlist_id = options_playlist_id[id]
		else:
			sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM html(' + str(int(url)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '" and xpath="//div[@class=\'cht-content-wrapper\']/div[@class=\'cht-content\']/div[@class=\'cht-entries\']/div[@class=\'cht-entry-wrapper\']"') + '&format=json&diagnostics=true&callback=', timeout=30)
	decoded_data = json.loads(codigo_fonte)
	try:
		if len(decoded_data['query']['results']['div']) > 0:
			if url=='1': addDir(translate(30521),'1',21,'')
			if mode==21:
				#checks if output has only an object or various and proceeds according
				if 'div' in decoded_data['query']['results']['div'] and 'img' in decoded_data['query']['results']['div']:
					try: artist = decoded_data['query']['results']['div']['div'][1]['div'][0]['p'].encode("utf8")
					except: artist = decoded_data['query']['results']['div']['div']['div'][1]['div'][0]['p'].encode("utf8")
					try: track_name = decoded_data['query']['results']['div']['div']['div'][1]['div'][1]['p'].encode("utf8")
					except: track_name = decoded_data['query']['results']['div']['div'][1]['div'][1]['p'].encode("utf8")
					try: iconimage = decoded_data['query']['results']['div']['img']['src'].encode("utf8")
					except: 
						try: iconimage = decoded_data['query']['results']['div']['div']['img']['src'].encode("utf8")
						except: iconimage = addonfolder+artfolder+'no_cover.png'
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
				else:
					for x in range(0, len(decoded_data['query']['results']['div'])):
						try: artist = decoded_data['query']['results']['div'][x]['div'][1]['div'][0]['p'].encode("utf8")
						except: artist = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][0]['p'].encode("utf8")
						try: track_name = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][1]['p'].encode("utf8")
						except: track_name = decoded_data['query']['results']['div'][x]['div'][1]['div'][1]['p'].encode("utf8")
						try: iconimage = decoded_data['query']['results']['div'][x]['img']['src'].encode("utf8")
						except: 
							try: iconimage = decoded_data['query']['results']['div'][x]['div']['img']['src'].encode("utf8")
							except: iconimage = addonfolder+artfolder+'no_cover.png'
						if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
						elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
			elif mode==22:
				#checks if output has only an object or various and proceeds according
				if 'div' in decoded_data['query']['results']['div'] and 'img' in decoded_data['query']['results']['div']:
					try: artist = decoded_data['query']['results']['div']['div'][1]['div'][0]['p'].encode("utf8")
					except: artist = decoded_data['query']['results']['div']['div']['div'][1]['div'][0]['p'].encode("utf8")
					try: album_name = decoded_data['query']['results']['div']['div']['div'][1]['div'][1]['p'].encode("utf8")
					except: album_name = decoded_data['query']['results']['div']['div'][1]['div'][1]['p'].encode("utf8")
					try: iconimage = decoded_data['query']['results']['div']['img']['src'].encode("utf8")
					except: 
						try: iconimage = decoded_data['query']['results']['div']['div']['img']['src'].encode("utf8")
						except: iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',28,iconimage,artist = artist,album = album_name,type = 'album')
				else:
					for x in range(0, len(decoded_data['query']['results']['div'])):
						try: artist = decoded_data['query']['results']['div'][x]['div'][1]['div'][0]['p'].encode("utf8")
						except: artist = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][0]['p'].encode("utf8")
						try: album_name = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][1]['p'].encode("utf8")
						except: album_name = decoded_data['query']['results']['div'][x]['div'][1]['div'][1]['p'].encode("utf8")
						try: iconimage = decoded_data['query']['results']['div'][x]['img']['src'].encode("utf8")
						except:
							try: iconimage = decoded_data['query']['results']['div'][x]['div']['img']['src'].encode("utf8")
							except: iconimage = addonfolder+artfolder+'no_cover.png'
						addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',28,iconimage,artist = artist,album = album_name,type = 'album')
	except: pass
	try:
		codigo_fonte_2 = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM html(' + str((int(url)+1)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '" and xpath="//div[@class=\'cht-content-wrapper\']/div[@class=\'cht-content\']/div[@class=\'cht-entries\']/div[@class=\'cht-entry-wrapper\']"') + '&format=json&diagnostics=true&callback=', timeout=30)
		decoded_data_2 = json.loads(codigo_fonte_2)
		if len(decoded_data_2['query']['results']['div']) > 0: addDir(translate(30411),str(int(url)+1),mode,addonfolder+artfolder+'next.png',playlist_id = playlist_id)
	except: pass	
	
def Billboard_charts(url,mode,playlist_id):
	#if mode==23: list billboard track charts
	#if mode==24: list billboard album charts
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str(int(url)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
	decoded_data = json.loads(codigo_fonte)
	try:
		if len(decoded_data['query']['results']['item']) > 0:
			if mode==23:
				#checks if output has only an object or various and proceeds according
				if 'artist' in decoded_data['query']['results']['item'] and 'chart_item_title' in decoded_data['query']['results']['item']:
					artist = decoded_data['query']['results']['item']['artist'].encode("utf8")
					track_name = decoded_data['query']['results']['item']['chart_item_title'].encode("utf8")
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,addonfolder+artfolder+'no_cover.png',search_query = artist+' '+track_name)
				else:
					for x in range(0, len(decoded_data['query']['results']['item'])):
						artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
						track_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
						if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,type = 'song')
						elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,addonfolder+artfolder+'no_cover.png',search_query = artist+' '+track_name)
			elif mode==24:
				#checks if output has only an object or various and proceeds according
				if 'artist' in decoded_data['query']['results']['item'] and 'chart_item_title' in decoded_data['query']['results']['item']:
					artist = decoded_data['query']['results']['item']['artist'].encode("utf8")
					track_name = decoded_data['query']['results']['item']['chart_item_title'].encode("utf8")
					addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',28,addonfolder+artfolder+'no_cover.png',artist = artist,album = album_name,type = 'album')
				else:
					for x in range(0, len(decoded_data['query']['results']['item'])):
						artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
						album_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
						addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',28,addonfolder+artfolder+'no_cover.png',artist = artist,album = album_name,type = 'album')
	except: pass
	try:
		codigo_fonte_2 = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str((int(url)+1)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
		decoded_data_2 = json.loads(codigo_fonte_2)
		if len(decoded_data_2['query']['results']['item']) > 0: addDir(translate(30411),str(int(url)+1),mode,addonfolder+artfolder+'next.png',playlist_id = playlist_id)
	except: pass

###################################################################################
#SEARCH AND LIST CONTENT

def Search_main():
	keyb = xbmc.Keyboard('', translate(30600))
	keyb.doModal()
	if (keyb.isConfirmed()):
		search_query = keyb.getText()
		if search_query=='': sys.exit(0)
	else: sys.exit(0)
	if search_query.startswith('tags:'):
		if search_query!='tags:':
			#playlists by tags
			codigo_fonte = abrir_url('http://8tracks.com/mix_sets/tags:'+urllib.quote(search_query[5:].replace(', ', '+').replace(',', '+'))+'.json?include=mixes+pagination&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['total_entries']
			if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',32,'',search_query = search_query)
	else:
		#tracks
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(search_query)+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		total_items = decoded_data['response'][0]
		if int(total_items)>0: addDir(translate(30601)+str(total_items)+translate(30602),'1',26,'',search_query = search_query)
		#albums
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.search&album='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: decoded_data['error']
		except:
			try:
				total_items = decoded_data['results']['opensearch:totalResults']
				if int(total_items)>0: addDir(translate(30603)+str(total_items)+translate(30604),'1',27,'',search_query = search_query)
			except: pass
		#toptracks
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: total_items = decoded_data['toptracks']['@attr']['total']
		except:
			try: total_items = decoded_data['toptracks']['total']
			except: total_items = 0
		if int(total_items)>0: addDir(translate(30605)+str(total_items)+translate(30606),'1',29,'',search_query = search_query)
		#setlists
		try: codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/search/setlists.json?artistName='+urllib.quote(search_query))
		except urllib2.URLError, e: codigo_fonte = "not found"
		if codigo_fonte != "not found":
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['setlists']['@total']
			addDir(translate(30607)+str(total_items)+translate(30608),'1',30,'',search_query = search_query)
		#playlists
		codigo_fonte = abrir_url('http://8tracks.com/mix_sets/keyword:'+urllib.quote(search_query)+'.json?include=mixes+pagination&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
		decoded_data = json.loads(codigo_fonte)
		total_items = decoded_data['total_entries']
		if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',32,'',search_query = search_query)
		#soundtracks
		if selfAddon.getSetting('hide_soundtrack')=="false":
			codigo_fonte = abrir_url('http://ast.vionlabs.com/api/search/'+urllib.quote(search_query)+'/')
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['total']
			if total_items>0: addDir(translate(30611)+str(total_items)+translate(30612),'0',34,'',search_query = search_query)

def Search_by_tracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	index = ((int(url)-1)*items_per_page)
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(search_query)+'&count='+str(items_per_page)+'&offset='+str(index)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	print codigo_fonte
	for x in range(1, len(decoded_data['response'])):
		artist = decoded_data['response'][x]['artist'].encode("utf8").replace("&amp;", "&")
		track_name = decoded_data['response'][x]['title'].encode("utf8")
		link = decoded_data['response'][x]['url'].encode("utf8")
		item_id = str(decoded_data['response'][x]['owner_id'])+'_'+str(decoded_data['response'][x]['aid'])
		addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,item_id = item_id,manualsearch = False,type = 'song')
	total_items = decoded_data['response'][0]
	if index+items_per_page<int(total_items): addDir(translate(30411),str(int(url)+1),26,addonfolder+artfolder+'next.png',search_query = search_query)
	
def Search_by_albums(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.search&album='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['results']['albummatches']['album']:
			artist = decoded_data['results']['albummatches']['album']['artist'].encode("utf8")
			album_name = decoded_data['results']['albummatches']['album']['name'].encode("utf8")
			mbid = decoded_data['results']['albummatches']['album']['mbid'].encode("utf8")
			try: iconimage = decoded_data['results']['albummatches']['album']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
		else:
			for x in range(0, len(decoded_data['results']['albummatches']['album'])):
				artist = decoded_data['results']['albummatches']['album'][x]['artist'].encode("utf8")
				album_name = decoded_data['results']['albummatches']['album'][x]['name'].encode("utf8")
				mbid = decoded_data['results']['albummatches']['album'][x]['mbid'].encode("utf8")
				try: iconimage = decoded_data['results']['albummatches']['album'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
			total_items = decoded_data['results']['opensearch:totalResults']
			if int(url)*items_per_page<int(total_items): addDir(translate(30411),str(int(url)+1),27,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def List_album_tracks(url,artist,album):
	if url: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&mbid='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	else: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&artist='+urllib.quote(artist)+'&album='+urllib.quote(album)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	count = 0
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['album']['tracks']['track']:
			artist = decoded_data['album']['tracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['album']['tracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
			count += 1
		else:
			for x in range(0, len(decoded_data['album']['tracks']['track'])):
				artist = decoded_data['album']['tracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['album']['tracks']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
				count += 1
	except: pass
	#if none result was found with last.fm api, we use 7digital api
	if artist and album and count==0:
		try:
			codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM xml WHERE url="http://api.7digital.com/1.2/release/search?q='+urllib.quote(artist+' '+album)+'&type=album&oauth_consumer_key=musichackday"') + '&format=json&diagnostics=true&callback=', timeout=30)
			decoded_data = json.loads(codigo_fonte)
			releaseid_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['id']
			title_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['title']
			artist_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['artist']['name']
			codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM xml WHERE url="http://api.7digital.com/1.2/release/tracks?releaseid='+releaseid_xml+'&oauth_consumer_key=musichackday&country=GB"') + '&format=json&diagnostics=true&callback=', timeout=30)
			decoded_data = json.loads(codigo_fonte)
			if artist.lower() == artist_xml.lower():
				for x in range(0, len(decoded_data['query']['results']['response']['tracks']['track'])):
					artist = decoded_data['query']['results']['response']['tracks']['track'][x]['artist']['name'].encode("utf8")
					track_name = decoded_data['query']['results']['response']['tracks']['track'][x]['title'].encode("utf8")
					try: iconimage = decoded_data['query']['results']['response']['tracks']['track'][x]['release']['image'].encode("utf8")
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
					count += 1
		except: pass

def Search_by_toptracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['toptracks']['track']:
			artist = decoded_data['toptracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['toptracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['toptracks']['track']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['toptracks']['track'])):
				artist = decoded_data['toptracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['toptracks']['track'][x]['name'].encode("utf8")
				#mbid = decoded_data['toptracks']['track'][x]['mbid'].encode("utf8")
				try: iconimage = decoded_data['toptracks']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
			total_pages = decoded_data['toptracks']['@attr']['totalPages']
			if int(url)<int(total_pages): addDir(translate(30411),str(int(url)+1),29,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def Search_by_setlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = 20 #impossible to use a custom value currently
	codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/search/setlists.json?artistName='+urllib.quote(search_query)+'&p='+url)
	if codigo_fonte != "not found":
		decoded_data = json.loads(codigo_fonte)
		try:
			#checks if output has only an object or various and proceeds according
			if 'artist' in decoded_data['setlists']['setlist']:
				date = decoded_data['setlists']['setlist']['@eventDate'].encode("utf8")
				artist = decoded_data['setlists']['setlist']['artist']['@name'].encode("utf8")
				location = decoded_data['setlists']['setlist']['venue']['@name'].encode("utf8")
				id = decoded_data['setlists']['setlist']['@id'].encode("utf8")
				iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,31,iconimage,type='setlist')
			else:
				for x in range(0, len(decoded_data['setlists']['setlist'])):
					date = decoded_data['setlists']['setlist'][x]['@eventDate'].encode("utf8")
					artist = decoded_data['setlists']['setlist'][x]['artist']['@name'].encode("utf8")
					location = decoded_data['setlists']['setlist'][x]['venue']['@name'].encode("utf8")
					id = decoded_data['setlists']['setlist'][x]['@id'].encode("utf8")
					iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,31,iconimage,artist = artist,type='setlist')
				total_items = decoded_data['setlists']['@total']
				if int(url)*items_per_page<int(total_items): addDir(translate(30411),str(int(url)+1),30,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass

def List_setlist_tracks(url):
	codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/setlist/'+url+'.json')
	decoded_data = json.loads(codigo_fonte)
	try:
		artist = decoded_data['setlist']['artist']['@name'].encode("utf8")
		for x in range(0, len(decoded_data['setlist']['sets']['set']['song'])):
			track_name = decoded_data['setlist']['sets']['set']['song'][x]['@name'].encode("utf8")
			iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
	except: pass

def Search_8tracks_playlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	if search_query.startswith('tags:'): codigo_fonte = abrir_url('http://8tracks.com/mix_sets/tags:'+urllib.quote(search_query[5:].replace(', ', '+').replace(',', '+'))+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	else: codigo_fonte = abrir_url('http://8tracks.com/mix_sets/keyword:'+urllib.quote(search_query)+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['mixes'])):
		username = decoded_data['mixes'][x]['user']['login'].encode("utf8")
		playlist_name = decoded_data['mixes'][x]['name'].encode("utf8")
		tracks_count = str(decoded_data['mixes'][x]['tracks_count'])
		playlist_id = str(decoded_data['mixes'][x]['id'])
		try: iconimage = decoded_data['mixes'][x]['cover_urls']['max200'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',33,iconimage,playlist_id = playlist_id,type='playlist')
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30411),str(int(url)+1),32,addonfolder+artfolder+'next.png',search_query = search_query)

def List_8tracks_tracks(url,iconimage,playlist_id):
	#official resolver method - more stable but no cache
	if selfAddon.getSetting('playlist_resolver_method')=="0":
		last_track = 0
		total_tracks = int(json.loads(abrir_url('http://8tracks.com/mixes/'+playlist_id+'.json?api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['mix']['tracks_count'])
		play_token = json.loads(abrir_url('http://8tracks.com/sets/new.json&api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['play_token']
		progress = xbmcgui.DialogProgress()
		progress.create(translate(30400),translate(30614))
		progress.update(0)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		if progress.iscanceled(): sys.exit(0)
		#load first track
		codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/play.json?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
		decoded_data = json.loads(codigo_fonte)
		progress.update(int(((0)*100)/(total_tracks)),translate(30614),translate(30615)+str(last_track+1)+translate(30616)+str(total_tracks))
		artist = decoded_data['set']['track']['performer'].encode("utf8")
		track_name = decoded_data['set']['track']['name'].encode("utf8")
		link = decoded_data['set']['track']['url'].encode("utf8")
		addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
		duration = int(decoded_data['set']['track']['play_duration'])
		listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
		listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
		playlist.add(link,listitem)
		if progress.iscanceled(): sys.exit(0)
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(playlist) #lets try to force a player to avoid no codec error
		#load remaining tracks
		if (last_track+1)<total_tracks:
			for x in range(last_track+1, total_tracks):
				try: codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477&format=jsonh&api_version=2')
				except urllib2.HTTPError, e: codigo_fonte = e.fp.read() #bypass 403 error
				decoded_data = json.loads(codigo_fonte)
				if progress.iscanceled(): sys.exit(0)
				try:
					progress.update(int(((x)*100)/(total_tracks)),translate(30614),translate(30615)+str(x+1)+translate(30616)+str(total_tracks))
					artist = decoded_data['set']['track']['performer'].encode("utf8")
					track_name = decoded_data['set']['track']['name'].encode("utf8")
					link = decoded_data['set']['track']['url'].encode("utf8")
					addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
					duration = int(decoded_data['set']['track']['play_duration'])
					listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
					listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
					playlist.add(link,listitem)
					print 'Debug: carregado track '+str(x)+' from official2'
				except:
					if decoded_data['status']=='403 Forbidden':
						for y in range((duration/2)+7, 0, -1):
							time.sleep(1)
							progress.update(int(((x)*100)/(total_tracks)),translate(30614),translate(30615)+str(x+1)+translate(30616)+str(total_tracks),translate(30617)+str(y)+translate(30618))
							if progress.iscanceled(): sys.exit(0)
						try:
							try: codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477&format=jsonh&api_version=2')
							except urllib2.HTTPError, e: codigo_fonte = e.fp.read() #bypass 403 error
							decoded_data = json.loads(codigo_fonte)
							progress.update(int(((x)*100)/(total_tracks)),translate(30614),'Carregando track '+str(x+1)+' de '+str(total_tracks))
							artist = decoded_data['set']['track']['performer'].encode("utf8")
							track_name = decoded_data['set']['track']['name'].encode("utf8")
							link = decoded_data['set']['track']['url'].encode("utf8")
							addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
							duration = int(decoded_data['set']['track']['play_duration'])
							listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
							listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
							playlist.add(link,listitem)
							print 'Debug: carregado track '+str(x)+' from official3'
						except:
							dialog = xbmcgui.Dialog()
							ok = dialog.ok(translate(30400), translate(30619))
							break
		if progress.iscanceled(): sys.exit(0)
		progress.update(100)
		progress.close()
	#omgcatz resolver method - with cache, faster in general
	if selfAddon.getSetting('playlist_resolver_method')=="1":
		# Get "correct" url from id
		req = urllib2.Request('https://8tracks.com/mixes/'+playlist_id+'/')
		res = urllib2.urlopen(req)
		playlist_url = res.geturl()
		# Let's use omgcatz to resolve and cache the playlist
		codigo_fonte = abrir_url_custom('http://omgcatz.com/run/fetch/eight.php', post = { 'url': playlist_url, 'playToken': '', 'mixId': '', 'trackNumber': '0' })
		decoded_data = json.loads(codigo_fonte)
		last_track = 0
		total_tracks = int(decoded_data['mix']['tracks_count'])
		progress = xbmcgui.DialogProgress()
		progress.create(translate(30400),translate(30620))
		progress.update(0)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		if progress.iscanceled(): sys.exit(0)
		for x in range(0, total_tracks):
			try:
				last_track = x
				progress.update(int(((x)*100)/(total_tracks)),translate(30620),translate(30615)+str(last_track+1)+translate(30616)+str(total_tracks))
				artist = decoded_data[str(x)]['artist'].encode("utf8")
				track_name = decoded_data[str(x)]['title'].encode("utf8")
				link = decoded_data[str(x)]['songUrl'].encode("utf8")
				duration = int(decoded_data[str(x)]['duration'])
				addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
				listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
				listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
				playlist.add(link,listitem)
				print 'Debug: carregado track '+str(x)+' from catz1'
			except:
				last_track = x-1
				break
		if progress.iscanceled(): sys.exit(0)
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(playlist) #lets try to force a player to avoid no codec error
		if (last_track+1)<total_tracks:
			play_token = decoded_data['play_token']
			mixId = str(decoded_data['mix']['id'])
			for x in range(last_track+1, total_tracks):
				codigo_fonte = abrir_url_custom('http://omgcatz.com/run/fetch/eight.php', post = { 'url': playlist_url, 'playToken': play_token, 'mixId': mixId, 'trackNumber': str(x) })
				decoded_data = json.loads(codigo_fonte)
				if progress.iscanceled(): sys.exit(0)
				try:
					progress.update(int(((x)*100)/(total_tracks)),translate(30620),translate(30615)+str(x+1)+translate(30616)+str(total_tracks))
					artist = decoded_data['0']['artist'].encode("utf8")
					track_name = decoded_data['0']['title'].encode("utf8")
					link = decoded_data['0']['songUrl'].encode("utf8")
					duration = int(decoded_data['0']['duration'])
					addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
					listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
					listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
					playlist.add(link,listitem)
					print 'Debug: carregado track '+str(x)+' from catz2'
				except:
					if decoded_data['error']==403:
						for y in range((duration/2)+7, 0, -1):
							time.sleep(1)
							progress.update(int(((x)*100)/(total_tracks)),translate(30620),translate(30615)+str(x+1)+translate(30616)+str(total_tracks),translate(30617)+str(y)+translate(30618))
							if progress.iscanceled(): sys.exit(0)
						try:
							codigo_fonte = abrir_url_custom('http://omgcatz.com/run/fetch/eight.php', post = { 'url': playlist_url, 'playToken': play_token, 'mixId': mixId, 'trackNumber': str(x) })
							decoded_data = json.loads(codigo_fonte)
							artist = decoded_data['0']['artist'].encode("utf8")
							track_name = decoded_data['0']['title'].encode("utf8")
							link = decoded_data['0']['songUrl'].encode("utf8")
							duration = int(decoded_data['0']['duration'])
							addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
							listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
							listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
							playlist.add(link,listitem)
							print 'Debug: carregado track '+str(x)+' from catz3'
						except:
							if decoded_data['error']==403:
								dialog = xbmcgui.Dialog()
								ok = dialog.ok(translate(30400), translate(30621))
								break
		if progress.iscanceled(): sys.exit(0)
		progress.update(100)
		progress.close()

def Search_atflick_soundtrack(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ast.vionlabs.com/api/search/'+urllib.quote(search_query)+'/'+str(items_per_page)+'/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['hits'])):
		try:
			name = decoded_data['hits'][x]['fields']['name'].encode("utf8")
			movie_id = str(decoded_data['hits'][x]['fields']['id'])
			try: iconimage = decoded_data['hits'][x]['fields']['posters'][1]['poster_link'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,movie_id,9,iconimage,type='soundtrack')
		except: pass
	#check if next page exist
	if int(url)*items_per_page+len(decoded_data['hits'])<int(decoded_data['total']): addDir(translate(30411),str(int(url)+1),34,addonfolder+artfolder+'next.png',playlist_id = playlist_id)

def Search_by_similartracks(artist,track_name):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=track.getSimilar&artist='+urllib.quote(artist)+'&track='+urllib.quote(track_name)+'&limit='+str(items_per_page)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['similartracks']['track']:
			artist = decoded_data['similartracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['similartracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['similartracks']['track']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['similartracks']['track'])):
				artist = decoded_data['similartracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['similartracks']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['similartracks']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
	except: pass

def Search_by_similarsoundtracks(url):
	codigo_fonte = abrir_url('http://ast.vionlabs.com/api/morelikethis/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['hits'])):
		try:
			name = decoded_data['hits'][x]['_source']['name'].encode("utf8")
			movie_id = str(decoded_data['hits'][x]['_source']['id'])
			try: iconimage = decoded_data['hits'][x]['_source']['posters'][1]['poster_link'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,movie_id,9,iconimage,type='soundtrack')
		except: pass

def Search_videoclip(artist,track_name,album):
	try:	
		search_string = urllib.quote(artist + ' ' + track_name + ' music video')
		codigo_fonte = abrir_url("http://gdata.youtube.com/feeds/api/videos?q="+ search_string +"&key=AIzaSyBbDY0UzvF5Es77M7S1UChMzNp0KsbaDPI&alt=json&category=Music&max-results=1")
	except: codigo_fonte = ''
	if codigo_fonte:
		try:
			codigo_fonte = eval(codigo_fonte)
			video_url = codigo_fonte["feed"]["entry"][0]["media$group"]['media$content'][0]['url']
			match = re.compile('v/(.+?)\?').findall(video_url)
		except: match = []
		if match:
			print 'Grabbed youtube id',match[0]
			video_path = "plugin://plugin.video.youtube?action=play_video&videoid="+match[0] 
			item = xbmcgui.ListItem(path=video_path)
			item.setInfo(type="music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)		
		else: 
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400), translate(30622))

###################################################################################
#DOWNLOADS AND RESOLVERS

def List_my_songs():
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30800))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		dirs = os.listdir(selfAddon.getSetting('downloads_folder'))
		for file in dirs:
			extension = os.path.splitext(file)[1]
			if extension == '.mp3' or extension == '.m4a': addLink(file,os.path.join(selfAddon.getSetting('downloads_folder'), file),39,addonfolder+artfolder+'no_cover.png',type = 'mymusic')

def Get_songfile_from_name(artist,track_name):
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(artist+' '+track_name)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	try: return decoded_data['response'][1]['url'].encode("utf8")
	except: return 'track_not_found'

def Resolve_songfile(url,artist,track_name,album,iconimage):
	#if a url is provided, the function reproduce it
	#else it gets the file from vk.com API using the artist and track_name info
	success = True
	if url=='' or url==None:
		progress = xbmcgui.DialogProgress()
		progress.create(translate(30400),translate(30801))
		progress.update(0)
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(artist+' '+track_name)+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		try: url=decoded_data['response'][1]['url'].encode("utf8")
		except:
			url=''
			success = False
		if progress.iscanceled(): sys.exit(0)
		progress.update(100)
		progress.close()
		item = xbmcgui.ListItem(path=url)
		item.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)
	else:
		item = xbmcgui.ListItem(path=url)
		item.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)

def Download_songfile(name,url,artist,track_name):
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30800))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		if url=="track_not_found":
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400),translate(30802))
			return
		elif url=='':
			url = Get_songfile_from_name(artist,track_name)
			if url=="track_not_found":
				dialog = xbmcgui.Dialog()
				ok = dialog.ok(translate(30400),translate(30802))
				return
		#get file extension
		if url.endswith('.m4a'): file_extension = '.m4a'
		else: file_extension = '.mp3'
		#correct the name - remove top track position and tags/labels
		regexfix = re.search('^\[COLOR yellow\][\d]+?\[/COLOR\] \-(.+?)$', name)
		if regexfix: name = regexfix.group(1)
		name = re.sub("\[/?(?:COLOR|B|I)[^]]*\]", "", name)
		name = re.sub('[<>:"/\|?*]', '', name) #remove not allowed characters in the filename
		params = { "url": url, "download_path": selfAddon.getSetting('downloads_folder'), "Title": name }
		downloader.download(name.decode("utf-8")+file_extension, params, async=False)

###################################################################################
#FAVORITES

#Info: version_fav is used to check/update favorites struture in future (if necessary)
#Current version: 0.01

def Favorites_menu():
	addDir(translate(30701),'songs',42,'')
	addDir(translate(30702),'albums',42,'')
	addDir(translate(30703),'setlists',42,'')
	addDir(translate(30704),'playlists',42,'')
	addDir(translate(30705),'soundtracks',42,'')

def List_favorites(url):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile): save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"soundtracks\": [], \n  \"songs\": [], \n  \"version_fav\": 0.01\n}")
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if url=='songs':
		for x in range(0, len(decoded_data['songs'])):
			if decoded_data['songs'][x]['type'].encode("utf8")=='vk.com': #get the direct link for a specific vk.com audio file id
				artist = decoded_data['songs'][x]['artist'].encode("utf8")
				track_name = decoded_data['songs'][x]['track_name'].encode("utf8")
				item_id = decoded_data['songs'][x]['item_id'].encode("utf8")
				try: url = json.loads(abrir_url('https://api.vk.com/method/audio.getById.json?audios='+item_id+'&access_token='+selfAddon.getSetting("vk_token")))['response'][0]['url'].encode("utf8")
				except: url = ''
				if decoded_data['songs'][x]['iconimage']: iconimage = decoded_data['songs'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addLink('[B]'+artist+'[/B] - '+track_name,url,39,iconimage,artist = artist,track_name = track_name,manualsearch = False,item_id = str(x),type='fav_song')
			elif decoded_data['songs'][x]['type'].encode("utf8")=='default': #call default song resolver method
				artist = decoded_data['songs'][x]['artist'].encode("utf8")
				track_name = decoded_data['songs'][x]['track_name'].encode("utf8")
				url = decoded_data['songs'][x]['url'].encode("utf8")
				if decoded_data['songs'][x]['iconimage']: iconimage = decoded_data['songs'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				if url or selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,url,39,iconimage,artist = artist,track_name = track_name,item_id = str(x),type='fav_song')
				else: addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name,item_id = str(x),type='fav_song')
	elif url=='albums':
		for x in range(0, len(decoded_data['albums'])):
			if decoded_data['albums'][x]['provider'].encode("utf8")=='itunes': #albums from itunes charts
				artist = decoded_data['albums'][x]['artist'].encode("utf8")
				album = decoded_data['albums'][x]['album'].encode("utf8")
				country = decoded_data['albums'][x]['country'].encode("utf8")
				url = decoded_data['albums'][x]['url'].encode("utf8")
				if decoded_data['albums'][x]['iconimage']: iconimage = decoded_data['albums'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album,url,19,iconimage,album = album,artist = artist,country = country,item_id = str(x),type='fav_album')
			elif decoded_data['albums'][x]['provider'].encode("utf8")=='default': #other albums from last.fm/7digital
				artist = decoded_data['albums'][x]['artist'].encode("utf8")
				album = decoded_data['albums'][x]['album'].encode("utf8")
				url = decoded_data['albums'][x]['url'].encode("utf8")
				if decoded_data['albums'][x]['iconimage']: iconimage = decoded_data['albums'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album,url,28,iconimage,artist = artist,album = album,item_id = str(x),type='fav_album')
	elif url=='setlists':
		for x in range(0, len(decoded_data['setlists'])):
			name = decoded_data['setlists'][x]['name'].encode("utf8")
			artist = decoded_data['setlists'][x]['artist'].encode("utf8")
			url = decoded_data['setlists'][x]['url'].encode("utf8")
			if decoded_data['setlists'][x]['iconimage']: iconimage = decoded_data['setlists'][x]['iconimage'].encode("utf8")
			else: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,url,31,iconimage,artist = artist,item_id = str(x),type='fav_setlist')
	elif url=='playlists':
		for x in range(0, len(decoded_data['playlists'])):
			if decoded_data['playlists'][x]['provider'].encode("utf8")=='digster': #playlists from digster
				name = decoded_data['playlists'][x]['name'].encode("utf8")
				url = decoded_data['playlists'][x]['playlist_id'].encode("utf8")
				country = decoded_data['playlists'][x]['country'].encode("utf8")
				if decoded_data['playlists'][x]['iconimage']: iconimage = decoded_data['playlists'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(name,url,6,iconimage,country = country,item_id = str(x),type='fav_playlist')
			elif decoded_data['playlists'][x]['provider'].encode("utf8")=='8tracks': #playlists from 8tracks
				name = decoded_data['playlists'][x]['name'].encode("utf8")
				playlist_id = decoded_data['playlists'][x]['playlist_id'].encode("utf8")
				if decoded_data['playlists'][x]['iconimage']: iconimage = decoded_data['playlists'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(name,'1',33,iconimage,playlist_id = playlist_id,item_id = str(x),type='fav_playlist')
	elif url=='soundtracks':
		for x in range(0, len(decoded_data['soundtracks'])):
			name = decoded_data['soundtracks'][x]['name'].encode("utf8")
			url = decoded_data['soundtracks'][x]['url'].encode("utf8")
			if decoded_data['soundtracks'][x]['iconimage']: iconimage = decoded_data['soundtracks'][x]['iconimage'].encode("utf8")
			else: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,url,9,iconimage,item_id = str(x),type='fav_soundtrack')

def Add_to_favorites(type,artist,album,country,name,playlist_id,track_name,url,iconimage,item_id):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile): save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"soundtracks\": [], \n  \"songs\": [], \n  \"version_fav\": 0.01\n}")
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if iconimage == addonfolder+artfolder+'no_cover.png': iconimage = None
	if type=='song':
		# vk.com mp3 url expires (is ip restricted), so is necessary use ids to save and restore music in favorites
		if url and url.find('vk.me/')>=0 or url.find('vk.com/')>=0 and item_id: decoded_data["songs"].append({"type": 'vk.com',"artist": artist,"track_name": track_name,"item_id": item_id,"iconimage": iconimage})
		# if is not a vk.com direct link, we use the default method to store in favorites
		else: decoded_data["songs"].append({"type": 'default',"artist": artist,"track_name": track_name,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification('[B]'+artist+'[/B] - '+track_name,translate(30700),'4000',iconimage)
	elif type=='album':
		#albums from itunes charts
		if country: decoded_data["albums"].append({"provider": 'itunes',"artist": artist,"album": album,"country": country,"url": url,"iconimage": iconimage})
		#other albums from last.fm/7digital
		else: decoded_data["albums"].append({"provider": 'default',"artist": artist,"album": album,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification('[B]'+artist+'[/B] - '+album,translate(30700),'4000',iconimage)
	elif type=='setlist':
		decoded_data["setlists"].append({"name": name,"artist": artist,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)
	elif type=='playlist':
		#digster playlists
		if country: decoded_data["playlists"].append({"provider": 'digster',"name": name,"playlist_id": url,"country": country,"iconimage": iconimage})
		#8tracks playlists
		else: decoded_data["playlists"].append({"provider": '8tracks',"name": name,"playlist_id": playlist_id,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)
	elif type=='soundtrack':
		decoded_data["soundtracks"].append({"name": name,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)

def Edit_favorites(url,type,item_id):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile):
		save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"soundtracks\": [], \n  \"songs\": [], \n  \"version_fav\": 0.01\n}")
		return
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if url=='moveup':#move up the item
		if type=='fav_song':
			if int(item_id)==0: decoded_data["songs"].insert(len(decoded_data["songs"])+1, decoded_data["songs"].pop(int(item_id)))
			else: decoded_data["songs"].insert(int(item_id)-1, decoded_data["songs"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			if int(item_id)==0: decoded_data["albums"].insert(len(decoded_data["albums"])+1, decoded_data["albums"].pop(int(item_id)))
			else: decoded_data["albums"].insert(int(item_id)-1, decoded_data["albums"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			if int(item_id)==0: decoded_data["setlists"].insert(len(decoded_data["setlists"])+1, decoded_data["setlists"].pop(int(item_id)))
			else: decoded_data["setlists"].insert(int(item_id)-1, decoded_data["setlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			if int(item_id)==0: decoded_data["playlists"].insert(len(decoded_data["playlists"])+1, decoded_data["playlists"].pop(int(item_id)))
			else: decoded_data["playlists"].insert(int(item_id)-1, decoded_data["playlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_soundtrack':
			if int(item_id)==0: decoded_data["soundtracks"].insert(len(decoded_data["soundtracks"])+1, decoded_data["soundtracks"].pop(int(item_id)))
			else: decoded_data["soundtracks"].insert(int(item_id)-1, decoded_data["soundtracks"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	elif url=='movedown':#move down the item
		if type=='fav_song':
			if int(item_id)==(len(decoded_data["songs"])-1): decoded_data["songs"].insert(0, decoded_data["songs"].pop(int(item_id)))
			else: decoded_data["songs"].insert(int(item_id)+1, decoded_data["songs"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			if int(item_id)==(len(decoded_data["albums"])-1): decoded_data["albums"].insert(0, decoded_data["albums"].pop(int(item_id)))
			else: decoded_data["albums"].insert(int(item_id)+1, decoded_data["albums"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			if int(item_id)==(len(decoded_data["setlists"])-1): decoded_data["setlists"].insert(0, decoded_data["setlists"].pop(int(item_id)))
			else: decoded_data["setlists"].insert(int(item_id)+1, decoded_data["setlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			if int(item_id)==(len(decoded_data["playlists"])-1): decoded_data["playlists"].insert(0, decoded_data["playlists"].pop(int(item_id)))
			else: decoded_data["playlists"].insert(int(item_id)+1, decoded_data["playlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_soundtrack':
			if int(item_id)==(len(decoded_data["soundtracks"])-1): decoded_data["soundtracks"].insert(0, decoded_data["soundtracks"].pop(int(item_id)))
			else: decoded_data["soundtracks"].insert(int(item_id)+1, decoded_data["soundtracks"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	elif url=='delete':#delete the item
		if type=='fav_song':
			del decoded_data["songs"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			del decoded_data["albums"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			del decoded_data["setlists"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			del decoded_data["playlists"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_soundtrack':
			del decoded_data["soundtracks"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	xbmc.executebuiltin('Container.Refresh')

###################################################################################
#USER SPACE

def Userspace_main():
	#vk.com user space
	if selfAddon.getSetting('vk_token')!='' and selfAddon.getSetting('vk_token')!=default_vk_token:
		#display vk.com menu
		addDir(translate(30850),'1',46,'',search_query = 'audio.get')
		addDir(translate(30851),'1',46,'',search_query = 'audio.getRecommendations')
	#last.fm user space
	if selfAddon.getSetting('lastfm_email')!='' and selfAddon.getSetting('lastfm_password')!='':
		selfAddon.setSetting('lastfm_token','')
		api_sig = hashlib.md5('api_key' + 'ca7bcdef4fda919aae12cb85be1b6794' + 'methodauth.getMobileSession' + 'password' + selfAddon.getSetting('lastfm_password') + 'username' + selfAddon.getSetting('lastfm_email') + 'b282ea6c4e937cc200ae43900304b506').hexdigest()
		codigo_fonte = abrir_url_custom('https://ws.audioscrobbler.com/2.0/', post = {'format': 'json', 'method': 'auth.getMobileSession', 'password': selfAddon.getSetting('lastfm_password'), 'username': selfAddon.getSetting('lastfm_email'), 'api_key': 'ca7bcdef4fda919aae12cb85be1b6794', 'api_sig': api_sig})
		decoded_data = json.loads(codigo_fonte)
		if 'error' in decoded_data:
			notification(translate(30861),translate(30863),'4000',addonfolder+artfolder+'notif_lastfm.png')
			selfAddon.setSetting('lastfm_token',value='')
		else:
			notification(translate(30861),translate(30864),'4000',addonfolder+artfolder+'notif_lastfm.png')
			selfAddon.setSetting('lastfm_token',value=decoded_data['session']['key'])
			userid_lastfm = decoded_data['session']['name']
		#dislay lastfm menu
		if selfAddon.getSetting('lastfm_token')!='':
			addDir(translate(30852),'1',47,'',search_query = 'user.getLovedTracks'+':'+userid_lastfm)
			addDir(translate(30853),'1',47,'',search_query = 'user.getRecentTracks'+':'+userid_lastfm)
			addDir(translate(30854),'1',47,'',search_query = 'user.getTopTracks'+':'+userid_lastfm)
			addDir(translate(30855),'1',47,'',search_query = 'user.getTopAlbums'+':'+userid_lastfm)
	#8tracks user space
	if selfAddon.getSetting('8tracks_email')!='' and selfAddon.getSetting('8tracks_password')!='':
		selfAddon.setSetting('8tracks_token','')
		codigo_fonte = abrir_url_custom('https://8tracks.com/sessions.json', post = {'login': selfAddon.getSetting('8tracks_email'), 'password': selfAddon.getSetting('8tracks_password'), 'api_version': '3'})
		decoded_data = json.loads(codigo_fonte)
		if decoded_data['status']!='200 OK':
			notification(translate(30862),translate(30863),'4000',addonfolder+artfolder+'notif_8tracks.png')
			selfAddon.setSetting('8tracks_token',value='')
		else:
			notification(translate(30862),translate(30864),'4000',addonfolder+artfolder+'notif_8tracks.png')
			selfAddon.setSetting('8tracks_token',value=decoded_data['user']['user_token'])
			userid_8tracks = str(decoded_data['user']['id'])
		#display 8tracks menu
		if selfAddon.getSetting('8tracks_token')!='':
			addDir(translate(30856),'1',48,'',search_query = 'liked:'+userid_8tracks)
			addDir(translate(30857),'1',48,'',search_query = 'listened:'+userid_8tracks)
			addDir(translate(30858),'1',48,'',search_query = 'dj:'+userid_8tracks)
			addDir(translate(30859),'1',48,'',search_query = 'recommended:'+userid_8tracks)

def My_vkcom(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	if search_query=='audio.get': #vk.com user musics
		index = ((int(url)-1)*items_per_page)
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.get.json?count='+str(items_per_page)+'&offset='+str(index)+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		for x in range(0, len(decoded_data['response'])):
			artist = decoded_data['response'][x]['artist'].encode("utf8").replace("&amp;", "&")
			track_name = decoded_data['response'][x]['title'].encode("utf8")
			link = decoded_data['response'][x]['url'].encode("utf8")
			item_id = str(decoded_data['response'][x]['owner_id'])+'_'+str(decoded_data['response'][x]['aid'])
			addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,item_id = item_id,manualsearch = False,type = 'song')
		#check if next page exist
		try:
			codigo_fonte = codigo_fonte = abrir_url('https://api.vk.com/method/audio.get.json?count='+str(items_per_page)+'&offset='+str((int(url)*items_per_page))+'&access_token='+selfAddon.getSetting("vk_token"))
			decoded_data = json.loads(codigo_fonte)
			if len(decoded_data['response'])>0:
				addDir(translate(30411),str(int(url)+1),46,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass
	elif search_query=='audio.getRecommendations': #vk.com user recomendations
		userid_vkcom = str(json.loads(abrir_url('https://api.vk.com/method/users.get.json?access_token='+selfAddon.getSetting("vk_token")))['response'][0]['uid'])
		index = ((int(url)-1)*items_per_page)
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.getRecommendations.json?uid='+userid_vkcom+'&count='+str(items_per_page)+'&offset='+str(index)+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		for x in range(0, len(decoded_data['response'])):
			artist = decoded_data['response'][x]['artist'].encode("utf8").replace("&amp;", "&")
			track_name = decoded_data['response'][x]['title'].encode("utf8")
			link = decoded_data['response'][x]['url'].encode("utf8")
			item_id = str(decoded_data['response'][x]['owner_id'])+'_'+str(decoded_data['response'][x]['aid'])
			addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,item_id = item_id,manualsearch = False,type = 'song')
		#check if next page exist
		try:
			codigo_fonte = codigo_fonte = abrir_url('https://api.vk.com/method/audio.getRecommendations.json?uid='+userid_vkcom+'&count='+str(items_per_page)+'&offset='+str((int(url)*items_per_page))+'&access_token='+selfAddon.getSetting("vk_token"))
			decoded_data = json.loads(codigo_fonte)
			if len(decoded_data['response'])>0:
				addDir(translate(30411),str(int(url)+1),46,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass

def My_lastfm(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	method = search_query.split(':', 1 )[0]
	userid_lastfm = search_query.split(':', 1 )[1]
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method='+method+'&user='+userid_lastfm+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	if method=='user.getTopAlbums': # retrieve user data regarding albums
		try:
			#checks if output has only an object or various and proceeds according
			if 'name' in decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']:
				artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['artist']['name'].encode("utf8")
				album_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['name'].encode("utf8")
				mbid = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['mbid'].encode("utf8")
				try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
			else:
				for x in range(0, len(decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'])):
					artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['artist']['name'].encode("utf8")
					album_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['name'].encode("utf8")
					mbid = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['mbid'].encode("utf8")
					try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['image'][3]['#text'].encode("utf8")
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
				total_pages = decoded_data[method[method.find('.get')+len('.get'):].lower()]['@attr']['totalPages']
				if int(url)<int(total_pages): addDir(translate(30411),str(int(url)+1),47,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass
	else: # retrieve user data regarding tracks
		try:
			#checks if output has only an object or various and proceeds according
			if 'name' in decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']:
				try: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['artist']['name'].encode("utf8")
				except: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['artist']['#text'].encode("utf8")
				track_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['name'].encode("utf8")
				try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
			else:
				for x in range(0, len(decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'])):
					try: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['artist']['name'].encode("utf8")
					except: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['artist']['#text'].encode("utf8")
					track_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['name'].encode("utf8")
					#mbid = decoded_data['toptracks']['track'][x]['mbid'].encode("utf8")
					try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['image'][3]['#text'].encode("utf8")
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name)
				total_pages = decoded_data[method[method.find('.get')+len('.get'):].lower()]['@attr']['totalPages']
				if int(url)<int(total_pages): addDir(translate(30411),str(int(url)+1),47,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass

def My_8tracks(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://8tracks.com/mix_sets/'+search_query+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'api_key=e165128668b69291bf8081dd743fa6b832b4f477', headers={'X-User-Token': selfAddon.getSetting('8tracks_token') })
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['mixes'])):
		username = decoded_data['mixes'][x]['user']['login'].encode("utf8")
		playlist_name = decoded_data['mixes'][x]['name'].encode("utf8")
		tracks_count = str(decoded_data['mixes'][x]['tracks_count'])
		playlist_id = str(decoded_data['mixes'][x]['id'])
		try: iconimage = decoded_data['mixes'][x]['cover_urls']['max200'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',33,iconimage,playlist_id = playlist_id,type='playlist')
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30411),str(int(url)+1),48,addonfolder+artfolder+'next.png',search_query = search_query)

###################################################################################
#SETTINGS

def Open_settings():
	xbmcaddon.Addon(addon_id).openSettings()

###################################################################################
#XBMC RANDOM FUNCTIONS: OPEN_URl; ADDLINK; ADDDIR, FANART, NOTIFICATION, ETC...

def get_artist_fanart(artist):
	if not xbmcvfs.exists(os.path.join(datapath,"artistfanart")): xbmcvfs.mkdir(os.path.join(datapath,"artistfanart"))
	artistfile = os.path.join(datapath,"artistfanart",urllib.quote(artist) + '.txt')
	if xbmcvfs.exists(artistfile):
		fanart_list = eval(readfile(artistfile))
		return str(fanart_list[randint(0,len(fanart_list))-1])
	else:
		try:
			codigo_fonte = abrir_url('http://www.theaudiodb.com/api/v1/json/1/search.php?s=' + urllib.quote(artist))
		except:
			codigo_fonte = ''
		if codigo_fonte:
			decoded_data = json.loads(codigo_fonte)
			if len(decoded_data) >= 1:
    				fanart_list = []
    				if decoded_data['artists'][0]['strArtistFanart']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart'])
    				if decoded_data['artists'][0]['strArtistFanart2']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart2'])
    				if decoded_data['artists'][0]['strArtistFanart3']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart3'])
        			if fanart_list:
        				save(artistfile,str(fanart_list))
    					return str(fanart_list[randint(0,len(fanart_list)-1)])
    				else:
    					return ''
     		else:
     			return ''

#Function to write to txt files
def save(filename,contents):
    fh = open(filename, 'w')
    fh.write(contents)
    fh.close()

#Function to read txt files
def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string

def notification(title,message,time,iconimage):
    xbmc.executebuiltin("XBMC.notification("+title+","+message+","+time+","+iconimage+")")

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def abrir_url_custom(url,**kwargs):
	for key, value in kwargs.items(): exec('%s = %s' % (key, repr(value)))
	if 'post' in locals():
		data = urllib.urlencode(post)
		req = urllib2.Request(url,data)
	else: req = urllib2.Request(url)
	if 'headers' in locals():
		for x in range(0, len(headers)):
			req.add_header(headers.keys()[x], headers.values()[x])
	if 'user_agent' in locals(): req.add_header('User-Agent', user_agent)
	else: req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0')
	if 'referer' in locals(): req.add_header('Referer', referer)
	if 'timeout' in locals(): response = urllib2.urlopen(req, timeout=timeout)
	else: response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,mode,iconimage,**kwargs):
	extra_args = ''
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
		extra_args = extra_args + '&' + str(key) + '=' + urllib.quote_plus(str(value))
	if selfAddon.getSetting('get_artist_fanart')=="true":
		try:
			fanart = get_artist_fanart(artist)
		except:
			fanart = ''
	else: fanart = ''
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+extra_args
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
	liz.setProperty('IsPlayable', 'true')
	liz.setProperty('fanart_image', fanart)
	cm = []
	if type and type!='mymusic':
		if 'manualsearch' in locals() and manualsearch==True or not 'manualsearch' in locals():
			if selfAddon.getSetting('playing_type') == "0": cm.append((translate(30803), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=26&url=1&search_query='+urllib.quote_plus(str(artist)+' '+str(track_name))+')'))
		cm.append((translate(30804), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=35&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+')'))
		if type=='song':
			if item_id: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+'&url='+urllib.quote_plus(url)+'&item_id='+urllib.quote_plus(item_id)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='fav_song':
			cm.append((translate(30808), 'RunPlugin(plugin://'+addon_id+'/?mode=44&url=moveup&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30809), 'RunPlugin(plugin://'+addon_id+'/?mode=44&url=movedown&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30810), 'RunPlugin(plugin://'+addon_id+'/?mode=44&url=delete&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
		cm.append((translate(30805), 'RunPlugin(plugin://'+addon_id+'/?mode=40&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
		if selfAddon.getSetting('playing_type') == "0": cm.append((translate(30806), 'RunPlugin(plugin://'+addon_id+'/?mode=37&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,folder=True,**kwargs):
	extra_args = ''
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
		extra_args = extra_args + '&' + str(key) + '=' + urllib.quote_plus(str(value))
	if selfAddon.getSetting('get_artist_fanart')=="true":
		try:
			fanart = get_artist_fanart(artist)
		except:
			fanart = ''
	else: fanart = ''
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+extra_args
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	cm = []
	if type:
		if type=='album':
			if country: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&country='+urllib.quote_plus(country)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='setlist': cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(url)+'&artist='+urllib.quote_plus(artist)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='playlist':
			if country: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(url)+'&country='+urllib.quote_plus(country)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&name='+urllib.quote_plus(name)+'&playlist_id='+urllib.quote_plus(playlist_id)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='soundtrack':
			cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=43&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30811), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=36&url='+urllib.quote_plus(url)+')'))
		elif type=='fav_song' or type=='fav_album' or type=='fav_setlist' or type=='fav_playlist' or type=='fav_soundtrack':
			if type=='fav_soundtrack': cm.append((translate(30811), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=36&url='+urllib.quote_plus(url)+')'))
			cm.append((translate(30808), 'RunPlugin(plugin://'+addon_id+'/?mode=44&url=moveup&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30809), 'RunPlugin(plugin://'+addon_id+'/?mode=44&url=movedown&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30810), 'RunPlugin(plugin://'+addon_id+'/?mode=44&url=delete&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None
artist=None
album=None
track_name=None
type=None
search_query=None
country=None
item_id=None
playlist_id=None
fanart=None


try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: artist=urllib.unquote_plus(params["artist"])
except: pass
try: album=urllib.unquote_plus(params["album"])
except: pass
try: track_name=urllib.unquote_plus(params["track_name"])
except: pass
try: type=urllib.unquote_plus(params["type"])
except: pass
try: search_query=urllib.unquote_plus(params["search_query"])
except: pass
try: country=urllib.unquote_plus(params["country"])
except: pass
try: item_id=urllib.unquote_plus(params["item_id"])
except: pass
try: playlist_id=urllib.unquote_plus(params["playlist_id"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Fanart: "+str(fanart)
if artist: print "Artist: "+str(artist)
if album: print "Album: "+str(album)
if track_name: print "Track Name: "+str(track_name)
if type: print "Type: "+str(type)
if search_query: print "Search Query: "+str(search_query)
if country: print "Country: "+str(country)
if item_id: print "Item Id: "+str(item_id)
if playlist_id: print "Playlist Id: "+str(playlist_id)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

# Main Menu
if mode==None: Main_menu()
# Recomendations
elif mode==1: Recomendations(url)
# Digster
elif mode==2: Digster_menu()
elif mode==3: Digster_sections()
elif mode==4: Digster_categories(url)
elif mode==5: List_digster_playlists(url,search_query)
elif mode==6: List_digster_tracks(url,country)
# Atflick soundtrack
elif mode==7: Atflick_menu()
elif mode==8: List_atflick_movies(url,playlist_id)
elif mode==9: List_atflick_albums(url)
elif mode==10: List_atflick_tracks(url)
# 8tracks playlists
elif mode==11: Eighttracks_menu()
elif mode==12: List_8tracks_suggestions(url,search_query)
# Charts
elif mode==13: Top_charts_menu()
elif mode==14: Vkcom_popular(url)
elif mode==15 or mode==16: Itunes_countries_menu(mode)
elif mode==17: Itunes_track_charts(url,country)
elif mode==18: Itunes_album_charts(url,country)
elif mode==19: Itunes_list_album_tracks(url,album,country)
elif mode==20: Beatport_top100(url,playlist_id)
elif mode==21 or mode==22: Officialcharts_uk(url,mode,playlist_id)
elif mode==23 or mode==24: Billboard_charts(url,mode,playlist_id)
# Search and list content
elif mode==25: Search_main()
elif mode==26: Search_by_tracks(url,search_query)
elif mode==27: Search_by_albums(url,search_query)
elif mode==28: List_album_tracks(url,artist,album)
elif mode==29: Search_by_toptracks(url,search_query)
elif mode==30: Search_by_setlists(url,search_query)
elif mode==31: List_setlist_tracks(url)
elif mode==32: Search_8tracks_playlists(url,search_query)
elif mode==33: List_8tracks_tracks(url,iconimage,playlist_id)
elif mode==34: Search_atflick_soundtrack(url,search_query)
elif mode==35: Search_by_similartracks(artist,track_name)
elif mode==36: Search_by_similarsoundtracks(url)
elif mode==37: Search_videoclip(artist,track_name,album)
# Downloads and Resolvers
elif mode==38: List_my_songs()
elif mode==39:
	if selfAddon.getSetting('playing_type') == "0" or type=='mymusic':
		Resolve_songfile(url,artist,track_name,album,iconimage)
	elif selfAddon.getSetting('playing_type') == "1":
		Search_videoclip(artist,track_name,album)
	else:pass
elif mode==40: Download_songfile(name,url,artist,track_name)
# Favorites
elif mode==41: Favorites_menu()
elif mode==42: List_favorites(url)
elif mode==43: Add_to_favorites(type,artist,album,country,name,playlist_id,track_name,url,iconimage,item_id)
elif mode==44: Edit_favorites(url,type,item_id)
# User space
elif mode==45: Userspace_main()
elif mode==46: My_vkcom(url,search_query)
elif mode==47: My_lastfm(url,search_query)
elif mode==48: My_8tracks(url,search_query)
# Settings
elif mode==49: Open_settings()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))