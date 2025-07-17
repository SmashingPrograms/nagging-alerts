import time
import subprocess
import random
import os

class FocusNag:
    def __init__(self):
        self.nagging_phrases = [
            "HEY! Portfolio project! NOW!",
            "Stop researching random film history!",
            "The streaming app won't build itself!",
            "CODE. WRITE CODE. RIGHT NOW.",
        ]
    
    def annoying_reminder(self):
        message = random.choice(self.nagging_phrases)
        
        # Visual notification
        subprocess.run(['osascript', '-e', f'display notification "{message}"'])
        
        # MAKE NOISE (choose one):
        # Option 1: System beep
        os.system('afplay /System/Library/Sounds/Funk.aiff')
        
        # Option 2: Multiple beeps for extra annoyance
        for _ in range(3):
            print('\a')  # Terminal bell sound
            time.sleep(0.5)
        
        print(f"\n🚨 FOCUS ALERT: {message} 🚨\n")