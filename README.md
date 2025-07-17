# Focus Nag 🎪

**The most annoying productivity tool ever created.**

A Python script that uses the scientifically proven most irritating sound ever made (the Crazy Bus theme) to psychologically terrorize you into being productive. Every 5 minutes, it downloads and plays the Crazy Bus theme song on endless repeat until you press ENTER and get back to work.

## Features 🚨

- **Live countdown timer** - Always know exactly how much time you have left before audio hell
- **Auto-downloads Crazy Bus theme** - Automatically fetches the most annoying sound known to humanity
- **Endless audio loop** - Plays the theme on repeat until you manually stop it
- **Process tracking & killing** - Properly terminates audio processes (no more orphaned sounds!)
- **Auto-installs dependencies** - Checks for and installs yt-dlp if needed
- **macOS notifications** - Desktop alerts to complement the audio nightmare
- **Comprehensive tests** - Because even chaos needs quality assurance

## Installation 📦

```bash
git clone https://github.com/SmashingPrograms/nagging-alerts
cd focus-nag
```

**Requirements:**
- Python 3.6+
- macOS (uses `afplay` and `osascript`)
- Internet connection (for downloading the Crazy Bus theme)

The script will automatically install `yt-dlp` if it's not present.

## Usage 🎯

### Start the Focus Nag
```bash
python3 nag.py
```

This will:
1. Check for dependencies and install if needed
2. Download the Crazy Bus theme (if not already present)
3. Start a 5-minute countdown timer
4. When timer hits zero: **UNLEASH AUDIO CHAOS**
5. Play Crazy Bus theme endlessly until you press ENTER
6. Reset timer and repeat

### Run Tests
```bash
python3 nag.py --tests
```

**Warning:** One test (`test_endless_crazy_bus_functionality`) will actually play the sound if you consent. Type 'CHAOS' when prompted to experience the full horror.

### Stop the Nag
- Press **ENTER** during audio playback to stop the current sound
- Press **Ctrl+C** at any time to quit the program entirely

## How It Works 🔧

1. **Timer Display**: Shows live countdown in format `⏰ Next nag in: 04:23`
2. **Audio Download**: Uses `yt-dlp` to fetch Crazy Bus theme from YouTube (video ID: `sC0cvwnG0Ik`)
3. **Process Management**: Uses `subprocess.Popen` to track audio processes for proper cleanup
4. **Endless Loop**: Starts audio in background thread, repeats until `stop_sound` flag is set
5. **Nuclear Cleanup**: Uses `pkill -f afplay` to ensure no orphaned audio processes

## File Structure 📁

```
.
├── nag.py                                    # Main script
├── Crazy Bus Title Screen [sC0cvwnG0Ik].m4a # Auto-downloaded (gitignored)
├── .gitignore                                # Protects humanity from Crazy Bus
└── README.md                                 # This file
```

## Configuration ⚙️

You can modify these variables in the `FocusNag` class:

```python
self.reminder_interval = 300  # 5 minutes in seconds
self.nagging_phrases = [
    "CODE. WRITE CODE. RIGHT NOW.",
    "What were you supposed to be working on again?",
]
```

## The Science Behind This Madness 🧬

The Crazy Bus theme song is widely considered one of the most annoying audio compositions ever created. Originally from a 2004 educational game, it features:

- Discordant carnival-style music
- Chaotic, unpredictable rhythm  
- Frequencies designed to trigger psychological discomfort
- No musical resolution or satisfaction

**This makes it perfect for productivity:** Your brain will desperately want to make it stop, forcing you to press ENTER and return to work.

## Warning ⚠️

**This tool is psychologically intense.** The Crazy Bus theme is genuinely difficult to listen to and may cause:
- Immediate desire to be productive
- Auditory discomfort
- Psychological motivation to avoid procrastination
- Neighbors asking what that horrible sound is

**Use responsibly.** Start with shorter intervals if you're not sure you can handle the full 5-minute experience.

## Troubleshooting 🔧

### Audio won't stop
```bash
# Nuclear option - kill all audio
sudo pkill -f afplay
```

### Can't download Crazy Bus theme
The script will fall back to macOS system sound `Basso.aiff` if download fails.

### Tests failing
Make sure you have a stable internet connection and that YouTube hasn't changed their API.

### "This is too evil"
Working as intended. That's the point.

## Contributing 🤝

This project is intentionally simple and chaotic. Potential improvements:

- [ ] Windows/Linux support (different audio players)
- [ ] Configurable audio files (though nothing beats Crazy Bus)
- [ ] Statistics tracking (time focused vs. time procrastinating)
- [ ] Integration with productivity apps
- [ ] Volume controls (currently relies on system volume)

## License 📄

This project is released under the "Use At Your Own Psychological Risk" license. 

The Crazy Bus theme song is automatically downloaded from YouTube and remains the intellectual property of its original creators. We use it here for the noble purpose of combating procrastination through audio-based psychological warfare.

## Acknowledgments 🙏

- **The creators of Crazy Bus** - For accidentally creating the perfect productivity tool
- **Every procrastinator** who will suffer beautifully while using this

---

**Remember: You're not just fighting procrastination. You're continuing a cultural lineage that stretches from 1928's "Sonny Boy" through 2004's Crazy Bus to your productive future.** 🎪✨

*Happy coding! (You literally have no choice now.)*