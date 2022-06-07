![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true](https://github.com/mkemper1/PP21-Mink_Kemper/blob/main/praxis_projekt_ss_2022/resources/assets/logo.png)
# PP21-Mink_Kemper

## Abstract
Während einer Ausgrabung werden sequentiell Schichten einer Fundstelle entfernt, um die darunter liegenden Erdschichten oder Gegenstände freizulegen. Jeder dieser Arbeitsschritte sorgt dafür, dass ein irreparabeler Schaden entsteht, welcher nicht rückwirkend aufgebessert werden kann. Um diesem Verlust zuvor zu kommen, werden Technologien wie Drohnen eingesetzt, um einen Scan des aktuellen Stands der Ausgrabung festzuhalten. Die daraus entstehenden Daten können durch den Einsatz von spezieller Software, bearbeitet und ausgewertet werden. Das Projekt baut auf einem, abgeschlossenen Master Projekt auf. Damals war es das Ziel, ein digitales Feldbuch zu entwicklen, welches allerdings zur Fertigstellung nicht die Möglichkeit bot, eingehende Daten im dreidimensionalem Raum zu bearbeiten.

Das Ziel ist es, eine unabhängige Erweiterung des bestehenden Systems zu erstellen, welches neben dem Erfüllen der damals nicht erreichten Anforderungen, auch neue Funktionen, welche aus dem direktenGespräch mit den Archäologen entstehen können, implementiert. Um ein System, welches speziell für die Umsetzung einer Menge an
Anforderungen, die in einem definierten Kontext gestellt sind, zu realisieren, muss sowohl Backend, als auch Frontend geplant und erstellt werden. Dies erfordert das Einarbeiten in das Themengebiet und die Recherche benötigter Ressourcen. Auf dieser Basis, wird ein Prototyp erstellt, welcher auf Absprache im Team in darauf folgenden Iterationsphasen weiter verbessert und angepasst wird.

Das Ergebnis stellt eine 3D-Anwendungssoftware dar, welche es ermöglicht, einkommende Daten eines Scans zu verarbeiten und darzustellen. Dem Benutzer des System wird dazu die Möglichkeit geboten, verschiedene Tätigkeiten, wie dem Extrahieren bestimmter Bereiche des Modells, durchzuf¨uhren. Das daraus entstandene, bearbeitet Modell kann als GeoTiff, einer abgewandelten Form des .tiff-Format, ausgegeben und gespeichert werden.


## Python Version
3.9

## Libraries
- os
- sys
- re
- time
- shutil
- subprocess
- pyvista
- pyvistaqt
- PyQt5
- pymeshlab
- pyacvd
- numpy
- mathplotlib
- functools
- fiona (.whl: https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
- gdal (.whl: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
- rasterio (.whl: https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio)
- geopandas

## Bemerkung
Aufgrund von Datenschutz können Datensätze der Ausgrabung nicht in diesem Repository hinterlegt werden.
