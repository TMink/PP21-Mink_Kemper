# PP21-Mink_Kemper

## Abstract
W¨ahrend einer Ausgrabung werden sequentiell Schichten einer
Fundstelle entfernt, um die darunter liegenden Erdschichten oder
Gegenst¨ande freizulegen. Jeder dieser Arbeitsschritte sorgt daf¨ur,
dass ein irreparabeler Schaden entsteht, welcher nicht r¨uckwirkend
aufgebessert werden kann. Um diesem Verlust zuvor zu kommen, werden Technologien wie Drohnen eingesetzt, um einen Scan des aktuellen
Stands der Ausgrabung festzuhalten. Die daraus entstehenden Daten
k¨onnen durch den Einsatz von spezieller Software, bearbeitet und ausgewertet werden.
Das Projekt baut auf einem, abgeschlossenen Master Projekt auf.
Damals war es das Ziel, ein digitales Feldbuch zu entwicklen, welches
allerdings zur Fertigstellung nicht die M¨oglichkeit bot, eingehende
Daten im dreidimensionalem Raum zu bearbeiten.
Das Ziel ist es, eine unabh¨angige Erweiterung des bestehenden Systems zu erstellen, welches neben dem Erf¨ullen der damals nicht erreichten Anforderungen, auch neue Funktionen, welche aus dem direkten
Gespr¨ach mit den Arch¨aologen entstehen k¨onnen, implementiert.
Um ein System, welches speziell f¨ur die Umsetzung einer Menge an
Anforderungen, die in einem definierten Kontext gestellt sind, zu realisieren, muss sowohl Backend, als auch Frontend geplant und erstellt
werden. Dies erfordert das Einarbeiten in das Themengebiet und die
Recherche ben¨otigter Ressourcen. Auf dieser Basis, wird ein Prototyp
erstellt, welcher auf Absprache im Team in darauf folgenden Iterationsphasen weiter verbessert und angepasst wird.
Das Ergebnis stellt eine 3D-Anwendungssoftware dar, welche es erm¨oglicht,
einkommende Daten eines Scans zu verarbeiten und darzustellen. Dem
Benutzer des System wird dazu die M¨oglichkeit geboten, verschiedene
T¨atigkeiten, wie dem Extrahieren bestimmter Bereiche des Modells,
durchzuf¨uhren. Das daraus entstandene, bearbeitet Modell kann als
GeoTiff, einer abgewandelten Form des .tiff-Format, ausgegeben und
gespeichert werden.


## Python Version
3.9

## Libraries
- pyvista
- PyQt5
- sys
- os
- pyvistaqt
- shutil
- pymeshlab
- pyacvd
- geopandas
- numpy
- subprocess
- re
- mathplotlib
- functools
- rasterio
- time
- fiona
- gdal
