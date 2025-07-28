"""CifraClub Module - Versão com suporte a link direto"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

CIFRACLUB_URL = "https://www.cifraclub.com.br/"

class CifraClub:
    """CifraClub Class - sem Selenium"""
    
    def cifra(self, artist: str, song: str) -> dict:
        result = {}

        # Monta URL amigável
        artist_slug = artist.lower().replace(" ", "-")
        song_slug = song.lower().replace(" ", "-")
        url = CIFRACLUB_URL + f"{artist_slug}/{song_slug}/"
        result['cifraclub_url'] = url

        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception:
            result['error'] = "Erro ao acessar o site do Cifra Club"
            return result

        soup = BeautifulSoup(response.text, 'html.parser')

        # Detalhes
        try:
            result['name'] = soup.find('h1', class_='t1').text.strip()
            result['artist'] = soup.find('h2', class_='t3').text.strip()
            img_youtube = soup.find('div', class_='player-placeholder').img['src']
            cod = img_youtube.split('/vi/')[1].split('/')[0]
            result['youtube_url'] = f"https://www.youtube.com/watch?v={cod}"
        except Exception:
            result['warning'] = "Não foi possível extrair os metadados."

        # Cifra
        try:
            cifra_tag = soup.find('pre')
            if cifra_tag:
                linhas = cifra_tag.get_text().split('\n')
                result['cifra'] = [linha for linha in linhas if linha.strip()]
            else:
                result['cifra'] = []
                result['warning'] = "Cifra não encontrada no HTML."
        except Exception:
            result['error'] = "Erro ao extrair a cifra"

        return result


class CifraClubLink:
    """Classe para extrair cifras a partir de um link completo do Cifra Club"""

    def __init__(self):
        self.cifra_club = CifraClub()

    def cifra(self, full_url: str) -> dict:
        result = {'cifraclub_url': full_url}
        
        try:
            parsed = urlparse(unquote(full_url))
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) < 2:
                result['error'] = "URL inválida. Esperado formato /artista/musica/"
                return result

            artist = path_parts[0]
            song = path_parts[1].replace("cifra.html", "").strip("-/")  # remove sufixo se presente

            return self.cifra_club.cifra(artist, song)
        
        except Exception:
            result['error'] = "Erro ao processar a URL fornecida"
            return result
