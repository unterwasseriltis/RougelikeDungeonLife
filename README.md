# VoidDrifter – Raumschiff Roguelike

Ein turn-basiertes Roguelike im Weltraum, entwickelt in Python mit python-tcod.

Sie steuern einen einsamen Überlebenden in einem zerstörten Raumschiff, der durch gefährliche Asteroidenfelder navigiert. Erkunden Sie prozedural generierte Sektoren, kämpfen Sie gegen mutierte Raumkreaturen und versuchen Sie, am Leben zu bleiben.

### Aktueller Entwicklungsstand

- Prozedurale Generierung von Asteroidenfeldern (Cellular Automata)
- Chunk-basiertes Weltsystem (unendlich erweiterbare Karte)
- Vollständiges Entity-Component-System (ECS)
- Field of View mit Fog of War
- HP-System mit klarer Anzeige
- Schadens- und Todesbehandlung mit Game Over Screen
- Erste KI-gesteuerte Kreatur (Raumdrifter), die sich zufällig bewegt
- Saubere System-Architektur (Input, Movement, Render, AI, Damage)

### Technologien

- **Python 3**
- **python-tcod** (libtcod)
- Entity-Component-System (ECS)
- NumPy für effiziente Kartenverarbeitung

### Steuerung

- **Pfeiltasten** → Bewegung
- **T** → Test-Schaden am Spieler (zum Testen)
- **ESC** → Beenden (bei Game Over)

### Installation

```bash
git clone https://github.com/IhrBenutzername/VoidDrifter.git
cd VoidDrifter

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install tcod
python main.py
