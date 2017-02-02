#!/usr/bin/env python3
# coding: utf8

import sys, os
import subprocess
from subprocess import PIPE, Popen
import re
import urllib.request, urllib.error, urllib.parse #Zum Holen der Internetseite
import os.path # zum Prüfen, ob die Datei da ist
import time
import fcntl
import select
from threading import Thread
import time
from configparser import ConfigParser

# Weiterentwicklungen: 
#Beim ersten Scannen wird der erste Tag des ersten Monats nicht berücksichtigt, muss gefixt werden
#Funktionen noch nicht nutzbar: GUI, Qualität (im Moment ist es nur die schlechteste Qualität), Playerwahl (im Moment nur mplayer), developermode ausschalten geht noch nicht) 

lt = time.localtime() # Tupel der aktuellen Zeit (lt bedeutet local time)
DL_URLS = [] # Liste der zu ladenden Videos
DM = 0 # DM bedeutet Deine Mudder oder Developer Mode
def Schreibe(Daten, Dateiname = "Daten.dat"): # Hauptsächlich zum Testen
	Datei = open(Dateiname,"a+")
	Datei.write(Daten)
	Datei.close()

def Lese_Daten(Dateiname = "Daten.dat"):
	Datei = open(Dateiname,"r")
	Daten = Datei.read()
	Datei.close()
	return Daten

def c_matchen(Quelle):
	''' Diese funktion matched c '''
	i_start = int((Quelle.find("sendungroyale"))) - 20
	i_end = int(i_start)+60
	string_roh = Quelle[i_start:i_end]
	string_match = re.search(r"([0-9].*)\"",string_roh)
	if string_match is not None:
		c = string_match.group(1)
		return c

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

def Teste_Content(URL,D,d,f): # Testet, ob Downloadbarer Link oder nicht und gebe einen Vollständigen DAtensatz zurück
	Quelle = Hole_Quelle(URL).decode('utf8') 
	if "sendungroyale" in Quelle:
		monat = d
		f = str(f)
		jahr = str(f[2:])
		a = 'https://downloadzdf-a.akamaihd.net/mp4/zdf/' 
		b = jahr+"/"+str(monat)+"/"
		c = c_matchen(Quelle)+"/" 
		tag = hole_tag(c)
		#d = "2/" # wird drei Zeilen weiter angepasst und eine Zahl 1 bis 3 ausprobiert, bis es passt
		e = c[:-1]
		f = "_476k_p9v13.mp4"
		for d_temp in range (1,9,1): # d herausfinden
			d = str(d_temp)+"/"
			URL = a+b+c+d+e+f # das ist nun die DownloadURL
			if DM == 1 : print("Zu testende Quelle: "+URL)
			if Teste_Quelle(URL) == True: # Datensatz zusammenstellen und zurückgeben
				Datensatz = str(jahr)+"##"+str(monat)+"##"+str(tag)+"##"+str(URL)+"\n"
				return Datensatz
	else:
		return False






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
	D = ["januar","februar","märz","april","mai","juni","juli","august","september","oktober","november","dezember"]
	if DM == 1 : print("Monat: %s, Starttag: %s - Endtag: %s\n" % (monat,t_start,t_end)) 
	if DM == 0 : print("Scanne: %s, %s…" % (D[monat-1],jahr)) 
	a = "https://www.zdf.de/comedy/neo-magazin-mit-jan-boehmermann/neo-magazin-royale-mit-jan-boehmermann-vom-"
	#b = tag
	c = "-"
	d = int(monat)
	e = "-"
#	F = ["2016","2017"]
	f = jahr
	#g = "-100.html" # geht nicht mehr, da auch -102.html sein könnte
	#g = (Zahl) von (100 bis 105) willkürlich gesetzt
	for b in range(int(t_start),int(t_end)+1):
		sys.stdout.write("\rScanne Tag: %s" % (b))
		sys.stdout.flush()
		for x in range(100,105,1): # g herausfinden
			g="-"+str(x)+".html"
			URL = a+str(b)+c+str(D[d-1])+e+str(f)+g # Das ist die erste URL. Hier muss contentURL geholt werden
			if Teste_Quelle(URL) == True:		
				if DM == 1 : print("ZDF-Mediathekeintrag vorhanden :"+URL)	
				url = Teste_Content(URL,D,d,f)	# das ist die URL zum Downloaden 
				if (url != False) and (url != None):
					Schreibe(url)
					if DM == 1 : print("Hinzugefuegte URL: "+ str(url))
					if DM == 0 : print("\nFolge gefunden: vom %s.%s.%s " % (b,d,f))
					sys.stdout.flush()
			else:
				if DM == 1 : print("Fehler bei existierendem Eintrag zur Folge: "+URL+"\n")


def scan_jahr(DL_URLS = [],jahr = "2017", m_start = "1",m_end = "12",b_jahr_start = False,b_jahr_end = False):
	
	print("Jahr: %s, Startmonat: %s - Endmonat: %s\n"%(jahr,m_start,m_end)) 
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
	eingabe = input("Wieviele Monate soll der scanner rückwirkend nach Folgen suchen?\n\t Achtung! Dauert pro Monat eventuell ein paar Minuten\nEingabe: ")
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
	scan_start = input("Wieviele Monate rückwirkend soll gescannt werden?")
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

def DB_clean(Auswahl):
	if "AllerAnfangIstSchwer" in Auswahl[0]: # Anfangsmarkierung
		del Auswahl[0]
	while (Auswahl[len(Auswahl)-1] == Auswahl[len(Auswahl)-2]):
		del Auswahl[len(Auswahl)-1]
	if "AllerAnfangIstSchwer" in Auswahl[len(Auswahl)-1]: # Anfangsmarkierung
		del Auswahl[len(Auswahl)-1]
	return Auswahl

DL_URLS = []
Auswahl = []

if os.path.isfile("Daten.dat") == True:
	Auswahl = Lese_Daten().rstrip().split('\n')
	Auswahl = DB_clean(Auswahl)
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

#---------------------------------------------

# Ladevorgang und abspielen
FNULL = open(os.devnull, 'w')
if os.path.isfile("Video_Royal.mp4") == True:
	os.remove("Video_Royal.mp4")
#----------------- Puffern _ START
Video_Info = Popen(['wget', '--spider',URL], stdin = PIPE, stderr = PIPE, stdout = PIPE)
while Video_Info.poll() == None:
	fcntl.fcntl(Video_Info.stderr.fileno(),fcntl.F_SETFL,fcntl.fcntl(Video_Info.stderr.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
	buf = ''
	while Video_Info.poll() == None:
		readx_err = select.select([Video_Info.stderr.fileno()], [], [], 0.1)[0]
		if readx_err:
			chunk = Video_Info.stderr.read().decode('utf-8')
			buf += chunk
			#if 'Länge:' in buf:
			buf_array = buf.strip().split()            
		else:
			break
Video_Info.wait()
Index_Laenge = buf_array.index('Länge:') # Der Index, wo das Wort <Länge:> steht. Einen Index später kommt die Zahl 
Lange_Datei_in_MB = int(buf_array[Index_Laenge+1])/(1024*1024)
#################################
VideoDaten = []
# Puffern _ ENDE
Ladevorgang=Popen(["wget","-O","Video_Royal.mp4",URL],stdin = PIPE, stderr = PIPE, stdout = PIPE)
while os.path.isfile("Video_Royal.mp4") == False: 
	time.sleep( 2 )	
x = 0 #Zähler, wie oft die Ladezeit kleiner sein soll, als die Restzeit
while Ladevorgang.poll() == None:
	if x == PUFFER2_in_Anzahl:
		break 
	fcntl.fcntl(Ladevorgang.stderr.fileno(),fcntl.F_SETFL,fcntl.fcntl(Ladevorgang.stderr.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
	buf = ''
	while Ladevorgang.poll() == None and x < PUFFER2_in_Anzahl: # Puffer zwei vielleicht an andere Stelle
		readx_err = select.select([Ladevorgang.stderr.fileno()], [], [], 0.1)[0]
		if readx_err:
			chunk = Ladevorgang.stderr.read().decode('utf-8')
			buf += chunk
			if '\n' in buf and '%' in buf and '.' in buf:
				try:
					Rate_Download = buf.strip().split()[6]
					Video_Geladen = buf.strip().split()[8]
				except IndexError:
					pass
				Rate_Download_Last_Sign = Rate_Download[len(Rate_Download)-1]
				Video_Geladen_Last_Sign = Video_Geladen[len(Video_Geladen)-1]
				if Rate_Download_Last_Sign == 'M' and Video_Geladen_Last_Sign == 'K':                
					Rest_Datei_in_MB = str(Lange_Datei_in_MB - int(Video_Geladen[:-1])/1024)					
					
					# das muss gemacht werden, damit Downloadrate . statt , hat, um damit rechnen zu können  	
					try:
						Rate_converted = Rate_Download[:-1].split(',')[0] +'.'+ Rate_Download[:-1].split(',')[1]	
					except IndexError:
						pass
					float(Rest_Datei_in_MB)					
					Download_Rest_Zeit_in_s = float(Rest_Datei_in_MB)/float(Rate_converted)
					if SENDEZEIT_in_s-Download_Rest_Zeit_in_s > PUFFER_in_s: 		#Prüfen, ob Downloadzeit kleiner als Sendezeit ist			
						x=x+1
					sys.stdout.write("\rVideo startet in: %s" % (PUFFER2_in_Anzahl-x))
					sys.stdout.flush()
					buf = ''
				else:
					break
t = Thread(target=lambda:Ladevorgang.communicate())
t.start()

if str(parser.get('videooptions','player')) == "0":
	Abspielen=subprocess.Popen(["omxplayer","-o","local","-b","Video_Royal.mp4"],stdout=FNULL, stderr=subprocess.STDOUT) # für omxplayer
else:
	Abspielen=subprocess.Popen(["mplayer","-fs","Video_Royal.mp4"],stdout=FNULL, stderr=subprocess.STDOUT)   # für mplayer

while Abspielen.poll() == None:
	pass
print("Programm beenden…")
Ladevorgang.terminate()
if os.path.isfile("Video_Royal.mp4") == True:
	os.remove("Video_Royal.mp4")
print("…das wars schon wieder")

