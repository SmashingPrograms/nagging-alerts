#!/usr/bin/env python3
import time
import subprocess
import random
import os
import signal
import sys
import unittest
from unittest.mock import patch, MagicMock
import argparse
import threading

class FocusNag:
   def __init__(self):
       self.nagging_phrases = [
           "CODE. WRITE CODE. RIGHT NOW.",
           "What were you supposed to be working on again?",
       ]
       self.running = True
       self.sound_file = './Crazy Bus Title Screen [sC0cvwnG0Ik].m4a'
       self.sound_processes = []  # Track all audio processes
       self.stop_sound = False
       self.reminder_interval = 300
       self.start_time = None
   
   def check_dependencies(self):
       """Check for yt-dlp and install if needed"""
       print("🔍 Checking dependencies...")
       
       try:
           subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
           print("✅ yt-dlp is installed")
       except (subprocess.CalledProcessError, FileNotFoundError):
           print("📦 yt-dlp not found. Installing...")
           try:
               subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
               print("✅ yt-dlp installed successfully")
           except subprocess.CalledProcessError:
               print("❌ Failed to install yt-dlp. Please install manually: pip install yt-dlp")
               sys.exit(1)
   
   def download_crazy_bus(self):
       """Download the Crazy Bus theme if it doesn't exist"""
       if not os.path.exists(self.sound_file):
           print("🎪 Crazy Bus theme not found. Downloading the audio nightmare...")
           try:
               subprocess.run(['yt-dlp', 'sC0cvwnG0Ik', '-f', '140'], check=True)
               print("💀 Crazy Bus theme downloaded successfully. Prepare for chaos!")
           except subprocess.CalledProcessError:
               print("❌ Failed to download Crazy Bus theme. Falling back to Basso...")
               self.sound_file = '/System/Library/Sounds/Basso.aiff'
       else:
           print("🎪 Crazy Bus theme found. Audio chaos ready!")
   
   def setup_audio(self):
       """Setup audio file - check dependencies and download if needed"""
       self.check_dependencies()
       self.download_crazy_bus()
   
   def kill_all_audio(self):
       """Kill all audio processes immediately"""
       print("🔇 KILLING ALL AUDIO PROCESSES...")
       
       # Kill all tracked processes
       for process in self.sound_processes:
           try:
               process.terminate()
               process.wait(timeout=1)
           except:
               try:
                   process.kill()
               except:
                   pass
       
       # Nuclear option - kill all afplay processes
       try:
           subprocess.run(['pkill', '-f', 'afplay'], capture_output=True)
       except:
           pass
       
       self.sound_processes.clear()
       self.stop_sound = True
   
   def signal_handler(self, signum, frame):
       print("\n👋 Focus nag stopped. Killing audio...")
       self.running = False
       self.kill_all_audio()
       sys.exit(0)
   
   def play_endless_sound(self):
       """Play sound on repeat until stopped - WITH PROPER PROCESS TRACKING"""
       while not self.stop_sound:
           try:
               # Use subprocess.Popen instead of os.system so we can control it
               if self.sound_file.endswith('.m4a'):
                   process = subprocess.Popen(['afplay', self.sound_file])
               else:
                   process = subprocess.Popen(['afplay', self.sound_file])
               
               # Track this process
               self.sound_processes.append(process)
               
               # Wait for it to finish or be killed
               process.wait()
               
               # Remove from tracking when done
               if process in self.sound_processes:
                   self.sound_processes.remove(process)
               
               time.sleep(0.1)  # Small delay between repeats
           except Exception as e:
               break
   
   def get_time_remaining(self):
       """Get remaining time until next reminder"""
       if self.start_time is None:
           return self.reminder_interval
       
       elapsed = time.time() - self.start_time
       remaining = self.reminder_interval - (elapsed % self.reminder_interval)
       return int(remaining)
   
   def format_time(self, seconds):
       """Format seconds as MM:SS"""
       minutes = seconds // 60
       seconds = seconds % 60
       return f"{minutes:02d}:{seconds:02d}"
   
   def display_timer(self):
       """Display countdown timer"""
       remaining = self.get_time_remaining()
       time_str = self.format_time(remaining)
       print(f"\r⏰ Next nag in: {time_str}  ", end="", flush=True)
   
   def annoying_reminder(self):
       message = random.choice(self.nagging_phrases)
       
       # Clear the timer line
       print("\r" + " " * 50)
       
       # Visual notification
       subprocess.run(['osascript', '-e', f'display notification "{message}"'])
       
       # Terminal output with timestamp
       timestamp = time.strftime("%H:%M:%S")
       print(f"\n[{timestamp}] 🚨 {message} 🚨")
       
       # Start endless sound in background thread
       self.stop_sound = False
       sound_thread = threading.Thread(target=self.play_endless_sound, daemon=True)
       sound_thread.start()
       
       # Wait for user to press ENTER to stop the sound
       if self.sound_file.endswith('.m4a'):
           print("🎪 CRAZY BUS IS PLAYING ENDLESSLY! Press ENTER to KILL THE AUDIO NIGHTMARE...")
       else:
           print("🔊 BASSO IS PLAYING ENDLESSLY! Press ENTER to stop the sound...")
       
       try:
           input()  # This blocks until user presses ENTER
       except KeyboardInterrupt:
           pass
       
       # PROPERLY KILL ALL AUDIO
       self.kill_all_audio()
       print("💀 Audio processes terminated with extreme prejudice!")
       print("-" * 50)
   
   def start_nagging(self):
       self.setup_audio()
       signal.signal(signal.SIGINT, self.signal_handler)
       
       print("🎯 Focus Nag started! Reminders every 5 minutes.")
       print("Press Ctrl+C to stop.")
       print("-" * 50)
       
       self.start_time = time.time()
       
       while self.running:
           self.display_timer()
           time.sleep(1)
           
           if self.get_time_remaining() <= 0:
               self.annoying_reminder()
               self.start_time = time.time()


class TestFocusNag(unittest.TestCase):
   
   def setUp(self):
       self.nag = FocusNag()
   
   def test_initialization(self):
       """Test that FocusNag initializes correctly"""
       self.assertTrue(self.nag.running)
       self.assertEqual(len(self.nag.nagging_phrases), 2)
       self.assertIn("CODE. WRITE CODE. RIGHT NOW.", self.nag.nagging_phrases)
       self.assertIn("What were you supposed to be working on again?", self.nag.nagging_phrases)
       # Test that sound file is set to Crazy Bus
       self.assertEqual(self.nag.sound_file, './Crazy Bus Title Screen [sC0cvwnG0Ik].m4a')
       self.assertFalse(self.nag.stop_sound)
   
   def test_time_formatting(self):
       """Test time formatting function"""
       self.assertEqual(self.nag.format_time(0), "00:00")
       self.assertEqual(self.nag.format_time(60), "01:00")
       self.assertEqual(self.nag.format_time(125), "02:05")
       self.assertEqual(self.nag.format_time(300), "05:00")
   
   @patch('subprocess.run')
   @patch('builtins.print')
   @patch('time.strftime')
   @patch('builtins.input')
   @patch('threading.Thread')
   def test_annoying_reminder(self, mock_thread, mock_input, mock_strftime, mock_print, mock_subprocess):
       """Test that annoying_reminder calls all the right functions"""
       mock_strftime.return_value = "12:34:56"
       mock_input.return_value = ""  # Simulate pressing ENTER immediately
       
       # Mock the thread
       mock_thread_instance = MagicMock()
       mock_thread.return_value = mock_thread_instance
       
       self.nag.annoying_reminder()
       
       # Check that subprocess.run was called multiple times (notification + pkill)
       self.assertGreaterEqual(mock_subprocess.call_count, 2)
       
       # Check specifically that the notification was called
       notification_calls = [call for call in mock_subprocess.call_args_list 
                           if 'osascript' in str(call)]
       self.assertEqual(len(notification_calls), 1)
       
       # Check specifically that pkill was called for cleanup
       pkill_calls = [call for call in mock_subprocess.call_args_list 
                     if 'pkill' in str(call)]
       self.assertEqual(len(pkill_calls), 1)
       
       # Check that thread was created and started
       mock_thread.assert_called_once()
       mock_thread_instance.start.assert_called_once()
       
       # Check that input was called (waiting for ENTER)
       mock_input.assert_called_once()
   
   @patch('os.path.exists')
   @patch('subprocess.run')
   def test_crazy_bus_download_needed(self, mock_subprocess, mock_exists):
       """Test that Crazy Bus downloads when file doesn't exist"""
       mock_exists.return_value = False  # File doesn't exist
       mock_subprocess.return_value = MagicMock()  # Mock successful command
       
       self.nag.download_crazy_bus()
       
       # Should have called yt-dlp to download
       calls = [call for call in mock_subprocess.call_args_list if 'yt-dlp' in str(call)]
       self.assertTrue(len(calls) > 0)
   
   @patch('os.path.exists')
   def test_crazy_bus_already_exists(self, mock_exists):
       """Test that download is skipped when file exists"""
       mock_exists.return_value = True  # File exists
       
       # This should complete without error
       self.nag.download_crazy_bus()
       
       # Sound file should still be set to Crazy Bus
       self.assertEqual(self.nag.sound_file, './Crazy Bus Title Screen [sC0cvwnG0Ik].m4a')
   
   def test_endless_crazy_bus_functionality(self):
       """Test the endless Crazy Bus - WARNING: MAXIMUM ANNOYANCE!"""
       print(f"\n🎪 WARNING: About to test ENDLESS CRAZY BUS!")
       print("💀 This will play the most annoying sound ever created on repeat!")
       print("🧠 This may cause psychological damage...")
       
       user_consent = input("Type 'CHAOS' to proceed with the Crazy Bus test (or anything else to skip): ")
       
       if user_consent.upper() == 'CHAOS':
           print("\n💀 DOWNLOADING AND STARTING CRAZY BUS IN 3 SECONDS...")
           
           # Setup audio (this will download if needed)
           self.nag.setup_audio()
           
           time.sleep(1)
           print("💀 3...")
           time.sleep(1) 
           print("💀 2...")
           time.sleep(1)
           print("💀 1...")
           time.sleep(1)
           print("🎪 CRAZY BUS HELL BEGINS NOW!")
           
           # Actually test the endless sound
           self.nag.annoying_reminder()
           
           print("✅ Crazy Bus test completed! You survived!")
       else:
           print("🎵 Crazy Bus test skipped. Your sanity thanks you!")
       
       # This always passes
       self.assertTrue(True)
   
   def test_signal_handler(self):
       """Test that signal handler stops the nag"""
       self.assertTrue(self.nag.running)
       self.assertFalse(self.nag.stop_sound)
       
       with patch('sys.exit') as mock_exit:
           with patch('builtins.print'):
               self.nag.signal_handler(signal.SIGINT, None)
       
       self.assertFalse(self.nag.running)
       self.assertTrue(self.nag.stop_sound)
       mock_exit.assert_called_once_with(0)


def run_tests():
   """Run the test suite"""
   print("🧪 Running FocusNag tests...")
   print("=" * 50)
   
   # Create test suite
   loader = unittest.TestLoader()
   suite = loader.loadTestsFromTestCase(TestFocusNag)
   
   # Run tests with verbose output
   runner = unittest.TextTestRunner(verbosity=2)
   result = runner.run(suite)
   
   # Print summary
   print("\n" + "=" * 50)
   if result.wasSuccessful():
       print("✅ All tests passed! Your nag is ready to annoy you properly.")
   else:
       print("❌ Some tests failed. Your nag might not work correctly.")
       print(f"Failures: {len(result.failures)}")
       print(f"Errors: {len(result.errors)}")
   
   return result.wasSuccessful()


if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="Focus Nag - Productivity reminder tool")
   parser.add_argument('--tests', action='store_true', help='Run automated tests')
   
   args = parser.parse_args()
   
   if args.tests:
       run_tests()
   else:
       nag = FocusNag()
       nag.start_nagging()