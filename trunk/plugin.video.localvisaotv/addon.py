#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 2014 Techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
import json
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.localvisaotv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

localvisao_url = 'http://www.localvisao.tv/'

################################################## 

#MENUS############################################
	
def LOCALVISAO():
	addDir('Arquivo','?arquivo_modo=1&pagina=1',2,addonfolder+artfolder+'arquivo.jpg')
	addDir('Trás-os-montes','index.php/tras-os-montes?pagina=1',1,addonfolder+artfolder+'tras-os-montes.jpg')
	addDir('Porto e Minho','index.php/porto-e-minho?pagina=1',1,addonfolder+artfolder+'porto-e-minho.jpg')
	addDir('Beira Interior','index.php/beira-interior?pagina=1',1,addonfolder+artfolder+'beira-interior.jpg')
	addDir('Beira Litoral','index.php/beira-litoral?pagina=1',1,addonfolder+artfolder+'beira-litoral.jpg')
	addDir('Lisboa e Vale do Tejo','index.php/lisboa-e-vale-do-tejo?pagina=1',1,addonfolder+artfolder+'lisboa-vale-tejo.jpg')
	addDir('Alentejo','index.php/alentejo?pagina=1',1,addonfolder+artfolder+'alentejo.jpg')
	addDir('Algarve','index.php/algarve?pagina=1',1,addonfolder+artfolder+'algarve.jpg')
	addDir('Desporto','index.php/desporto?pagina=1',1,addonfolder+artfolder+'desporto.jpg')
	addDir('Mundo Académico','index.php/mundo-academico?pagina=1',1,addonfolder+artfolder+'mundo-academico.jpg')
	addDir('Definições','',3,addonfolder+artfolder+'definicoes.jpg',False)

###################################################################################
#FUNCOES

def Listar_Localvisao(url):
	videos_per_page = int(selfAddon.getSetting('vid_per_page'))
	pagina = re.search('^(.+?)\?pagina=([\d]+?)$', url).group(2)
	url = re.search('^(.+?)\?pagina=([\d]+?)$', url).group(1)
	total_videos = json.loads(abrir_url('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed WHERE url="' + localvisao_url + url + '?format=feed&type=rss' + '"') + '&format=json&diagnostics=true&callback='))['query']['count']
	codigo_fonte = abrir_url('http://pipes.yahoo.com/pipes/pipe.run?_id=e1b35882a575486995d9dd51a01fd243&_render=json&yql_query=' + urllib.quote_plus('SELECT * FROM feed(' + str(int(pagina)*videos_per_page-videos_per_page+1) + ',' + str(videos_per_page) + ') WHERE url="' + localvisao_url + url + '?format=feed&type=rss' + '"'))
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, decoded_data['count']):
		data = decoded_data['value']['items'][x]['pubDate'].encode("utf8")
		name = decoded_data['value']['items'][x]['title'].encode("utf8")
		link = decoded_data['value']['items'][x]['link'].encode("utf8")
		descricao = decoded_data['value']['items'][x]['description'].encode("utf8")
		iconimage = decoded_data['value']['items'][x]['thumbnail'].encode("utf8")
		addLink('[COLOR yellow]'+data[:-5] + '[/COLOR] - ' + name,link,100,iconimage,cleanhtml(descricao))
	if int(total_videos)-(int(pagina)*videos_per_page)>0:
		addDir('Próximo >>',url+'?pagina='+str(int(pagina)+1),mode,'')
	
def Listar_Arquivo(url):
	videos_per_page = int(selfAddon.getSetting('vid_per_page'))
	arquivo_modo = re.search('^\?arquivo_modo=([\d]+)&pagina=([\d]+)', url).group(1)
	pagina = re.search('^\?arquivo_modo=([\d]+)&pagina=([\d]+)', url).group(2)
	#listar os últimos videos do arquivo
	if int(arquivo_modo) == 1:
		if int(pagina)==1:
			addDir('[B]Pesquisar[/B]','?arquivo_modo=2&pagina=1',2,addonfolder+artfolder+'pesquisar.jpg')
			if selfAddon.getSetting('disp_vid_p_conc') == 'true':
				addDir('[B]Vídeos por Concelho[/B]','?arquivo_modo=3&pagina=1',2,addonfolder+artfolder+'mapas.jpg')
		codigo_fonte = abrir_url('https://services.sapo.pt/videos/JSON2/User/localvisao?page=' + pagina + '&limit=' + str(videos_per_page))
		decoded_data = json.loads(codigo_fonte)
		total_videos = decoded_data['rss']['channel']['opensearch:totalResults'].encode("utf8")
		if int(total_videos)>0:
			if int(total_videos)==1 or int(total_videos)-int(decoded_data['rss']['channel']['opensearch:startIndex'].encode("utf8"))==1:
				data = decoded_data['rss']['channel']['item']['pubDate'].encode("utf8")
				name = decoded_data['rss']['channel']['item']['title'].encode("utf8")
				link = decoded_data['rss']['channel']['item']['sapo:videoURL'].encode("utf8")
				descricao = decoded_data['rss']['channel']['item']['sapo:synopse'].encode("utf8")
				iconimage = decoded_data['rss']['channel']['item']['media:content']['url'].encode("utf8")
				addLink('[COLOR yellow]'+data[:-5] + '[/COLOR] - ' + name,link,101,iconimage,cleanhtml(descricao))
			else:
				for x in range(0, len(decoded_data['rss']['channel']['item'])):
					data = decoded_data['rss']['channel']['item'][x]['pubDate'].encode("utf8")
					name = decoded_data['rss']['channel']['item'][x]['title'].encode("utf8")
					link = decoded_data['rss']['channel']['item'][x]['sapo:videoURL'].encode("utf8")
					descricao = decoded_data['rss']['channel']['item'][x]['sapo:synopse'].encode("utf8")
					iconimage = decoded_data['rss']['channel']['item'][x]['media:content']['url'].encode("utf8")
					addLink('[COLOR yellow]'+data[:-5] + '[/COLOR] - ' + name,link,101,iconimage,cleanhtml(descricao))
			if int(total_videos)-(int(pagina)*videos_per_page)>0:
				addDir('Próximo >>','?arquivo_modo=' + arquivo_modo + '&pagina=' + str(int(pagina)+1),mode,'')
	#pesquisar no arquivo...
	if int(arquivo_modo) == 2:
		addDir('[B]Pesquisar novamente...[/B]','?arquivo_modo=2&pagina=1',2,addonfolder+artfolder+'pesquisar.jpg')
		if int(pagina)==1:
			keyb = xbmc.Keyboard('', 'Pesquisar por...')
			keyb.doModal()
			if (keyb.isConfirmed()):
				search = keyb.getText()
				if search=='': sys.exit(0)
				search=urllib.quote(search)
			addDir('[B]Ver Últimos Vídeos[/B]','?arquivo_modo=1&pagina=1',2,addonfolder+artfolder+'ultimos-videos.jpg')
			if selfAddon.getSetting('disp_vid_p_conc') == 'true':
				addDir('[B]Vídeos por Concelho[/B]','?arquivo_modo=3&pagina=1',2,addonfolder+artfolder+'mapas.jpg')
		else:
			search = re.search('&search=(.+)$', url).group(1)
		codigo_fonte = abrir_url('https://services.sapo.pt/videos/JSON2/Query?user=localvisao&search=' + search + '&page=' + pagina + '&limit=' + str(videos_per_page))
		decoded_data = json.loads(codigo_fonte)
		total_videos = decoded_data['rss']['channel']['opensearch:totalResults'].encode("utf8")
		if int(total_videos)>0:
			if int(total_videos)==1 or int(total_videos)-int(decoded_data['rss']['channel']['opensearch:startIndex'].encode("utf8"))==1:
				data = decoded_data['rss']['channel']['item']['pubDate'].encode("utf8")
				name = decoded_data['rss']['channel']['item']['title'].encode("utf8")
				link = decoded_data['rss']['channel']['item']['sapo:videoURL'].encode("utf8")
				descricao = decoded_data['rss']['channel']['item']['sapo:synopse'].encode("utf8")
				iconimage = decoded_data['rss']['channel']['item']['media:content']['url'].encode("utf8")
				addLink('[COLOR yellow]'+data[:-5] + '[/COLOR] - ' + name,link,101,iconimage,cleanhtml(descricao))
			else:
				for x in range(0, len(decoded_data['rss']['channel']['item'])):
					data = decoded_data['rss']['channel']['item'][x]['pubDate'].encode("utf8")
					name = decoded_data['rss']['channel']['item'][x]['title'].encode("utf8")
					link = decoded_data['rss']['channel']['item'][x]['sapo:videoURL'].encode("utf8")
					descricao = decoded_data['rss']['channel']['item'][x]['sapo:synopse'].encode("utf8")
					iconimage = decoded_data['rss']['channel']['item'][x]['media:content']['url'].encode("utf8")
					addLink('[COLOR yellow]'+data[:-5] + '[/COLOR] - ' + name,link,101,iconimage,cleanhtml(descricao))
			if int(total_videos)-(int(pagina)*videos_per_page)>0:
				addDir('Próximo >>','?arquivo_modo=' + arquivo_modo + '&pagina=' + str(int(pagina)+1) + '&search=' + search,mode,'')
	#mostrar conteúdo por concelho
	if int(arquivo_modo) == 3:
		distrito = re.search('&distrito=(.+)&.+?', url)
		if distrito != None:
			distrito = distrito.group(1)
		else:
			distrito = None
		playview = re.search('&playview=(.+)$', url)
		if playview != None:
			playview = playview.group(1)
		else:
			playview = None
		if distrito == None:
			addDir('[I]Escolha o distrito abaixo:[/I]','?arquivo_modo=3&pagina=1',2,'')
			addDir('Aveiro','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=',2,'')
			addDir('Beja','?arquivo_modo=3&pagina=1&distrito=beja&playview=',2,'')
			addDir('Braga','?arquivo_modo=3&pagina=1&distrito=braga&playview=',2,'')
			addDir('Bragança','?arquivo_modo=3&pagina=1&distrito=braganca&playview=',2,'')
			addDir('Castelo Branco','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=',2,'')
			addDir('Coimbra','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=',2,'')
			addDir('Évora','?arquivo_modo=3&pagina=1&distrito=evora&playview=',2,'')
			addDir('Faro','?arquivo_modo=3&pagina=1&distrito=faro&playview=',2,'')
			addDir('Guarda','?arquivo_modo=3&pagina=1&distrito=guarda&playview=',2,'')
			addDir('Leiria','?arquivo_modo=3&pagina=1&distrito=leiria&playview=',2,'')
			addDir('Lisboa','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=',2,'')
			addDir('Portalegre','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=',2,'')
			addDir('Porto','?arquivo_modo=3&pagina=1&distrito=porto&playview=',2,'')
			addDir('Santarém','?arquivo_modo=3&pagina=1&distrito=santarem&playview=',2,'')
			addDir('Setúbal','?arquivo_modo=3&pagina=1&distrito=setubal&playview=',2,'')
			addDir('Viana do Castelo','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=',2,'')
			addDir('Vila Real','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=',2,'')
			addDir('Viseu','?arquivo_modo=3&pagina=1&distrito=viseu&playview=',2,'')
			addDir('Açores','?arquivo_modo=3&pagina=1&distrito=acores&playview=',2,'')
			addDir('Madeira','?arquivo_modo=3&pagina=1&distrito=madeira&playview=',2,'')
		elif distrito != None and playview == None:
			if distrito == 'aveiro':
				addDir('Águeda','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=2',2,'')
				addDir('Albergaria-a-Velha','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=3',2,'')
				addDir('Anadia','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=4',2,'')
				addDir('Arouca','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=5',2,'')
				addDir('Aveiro','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=6',2,'')
				addDir('Castelo de Paiva','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=7',2,'')
				addDir('Espinho','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=8',2,'')
				addDir('Estarreja','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=9',2,'')
				addDir('Ílhavo','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=11',2,'')
				addDir('Mealhada','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=12',2,'')
				addDir('Murtosa','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=13',2,'')
				addDir('Oliveira de Azeméis','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=14',2,'')
				addDir('Oliveira do Bairro','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=15',2,'')
				addDir('Ovar','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=16',2,'')
				addDir('Santa Maria da Feira','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=10',2,'')
				addDir('São João da Madeira','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=17',2,'')
				addDir('Sever do Vouga','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=18',2,'')
				addDir('Vagos','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=19',2,'')
				addDir('Vale de Cambra','?arquivo_modo=3&pagina=1&distrito=aveiro&playview=20',2,'')
			elif distrito == 'beja':
				addDir('Aljustrel','?arquivo_modo=3&pagina=1&distrito=beja&playview=21',2,'')
				addDir('Almodovar','?arquivo_modo=3&pagina=1&distrito=beja&playview=22',2,'')
				addDir('Alvito','?arquivo_modo=3&pagina=1&distrito=beja&playview=23',2,'')
				addDir('Barrancos','?arquivo_modo=3&pagina=1&distrito=beja&playview=24',2,'')
				addDir('Beja','?arquivo_modo=3&pagina=1&distrito=beja&playview=25',2,'')
				addDir('Castro Verde','?arquivo_modo=3&pagina=1&distrito=beja&playview=26',2,'')
				addDir('Cuba','?arquivo_modo=3&pagina=1&distrito=beja&playview=27',2,'')
				addDir('Ferreira do Alentejo','?arquivo_modo=3&pagina=1&distrito=beja&playview=28',2,'')
				addDir('Mértola','?arquivo_modo=3&pagina=1&distrito=beja&playview=29',2,'')
				addDir('Moura','?arquivo_modo=3&pagina=1&distrito=beja&playview=30',2,'')
				addDir('Odemira','?arquivo_modo=3&pagina=1&distrito=beja&playview=31',2,'')
				addDir('Ourique','?arquivo_modo=3&pagina=1&distrito=beja&playview=32',2,'')
				addDir('Serpa','?arquivo_modo=3&pagina=1&distrito=beja&playview=33',2,'')
				addDir('Vidigueira','?arquivo_modo=3&pagina=1&distrito=beja&playview=34',2,'')
			elif distrito == 'braga':
				addDir('Amares','?arquivo_modo=3&pagina=1&distrito=braga&playview=35',2,'')
				addDir('Barcelos','?arquivo_modo=3&pagina=1&distrito=braga&playview=36',2,'')
				addDir('Braga','?arquivo_modo=3&pagina=1&distrito=braga&playview=37',2,'')
				addDir('Cabeceiras de Basto','?arquivo_modo=3&pagina=1&distrito=braga&playview=38',2,'')
				addDir('Celorico de Basto','?arquivo_modo=3&pagina=1&distrito=braga&playview=39',2,'')
				addDir('Esposende','?arquivo_modo=3&pagina=1&distrito=braga&playview=40',2,'')
				addDir('Fafe','?arquivo_modo=3&pagina=1&distrito=braga&playview=41',2,'')
				addDir('Guimarães','?arquivo_modo=3&pagina=1&distrito=braga&playview=42',2,'')
				addDir('Póvoa de Lanhoso','?arquivo_modo=3&pagina=1&distrito=braga&playview=43',2,'')
				addDir('Terras de Bouro','?arquivo_modo=3&pagina=1&distrito=braga&playview=44',2,'')
				addDir('Vieira do Minho','?arquivo_modo=3&pagina=1&distrito=braga&playview=45',2,'')
				addDir('Vila Nova de Famalicão','?arquivo_modo=3&pagina=1&distrito=braga&playview=46',2,'')
				addDir('Vila Verde','?arquivo_modo=3&pagina=1&distrito=braga&playview=47',2,'')
				addDir('Vizela','?arquivo_modo=3&pagina=1&distrito=braga&playview=48',2,'')
			elif distrito == 'braganca':
				addDir('Alfândega da Fé','?arquivo_modo=3&pagina=1&distrito=braganca&playview=49',2,'')
				addDir('Bragança','?arquivo_modo=3&pagina=1&distrito=braganca&playview=50',2,'')
				addDir('Carrazeda de Ansiães','?arquivo_modo=3&pagina=1&distrito=braganca&playview=51',2,'')
				addDir('Freixo de Espada à Cinta','?arquivo_modo=3&pagina=1&distrito=braganca&playview=52',2,'')
				addDir('Macedo de Cavaleiros','?arquivo_modo=3&pagina=1&distrito=braganca&playview=53',2,'')
				addDir('Miranda do Douro','?arquivo_modo=3&pagina=1&distrito=braganca&playview=54',2,'')
				addDir('Mirandela','?arquivo_modo=3&pagina=1&distrito=braganca&playview=55',2,'')
				addDir('Mogadouro','?arquivo_modo=3&pagina=1&distrito=braganca&playview=56',2,'')
				addDir('Moncorvo','?arquivo_modo=3&pagina=1&distrito=braganca&playview=57',2,'')
				addDir('Vila Flor','?arquivo_modo=3&pagina=1&distrito=braganca&playview=58',2,'')
				addDir('Vimioso','?arquivo_modo=3&pagina=1&distrito=braganca&playview=59',2,'')
				addDir('Vinhais','?arquivo_modo=3&pagina=1&distrito=braganca&playview=60',2,'')
			elif distrito == 'castelobranco':
				addDir('Belmonte','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=61',2,'')
				addDir('Castelo Branco','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=62',2,'')
				addDir('Covilhã','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=63',2,'')
				addDir('Fundão','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=64',2,'')
				addDir('Idanha-a-Nova','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=65',2,'')
				addDir('Oleiros','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=66',2,'')
				addDir('Penamacôr','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=67',2,'')
				addDir('Proença-a-Nova','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=68',2,'')
				addDir('Sertã','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=69',2,'')
				addDir('Vila de Rei','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=70',2,'')
				addDir('Vila Velha de Ródão','?arquivo_modo=3&pagina=1&distrito=castelobranco&playview=71',2,'')
			elif distrito == 'coimbra':
				addDir('Arganil','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=72',2,'')
				addDir('Cantanhede','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=73',2,'')
				addDir('Coimbra','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=74',2,'')
				addDir('Condeixa-a-Nova','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=75',2,'')
				addDir('Figueira da Foz','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=76',2,'')
				addDir('Góis','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=77',2,'')
				addDir('Lousã','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=78',2,'')
				addDir('Mira','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=79',2,'')
				addDir('Miranda do Corvo','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=80',2,'')
				addDir('Montemor-o-Velho','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=81',2,'')
				addDir('Oliveira do Hospital','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=82',2,'')
				addDir('Pampilhosa da Serra','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=83',2,'')
				addDir('Penacova','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=84',2,'')
				addDir('Penela','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=85',2,'')
				addDir('Soure','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=86',2,'')
				addDir('Tábua','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=87',2,'')
				addDir('Vila Nova de Poiares','?arquivo_modo=3&pagina=1&distrito=coimbra&playview=88',2,'')
			elif distrito == 'evora':
				addDir('Alandroal','?arquivo_modo=3&pagina=1&distrito=evora&playview=89',2,'')
				addDir('Arraiolos','?arquivo_modo=3&pagina=1&distrito=evora&playview=90',2,'')
				addDir('Borba','?arquivo_modo=3&pagina=1&distrito=evora&playview=91',2,'')
				addDir('Estremoz','?arquivo_modo=3&pagina=1&distrito=evora&playview=92',2,'')
				addDir('Évora','?arquivo_modo=3&pagina=1&distrito=evora&playview=93',2,'')
				addDir('Montemor-o-Novo','?arquivo_modo=3&pagina=1&distrito=evora&playview=94',2,'')
				addDir('Mora','?arquivo_modo=3&pagina=1&distrito=evora&playview=95',2,'')
				addDir('Mourão','?arquivo_modo=3&pagina=1&distrito=evora&playview=96',2,'')
				addDir('Portel','?arquivo_modo=3&pagina=1&distrito=evora&playview=97',2,'')
				addDir('Redondo','?arquivo_modo=3&pagina=1&distrito=evora&playview=98',2,'')
				addDir('Reguengos de Monsaraz','?arquivo_modo=3&pagina=1&distrito=evora&playview=99',2,'')
				addDir('Vendas Novas','?arquivo_modo=3&pagina=1&distrito=evora&playview=100',2,'')
				addDir('Viana do Alentejo','?arquivo_modo=3&pagina=1&distrito=evora&playview=101',2,'')
				addDir('Vila Viçosa','?arquivo_modo=3&pagina=1&distrito=evora&playview=102',2,'')
			elif distrito == 'faro':
				addDir('Albufeira','?arquivo_modo=3&pagina=1&distrito=faro&playview=103',2,'')
				addDir('Alcoutim','?arquivo_modo=3&pagina=1&distrito=faro&playview=104',2,'')
				addDir('Aljezur','?arquivo_modo=3&pagina=1&distrito=faro&playview=105',2,'')
				addDir('Castro Marim','?arquivo_modo=3&pagina=1&distrito=faro&playview=106',2,'')
				addDir('Faro','?arquivo_modo=3&pagina=1&distrito=faro&playview=107',2,'')
				addDir('Lagoa (Algarve)','?arquivo_modo=3&pagina=1&distrito=faro&playview=108',2,'')
				addDir('Lagos','?arquivo_modo=3&pagina=1&distrito=faro&playview=109',2,'')
				addDir('Loulé','?arquivo_modo=3&pagina=1&distrito=faro&playview=110',2,'')
				addDir('Monchique','?arquivo_modo=3&pagina=1&distrito=faro&playview=111',2,'')
				addDir('Olhão','?arquivo_modo=3&pagina=1&distrito=faro&playview=112',2,'')
				addDir('Portimão','?arquivo_modo=3&pagina=1&distrito=faro&playview=113',2,'')
				addDir('São Brás de Alportel','?arquivo_modo=3&pagina=1&distrito=faro&playview=114',2,'')
				addDir('Silves','?arquivo_modo=3&pagina=1&distrito=faro&playview=115',2,'')
				addDir('Tavira','?arquivo_modo=3&pagina=1&distrito=faro&playview=116',2,'')
				addDir('Vila do Bispo','?arquivo_modo=3&pagina=1&distrito=faro&playview=117',2,'')
				addDir('Vila Real de Santo António','?arquivo_modo=3&pagina=1&distrito=faro&playview=118',2,'')
			elif distrito == 'guarda':
				addDir('Aguiar da Beira','?arquivo_modo=3&pagina=1&distrito=guarda&playview=119',2,'')
				addDir('Almeida','?arquivo_modo=3&pagina=1&distrito=guarda&playview=120',2,'')
				addDir('Celorico da Beira','?arquivo_modo=3&pagina=1&distrito=guarda&playview=121',2,'')
				addDir('Figueira de Castelo Rodrigo','?arquivo_modo=3&pagina=1&distrito=guarda&playview=122',2,'')
				addDir('Fornos de Algodres','?arquivo_modo=3&pagina=1&distrito=guarda&playview=123',2,'')
				addDir('Gouveia','?arquivo_modo=3&pagina=1&distrito=guarda&playview=124',2,'')
				addDir('Guarda','?arquivo_modo=3&pagina=1&distrito=guarda&playview=125',2,'')
				addDir('Manteigas','?arquivo_modo=3&pagina=1&distrito=guarda&playview=126',2,'')
				addDir('Mêda','?arquivo_modo=3&pagina=1&distrito=guarda&playview=127',2,'')
				addDir('Pinhel','?arquivo_modo=3&pagina=1&distrito=guarda&playview=128',2,'')
				addDir('Sabugal','?arquivo_modo=3&pagina=1&distrito=guarda&playview=129',2,'')
				addDir('Seia','?arquivo_modo=3&pagina=1&distrito=guarda&playview=130',2,'')
				addDir('Trancoso','?arquivo_modo=3&pagina=1&distrito=guarda&playview=131',2,'')
				addDir('Vila Nova de Foz Côa','?arquivo_modo=3&pagina=1&distrito=guarda&playview=132',2,'')
			elif distrito == 'leiria':
				addDir('Alcobaça','?arquivo_modo=3&pagina=1&distrito=leiria&playview=133',2,'')
				addDir('Alvaiázere','?arquivo_modo=3&pagina=1&distrito=leiria&playview=134',2,'')
				addDir('Ansião','?arquivo_modo=3&pagina=1&distrito=leiria&playview=135',2,'')
				addDir('Batalha','?arquivo_modo=3&pagina=1&distrito=leiria&playview=136',2,'')
				addDir('Bombarral','?arquivo_modo=3&pagina=1&distrito=leiria&playview=137',2,'')
				addDir('Caldas da Rainha','?arquivo_modo=3&pagina=1&distrito=leiria&playview=138',2,'')
				addDir('Castanheira de Pêra','?arquivo_modo=3&pagina=1&distrito=leiria&playview=139',2,'')
				addDir('Figueiró dos Vinhos','?arquivo_modo=3&pagina=1&distrito=leiria&playview=140',2,'')
				addDir('Leiria','?arquivo_modo=3&pagina=1&distrito=leiria&playview=141',2,'')
				addDir('Marinha Grande','?arquivo_modo=3&pagina=1&distrito=leiria&playview=142',2,'')
				addDir('Nazaré','?arquivo_modo=3&pagina=1&distrito=leiria&playview=143',2,'')
				addDir('Óbidos','?arquivo_modo=3&pagina=1&distrito=leiria&playview=144',2,'')
				addDir('Pedrogão Grande','?arquivo_modo=3&pagina=1&distrito=leiria&playview=145',2,'')
				addDir('Peniche','?arquivo_modo=3&pagina=1&distrito=leiria&playview=146',2,'')
				addDir('Pombal','?arquivo_modo=3&pagina=1&distrito=leiria&playview=147',2,'')
				addDir('Porto de Mós','?arquivo_modo=3&pagina=1&distrito=leiria&playview=148',2,'')
			elif distrito == 'lisboa':
				addDir('Alenquer','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=149',2,'')
				addDir('Arruda dos Vinhos','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=150',2,'')
				addDir('Azambuja','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=151',2,'')
				addDir('Cadaval','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=152',2,'')
				addDir('Cascais','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=153',2,'')
				addDir('Lisboa','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=154',2,'')
				addDir('Loures','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=155',2,'')
				addDir('Lourinhã','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=156',2,'')
				addDir('Mafra','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=157',2,'')
				addDir('Oeiras','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=158',2,'')
				addDir('Sintra','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=159',2,'')
				addDir('Sobral de Monte Agraço','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=160',2,'')
				addDir('Torres Vedras','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=161',2,'')
				addDir('Vila Franca de Xira','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=162',2,'')
				addDir('Amadora','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=163',2,'')
				addDir('Odivelas','?arquivo_modo=3&pagina=1&distrito=lisboa&playview=164',2,'')
			elif distrito == 'portalegre':
				addDir('Alter do Chão','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=165',2,'')
				addDir('Arronches','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=166',2,'')
				addDir('Avis','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=167',2,'')
				addDir('Campo Maior','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=168',2,'')
				addDir('Castelo de Vide','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=169',2,'')
				addDir('Crato','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=170',2,'')
				addDir('Elvas','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=171',2,'')
				addDir('Fronteira','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=172',2,'')
				addDir('Gavião','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=173',2,'')
				addDir('Marvão','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=174',2,'')
				addDir('Monforte','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=175',2,'')
				addDir('Nisa','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=176',2,'')
				addDir('Ponte de Sôr','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=177',2,'')
				addDir('Portalegre','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=178',2,'')
				addDir('Sousel','?arquivo_modo=3&pagina=1&distrito=portalegre&playview=179',2,'')
			elif distrito == 'porto':
				addDir('Amarante','?arquivo_modo=3&pagina=1&distrito=porto&playview=180',2,'')
				addDir('Baião','?arquivo_modo=3&pagina=1&distrito=porto&playview=181',2,'')
				addDir('Felgueiras','?arquivo_modo=3&pagina=1&distrito=porto&playview=182',2,'')
				addDir('Gondomar','?arquivo_modo=3&pagina=1&distrito=porto&playview=183',2,'')
				addDir('Lousada','?arquivo_modo=3&pagina=1&distrito=porto&playview=184',2,'')
				addDir('Maia','?arquivo_modo=3&pagina=1&distrito=porto&playview=185',2,'')
				addDir('Marco de Canaveses','?arquivo_modo=3&pagina=1&distrito=porto&playview=186',2,'')
				addDir('Matosinhos','?arquivo_modo=3&pagina=1&distrito=porto&playview=187',2,'')
				addDir('Paços de Ferreira','?arquivo_modo=3&pagina=1&distrito=porto&playview=188',2,'')
				addDir('Paredes','?arquivo_modo=3&pagina=1&distrito=porto&playview=189',2,'')
				addDir('Penafiel','?arquivo_modo=3&pagina=1&distrito=porto&playview=190',2,'')
				addDir('Porto','?arquivo_modo=3&pagina=1&distrito=porto&playview=191',2,'')
				addDir('Póvoa de Varzim','?arquivo_modo=3&pagina=1&distrito=porto&playview=192',2,'')
				addDir('Santo Tirso','?arquivo_modo=3&pagina=1&distrito=porto&playview=193',2,'')
				addDir('Trofa','?arquivo_modo=3&pagina=1&distrito=porto&playview=197',2,'')
				addDir('Valongo','?arquivo_modo=3&pagina=1&distrito=porto&playview=194',2,'')
				addDir('Vila do Conde','?arquivo_modo=3&pagina=1&distrito=porto&playview=195',2,'')
				addDir('Vila Nova de Gaia','?arquivo_modo=3&pagina=1&distrito=porto&playview=196',2,'')
			elif distrito == 'santarem':
				addDir('Abrantes','?arquivo_modo=3&pagina=1&distrito=santarem&playview=198',2,'')
				addDir('Alcanena','?arquivo_modo=3&pagina=1&distrito=santarem&playview=199',2,'')
				addDir('Almeirim','?arquivo_modo=3&pagina=1&distrito=santarem&playview=200',2,'')
				addDir('Alpiarça','?arquivo_modo=3&pagina=1&distrito=santarem&playview=201',2,'')
				addDir('Benavente','?arquivo_modo=3&pagina=1&distrito=santarem&playview=202',2,'')
				addDir('Cartaxo','?arquivo_modo=3&pagina=1&distrito=santarem&playview=203',2,'')
				addDir('Chamusca','?arquivo_modo=3&pagina=1&distrito=santarem&playview=204',2,'')
				addDir('Constância','?arquivo_modo=3&pagina=1&distrito=santarem&playview=205',2,'')
				addDir('Coruche','?arquivo_modo=3&pagina=1&distrito=santarem&playview=206',2,'')
				addDir('Entrocamento','?arquivo_modo=3&pagina=1&distrito=santarem&playview=207',2,'')
				addDir('Ferreira do Zêzere','?arquivo_modo=3&pagina=1&distrito=santarem&playview=208',2,'')
				addDir('Golegã','?arquivo_modo=3&pagina=1&distrito=santarem&playview=209',2,'')
				addDir('Mação','?arquivo_modo=3&pagina=1&distrito=santarem&playview=210',2,'')
				addDir('Rio Maior','?arquivo_modo=3&pagina=1&distrito=santarem&playview=211',2,'')
				addDir('Salvaterra de Magos','?arquivo_modo=3&pagina=1&distrito=santarem&playview=212',2,'')
				addDir('Santarém','?arquivo_modo=3&pagina=1&distrito=santarem&playview=213',2,'')
				addDir('Sardoal','?arquivo_modo=3&pagina=1&distrito=santarem&playview=214',2,'')
				addDir('Tomar','?arquivo_modo=3&pagina=1&distrito=santarem&playview=215',2,'')
				addDir('Torres Novas','?arquivo_modo=3&pagina=1&distrito=santarem&playview=216',2,'')
				addDir('Vila Nova da Barquinha','?arquivo_modo=3&pagina=1&distrito=santarem&playview=217',2,'')
				addDir('Vila Nova de Ourém','?arquivo_modo=3&pagina=1&distrito=santarem&playview=218',2,'')
			elif distrito == 'setubal':
				addDir('Alcácer do Sal','?arquivo_modo=3&pagina=1&distrito=setubal&playview=219',2,'')
				addDir('Alcochete','?arquivo_modo=3&pagina=1&distrito=setubal&playview=220',2,'')
				addDir('Almada','?arquivo_modo=3&pagina=1&distrito=setubal&playview=221',2,'')
				addDir('Barreiro','?arquivo_modo=3&pagina=1&distrito=setubal&playview=222',2,'')
				addDir('Grândola','?arquivo_modo=3&pagina=1&distrito=setubal&playview=223',2,'')
				addDir('Moita','?arquivo_modo=3&pagina=1&distrito=setubal&playview=224',2,'')
				addDir('Montijo','?arquivo_modo=3&pagina=1&distrito=setubal&playview=225',2,'')
				addDir('Palmela','?arquivo_modo=3&pagina=1&distrito=setubal&playview=226',2,'')
				addDir('Santiago do Cacém','?arquivo_modo=3&pagina=1&distrito=setubal&playview=227',2,'')
				addDir('Seixal','?arquivo_modo=3&pagina=1&distrito=setubal&playview=228',2,'')
				addDir('Sesimbra','?arquivo_modo=3&pagina=1&distrito=setubal&playview=229',2,'')
				addDir('Setúbal','?arquivo_modo=3&pagina=1&distrito=setubal&playview=230',2,'')
				addDir('Sines','?arquivo_modo=3&pagina=1&distrito=setubal&playview=231',2,'')
			elif distrito == 'vianadocastelo':
				addDir('Arcos de Valdevez','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=232',2,'')
				addDir('Caminha','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=233',2,'')
				addDir('Melgaço','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=234',2,'')
				addDir('Monção','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=235',2,'')
				addDir('Paredes de Coura','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=236',2,'')
				addDir('Ponte da Barca','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=237',2,'')
				addDir('Ponte de Lima','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=238',2,'')
				addDir('Valença','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=239',2,'')
				addDir('Viana do Castelo','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=240',2,'')
				addDir('Vila Nova de Cerveira','?arquivo_modo=3&pagina=1&distrito=vianadocastelo&playview=241',2,'')
			elif distrito == 'vilareal':
				addDir('Alijó','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=242',2,'')
				addDir('Boticas','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=243',2,'')
				addDir('Chaves','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=244',2,'')
				addDir('Mesão Frio','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=245',2,'')
				addDir('Mondim de Basto','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=246',2,'')
				addDir('Montalegre','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=247',2,'')
				addDir('Murça','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=248',2,'')
				addDir('Peso da Régua','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=249',2,'')
				addDir('Ribeira de Pena','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=250',2,'')
				addDir('Sabrosa','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=251',2,'')
				addDir('Santa Marta de Penaguião','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=252',2,'')
				addDir('Valpaços','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=253',2,'')
				addDir('Vila Pouca de Aguiar','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=254',2,'')
				addDir('Vila Real','?arquivo_modo=3&pagina=1&distrito=vilareal&playview=255',2,'')
			elif distrito == 'viseu':
				addDir('Armamar','?arquivo_modo=3&pagina=1&distrito=viseu&playview=256',2,'')
				addDir('Carregal do Sal','?arquivo_modo=3&pagina=1&distrito=viseu&playview=257',2,'')
				addDir('Castro Daire','?arquivo_modo=3&pagina=1&distrito=viseu&playview=258',2,'')
				addDir('Cinfães','?arquivo_modo=3&pagina=1&distrito=viseu&playview=259',2,'')
				addDir('Lamego','?arquivo_modo=3&pagina=1&distrito=viseu&playview=260',2,'')
				addDir('Mangualde','?arquivo_modo=3&pagina=1&distrito=viseu&playview=261',2,'')
				addDir('Moimenta da Beira','?arquivo_modo=3&pagina=1&distrito=viseu&playview=262',2,'')
				addDir('Mortágua','?arquivo_modo=3&pagina=1&distrito=viseu&playview=263',2,'')
				addDir('Nelas','?arquivo_modo=3&pagina=1&distrito=viseu&playview=264',2,'')
				addDir('Oliveira dos Frades','?arquivo_modo=3&pagina=1&distrito=viseu&playview=265',2,'')
				addDir('Penalva do Castelo','?arquivo_modo=3&pagina=1&distrito=viseu&playview=266',2,'')
				addDir('Penedono','?arquivo_modo=3&pagina=1&distrito=viseu&playview=267',2,'')
				addDir('Resende','?arquivo_modo=3&pagina=1&distrito=viseu&playview=268',2,'')
				addDir('Santa Comba Dão','?arquivo_modo=3&pagina=1&distrito=viseu&playview=269',2,'')
				addDir('São João da Pesqueira','?arquivo_modo=3&pagina=1&distrito=viseu&playview=270',2,'')
				addDir('São Pedro do Sul','?arquivo_modo=3&pagina=1&distrito=viseu&playview=271',2,'')
				addDir('Sátão','?arquivo_modo=3&pagina=1&distrito=viseu&playview=272',2,'')
				addDir('Sernancelhe','?arquivo_modo=3&pagina=1&distrito=viseu&playview=273',2,'')
				addDir('Tabuaço','?arquivo_modo=3&pagina=1&distrito=viseu&playview=274',2,'')
				addDir('Tarouca','?arquivo_modo=3&pagina=1&distrito=viseu&playview=275',2,'')
				addDir('Tondela','?arquivo_modo=3&pagina=1&distrito=viseu&playview=276',2,'')
				addDir('Vila Nova de Paiva','?arquivo_modo=3&pagina=1&distrito=viseu&playview=277',2,'')
				addDir('Viseu','?arquivo_modo=3&pagina=1&distrito=viseu&playview=278',2,'')
				addDir('Vouzela','?arquivo_modo=3&pagina=1&distrito=viseu&playview=279',2,'')
			elif distrito == 'acores':
				addDir('Angra do Heroísmo','?arquivo_modo=3&pagina=1&distrito=acores&playview=280',2,'')
				addDir('Calheta (Açores)','?arquivo_modo=3&pagina=1&distrito=acores&playview=281',2,'')
				addDir('Corvo','?arquivo_modo=3&pagina=1&distrito=acores&playview=282',2,'')
				addDir('Horta','?arquivo_modo=3&pagina=1&distrito=acores&playview=283',2,'')
				addDir('Lagoa (Açores)','?arquivo_modo=3&pagina=1&distrito=acores&playview=284',2,'')
				addDir('Lajes das Flores','?arquivo_modo=3&pagina=1&distrito=acores&playview=285',2,'')
				addDir('Lajes do Pico','?arquivo_modo=3&pagina=1&distrito=acores&playview=286',2,'')
				addDir('Madalena','?arquivo_modo=3&pagina=1&distrito=acores&playview=287',2,'')
				addDir('Nordeste','?arquivo_modo=3&pagina=1&distrito=acores&playview=288',2,'')
				addDir('Ponta Delgada','?arquivo_modo=3&pagina=1&distrito=acores&playview=289',2,'')
				addDir('Povoação','?arquivo_modo=3&pagina=1&distrito=acores&playview=290',2,'')
				addDir('Praia da Vitória','?arquivo_modo=3&pagina=1&distrito=acores&playview=291',2,'')
				addDir('Ribeira Grande','?arquivo_modo=3&pagina=1&distrito=acores&playview=292',2,'')
				addDir('Santa Cruz das Flores','?arquivo_modo=3&pagina=1&distrito=acores&playview=293',2,'')
				addDir('Santa Cruz da Graciosa','?arquivo_modo=3&pagina=1&distrito=acores&playview=294',2,'')
				addDir('São Roque do Pico','?arquivo_modo=3&pagina=1&distrito=acores&playview=295',2,'')
				addDir('Velas','?arquivo_modo=3&pagina=1&distrito=acores&playview=296',2,'')
				addDir('Vila do Porto','?arquivo_modo=3&pagina=1&distrito=acores&playview=297',2,'')
				addDir('Vila Franca do Campo','?arquivo_modo=3&pagina=1&distrito=acores&playview=298',2,'')
			elif distrito == 'madeira':
				addDir('Calheta (Madeira)','?arquivo_modo=3&pagina=1&distrito=madeira&playview=300',2,'')
				addDir('Câmara de Lobos','?arquivo_modo=3&pagina=1&distrito=madeira&playview=303',2,'')
				addDir('Funchal','?arquivo_modo=3&pagina=1&distrito=madeira&playview=299',2,'')
				addDir('Machico','?arquivo_modo=3&pagina=1&distrito=madeira&playview=302',2,'')
				addDir('Ponta do Sol','?arquivo_modo=3&pagina=1&distrito=madeira&playview=304',2,'')
				addDir('Porto Moniz','?arquivo_modo=3&pagina=1&distrito=madeira&playview=305',2,'')
				addDir('Porto Santo','?arquivo_modo=3&pagina=1&distrito=madeira&playview=306',2,'')
				addDir('Ribeira Brava','?arquivo_modo=3&pagina=1&distrito=madeira&playview=307',2,'')
				addDir('Santa Cruz','?arquivo_modo=3&pagina=1&distrito=madeira&playview=308',2,'')
				addDir('Santana','?arquivo_modo=3&pagina=1&distrito=madeira&playview=309',2,'')
				addDir('São Vicente','?arquivo_modo=3&pagina=1&distrito=madeira&playview=302',2,'')
		elif distrito != None and playview != None:
			codigo_fonte = abrir_url('https://services.sapo.pt/videos/JSON2/Channel/localvisao/' + playview + '?page=' + pagina + '&limit=' + str(videos_per_page))
			decoded_data = json.loads(codigo_fonte)
			total_videos = decoded_data['rss']['channel']['opensearch:totalResults'].encode("utf8")
			if int(total_videos)>0:
				if int(total_videos)==1 or int(total_videos)-int(decoded_data['rss']['channel']['opensearch:startIndex'].encode("utf8"))==1:
					data = decoded_data['rss']['channel']['item']['pubDate'].encode("utf8")
					name = decoded_data['rss']['channel']['item']['title'].encode("utf8")
					link = decoded_data['rss']['channel']['item']['sapo:videoURL'].encode("utf8")
					descricao = decoded_data['rss']['channel']['item']['sapo:synopse'].encode("utf8")
					iconimage = decoded_data['rss']['channel']['item']['media:content']['url'].encode("utf8")
					addLink('[COLOR yellow]'+data[:-5] + '[/COLOR] - ' + name,link,101,iconimage,cleanhtml(descricao))
				else:
					for x in range(0, len(decoded_data['rss']['channel']['item'])):
						data = decoded_data['rss']['channel']['item'][x]['pubDate'].encode("utf8")
						name = decoded_data['rss']['channel']['item'][x]['title'].encode("utf8")
						link = decoded_data['rss']['channel']['item'][x]['sapo:videoURL'].encode("utf8")
						descricao = decoded_data['rss']['channel']['item'][x]['sapo:synopse'].encode("utf8")
						iconimage = decoded_data['rss']['channel']['item'][x]['media:content']['url'].encode("utf8")
						addLink('[COLOR yellow]'+data[:-5] + '[/COLOR] - ' + name,link,101,iconimage,cleanhtml(descricao))
				if int(total_videos)-(int(pagina)*videos_per_page)>0:
					addDir('Próximo >>','?arquivo_modo=' + arquivo_modo + '&pagina=' + str(int(pagina)+1) + '&distrito=' + distrito + '&playview=' + playview,mode,'')			

def cleanhtml(raw_html):
	cleanr =re.compile('<.*?>')
	cleantext = re.sub(cleanr,'', raw_html)
	return cleantext
	
def Abrir_definicoes():
	xbmcaddon.Addon(addon_id).openSettings()
	
def Resolver_url_localvisao(url):
	source_code = abrir_url(url)
	match = re.search("clip: {.+?url: '(.+?)'.+?}", source_code, re.MULTILINE|re.DOTALL)
	if match != None:
		tmp_url = match.group(1)
		req = urllib2.Request(tmp_url)
		res = urllib2.urlopen(req)
		url = res.geturl()
	else:
		url = ''
	play(url,name,iconimage)
	
def Resolver_url_sapo(url):
	source_code = abrir_url(url)
	match = re.search('<meta property="og:video" content="http://imgs.sapo.pt/sapovideo/swf/flvplayer-sapo.swf\?file=(.+?)/mov.+?"/>', source_code)
	if match != None:
		tmp_url = match.group(1) + '/mov'
		req = urllib2.Request(tmp_url)
		res = urllib2.urlopen(req)
		url = res.geturl()
	else:
		url = ''
	play(url,name,iconimage)
	
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
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0')
	response = urllib2.urlopen(req, timeout=60)
	link=response.read()
	response.close()
	return link

def addLink(name,url,mode,iconimage,desc):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok

def addDir(name,url,mode,iconimage,pasta=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
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


if mode==None: LOCALVISAO()
elif mode==1: Listar_Localvisao(url)
elif mode==2: Listar_Arquivo(url)
elif mode==3: Abrir_definicoes()
elif mode==100: Resolver_url_localvisao(url)
elif mode==101: Resolver_url_sapo(url)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))