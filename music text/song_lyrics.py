import time
import sys

def typewriter_print(text, char_delay=0.06):
    """Print text like a typewriter (character by character)."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(char_delay)
    print()

def print_song_lyrics(song_title, lyrics, char_delay=0.06, line_pause=0.2):
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
    song = """Ho slow motion angreza
              Hun kyun time ganvaye
              Ho slow motion angreza
              Hun kyun time ganvaye
              Seedhe baahon mein bhar le
              Sarsari kyun badhaye
              Meri whiskiye, meri tharriye
              Tu menu chadh gayi, meri soniye
              Roko na, toko na
              Ho mujhko peene do rajke
              Ghul-mil ghul-mil launda ghul-mil ghul-mil
              Ghul-mil ghul-mil launda ghul-mil ghul-mil
              Sing!"""

    song_title = "Kya huwa teraa vada"
    
    print("\n🎶 Welcome to Typewriter Lyrics Display 🎶\n")
    print_song_lyrics(song_title, song, char_delay=0.08, line_pause=0.4)

if __name__ == "__main__":
    main()
