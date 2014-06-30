#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 2014 Techdealer

##############LIBRARIES TO IMPORT AND SETTINGS####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,datetime,os,xbmcvfs
import json
import random
h = HTMLParser.HTMLParser()

import SimpleDownloader as downloader
downloader = downloader.SimpleDownloader()
from t0mm0.common.addon import Addon
from random import randint

addon_id = 'plugin.audio.musicbox'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
translation = selfAddon.getLocalizedString
datapath = Addon(addon_id).get_profile()

def translate(text):
	return translation(text).encode('utf-8')
	  
###################################################################################
#MAIN MENU

def Main_menu():
	if selfAddon.getSetting('vk_token') == "":
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400), translate(30401))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q=eminem&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		if 'error' in decoded_data:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400), translate(30402))
			xbmcaddon.Addon(addon_id).openSettings()
		else:
			addDir(translate(30403),'1',1,addonfolder+artfolder+'recomended.png')
			addDir(translate(30404),'1',2,addonfolder+artfolder+'digster.png')
			addDir(translate(30405),'1',7,addonfolder+artfolder+'charts.png')
			addDir(translate(30406),'1',15,addonfolder+artfolder+'search.png')
			addDir(translate(30407),'1',24,addonfolder+artfolder+'mymusic.png')
			addDir(translate(30408),'',27,addonfolder+artfolder+'configs.png',False)

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
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name)
		elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name)
		elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
	total_pages = decoded_data['tracks']['@attr']['totalPages']
	if int(url)<int(total_pages): addDir(translate(30409),str(int(url)+1),1,addonfolder+artfolder+'next.png')

###################################################################################
#DIGSTER	

def Digster_menu():
	addDir('[COLOR blue][B]'+translate(30113)+':[/B][/COLOR] '+['Adria','Australia','Austria','Belgium','Denmark','Estonia','Finland','France','Germany','Latvia','Lithuania','Mexico','Netherlands','New Zeland','Norway','Poland','Portugal','Romania','Spain','Sweden','Switzerland','United Kingdom','USA'][int(selfAddon.getSetting('digster_country'))],'',2,'',False)
	addDir(translate(30450),'',3,'')
	addDir(translate(30451),'genre',4,'')
	addDir(translate(30452),'mood',4,'')
	addDir(translate(30453),'suitable',4,'')

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
		addDir(title,slug,6,iconimage)
	#check if next page exist
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists?posts_per_page='+str(items_per_page)+'&paged='+str(int(url)+1)+search_query)
	decoded_data = json.loads(codigo_fonte)
	if len(decoded_data['playlists'])>0: addDir(translate(30409),str(int(url)+1),5,addonfolder+artfolder+'next.png',search_query = search_query)

def List_digster_tracks(url):
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
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
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name)
		elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name)
		elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)

###################################################################################
#CHARTS

def Top_charts_menu():
	addDir(translate(30500),'1',8,'')
	addDir(translate(30501),'1',9,'')
	addDir(translate(30502),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-100')
	addDir(translate(30503),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/billboard-200')
	addDir(translate(30504),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-songs')
	addDir(translate(30505),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-albums')
	addDir(translate(30506),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/pop-songs')
	addDir(translate(30507),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/country-songs')
	addDir(translate(30508),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/country-albums')
	addDir(translate(30509),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-songs')
	addDir(translate(30510),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-albums')
	addDir(translate(30511),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-songs')
	addDir(translate(30512),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-albums')
	addDir(translate(30513),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-r-and-b-hip-hop-airplay')
	addDir(translate(30514),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/dance-electronic-albums')
	addDir(translate(30515),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-songs')
	addDir(translate(30516),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-albums')

def Itunes_countries_menu(mode):
	country_name = ["Albania","Algeria","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Botswana","Brazil","British Virgin Islands","Brunei Darussalam","Bulgaria","Burkina Faso","Cambodia","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo, Republic of the","Costa Rica","Croatia","Cyprus","Czech Republic","Denmark","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Fiji","Finland","France","Gambia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea-Bissau","Guyana","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Korea, Republic Of","Kuwait","Kyrgyzstan","Lao, People's Democratic Republic","Latvia","Lebanon","Liberia","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Mauritania","Mauritius","Mexico","Micronesia, Federated States of","Moldova","Mongolia","Montserrat","Mozambique","Namibia","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Saudi Arabia","Senegal","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","South Africa","Spain","Sri Lanka","St. Kitts and Nevis","St. Lucia","St. Vincent and The Grenadines","Suriname","Swaziland","Sweden","Switzerland","São Tomé and Príncipe","Taiwan","Tajikistan","Tanzania","Thailand","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Venezuela","Vietnam","Yemen","Zimbabwe"]
	country_code = ["al","dz","ao","ai","ag","ar","am","au","at","az","bs","bh","bb","by","be","bz","bj","bm","bt","bo","bw","br","vg","bn","bg","bf","kh","ca","cv","ky","td","cl","cn","co","cg","cr","hr","cy","cz","dk","dm","do","ec","eg","sv","ee","fj","fi","fr","gm","de","gh","gr","gd","gt","gw","gy","hn","hk","hu","is","in","id","ie","ir","it","jm","jp","jo","kz","ke","kr","kw","kg","la","lv","lb","lr","lt","lu","mo","mk","mg","mw","my","ml","mt","mr","mu","mx","fm","md","mn","ms","mz","na","np","nl","nz","ni","ne","ng","no","om","pk","pw","pa","pg","py","pe","ph","pl","pt","qa","ro","ru","sa","sn","sc","sl","sg","sk","si","sb","za","es","lk","kn","lc","vc","sr","sz","se","ch","st","tw","tj","tz","th","tt","tn","tr","tm","tc","ug","ua","ae","gb","us","uy","uz","ve","vn","ye","zw"]
	for x in range(0, len(country_name)):
		if country_code[x] not in ["al","dz","ao","bj","bt","td","cn","cg","gy","is","jm","kr","kw","lr","mk","mg","mw","ml","mr","ms","pk","pw","sn","sc","sl","sb","lc","vc","sr","st","tz","tn","tc","uy","ye"]: #Countries without music store
			if mode==8: addDir(country_name[x],'1',10,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])
			elif mode==9: addDir(country_name[x],'1',11,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])

def Itunes_track_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topsongs/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
		track_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
		try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name)
		elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name)
		elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
	if int(int(url)*items_per_page)<300: addDir(translate(30409),str(int(url)+1),10,addonfolder+artfolder+'next.png',country = country)

def Itunes_album_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topalbums/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
		album_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
		id = decoded_data['feed']['entry'][x]['id']['attributes']['im:id'].encode("utf8")
		try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+artist+'[/B] - '+album_name,id,12,iconimage,album = album_name,country = country)
	if int(int(url)*items_per_page)<300: addDir(translate(30409),str(int(url)+1),14,addonfolder+artfolder+'next.png',country = country)

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
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name,album = album)
				elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name,album = album)
				elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
	except: pass
		
def Billboard_charts(url,mode,playlist_id):
	#if mode==8: list billboard track charts
	#if mode==9: list billboard album charts
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str(int(url)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
	decoded_data = json.loads(codigo_fonte)
	try:
		if len(decoded_data['query']['results']['item']) > 0:
			if mode==13:
				for x in range(0, len(decoded_data['query']['results']['item'])):
					artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
					track_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',25,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name)
					elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name)
					elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',16,addonfolder+artfolder+'no_cover.png',search_query = artist+' '+track_name)
			elif mode==14:
				for x in range(0, len(decoded_data['query']['results']['item'])):
					artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
					album_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
					addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',18,addonfolder+artfolder+'no_cover.png',artist = artist,album = album_name)
	except: pass
	try:
		codigo_fonte_2 = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str((int(url)+1)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
		decoded_data_2 = json.loads(codigo_fonte_2)
		if len(decoded_data_2['query']['results']['item']) > 0: addDir(translate(30409),str(int(url)+1),mode,addonfolder+artfolder+'next.png',playlist_id = playlist_id)
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
			codigo_fonte = abrir_url('http://8tracks.com/mix_sets/tags:'+urllib.quote(search_query[5:].replace(', ', '+').replace(',', '+'))+'.json?include=mixes+pagination'+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['total_entries']
			if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',22,'',search_query = search_query)
	else:
		#tracks
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(search_query)+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		total_items = decoded_data['response'][0]
		if int(total_items)>0: addDir(translate(30601)+str(total_items)+translate(30602),'1',16,'',search_query = search_query)
		#albums
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: decoded_data['error']
		except:
			try: total_items = decoded_data['topalbums']['@attr']['total']
			except: total_items = decoded_data['topalbums']['total']
			if int(total_items)>0: addDir(translate(30603)+str(total_items)+translate(30604),'1',17,'',search_query = search_query)
		#toptracks
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: total_items = decoded_data['toptracks']['@attr']['total']
		except:
			try: total_items = decoded_data['toptracks']['total']
			except: total_items = 0
		if int(total_items)>0: addDir(translate(30605)+str(total_items)+translate(30606),'1',19,'',search_query = search_query)
		#setlists
		try: codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/search/setlists.json?artistName='+urllib.quote(search_query))
		except urllib2.URLError, e: codigo_fonte = "not found"
		if codigo_fonte != "not found":
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['setlists']['@total']
			addDir(translate(30607)+str(total_items)+translate(30608),'1',20,'',search_query = search_query)
		#playlists
		codigo_fonte = abrir_url('http://8tracks.com/mix_sets/keyword:'+urllib.quote(search_query)+'.json?include=mixes+pagination'+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
		decoded_data = json.loads(codigo_fonte)
		total_items = decoded_data['total_entries']
		if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',22,'',search_query = search_query)

def Search_by_tracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	index = ((int(url)-1)*items_per_page)
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(search_query)+'&count='+str(items_per_page)+'&offset='+str(index)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	for x in range(1, len(decoded_data['response'])):
		artist = decoded_data['response'][x]['artist'].encode("utf8").replace("&amp;", "&")
		track_name = decoded_data['response'][x]['title'].encode("utf8")
		link = decoded_data['response'][x]['url'].encode("utf8")
		addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False)
	total_items = decoded_data['response'][0]
	if index+items_per_page<int(total_items): addDir(translate(30409),str(int(url)+1),16,addonfolder+artfolder+'next.png',search_query = search_query)
	
def Search_by_albums(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		for x in range(0, len(decoded_data['topalbums']['album'])):
			artist = decoded_data['topalbums']['album'][x]['artist']['name'].encode("utf8")
			album_name = decoded_data['topalbums']['album'][x]['name'].encode("utf8")
			mbid = decoded_data['topalbums']['album'][x]['mbid'].encode("utf8")
			try: iconimage = decoded_data['topalbums']['album'][x]['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir('[B]'+artist+'[/B] - '+album_name,mbid,18,iconimage, artist = artist, album = album_name)
		total_pages = decoded_data['topalbums']['@attr']['totalPages']
		if int(url)<int(total_pages): addDir(translate(30409),str(int(url)+1),17,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def List_album_tracks(url,artist,album):
	if url: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&mbid='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	else: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&artist='+urllib.quote(artist)+'&album='+urllib.quote(album)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['album']['tracks']['track']:
			artist = decoded_data['album']['tracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['album']['tracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name,album = album)
			elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name,album = album)
			elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['album']['tracks']['track'])):
				artist = decoded_data['album']['tracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['album']['tracks']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name,album = album)
				elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name,album = album)
				elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
	except: pass

def Search_by_toptracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
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
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name)
			elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name)
			elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['toptracks']['track'])):
				artist = decoded_data['toptracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['toptracks']['track'][x]['name'].encode("utf8")
				#mbid = decoded_data['toptracks']['track'][x]['mbid'].encode("utf8")
				try: iconimage = decoded_data['toptracks']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name)
				elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name)
				elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
			total_pages = decoded_data['toptracks']['@attr']['totalPages']
			if int(url)<int(total_pages): addDir(translate(30409),str(int(url)+1),19,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def Search_by_setlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
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
				addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,21,iconimage)
			else:
				for x in range(0, len(decoded_data['setlists']['setlist'])):
					date = decoded_data['setlists']['setlist'][x]['@eventDate'].encode("utf8")
					artist = decoded_data['setlists']['setlist'][x]['artist']['@name'].encode("utf8")
					location = decoded_data['setlists']['setlist'][x]['venue']['@name'].encode("utf8")
					id = decoded_data['setlists']['setlist'][x]['@id'].encode("utf8")
					iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,21,iconimage)
				total_items = decoded_data['setlists']['@total']
				if int(url)*items_per_page<int(total_items): addDir(translate(30409),str(int(url)+1),20,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass

def List_setlist_tracks(url):
	codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/setlist/'+url+'.json')
	decoded_data = json.loads(codigo_fonte)
	try:
		artist = decoded_data['setlist']['artist']['@name'].encode("utf8")
		for x in range(0, len(decoded_data['setlist']['sets']['set']['song'])):
			track_name = decoded_data['setlist']['sets']['set']['song'][x]['@name'].encode("utf8")
			iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',25,iconimage,artist = artist,track_name = track_name)
			elif selfAddon.getSetting('track_resolver_method')=="1": addLink('[B]'+artist+'[/B] - '+track_name,Get_songfile_from_name(artist,track_name),100,iconimage,artist = artist,track_name = track_name)
			elif selfAddon.getSetting('track_resolver_method')=="2": addDir('[B]'+artist+'[/B] - '+track_name,'1',16,iconimage,search_query = artist+' '+track_name)
	except: pass

def Search_8tracks_playlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
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
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',23,iconimage,playlist_id = playlist_id)
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30409),str(int(url)+1),22,addonfolder+artfolder+'next.png',search_query = search_query)

def List_8tracks_tracks(url,iconimage,playlist_id):
	#official resolver method - more stable but no cache
	if selfAddon.getSetting('playlist_resolver_method')=="0":
		last_track = 0
		total_tracks = int(json.loads(abrir_url('http://8tracks.com/mixes/'+playlist_id+'.json?api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['mix']['tracks_count'])
		play_token = json.loads(abrir_url('http://8tracks.com/sets/new.json&api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['play_token']
		progress = xbmcgui.DialogProgress()
		progress.create(translate(30400),translate(30612))
		progress.update(0)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		if progress.iscanceled(): sys.exit(0)
		#load first track
		codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/play.json?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
		decoded_data = json.loads(codigo_fonte)
		progress.update(int(((0)*100)/(total_tracks)),translate(30612),translate(30613)+str(last_track+1)+translate(30614)+str(total_tracks))
		artist = decoded_data['set']['track']['performer'].encode("utf8")
		track_name = decoded_data['set']['track']['name'].encode("utf8")
		link = decoded_data['set']['track']['url'].encode("utf8")
		addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False)
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
					progress.update(int(((x)*100)/(total_tracks)),translate(30612),translate(30613)+str(x+1)+translate(30614)+str(total_tracks))
					artist = decoded_data['set']['track']['performer'].encode("utf8")
					track_name = decoded_data['set']['track']['name'].encode("utf8")
					link = decoded_data['set']['track']['url'].encode("utf8")
					addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False)
					duration = int(decoded_data['set']['track']['play_duration'])
					listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
					listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
					playlist.add(link,listitem)
					print 'Debug: carregado track '+str(x)+' from official2'
				except:
					if decoded_data['status']=='403 Forbidden':
						for y in range((duration/2)+7, 0, -1):
							time.sleep(1)
							progress.update(int(((x)*100)/(total_tracks)),translate(30612),translate(30613)+str(x+1)+translate(30614)+str(total_tracks),translate(30615)+str(y)+translate(30616))
							if progress.iscanceled(): sys.exit(0)
						try:
							try: codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477&format=jsonh&api_version=2')
							except urllib2.HTTPError, e: codigo_fonte = e.fp.read() #bypass 403 error
							decoded_data = json.loads(codigo_fonte)
							progress.update(int(((x)*100)/(total_tracks)),translate(30612),'Carregando track '+str(x+1)+' de '+str(total_tracks))
							artist = decoded_data['set']['track']['performer'].encode("utf8")
							track_name = decoded_data['set']['track']['name'].encode("utf8")
							link = decoded_data['set']['track']['url'].encode("utf8")
							addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False)
							duration = int(decoded_data['set']['track']['play_duration'])
							listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
							listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
							playlist.add(link,listitem)
							print 'Debug: carregado track '+str(x)+' from official3'
						except:
							dialog = xbmcgui.Dialog()
							ok = dialog.ok(translate(30400), translate(30617))
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
		progress.create(translate(30400),translate(30618))
		progress.update(0)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		if progress.iscanceled(): sys.exit(0)
		for x in range(0, total_tracks):
			try:
				last_track = x
				progress.update(int(((x)*100)/(total_tracks)),translate(30618),translate(30613)+str(last_track+1)+translate(30614)+str(total_tracks))
				artist = decoded_data[str(x)]['artist'].encode("utf8")
				track_name = decoded_data[str(x)]['title'].encode("utf8")
				link = decoded_data[str(x)]['songUrl'].encode("utf8")
				duration = int(decoded_data[str(x)]['duration'])
				addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False)
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
					progress.update(int(((x)*100)/(total_tracks)),translate(30618),translate(30613)+str(x+1)+translate(30614)+str(total_tracks))
					artist = decoded_data['0']['artist'].encode("utf8")
					track_name = decoded_data['0']['title'].encode("utf8")
					link = decoded_data['0']['songUrl'].encode("utf8")
					duration = int(decoded_data['0']['duration'])
					addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False)
					listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
					listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
					playlist.add(link,listitem)
					print 'Debug: carregado track '+str(x)+' from catz2'
				except:
					if decoded_data['error']==403:
						for y in range((duration/2)+7, 0, -1):
							time.sleep(1)
							progress.update(int(((x)*100)/(total_tracks)),translate(30618),translate(30613)+str(x+1)+translate(30614)+str(total_tracks),translate(30615)+str(y)+translate(30616))
							if progress.iscanceled(): sys.exit(0)
						try:
							codigo_fonte = abrir_url_custom('http://omgcatz.com/run/fetch/eight.php', post = { 'url': playlist_url, 'playToken': play_token, 'mixId': mixId, 'trackNumber': str(x) })
							decoded_data = json.loads(codigo_fonte)
							artist = decoded_data['0']['artist'].encode("utf8")
							track_name = decoded_data['0']['title'].encode("utf8")
							link = decoded_data['0']['songUrl'].encode("utf8")
							duration = int(decoded_data['0']['duration'])
							addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False)
							listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
							listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
							playlist.add(link,listitem)
							print 'Debug: carregado track '+str(x)+' from catz3'
						except:
							if decoded_data['error']==403:
								dialog = xbmcgui.Dialog()
								ok = dialog.ok(translate(30400), translate(30619))
								break
		if progress.iscanceled(): sys.exit(0)
		progress.update(100)
		progress.close()

###################################################################################
#DOWNLOADS AND RESOLVERS

def List_my_songs():
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30700))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		dirs = os.listdir(selfAddon.getSetting('downloads_folder'))
		for file in dirs:
			extension = os.path.splitext(file)[1]
			if extension == '.mp3' or extension == '.m4a': addLink(file,os.path.join(selfAddon.getSetting('downloads_folder'), file),100,addonfolder+artfolder+'no_cover.png')

def Get_songfile_from_name(artist,track_name):
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(artist+' '+track_name)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	try: return decoded_data['response'][1]['url'].encode("utf8")
	except: return 'track_not_found'

def Resolve_songfile_from_name(artist,track_name,name,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create(translate(30400),translate(30701))
	progress.update(0)
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(artist+' '+track_name)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	try: url=decoded_data['response'][1]['url'].encode("utf8")
	except: url='track_not_found'
	if progress.iscanceled(): sys.exit(0)
	progress.update(100)
	progress.close()
	play(url,name,iconimage,artist,track_name,album,fanart)

def Download_songfile(name,url,artist,track_name):
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30700))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		if url=="track_not_found":
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400),translate(30702))
			return
		elif url=='':
			url = Get_songfile_from_name(artist,track_name)
			if url=="track_not_found":
				dialog = xbmcgui.Dialog()
				ok = dialog.ok(translate(30400),translate(30702))
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
#SETTINGS

def Open_settings():
	xbmcaddon.Addon(addon_id).openSettings()

###################################################################################
#PLAYER...
	
def play(url,name,iconimage,artist,track_name,album,fanart=''):
	if url=="track_not_found":
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30702))
	else:
		listitem = xbmcgui.ListItem(label=name, iconImage=str(iconimage), thumbnailImage=str(iconimage), path=url)
		listitem.setProperty('IsPlayable', 'true')
		listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'album':album})
		listitem.setProperty('fanart_image', fanart)
		try: xbmc.Player().play(item=url, listitem=listitem)
		except:
			pass
			self.message("Couldn't play item.")

###################################################################################
#XBMC RANDOM FUNCTIONS: OPEN_URl; ADDLINK; ADDDIR, FANART, ETC...

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
		#else:
     	#	return ''

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


def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0')
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
	liz.setInfo(type="Audio", infoLabels={"Title": name})
	liz.setProperty('fanart_image', fanart)
	if 'manualsearch' in locals() and manualsearch==False:
		liz.addContextMenuItems( [(translate(30704), 'RunPlugin(plugin://'+addon_id+'/?mode=26&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')')], replaceItems=True )
	else:
		liz.addContextMenuItems( [(translate(30703), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=16&url=1&search_query='+urllib.quote_plus(str(artist)+' '+str(track_name))+')'),(translate(30704), 'RunPlugin(plugin://'+addon_id+'/?mode=26&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')')], replaceItems=True )
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
	liz.addContextMenuItems([], replaceItems=True)
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
search_query=None
country=None
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
try: search_query=urllib.unquote_plus(params["search_query"])
except: pass
try: country=urllib.unquote_plus(params["country"])
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
if search_query: print "Search Query: "+str(search_query)
if country: print "Country: "+str(country)
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
elif mode==6: List_digster_tracks(url)
# Charts
elif mode==7: Top_charts_menu()
elif mode==8 or mode==9: Itunes_countries_menu(mode)
elif mode==10: Itunes_track_charts(url,country)
elif mode==11: Itunes_album_charts(url,country)
elif mode==12: Itunes_list_album_tracks(url,album,country)
elif mode==13 or mode==14: Billboard_charts(url,mode,playlist_id)
# Search and list content
elif mode==15: Search_main()
elif mode==16: Search_by_tracks(url,search_query)
elif mode==17: Search_by_albums(url,search_query)
elif mode==18: List_album_tracks(url,artist,album)
elif mode==19: Search_by_toptracks(url,search_query)
elif mode==20: Search_by_setlists(url,search_query)
elif mode==21: List_setlist_tracks(url)
elif mode==22: Search_8tracks_playlists(url,search_query)
elif mode==23: List_8tracks_tracks(url,iconimage,playlist_id)
# Downloads and Resolvers
elif mode==24: List_my_songs()
elif mode==25: Resolve_songfile_from_name(artist,track_name,name,iconimage)
elif mode==26: Download_songfile(name,url,artist,track_name)
# Settings
elif mode==27: Open_settings()
# Other Functions
elif mode==100: play(url,name,iconimage,artist,track_name,album,fanart)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
