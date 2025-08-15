import webbrowser

def open_website(site_name: str):
    """Open a website by name (e.g., 'youtube', 'google')."""
    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.com",
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com",
        "whatsapp": "https://www.whatsapp.com",
        "github": "https://www.github.com"
    }
    url = sites.get(site_name.lower())
    if url:
        webbrowser.open(url)
        return True
    return False

def open_url(url: str):
    """Open a given URL in the default browser."""
    webbrowser.open(url)

def google_search(query: str):
    """Perform a Google search for the given query."""
    url = f"https://www.google.com/search?q={query.strip().replace(' ', '+')}"
    webbrowser.open(url)
