# Qud-like Roguelite

Ein turn-basiertes Roguelite in Entwicklung, inspiriert von **Caves of Qud**.  
Ziel ist es, eine tiefgehende, prozedural generierte Welt mit organischen Höhlen, Simulation und atmosphärischer Tile-Grafik zu schaffen.

## Über das Projekt

Dieses Projekt ist ein reines Code-basiertes Roguelike, das mit **Python** und der Bibliothek **python-tcod** entwickelt wird.  
Der Fokus liegt auf:
- Prozeduraler Höhlengenerierung mittels Cellular Automata
- Field of View (Sichtfeld) und Fog of War
- Turn-basierter Bewegung
- Modularer Architektur (vorbereitet für Entity-Component-System)
- Visuellem Stil, der an *Caves of Qud* angelehnt ist

## Technische Grundlage

- **Sprache**: Python 3.11+
- **Bibliothek**: [python-tcod](https://github.com/libtcod/python-tcod) (Version 21.x)
- **Entwicklungsumgebung**: Visual Studio Code
- **Rendering**: Tile-basiertes Konsolen-Rendering mit eigenem Tileset
- **Map-Generierung**: Cellular Automata für organische, höhlenartige Karten

## Features (aktueller Stand)

- ✅ Prozedurale Höhlengenerierung mit Cellular Automata
- ✅ Kollisionserkennung (nur begehbare Felder)
- ✅ Field of View mit Shadow-Casting-Algorithmus
- ✅ Exploration-System (Fog of War: erkundete Bereiche bleiben sichtbar)
- ✅ Saubere Trennung von Map, Rendering und Input
- ✅ Modulare Projektstruktur

## Projektstruktur
