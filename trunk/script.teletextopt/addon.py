#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 2014 techdealer

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,httplib,sys

addon_id = 'script.teletextopt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

################################################## 

###################################################################################
#FUNCOES
class TeletextoWindow(xbmcgui.WindowDialog):
	def __init__(self,canal,page):
		self.page = page
		self.canal = canal
		self.Open_page()

	def onControl(self, control):
		if control == self.anterior:
			if len(self.txt_array)>1:
				if self.sub_page==1:
					self.sub_page = len(self.txt_array)
				else:
					self.sub_page -= 1
				self.Change_sub_page()
		elif control == self.proximo:
			if len(self.txt_array)>1:
				if self.sub_page==len(self.txt_array):
					self.sub_page = 1
				else:
					self.sub_page += 1
				self.Change_sub_page()
		elif control == self.page_input:
			self.page = Page_Search()
			self.Open_page()
		elif control == self.addon_exit:
			self.close()
		elif control == self.switch_canal:
			tmp_canal = Escolher_Canal()
			if tmp_canal > 0:
				self.canal = tmp_canal
				self.page = 100
				self.Open_page()
		
	def onAction(self, action):
		action_id = action.getId()
		if action_id == 1: #sub_page anterior
			if len(self.txt_array)>1:
				if self.sub_page==1:
					self.sub_page = len(self.txt_array)
				else:
					self.sub_page -= 1
				self.Change_sub_page()
		elif action_id == 2: #sub_page proximo
			if len(self.txt_array)>1:
				if self.sub_page==len(self.txt_array):
					self.sub_page = 1
				else:
					self.sub_page += 1
				self.Change_sub_page()
		elif action_id == 4: #pagina anterior
			if self.page == 100:
				self.page = 888
			else:
				self.page -= 1
			self.Open_page()
		elif action_id == 3: #proxima pagina
			if self.page == 888:
				self.page = 100
			else:
				self.page += 1
			self.Open_page()
		elif action_id == 7: # enter
			self.page = Page_Search()
			self.Open_page()
		elif action_id == 10 or action_id == 92: #esc or backspace
			self.close()
		elif action_id == 12: # barra de espacos
			tmp_canal = Escolher_Canal()
			if tmp_canal > 0:
				self.canal = tmp_canal
				self.page = 100
				self.Open_page()
		
	def Open_page(self):
		self.txt_array = []
		if self.canal == 1:
			if page_exists('http://www.rtp.pt/wportal/fab-txt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_0001.png')==True:
				codigo_fonte = abrir_url('http://www.rtp.pt/wportal/fab-txt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_0001.htm')
				total_pages = re.search('">([0-9]+)</A>&nbsp;&nbsp;<A HREF="', codigo_fonte)
				if total_pages==None:
						self.txt_array.append('http://www.rtp.pt/wportal/fab-txt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_0001.png')
				else:
					total_pages = total_pages.group(1)
					for i in range(1,int(total_pages)+1):
						self.txt_array.append('http://www.rtp.pt/wportal/fab-txt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_' + str(i).rjust(4, '0') + '.png')
		elif self.canal == 2:
			if page_exists('http://teletexto.sic.aeiou.pt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_0001.htm')==True:
				codigo_fonte = abrir_url('http://teletexto.sic.aeiou.pt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_0001.htm')
				total_pages = re.search('([0-9]+)(</a>)?&nbsp;&nbsp;|&nbsp;&nbsp;(<a href=".">)?&gt;&gt;(</a>)?', codigo_fonte)
				if total_pages != None:
					if total_pages.group(1)=="1":
						self.txt_array.append('http://teletexto.sic.aeiou.pt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_0001.png')
					else:
						total_pages = total_pages.group(1)
						for i in range(1,int(total_pages)+1):
							self.txt_array.append('http://teletexto.sic.aeiou.pt/'+ str(self.page - int(str(self.page)[-2:])) +'/' + str(self.page) + '_' + str(i).rjust(4, '0') + '.png')
		self.sub_page = 1
		if len(self.txt_array)>0:
			self.background = xbmcgui.ControlImage(0,0,1280,720,self.txt_array[self.sub_page-1])
			self.addControl(self.background)
		else:
			self.background = xbmcgui.ControlImage(0,0,1280,720,addonfolder+artfolder+'notfound.jpg')
			self.addControl(self.background)
		if len(self.txt_array)>1:
			self.pagelabel = xbmcgui.ControlLabel(38,5,500,500,'Página '+str(self.page)+' - '+str(self.sub_page)+'/'+str(len(self.txt_array)), font='font24_title', angle=-90)
			self.addControl(self.pagelabel)
		else:
			self.pagelabel = xbmcgui.ControlLabel(38,5,500,500,'Página '+str(self.page), font='font24_title', angle=-90)
			self.addControl(self.pagelabel)
		self.switch_canal = xbmcgui.ControlButton(1202,0,80,70,'', focusTexture=addonfolder+artfolder+'switch.png', noFocusTexture=addonfolder+artfolder+'switch.png')
		self.addControl(self.switch_canal)
		self.page_input = xbmcgui.ControlButton(0,240,80,70,'', focusTexture=addonfolder+artfolder+'comando.png', noFocusTexture=addonfolder+artfolder+'comando.png')
		self.addControl(self.page_input)
		self.addon_exit = xbmcgui.ControlButton(1202,240,80,70,'', focusTexture=addonfolder+artfolder+'sair.png', noFocusTexture=addonfolder+artfolder+'sair.png')
		self.addControl(self.addon_exit)
		self.anterior = xbmcgui.ControlButton(0,652,80,70,'', focusTexture=addonfolder+artfolder+'anterior.png', noFocusTexture=addonfolder+artfolder+'anterior.png')
		self.addControl(self.anterior)
		self.proximo = xbmcgui.ControlButton(1202,652,80,70,'',focusTexture=addonfolder+artfolder+'proximo.png', noFocusTexture=addonfolder+artfolder+'proximo.png')
		self.addControl(self.proximo)
		
	def Change_sub_page(self):
		self.background = xbmcgui.ControlImage(0,0,1280,720,self.txt_array[self.sub_page-1])
		self.addControl(self.background)
		self.pagelabel = xbmcgui.ControlLabel(38,5,500,500,'Página '+str(self.page)+' - '+str(self.sub_page)+'/'+str(len(self.txt_array)), font='font24_title', angle=-90)
		self.addControl(self.pagelabel)
		self.switch_canal = xbmcgui.ControlButton(1202,0,80,70,'', focusTexture=addonfolder+artfolder+'switch.png', noFocusTexture=addonfolder+artfolder+'switch.png')
		self.addControl(self.switch_canal)
		self.page_input = xbmcgui.ControlButton(0,240,80,70,'', focusTexture=addonfolder+artfolder+'comando.png', noFocusTexture=addonfolder+artfolder+'comando.png')
		self.addControl(self.page_input)
		self.addon_exit = xbmcgui.ControlButton(1202,240,80,70,'', focusTexture=addonfolder+artfolder+'sair.png', noFocusTexture=addonfolder+artfolder+'sair.png')
		self.addControl(self.addon_exit)
		self.anterior = xbmcgui.ControlButton(0,652,80,70,'', focusTexture=addonfolder+artfolder+'anterior.png', noFocusTexture=addonfolder+artfolder+'anterior.png')
		self.addControl(self.anterior)
		self.proximo = xbmcgui.ControlButton(1202,652,80,70,'',focusTexture=addonfolder+artfolder+'proximo.png', noFocusTexture=addonfolder+artfolder+'proximo.png')
		self.addControl(self.proximo)
		
def page_exists(location):
	request = urllib2.Request(location)
	request.get_method = lambda : 'HEAD'
	try:
		response = urllib2.urlopen(request)
		return True
	except urllib2.HTTPError:
		return False
		
def Page_Search():
    page = xbmcgui.Dialog().numeric(0,'Abrir a página...')
    page=int(page)
    if page>888 or page<100:
        Page_Search()
    else:
		return page
		
def Escolher_Canal():
	canal = xbmcgui.Dialog().select('Escolha um canal...', ['RTP','SIC'])+1
	return canal
    
def Open_Teletext(canal,page):
	window = TeletextoWindow(canal,page)
	window.doModal()
	
###################################################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

###############################################################################################################
#                                                 ADDON STARTUP                                               #
###############################################################################################################

canal = Escolher_Canal()
if canal == 0:
	sys.exit(0)
Open_Teletext(canal,100)