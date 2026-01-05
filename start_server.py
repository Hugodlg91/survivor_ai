"""
Serveur HTTP local pour L'IA Survivante
Lance un serveur web pour éviter les problèmes CORS
"""

import http.server
import socketserver
import os

# Configuration
PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    """Démarre le serveur HTTP local"""
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("🌐 SERVEUR WEB LOCAL DÉMARRÉ")
        print("=" * 60)
        print()
        print(f"📍 URL de l'overlay : http://localhost:{PORT}/overlay.html")
        print()
        print("🎮 Instructions :")
        print("   1. Copie l'URL ci-dessus")
        print("   2. Colle-la dans ton navigateur")
        print("   3. Lance 'python test_simulation.py' dans un autre terminal")
        print("   4. L'overlay se mettra à jour automatiquement !")
        print()
        print("💡 Pour TikTok Live Studio :")
        print(f"   Source Navigateur → http://localhost:{PORT}/overlay.html")
        print()
        print("⏹️  Appuie sur Ctrl+C pour arrêter le serveur")
        print("=" * 60)
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Serveur arrêté proprement")

if __name__ == "__main__":
    main()
