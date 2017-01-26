# ZDF-NEO-ROYAL-f-r-den-Raspberry-Pi
Als waschechter NERD will man ZDF NEO ROYAL über den Raspberry-Pi schauen. Das geht aber nicht, denn viel zu Träge geht das Laden der fiesen Homepage vor sich und als Stream kann man es ohnehin vergessen. Die Lösung: Dieser schlanke Player für die Konsole.

Das Programm muss mit Python 3.x ausgeführt werden. Dabei gibt es eine kurze Abfrage beim ersten Start bezüglich einiger Parameter, welche aber derzeit noch nicht alle berücksichtigt werden, sondern konstant gesetzt sind. Grundsätzlich werden diese  berücksichtigt und in einer config.ini gespeichert. Weiterhin erstellt ihr euch mit dem Code eine Daten.dat, in der der Downloadlink zu den Folgen abgelegt und dann mittels einfacher Menüführung abgerufen wird, will man eine Folge ansehen.

Für das Herunterladen wird wget verwendet, für das Abspielen wird omxplayer oder mplayer – je nach eurer Wahl in der anfänglichen Installationsroutine – verwendet. 
