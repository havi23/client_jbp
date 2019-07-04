import esky
import sys

if hasattr(sys,"frozen"):
    app = esky.Esky(sys.executable,"http://teenspirit.com.br/exemplo_boneca/")
    app.auto_update()
