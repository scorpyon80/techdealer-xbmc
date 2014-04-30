#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 2014 techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
import json
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.vejoaovivo'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

################################################## 

#MENUS############################################

def Menu_Principal():
	addDir_Page('Canais','canal?channelFriendlyName=',2,addonfolder+artfolder+'canais.png',1)
	addDir('Cidades','',1,addonfolder+artfolder+'cidades.png')
	addDir_Page('Pesquisar','filtro?',2,addonfolder+artfolder+'pesquisar.png',1)
	addDir('Definições','1',4,addonfolder+artfolder+'definicoes.png',False)
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def Menu_Cidades():
	addDir_Page('[COLOR yellow][B]AL - Alagoas[/B][/COLOR]','local?stateAcronym=al&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]BA - Bahia[/B][/COLOR]','local?stateAcronym=ba&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]CE - Ceará[/B][/COLOR]','local?stateAcronym=ce&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]DF - Distrito Federal[/B][/COLOR]','local?stateAcronym=df&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]ES - Espírito Santo[/B][/COLOR]','local?stateAcronym=es&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]MS - Mato Grosso do Sul[/B][/COLOR]','local?stateAcronym=ms&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]MG - Minas Gerais[/B][/COLOR]','local?stateAcronym=mg&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]PR - Paraná[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]PE - Pernambuco[/B][/COLOR]','local?stateAcronym=pe&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]RJ - Rio de Janeiro[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]RN - Rio Grande do Norte[/B][/COLOR]','local?stateAcronym=rn&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]RS - Rio Grande do Sul[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]SC - Santa Catarina[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)
	addDir_Page('[COLOR yellow][B]SP - São Paulo[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=',2,addonfolder+artfolder+'foldericon.png',1)

###################################################################################
#FUNCOES

def Listar_Canais(url,pagina):
	videos_per_page = int(selfAddon.getSetting('videos_per_page'))
	if url=='filtro?' and pagina==1:
		keyb = xbmc.Keyboard('', 'Pesquisar por...')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			search=urllib.quote(search)
		addDir_Page('[COLOR yellow][B]Pesquisar novamente...[/B][/COLOR]','filtro?',2,'',1)
		try:
			search
		except:
			sys.exit(0)
		url = 'filtro?onde='+search
	#Menu Canais - subcategorias
	elif url=='canal?channelFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Aeroportos[/B][/COLOR]','canal?channelFriendlyName=aeroportos',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Animais[/B][/COLOR]','canal?channelFriendlyName=animais',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Estádios de Futebol[/B][/COLOR]','canal?channelFriendlyName=estadios-futebol',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Futebol - society[/B][/COLOR]','canal?channelFriendlyName=futebol-society',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Melhores destinos[/B][/COLOR]','canal?channelFriendlyName=melhores-destinos',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Pontos Turísticos[/B][/COLOR]','canal?channelFriendlyName=pontos-turisticos',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Praias[/B][/COLOR]','canal?channelFriendlyName=praias',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Rodovias[/B][/COLOR]','canal?channelFriendlyName=rodovias',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Skate[/B][/COLOR]','canal?channelFriendlyName=skate',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Surf[/B][/COLOR]','canal?channelFriendlyName=surf',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Trânsito[/B][/COLOR]','canal?channelFriendlyName=transito',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]TV[/B][/COLOR]','canal?channelFriendlyName=tv',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Universidades[/B][/COLOR]','canal?channelFriendlyName=universidades',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado AL - subcategorias
	elif url=='local?stateAcronym=al&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Maceió[/B][/COLOR]','local?stateAcronym=al&cityFriendlyName=maceio',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado BA - subcategorias
	elif url=='local?stateAcronym=ba&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Alagoinhas[/B][/COLOR]','local?stateAcronym=ba&cityFriendlyName=alagoinhas',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Barreiras[/B][/COLOR]','local?stateAcronym=ba&cityFriendlyName=barreiras',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Itacaré[/B][/COLOR]','local?stateAcronym=ba&cityFriendlyName=itacare',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Juazeiro[/B][/COLOR]','local?stateAcronym=ba&cityFriendlyName=juazeiro',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Lauro de Freitas[/B][/COLOR]','local?stateAcronym=ba&cityFriendlyName=lauro-de-freitas',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Salvador[/B][/COLOR]','local?stateAcronym=ba&cityFriendlyName=salvador',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado CE - subcategorias
	elif url=='local?stateAcronym=ce&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Fortaleza[/B][/COLOR]','local?stateAcronym=ce&cityFriendlyName=fortaleza',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado DF - subcategorias
	elif url=='local?stateAcronym=df&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Águas Claras[/B][/COLOR]','local?stateAcronym=df&cityFriendlyName=aguas-calras',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Brasília[/B][/COLOR]','local?stateAcronym=df&cityFriendlyName=brasilia',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Taguatinga[/B][/COLOR]','local?stateAcronym=df&cityFriendlyName=taguatinga',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado ES - subcategorias
	elif url=='local?stateAcronym=es&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Venda Nova do Imigrante[/B][/COLOR]','local?stateAcronym=es&cityFriendlyName=venda%20nova%20do%20imigrante',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Vila Velha[/B][/COLOR]','local?stateAcronym=es&cityFriendlyName=vila-velha',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Vitoria[/B][/COLOR]','local?stateAcronym=es&cityFriendlyName=vitoria',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado MS - subcategorias
	elif url=='local?stateAcronym=ms&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Itaquiraí[/B][/COLOR]','local?stateAcronym=ms&cityFriendlyName=itaquirai',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado MG - subcategorias
	elif url=='local?stateAcronym=mg&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Belo Horizonte[/B][/COLOR]','local?stateAcronym=mg&cityFriendlyName=belo-horizonte',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Contagem[/B][/COLOR]','local?stateAcronym=mg&cityFriendlyName=contagem',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado PR - subcategorias
	elif url=='local?stateAcronym=pr&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Ampére[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=ampere',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Arapongas[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=arapongas',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Araucária[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=araucaria',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Curitiba[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=curitiba',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Fazenda Rio Grande[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=fazenda-rio-grande',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Guaratuba[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=guaratuba',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Londrina[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=londrina',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Maringá[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=maringa',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Matinhos[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=matinhos',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Paranaguá[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=paranagua',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Pato Branco[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=pato%20branco',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Pinhais[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=pinhais',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Pontal do Paraná[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=pontal-do-parana',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São José dos Pinhais[/B][/COLOR]','local?stateAcronym=pr&cityFriendlyName=sao-jose-dos-pinhais',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado PE - subcategorias
	elif url=='local?stateAcronym=pe&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Afogados da Ingazeira[/B][/COLOR]','local?stateAcronym=pe&cityFriendlyName=afogados-da-ingazeira',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Jaboatão dos Guararapes[/B][/COLOR]','local?stateAcronym=pe&cityFriendlyName=jaboatao-dos-guararapes',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Olinda[/B][/COLOR]','local?stateAcronym=pe&cityFriendlyName=olinda',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Recife[/B][/COLOR]','local?stateAcronym=pe&cityFriendlyName=recife',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado RJ - subcategorias
	elif url=='local?stateAcronym=rj&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Angra dos Reis[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=angra-dos-reis',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Araruama[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=araruama',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Armação dos Búzios[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=armacao-dos-buzios',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Arraial do Cabo[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=arraial-do-cabo',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Duque de Caxias[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=duque-de-caxias',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Niterói[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=niteroi',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Nova Iguaçu[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=nova-iguacu',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Paraty[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=paraty',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Petrópolis[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=petropolis',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Rio de Janeiro[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=rio-de-janeiro',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São Gonçalo[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=sao-goncalo',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Saquarema[/B][/COLOR]','local?stateAcronym=rj&cityFriendlyName=saquarema',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado RN - subcategorias
	elif url=='local?stateAcronym=rn&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Natal[/B][/COLOR]','local?stateAcronym=rn&cityFriendlyName=natal',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado RS - subcategorias
	elif url=='local?stateAcronym=rs&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Cachoeirinha[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=cachoeirinha',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Capão da Canoa[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=capao-da-canoa',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Gramado[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=gramado',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Gravataí[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=gravatai',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Nova Petrópolis[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=nova-petropolis',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Pelotas[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=pelotas',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Porto Alegre[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=porto-alegre',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Santa Cruz do Sul[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=santa-cruz-do-sul',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Torres[/B][/COLOR]','local?stateAcronym=rs&cityFriendlyName=torres',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado SC - subcategorias
	elif url=='local?stateAcronym=sc&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Araquari[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=araquari',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Balneário Barra do Sul[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=balneario-barra-do-sul',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Balneário Camboriú[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=balneario-camboriu',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Barra Velha[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=barra-velha',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Biguaçu[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=biguacu',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Blumenau[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=blumenau',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Bombinhas[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=bombinhas',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Camboriú[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=camboriu',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Cocal do Sul[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=cocal-do-sul',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Criciúma[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=criciuma',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Florianopolis[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=florianopolis',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Garopaba[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=garopaba',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Garuva[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=garuva',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Gaspar[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=Gaspar',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Ilhota[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=ilhota',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Imbituba [/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=imbituba',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Itajaí[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=itajai',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Itapema[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=itapema',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Itapoá[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=itapoa',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Jaraguá do Sul[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=jaragua-do-sul',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Joinville[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=joinville',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Lages[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=lages',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Laguna[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=laguna',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Lauro Muller[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=lauro-muller',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Navegantes[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=navegantes',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Orleans[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=orleans',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Palhoça[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=palhoca',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Penha[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=penha',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Piçarras[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=picarras',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Porto Belo[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=porto-belo',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Rio Negrinho[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=rio-negrinho',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São Francisco do Sul[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=sao-francisco-do-sul',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São Joaquim[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=sao-joaquim',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São José[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=sao-jose',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Tijucas[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=tijucas',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Urubici[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=urubici',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Urupema[/B][/COLOR]','local?stateAcronym=sc&cityFriendlyName=urupema',2,addonfolder+artfolder+'foldericon.png',1)
	#Estado SP - subcategorias
	elif url=='local?stateAcronym=sp&cityFriendlyName=' and pagina==1:
		addDir_Page('[COLOR yellow][B]Aparecida[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=aparecida',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Barueri[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=barueri',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Campinas[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=campinas',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Campos do Jordão[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=campos-do-jordao',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Cotia[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=cotia',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Guarujá[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=guaruja',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Guarulhos[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=guarulhos',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Ilhabela[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=ilhabela',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Itaquaquecetuba[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=Itaquaquecetuba',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Jundiaí[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=jundiai',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Osasco[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=osasco',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Praia Grande[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=praia-grande',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Santo Amaro[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=santo-amaro',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Santo André[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=santo-andre',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São Bernardo do Campo[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=sao-bernardo-do-campo',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São Caetano do Sul[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=sao-caetano-do-sul',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São Paulo[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=sao-paulo',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]São Sebastião[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=sao-sebastiao',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Suzano[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=suzano',2,addonfolder+artfolder+'foldericon.png',1)
		addDir_Page('[COLOR yellow][B]Ubatuba[/B][/COLOR]','local?stateAcronym=sp&cityFriendlyName=ubatuba',2,addonfolder+artfolder+'foldericon.png',1)
	codigo_fonte = abrir_url('http://www.vejoaovivo.com.br/paginator/'+url+'&offset='+str(pagina-1)+'&max='+str(videos_per_page))
	decoded_data = json.loads(codigo_fonte)
	listOfCams = decoded_data['listOfCams'].encode('utf_8')
	total_videos = decoded_data['totalCameras']
	match = re.compile("<a href=\"(.+?)\".+?title=\".+?\">.+?<img src=['\"](.+?)['\"].+?>.+?<h5>(.+?)</h5>.+?<h6>.+?</h6>.+?</a>",re.DOTALL).findall(listOfCams)
	if match != None:
		for link, iconimage, name in match:
			if iconimage=='/images/camera-manutencao-small.jpg':
				iconimage = 'http://www.vejoaovivo.com.br/images/camera-manutencao-small.jpg'
			addDir(name,'http://www.vejoaovivo.com.br'+link,3,iconimage,False)
	if int(total_videos)-(int(pagina)*videos_per_page)>0:
		addDir_Page('[COLOR blue]Página '+str(int(pagina)+1)+' >>[/COLOR]',url,mode,'',int(int(pagina)+1))
		
def Abrir_definicoes():
	xbmcaddon.Addon(addon_id).openSettings()
		
def Encontrar_fonte(name,url,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Vejo ao Vivo', 'Procurando fonte...')
	progress.update(0)
	codigo_fonte = abrir_url(url)
	match = re.search('<input id="current-camera-id".+?value="(.+?)" />', codigo_fonte)
	if match != None:
		codigo_fonte_2 = abrir_url('http://www.vejoaovivo.com.br/camera/retrieveCameraUrls?id='+match.group(1))
		decoded_data = json.loads(codigo_fonte_2)
		if selfAddon.getSetting('typestream') == "0":
			progress.update(100)
			progress.close()
			play(name,decoded_data['flowplayerRtmpNetConnectionUrl']+' playPath='+decoded_data['flowplayerClipUrl']+' live=true',iconimage)
		elif selfAddon.getSetting('typestream') == "1":
			progress.update(100)
			progress.close()
			play(name,decoded_data['flowplayerIpadUrl'],iconimage)
		
def play(name,url,iconimage):
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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.png')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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


if mode==None: Menu_Principal()
elif mode==1: Menu_Cidades()
elif mode==2: Listar_Canais(url,pagina)
elif mode==3: Encontrar_fonte(name,url,iconimage)
elif mode==4: Abrir_definicoes()

xbmcplugin.endOfDirectory(int(sys.argv[1]))