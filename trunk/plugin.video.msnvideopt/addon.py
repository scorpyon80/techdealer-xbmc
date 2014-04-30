#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 2014 Techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,json
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.msnvideopt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

################################################## 

#MENUS############################################

def MSN_MENU():
	addDir_Page('Informação','<tag namespace="msnvideo_top_cat">mcm_noticias</tag>',1,addonfolder+artfolder+'informacao.jpg',1)
	addDir_Page('Desporto','<tag namespace="msnvideo_top_cat">mcm_desporto</tag>',1,addonfolder+artfolder+'desporto.jpg',1)
	addDir_Page('Cinema','<tag namespace="msnvideo_top_cat">cinefilos_trailers</tag>',1,addonfolder+artfolder+'cinema.jpg',1)
	addDir_Page('Música','<tag namespace="msnvideo_top_cat">musica</tag>',1,addonfolder+artfolder+'musica.jpg',1)
	addDir_Page('Famosos & Lifestyle','<tag namespace="msnvideo_top_cat">mcm_famosos_lifestyle</tag>',1,addonfolder+artfolder+'famosos-life.jpg',1)
	addDir_Page('Humor','<tag namespace="vc_supplier">ptpt_stupid videos</tag>',1,addonfolder+artfolder+'humor.jpg',1)
	addDir_Page('Outros','<tag namespace="msnvideo_top_cat">tecnologia</tag>',1,addonfolder+artfolder+'outros.jpg',1)
	addDir_Page('Tvi','<tag namespace="msnvideo_top_cat">mcm_programas_tvi</tag>',1,addonfolder+artfolder+'tvi.jpg',1)
	xbmc.executebuiltin("Container.SetViewMode(500)")

###################################################################################
#FUNCOES

def Listar_Videos_Msn(url,pagina):
	#info
	#<usageDataType> Played
	#<sortDirection> Ascending | Descending
	#<usageCountType> HourlyChange | HourlyCount | DailyCount | WeeklyCount | MonthlyCount | TotalCount
	#<sortField> Date | Usage
	#<type> Tag | Market
	if pagina==1:
		addDir_Page('[COLOR red][B]+Vistos[/B][/COLOR]',url,2,addonfolder+artfolder+'foldericon.png',1)
	#Menu Informação - subcategorias
	if url=='<tag namespace="msnvideo_top_cat">mcm_noticias</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Economia[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_economia</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Informação[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_informacao</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	elif url=='<tag namespace="msnvideo_top_cat">mcm_economia</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Económico TV[/B][/COLOR]','<tag namespace="msnvideo_top_cat">economicotv</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	#Menu Desporto - subcategorias
	elif url=='<tag namespace="msnvideo_top_cat">mcm_desporto</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Lusa[/B][/COLOR]','<tag namespace="msnvideo_top_cat">lusadesporto</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	#Menu Cinema - subcategorias
	elif url=='<tag namespace="msnvideo_top_cat">cinefilos_trailers</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Animação[/B][/COLOR]','<tag namespace="msnvideo_top_cat">cinefilos_animacao</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Bandas Sonoras[/B][/COLOR]','<tag namespace="vc_source">ptpt_cinefilos:ptpt_cinefilos_bandas sonoras</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Documentários[/B][/COLOR]','<tag namespace="vc_source">ptpt_cinefilos:ptpt_cinefilos_documentários</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Entrevistas[/B][/COLOR]','<tag namespace="vc_source">ptpt_cinefilos:ptpt_cinefilos_entrevistas</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Especiais[/B][/COLOR]','<tag namespace="vc_source">ptpt_cinefilos:ptpt_cinefilos_especiais</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Cinebox[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_cinema</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Hd[/B][/COLOR]','<tag namespace="msnvideo_top_cat">cinefilos_hd</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	#Menu Musica - subcategorias
	elif url=='<tag namespace="msnvideo_top_cat">musica</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Videoclips[/B][/COLOR]','<tag namespace="msnvideo_top_cat">videoclips</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	#Menu Famosos & Lifestyle - subcategorias
	elif url=='<tag namespace="msnvideo_top_cat">mcm_famosos_lifestyle</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Famosos[/B][/COLOR]','<tag namespace="msnvideo_top_cat">famosos</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	#Menu Outros - subcategorias
	elif url=='<tag namespace="msnvideo_top_cat">tecnologia</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Jogos[/B][/COLOR]','<tag namespace="msnvideo_top_cat">jogos</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Publicidade[/B][/COLOR]','<tag namespace="msnvideo_top_cat">publicidade</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	elif url=='<tag namespace="msnvideo_top_cat">jogos</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Xbox[/B][/COLOR]','<tag namespace="msnvideo_top_cat">xbox</tag>',1,'',1)
	#Menu Tvi - subcategorias
	elif url=='<tag namespace="msnvideo_top_cat">mcm_programas_tvi</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Entretenimento[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_entretenimento</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]I Love it[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_iloveit</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Secret Story[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_secretstory</tag>',1,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Tvi 24[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_programas_tvi24</tag>',1,addonfolder+artfolder+'foldericon.png',1)
	elif url=='<tag namespace="msnvideo_top_cat">mcm_entretenimento</tag>' and pagina==1:
		addDir_Page('[COLOR yellow][B]Morangos com Açucar[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_morangos_com_acucar</tag>',1,'',1)
		addDir_Page('[COLOR yellow][B]A Tua Cara não me é estranha[/B][/COLOR]','<tag namespace="msnvideo_top_cat">mcm_atcnmee</tag>',1,'',1)
	codigo_fonte = abrir_url('http://video.pt.msn.com/?rt=ajax&IID=1&dependencies=&currentpage='+str(pagina)+'&activeitemindex=-1&videocontent='+urllib.quote('<videoQuery><videoSort><usageDataType>Played</usageDataType><sortDirection>Descending</sortDirection><usageCountType>HourlyChange</usageCountType><sortField>Date</sortField></videoSort><videoFilter><relatedAlgorithm>0</relatedAlgorithm><tags>'+url+'</tags><format>All</format><dataCatalog>Video</dataCatalog><type>Tag</type><source>Msn</source><safetyFilter>Moderate</safetyFilter></videoFilter></videoQuery>')+'&nospping=false&persistentquerystringparams='+urllib.quote('<dictionary></dictionary>')+'&id=ux1_2_1_4_1_1_1_1_3')
	match = re.compile('<div class="vxp_tooltipTarget">.+?<span class="vxp_anchor">.+?<div class="vxp_gallery_thumb">.+?<a data-insttype="video".+?href="(.+?)" class="vxp_motionThumb vxp_playerUrl".+?title="(.+?)".+?>.+?<img.+?src="(.+?)" />.+?<div class="vxp_extra">.+?<em class="vxp_gallery_date vxp_tb1">(.+?)</em>.+?<em class="vxp_gallery_duration vxp_tb1">(.+?)</em>.+?</div>.+?<div class="vxp_tooltip_data" data-title="(.+?)">.+?</div>',re.MULTILINE|re.DOTALL).findall(codigo_fonte)
	for link, descricao, image, data, duracao, name in match:
		addLink(data.lstrip()+' - '+name+' ('+duracao.lstrip()+')',link,100,h.unescape(image),descricao)
	#verificar se próxima pagina existe
	codigo_fonte = abrir_url('http://video.pt.msn.com/?rt=ajax&IID=1&dependencies=&currentpage='+str(int(pagina)+1)+'&activeitemindex=-1&videocontent='+urllib.quote('<videoQuery><videoSort><usageDataType>Played</usageDataType><sortDirection>Descending</sortDirection><usageCountType>HourlyChange</usageCountType><sortField>Date</sortField></videoSort><videoFilter><relatedAlgorithm>0</relatedAlgorithm><tags>'+url+'</tags><format>All</format><dataCatalog>Video</dataCatalog><type>Tag</type><source>Msn</source><safetyFilter>Moderate</safetyFilter></videoFilter></videoQuery>')+'&nospping=false&persistentquerystringparams='+urllib.quote('<dictionary></dictionary>')+'&id=ux1_2_1_4_1_1_1_1_3')
	match = re.search('<div class="vxp_tooltipTarget">.+?<span class="vxp_anchor">.+?<div class="vxp_gallery_thumb">.+?<a data-insttype="video".+?href="(.+?)" class="vxp_motionThumb vxp_playerUrl".+?title="(.+?)".+?>.+?<img.+?src="(.+?)" />.+?<div class="vxp_extra">.+?<em class="vxp_gallery_date vxp_tb1">(.+?)</em>.+?<em class="vxp_gallery_duration vxp_tb1">(.+?)</em>.+?</div>.+?<div class="vxp_tooltip_data" data-title="(.+?)">.+?</div>',codigo_fonte,re.MULTILINE|re.DOTALL)
	if match != None:
		addDir_Page('[COLOR blue]Página '+str(pagina+1)+' >>[/COLOR]',url,mode,'',pagina+1)
		
def Listar_Mais_Vistos(url,mode,pagina):
	periodo_name = ['Última hora','Dia','Semana','Mês','Sempre']
	periodo_tag = ['HourlyCount','DailyCount','WeeklyCount','MonthlyCount','TotalCount']
	if pagina==1 and mode==2:
		mode = int(xbmcgui.Dialog().select('Escolha um período de tempo:', periodo_name))+1
	periodo_tag = periodo_tag[mode-1]
	codigo_fonte = abrir_url('http://video.pt.msn.com/?rt=ajax&IID=1&dependencies=&currentpage='+str(pagina)+'&activeitemindex=-1&videocontent='+urllib.quote('<videoQuery><videoSort><usageDataType>Played</usageDataType><sortDirection>Descending</sortDirection><usageCountType>'+periodo_tag+'</usageCountType><sortField>Usage</sortField></videoSort><videoFilter><relatedAlgorithm>0</relatedAlgorithm><tags>'+url+'</tags><format>All</format><dataCatalog>Video</dataCatalog><type>Tag</type><source>Msn</source><safetyFilter>Moderate</safetyFilter></videoFilter></videoQuery>')+'&nospping=false&persistentquerystringparams='+urllib.quote('<dictionary></dictionary>')+'&id=ux1_2_1_4_1_1_1_1_3')
	match = re.compile('<div class="vxp_tooltipTarget">.+?<span class="vxp_anchor">.+?<div class="vxp_gallery_thumb">.+?<a data-insttype="video".+?href="(.+?)" class="vxp_motionThumb vxp_playerUrl".+?title="(.+?)".+?>.+?<img.+?src="(.+?)" />.+?<div class="vxp_extra">.+?<em class="vxp_gallery_date vxp_tb1">(.+?)</em>.+?<em class="vxp_gallery_duration vxp_tb1">(.+?)</em>.+?</div>.+?<div class="vxp_tooltip_data" data-title="(.+?)">.+?</div>',re.MULTILINE|re.DOTALL).findall(codigo_fonte)
	for link, descricao, image, data, duracao, name in match:
		addLink(data.lstrip()+' - '+name+' ('+duracao.lstrip()+')',link,100,h.unescape(image),descricao)
	#verificar se próxima pagina existe
	codigo_fonte = abrir_url('http://video.pt.msn.com/?rt=ajax&IID=1&dependencies=&currentpage='+str(int(pagina)+1)+'&activeitemindex=-1&videocontent='+urllib.quote('<videoQuery><videoSort><usageDataType>Played</usageDataType><sortDirection>Descending</sortDirection><usageCountType>'+periodo_tag+'</usageCountType><sortField>Usage</sortField></videoSort><videoFilter><relatedAlgorithm>0</relatedAlgorithm><tags>'+url+'</tags><format>All</format><dataCatalog>Video</dataCatalog><type>Tag</type><source>Msn</source><safetyFilter>Moderate</safetyFilter></videoFilter></videoQuery>')+'&nospping=false&persistentquerystringparams='+urllib.quote('<dictionary></dictionary>')+'&id=ux1_2_1_4_1_1_1_1_3')
	match = re.search('<div class="vxp_tooltipTarget">.+?<span class="vxp_anchor">.+?<div class="vxp_gallery_thumb">.+?<a data-insttype="video".+?href="(.+?)" class="vxp_motionThumb vxp_playerUrl".+?title="(.+?)".+?>.+?<img.+?src="(.+?)" />.+?<div class="vxp_extra">.+?<em class="vxp_gallery_date vxp_tb1">(.+?)</em>.+?<em class="vxp_gallery_duration vxp_tb1">(.+?)</em>.+?</div>.+?<div class="vxp_tooltip_data" data-title="(.+?)">.+?</div>',codigo_fonte,re.MULTILINE|re.DOTALL)
	if match != None:
		addDir_Page('[COLOR blue]Página '+str(pagina+1)+' >>[/COLOR]',url,mode,'',pagina+1)
		
def Resolver_url_msn(url,name,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Msn Vídeo Portugal', 'Procurando fonte...')
	progress.update(0)
	if progress.iscanceled():
		sys.exit(0)
	msn_opcao_nome = []
	msn_opcao_url = []
	source_code = abrir_url(url)
	progress.update(50)
	if progress.iscanceled():
		sys.exit(0)
	match = re.compile("{formatCode: ([\d]+), url: '(.+?)', width: ([\d]+), height: ([\d]+), bitrate: ([\d]+)}").findall(source_code)
	if match != None:
		for formatcode, link, width, height, bitrate in match:
			msn_opcao_nome.append('Código: '+formatcode+', Largura: '+width+', Altura: '+height+', Bitrate: '+bitrate)
			msn_opcao_url.append(link.decode('string_escape'))
	else:
		progress.close()
		sys.exit(0)
	progress.update(100)
	progress.close()
	if msn_opcao_nome and msn_opcao_url:
		video_id = xbmcgui.Dialog().select('Escolha uma opção:', msn_opcao_nome)
		if video_id != -1:
			play(msn_opcao_url[video_id],name,iconimage)
	
def play(url,name,iconimage):
	listitem = xbmcgui.ListItem(label=name, iconImage=str(iconimage), thumbnailImage=str(iconimage), path=url)
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmc.Player().play(item=url, listitem=listitem)
	except:
		pass
		self.message("Couldn't play item.")

###################################################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,mode,iconimage,desc=None):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok
	
def addDir_Page(name,url,mode,iconimage,pagina,folder=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&pagina="+str(pagina)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addDir(name,url,mode,iconimage,folder=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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
pagina=None


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
try:
        pagina=int(params["pagina"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Pagina: "+str(pagina)


###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################


if mode==None: MSN_MENU()
elif mode==1: Listar_Videos_Msn(url,pagina)
elif mode>=2 and mode<=6: Listar_Mais_Vistos(url,mode,pagina)
elif mode==100: Resolver_url_msn(url,name,iconimage)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
