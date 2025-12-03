import time
import sys

def typewriter_print(text, char_delay=0.1):
    """Print text like a typewriter (character by character)."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(char_delay)
    print()

def print_song_lyrics(song_title, lyrics, char_delay=0.1, line_pause=0.1):
    """Print song title and lyrics with typewriter effect."""
    print("\n" + "="*50)
    print(f"🎵 {song_title} 🎵")
    print("="*50 + "\n")
    time.sleep(0.5)
    
    lines = lyrics.strip().split('\n')
    for line in lines:
        if line.strip():  # Skip empty lines
            sys.stdout.write("♪ ")
            sys.stdout.flush()
            typewriter_print(line.strip(), char_delay=char_delay)
            time.sleep(line_pause)
        else:
            print()  # Preserve empty lines for verse breaks
            time.sleep(0.4)
    
    print("\n")

def main():
    # Single song lyrics
    song = """Keh doon tumhe ya chup rahu Dill mein mere 
    aaj kyaa hai Jo bolo toh janu Guru tumko manu Chalo 
    ye bhi waada hai Socha hai tumane ke chalte he jaaye 
    Taaro se aage koi duniyaan basaye Sochaa hain ye ke tumhe
    rasta bhulaye Suni jagah peh kahi chhedhe daraye Are naa
    naa, Haaye re naa naa, Ye naa kehna Arre nahi re, 
    nahi re, nahi re, Nahi re, nahi re, nahi re, nahi
    re Nahi nahi"""

    song_title = "Sajde"
    
    print("\n🎶 Welcome to Typewriter Lyrics Display 🎶\n")
    print_song_lyrics(song_title, song, char_delay=0.18, line_pause=1.2)

if __name__ == "__main__":
    main()
