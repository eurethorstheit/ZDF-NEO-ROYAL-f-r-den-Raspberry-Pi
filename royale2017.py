#!/usr/bin/env python3
# coding: utf8

import sys, os
import subprocess
from subprocess import PIPE, Popen, call
import re
import urllib.request, urllib.error, urllib.parse #Zum Holen der Internetseite
import os.path # zum Prüfen, ob die Datei da ist
import time
from threading import Thread
import time
from configparser import ConfigParser

# Weiterentwicklungen: 

# Wichtige Grundlagen: youtube-dl ab version 2017.02.14



# Medieneintrag vorhanden: 
# https://www.zdf.de/comedy/neo-magazin-mit-jan-boehmermann/neo-magazin-royale-mit-jan-boehmermann-vom-9-februar-2017-100.html



lt = time.localtime() # Tupel der aktuellen Zeit (lt bedeutet local time)
DL_URLS = [] # Liste der zu ladenden Videos
DM = 0 # DM bedeutet Deine Mudda oder Developer Mode

def log(Daten, Dateiname = "errorlog.dat"): # Hauptsächlich zum Testen
	''' Zum loggen von Fehlermeldungen '''
	Datei = open(Dateiname,"a+")
	Datei.write(Daten)
	Datei.close()


def Schreibe(Daten, Dateiname = "Daten.dat"): # Hauptsächlich zum Testen
	Datei = open(Dateiname,"a+")
	Datei.write(Daten)
	Datei.close()

def Lese_Daten(Dateiname = "Daten.dat"):
	Datei = open(Dateiname,"r")
	Daten = Datei.read()
	Datei.close()
	return Daten

def hole_tag(c): # Holt den Tag aus c heraus
	Tag = re.match(r"(^[0-9]+)",c)
	tag = Tag.group(1)
	tag = tag[len(tag)-2:]
	return tag
	
def Teste_Quelle(url): # Pruefen, ob eine URL vorhanden ist
	try:
		resp = urllib.request.urlopen(url)
		contents = True
		return contents
	except urllib.error.HTTPError as error:
		contents = False
		return contents

def Hole_Datum_Last_Entry():
	if os.path.isfile("Daten.dat") == True:
		Daten = Lese_Daten().rstrip().split('\n') # None-Eintraege herausfiltern
		Daten = Daten[len(Daten)-1].split('##')
		Date_Last_Entry = Daten
		return Date_Last_Entry[0:3]

def Hole_Quelle(url): # Herunterladen einer URL
	try:
		resp = urllib.request.urlopen(url)
		contents = resp.read()
		return contents
	except urllib.error.HTTPError as error:
		contents = False
		return contents

def hole_f():
	x = 1
	print("\n------------------------\n")
	for key in F:	
		print(str(x) +". "+ key)
		x += 1
	temp = input("Wähl ein Jahr:")
	return F[int(temp)-1]

def scan_monat(DL_URLS = [],jahr = "2017", monat = "1", t_start = "1",t_end = "31"):
	MONATE = ["januar","februar","märz","april","mai","juni","juli","august","september","oktober","november","dezember"]
	if DM == 1 : print("Monat: %s, Starttag: %s - Endtag: %s\n" % (monat,t_start,t_end)) 
	if DM == 0 : print("Scanne: %s, %s…" % (D[monat-1],jahr)) 

	for b in range(int(t_start),int(t_end)+1):
		sys.stdout.write("\rScanne Tag: %s" % (b))
		sys.stdout.flush()
		for x in range(100,103,1): # g herausfinden
				# Zusammensetzen der vollständigen DownloadURL
			a = 'https://www.zdf.de/comedy/neo-magazin-mit-jan-boehmermann/neo-magazin-royale-mit-jan-boehmermann-vom-' 
			b = str(b)+'-'
			c = str(MONATE[int(monat)-1])+'-'
			d = str(jahr)
			e="-"+str(x)+".html"
				# Vollständige Download-URL
			URL = a+b+c+d+e 
			if Teste_Quelle(URL) == True:		
					# Zusammenstellen des Datensatzes und schreiben in Daten.dat
				if DM == 1 : print("ZDF-Medieneintrag vorhanden :"+URL)	
				Datensatz = d[3:]+'##'+str(monat)+'##'+b[:-1]+'##'+URL		
				if DM == 1: print('Datensatz: ' + Datensatz)
				Schreibe(Datensatz)
				if DM == 1 : log("Hinzugefuegte URL: "+ str(URL))
				print("\nFolge gefunden: vom %s.%s.%s " % (b,monat,jahr))
				sys.stdout.flush()
			else:
				if DM == 1 : log("Fehler bei existierendem Eintrag zur Folge: "+URL+"\n")


def scan_jahr(DL_URLS = [],jahr = "2017", m_start = "1",m_end = "12",b_jahr_start = False,b_jahr_end = False):
	
	print("\nJahr: %s, Startmonat: %s - Endmonat: %s\n"%(jahr,m_start,m_end)) 
	''' Grundlegende Strings zum Aufbau der zu durchsuchenden Website '''
	for monat in range(int(m_start),int(m_end)+1,1):
		if (monat == int(Last_Entry[1]) and (b_jahr_start == True)): # Hier werden die Monatsgrenzen m_start und m_end für das jeweilige Jahr festgelegt
			t_start = int(Last_Entry[2])+1 
			if DM == 1 : print("Starttag:"+str(t_start))
		else:
			t_start = 1
		if ( (monat == lt[1]) and (b_jahr_end == True) ):
			t_end = lt[2]
		else:
			t_end = 31

		scan_monat(DL_URLS,jahr,monat,t_start,t_end)

def starte_scan(DL_URLS = [],Last_Entry = Hole_Datum_Last_Entry(),lt = time.localtime()):
	for jahr in range(int(Last_Entry[0]),lt[0]+1):  # Gehe die Jahre durch bis zur aktuellen Zeit +1, weil Kopfgesteuert
		b_jahr_start = False # Markierer für die späteren if Abfragen
		b_jahr_end = False
		if jahr == int(Last_Entry[0]): # Hier werden die Monatsgrenzen m_start und m_end für das jeweilige Jahr festgelegt
			b_jahr_start = True
			m_start = Last_Entry[1] 
		else:
			m_start = 1
		if jahr == lt[0]:
			m_end = lt[1]
		else:
			m_end = 12
		if jahr == lt[0]:
			b_jahr_end = True
		scan_jahr(DL_URLS,jahr,m_start,m_end,b_jahr_start,b_jahr_end)
	return DL_URLS

def first_use(lt, zahl): # das erste mal 
	first_month = int(lt[1]) - int(zahl)
	if (first_month < 1):
		first_jahr = int(lt[0]) - 1
		first_month = 12 + first_month
	else:
		first_jahr = int(lt[0]) 
	print("Erster Monat:" + str(first_month))
	print("Erstes Jahr:" + str(first_jahr)[2:])
	Erster_Datensatz = str(first_jahr)[2:]+"##"+str(first_month)+"##0##AllerAnfangIstSchwer\n"
	Schreibe(Erster_Datensatz)


def hole_restzeit():
	''' Diese Funktion holt die Restzeit des Downloads '''
	for line in Ladeprozess.stdout:
		match = re.search(r'(ETA)(.*)',str(line))
		if (match != None):
			match = str(match.group(2))[:-3].strip()
			if len(match) == 5:
				print('4-Stellig')
				match = match.split(':')
				time_download_sek = int((int(match[0])*60 + int(match[0]))/60)
				return time_download_min

def video_puffer():
			# Hole Gesamtzeit -- Achtung, Datei muss bereits auf dem Rechner sein. Falls zu schnell, kanns Probleme geben
	gesamtzeit = 45
	print('Videopuffer…')
	input('…')
	while Ladeprozess.poll() == None:
		input('In der Schleife')	
		restzeit = hole_restzeit()	
		print(restzeit)
		if restzeit < gesamtzeit:
			break
	

parser = ConfigParser()

if os.path.isfile("config.ini") == False:
	print("\n----------------------------------\nDas ist die erste Verwendung des Players. Zunächst müssen einige Einstellungen vorgenommen werden und eine Liste der Folgen muss erstellt werden Das kann einige Minuten dauern.\n----------------------------------\n")

	parser.add_section('developermode')
	parser.add_section('gui')
	parser.add_section('videooptions')
	parser.add_section('folgen')

	eingabe = input("Developermode an ? Wenn ja, dann werden wesentlich mehr printausgaben an die Console übergeben.\n \t0 -- nein\n\t1 -- ja\n Eingabe: ")
	parser.set('developermode','on',str(eingabe))
	eingabe = input("Verwendung einer graphischen Oberfläche beim nächsten Start -derzeit noch nicht verfügbar-?\n\t0 -- nein\n\t1 -- ja\nEingabe: ")
	parser.set('gui','on',eingabe)
	eingabe = input("Videoplayer? Beim Raspberry Pi ist es für gewöhnlich der omxplayer.Möglicherweise ändert sich das je nach Modell auch noch, entsprechend die Option.\n\t0 -- omxplayer\n\t1 -- mplayer\nEingabe: ")
	parser.set('videooptions','player',eingabe)
	eingabe = input("Videoqualität?\n\t0 -- schlecht\n\t1 -- mittel\n\t2 -- gut\nEingabe: ")
	parser.set('videooptions','quality',eingabe)
	eingabe = input("Pufferzeit berechnen. Bitte Zahl zwischen 0 und 2 eingeben.\n\t0 -- keinen Puffer\n\t1 -- doppelter Puffer\n\t2 -- dreifacher Puffer\nEingabe: ")
	parser.set('videooptions','buffer',eingabe)
	eingabe = input("\tWieviele Monate soll der scanner rückwirkend nach Folgen suchen?\n\t Achtung! Dauert pro Monat eventuell ein paar Minuten\nEingabe: ")
	parser.set('folgen','monate',eingabe)
	datei = open('config.ini','w')
	parser.write(datei)
	datei.close()
	datei = open('config.ini','w')
	parser.write(datei)
	parser.read('config.ini')

	input(" Die Einstellungen sind abgeschlossen. Je höhe die Zahl beim Puffer und je schlechter die Bildqualität, desto sicherer läuft das Video ohne ruckeln ab. Die Einstellungen müssen ausprobiert und individuell angepasst werden\nDie Optionen werden in der Datei config.ini gespeichert und können jederzeit manuell geändert werden. Lösche die Datei config.ini, wenn sich das Startmenü wiederholen soll.\nScannen nach Folgen beginnt nun nach betätigen der Eingabetaste\n\tEingabetaste für weiter…")
	print("Searching…")
	
	scan_start = int(parser.get('folgen','monate'))
	first_use(lt,scan_start)
	Last_Entry = Hole_Datum_Last_Entry() # Tupel Jahr,Monat,Tag
	Last_Entry[0] = "20"+Last_Entry[0] # 2016 und nicht 16
	starte_scan(DL_URLS,Last_Entry)


parser.read('config.ini')
DM = int(parser.get('developermode','on'))

SENDEZEIT_in_s = 20 * 45 
PUFFER_in_s = int(parser.get('videooptions','buffer'))*45
PUFFER2_in_Anzahl = 100



# Scannen und Liste aktualisieren

if os.path.isfile("Daten.dat") == True:
	Last_Entry = Hole_Datum_Last_Entry() # Tupel Jahr,Monat,Tag
	Last_Entry[0] = "20"+Last_Entry[0] # 2016 und nicht 16


if os.path.isfile("Daten.dat") == True:
	print("--------------------------------------------------\nAktueller Stand der Liste: %s. %s. %s\n--------------------------------------------------" %(Last_Entry[2],Last_Entry[1],Last_Entry[0]))
	eingabe = ""
else:
	print("Noch keine Liste angelegt")
	scan_start = input("\tWieviele Monate rückwirkend soll gescannt werden?\nAntwort: ")
	first_use(lt,scan_start)
	Last_Entry = Hole_Datum_Last_Entry() # Tupel Jahr,Monat,Tag
	Last_Entry[0] = "20"+Last_Entry[0] # 2016 und nicht 16
	eingabe = "1"

while (eingabe != "0") and (eingabe != "1"):
	eingabe = input("Nach neuen Folgen scannen ?\n\t0 -- nein, weiter zur Liste\n\t1 -- ja, bring mich auf den neusten Stand\nEingabe: ")

if eingabe == "1":
	print("Starte Scanner…")		
	starte_scan(DL_URLS,Last_Entry)
	print("\rScanvorgang abgeschlossen")

else:
	pass


####################################### Menue erstellen

DL_URLS = []
Auswahl = []

if os.path.isfile("Daten.dat") == True:
	Auswahl = None
	while Auswahl == None:
#		Auswahl = DB_clean(Lese_Daten().rstrip().split('\n'))   ###Ohne DB_Clean
		Auswahl = Lese_Daten().rstrip().split('\n')
		if Auswahl == None:
			scan_start = input("\tWieviele Monate rückwirkend soll gescannt werden?\nAntwort: ")
			first_use(lt,scan_start)
			Last_Entry = Hole_Datum_Last_Entry() # Tupel Jahr,Monat,Tag
			Last_Entry[0] = "20"+Last_Entry[0] # 2016 und nicht 16
			print("Starte Scanner…")		
			starte_scan(DL_URLS,Last_Entry)
			print("\rScanvorgang abgeschlossen")
#			Auswahl = DB_clean(Lese_Daten().rstrip().split('\n'))  ### Ohne DB_Clean
			Auswahl = Lese_Daten().rstrip().split('\n')

	print("\nListe der Folgen:")
	x = 1
	for key in Auswahl:
		temp = key.split('##')
		if len(temp) == 4:
			print("\t%s. -- Sendung vom %s. %s. %s" % (str(x),temp[2],temp[1],"20"+temp[0]))
			x += 1

Eingabe = input("Wähle eine Sendung: ")
URL = Auswahl[int(Eingabe)-1].split('##')[3]
if DM == 1 : print("Videolink: "+ URL)






print("\nLadevorgang beginnen und Puffer zum Abspielen vorbereiten…")




# Ladevorgang und abspielen




Ladeprozess = Popen(['youtube-dl','-o','Video_Royal.mp4', URL],stdout = PIPE)

#Puffer
video_puffer()


if str(parser.get('videooptions','player')) == "0":
	Abspielen=subprocess.Popen(["omxplayer","-o","local","-b","Video_Royal.mp4"]) # für omxplayer
else:
	Abspielen=subprocess.Popen(["mplayer","-fs","Video_Royal.mp4"])   # für mplayer

while Abspielen.poll() == None:
	pass
print("Programm beenden…")
Ladevorgang.terminate()
if os.path.isfile("Video_Royal.mp4") == True:
	os.remove("Video_Royal.mp4")
print("…das wars schon wieder")

