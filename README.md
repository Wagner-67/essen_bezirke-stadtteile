# Essen Stadtbezirke und Stadtteile Visualisierung

Dieses Python-Skript erstellt eine Karte der Stadt **Essen**, auf der die Stadtbezirke und Stadtteile angezeigt werden. Die Bezirke werden als schwarze Grenzen dargestellt, die Stadtteile farbig gefüllt. Zusätzlich werden die Namen von Bezirken und Stadtteilen direkt auf der Karte angezeigt. Eine einfache Maßstabsleiste ist ebenfalls enthalten von chatgpt

---

## Features

- Lädt GeoJSON-Dateien für Bezirke (`stadtbezirke.geojson`) und Stadtteile (`stadtteile.geojson`)
- Ermittelt automatisch die Spalten, die Namen der Bezirke bzw. Stadtteile enthalten
- Transformiert die Geometrien in Web-Mercator (`EPSG:3857`) für eine bessere Darstellung
- Plottet Stadtteile gefüllt und Bezirke nur als Grenzen
- Beschriftet Bezirke und Stadtteile mit ihren Namen
- Fügt eine einfache Maßstabsleiste hinzu
- Speichert die Karte als PNG und PDF

---

## Installation

1. Python 3.x installieren  
2. Benötigte Pakete installieren:

```bash
pip install geopandas matplotlib
