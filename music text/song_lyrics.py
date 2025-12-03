import time
import sys

def typewriter_print(text, char_delay=0.02):
    """Print text like a typewriter (character by character)."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(char_delay)
    print()

def print_song_lyrics(song_title, lyrics, char_delay=0.02, line_pause=0.5):
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
            time.sleep(0.3)
    
    print("\n")

def main():
    # Single song lyrics
    song = """Sajde bichhawan ve gali gali Ho gali gali, 
    ho gali gali Jis shehar vich mera yaar vasda Kamaana 
    painda ae khad ke, ho khad ke Ho etthe rab na koi udhar 
    labda Ek khwaab ne aakhein kholi hain Kya mod aaya hai
    kahani mein Woh bheeg rahi hai barish mein Hmm aur aag 
    lagi hai paani mein"""

    song_title = "Yesterday - sahiba"
    
    print("\n🎶 Welcome to Typewriter Lyrics Display 🎶\n")
    print_song_lyrics(song_title, song, char_delay=0.03, line_pause=0.4)

if __name__ == "__main__":
    main()
