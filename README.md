# VoidDrifter – Raumschiff Roguelike

**VoidDrifter** ist ein turn-basiertes Roguelike im Weltraum-Setting.  
Du steuerst den letzten Überlebenden eines zerstörten Raumschiffs, der durch gefährliche Asteroidenfelder navigieren muss. Erkunde prozedural generierte Sektoren, kämpfe gegen mutierte Raumkreaturen und versuche, so lange wie möglich zu überleben.

Das Projekt befindet sich in einer frühen, aber technisch soliden Entwicklungsphase und dient als Grundlage für ein atmosphärisches Hard-Science-Fiction-Roguelike.

### Aktueller Entwicklungsstand

#### Kern-Features
- **Prozedurale Generierung** von Asteroidenfeldern mittels Cellular Automata
- **Unendlich erweiterbare Welt** durch Chunk-System (derzeit deaktiviert)
- **Vollständiges Entity-Component-System (ECS)** mit klarer Trennung von Daten und Logik
- **Field of View** mit Fog of War (Sichtfeld + erkundete Bereiche)
- **HP-System** mit klarer, mittig unten platzierter Leiste
- **Schadens- und Todesbehandlung** inklusive Game Over Screen
- **Erste KI-gesteuerte Kreatur**: „Raumdrifter“ – bewegt sich zufällig
- **Nahkampf-System**: Der Spieler kann Kreaturen angreifen, wenn er direkt daneben steht
- **Render Order** – Entities werden in der richtigen Reihenfolge gezeichnet
- Saubere System-Architektur (InputSystem, MovementSystem, RenderSystem, AISystem, DamageSystem, CombatSystem)

### Steuerung

- **Pfeiltasten** → Bewegung
- **Leertaste** oder **A** → Nahkampfangriff (wenn direkt neben einer Kreatur)
- **T** → Test-Schaden am Spieler (zum Debuggen)
- **ESC** → Spiel beenden (bei Game Over)

### Technische Umsetzung

- **Sprache**: Python 3.11+
- **Bibliothek**: python-tcod (libtcod)
- **Architektur**: Entity-Component-System (ECS)
- **Kartenverarbeitung**: NumPy + strukturierte Arrays
- **Rendering**: Tile-basiert mit Field of View

### Installation & Ausführung

```bash
git clone https://github.com/IhrBenutzername/VoidDrifter.git
cd VoidDrifter

# Virtuelle Umgebung erstellen
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# Abhängigkeiten installieren
pip install tcod

# Spiel starten
python main.py
