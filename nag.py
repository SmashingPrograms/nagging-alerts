#!/usr/bin/env python3
import time
import subprocess
import random
import os
import signal
import sys

class FocusNag:
    def __init__(self):
        self.nagging_phrases = [
            "CODE. WRITE CODE. RIGHT NOW.",
            "What were you supposed to be working on again?",
        ]
        self.running = True
    
    def signal_handler(self, signum, frame):
        print("\n👋 Focus nag stopped. Good luck staying on task!")
        self.running = False
        sys.exit(0)
    
    def annoying_reminder(self):
        message = random.choice(self.nagging_phrases)
        
        # Visual notification
        subprocess.run(['osascript', '-e', f'display notification "{message}"'])
        
        # Sound
        os.system('afplay /System/Library/Sounds/Funk.aiff')
        
        # Terminal output with timestamp
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] 🚨 {message} 🚨")
    
    def start_nagging(self):
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🎯 Focus Nag started! Reminders every 5 minutes.")
        print("Press Ctrl+C to stop.")
        print("-" * 50)
        
        while self.running:
            time.sleep(300)  # 5 minutes
            if self.running:
                self.annoying_reminder()

if __name__ == "__main__":
    nag = FocusNag()
    nag.start_nagging()