import webbrowser

def play_music(song_name: str):
    """Play a song on YouTube by opening the search results."""
    url = f"https://www.youtube.com/results?search_query={song_name.strip().replace(' ', '+')}"
    webbrowser.open(url)
