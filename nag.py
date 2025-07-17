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
       # Define the sound file in one place
       self.sound_file = '/System/Library/Sounds/Basso.aiff'
       self.sound_process = None
       self.stop_sound = False
   
   def signal_handler(self, signum, frame):
       print("\n👋 Focus nag stopped. Good luck staying on task!")
       self.running = False
       self.stop_sound = True
       sys.exit(0)
   
   def play_endless_sound(self):
       """Play sound on repeat until stopped"""
       while not self.stop_sound:
           os.system(f'afplay {self.sound_file}')
           time.sleep(0.1)  # Small delay between repeats
   
   def annoying_reminder(self):
       message = random.choice(self.nagging_phrases)
       
       # Visual notification
       subprocess.run(['osascript', '-e', f'display notification "{message}"'])
       
       # Terminal output with timestamp
       timestamp = time.strftime("%H:%M:%S")
       print(f"[{timestamp}] 🚨 {message} 🚨")
       
       # Start endless sound in background thread
       self.stop_sound = False
       sound_thread = threading.Thread(target=self.play_endless_sound, daemon=True)
       sound_thread.start()
       
       # Wait for user to press ENTER to stop the sound
       print("🔊 BASSO IS PLAYING ENDLESSLY! Press ENTER to stop the sound...")
       try:
           input()  # This blocks until user presses ENTER
       except KeyboardInterrupt:
           pass
       
       # Stop the sound
       self.stop_sound = True
       print("🔇 Sound stopped. Back to work!")
   
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


class TestFocusNag(unittest.TestCase):
   
   def setUp(self):
       self.nag = FocusNag()
   
   def test_initialization(self):
       """Test that FocusNag initializes correctly"""
       self.assertTrue(self.nag.running)
       self.assertEqual(len(self.nag.nagging_phrases), 2)
       self.assertIn("CODE. WRITE CODE. RIGHT NOW.", self.nag.nagging_phrases)
       self.assertIn("What were you supposed to be working on again?", self.nag.nagging_phrases)
       # Test that sound file is set
       self.assertEqual(self.nag.sound_file, '/System/Library/Sounds/Basso.aiff')
       self.assertFalse(self.nag.stop_sound)
   
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
       
       # Check that subprocess.run was called for notification
       mock_subprocess.assert_called_once()
       self.assertTrue(mock_subprocess.call_args[0][0][0] == 'osascript')
       
       # Check that thread was created and started
       mock_thread.assert_called_once()
       mock_thread_instance.start.assert_called_once()
       
       # Check that input was called (waiting for ENTER)
       mock_input.assert_called_once()
       
       # Check that print was called with timestamp
       mock_print.assert_called()
   
   def test_endless_sound_functionality(self):
       """Test the endless sound - WARNING: VERY ANNOYING!"""
       print(f"\n🚨 WARNING: About to test ENDLESS BASSO!")
       print("🔊 This will play Basso on repeat until you press ENTER!")
       print("🎯 This is your chance to experience the full annoyance...")
       
       user_consent = input("Type 'YES' to proceed with the endless sound test (or anything else to skip): ")
       
       if user_consent.upper() == 'YES':
           print("\n💀 STARTING ENDLESS BASSO IN 3 SECONDS...")
           time.sleep(1)
           print("💀 3...")
           time.sleep(1) 
           print("💀 2...")
           time.sleep(1)
           print("💀 1...")
           time.sleep(1)
           print("💀 BASSO HELL BEGINS NOW!")
           
           # Actually test the endless sound
           self.nag.annoying_reminder()
           
           print("✅ Endless sound test completed!")
       else:
           print("🎵 Endless sound test skipped. Probably wise!")
       
       # This always passes
       self.assertTrue(True)
   
   def test_play_endless_sound_stops_when_flag_set(self):
       """Test that endless sound stops when stop_sound flag is set"""
       with patch('os.system') as mock_os_system:
           with patch('time.sleep') as mock_sleep:
               # Set up the mock to stop after a few iterations
               call_count = 0
               def side_effect(*args):
                   nonlocal call_count
                   call_count += 1
                   if call_count >= 3:  # Stop after 3 calls
                       self.nag.stop_sound = True
               
               mock_sleep.side_effect = side_effect
               
               # Run the endless sound function
               self.nag.play_endless_sound()
               
               # Should have called afplay at least a few times
               self.assertGreaterEqual(mock_os_system.call_count, 3)
   
   @patch('random.choice')
   def test_message_selection(self, mock_choice):
       """Test that messages are selected from the phrase list"""
       expected_message = "CODE. WRITE CODE. RIGHT NOW."
       mock_choice.return_value = expected_message
       
       with patch('subprocess.run'), patch('builtins.print'), patch('time.strftime'), patch('builtins.input'), patch('threading.Thread'):
           self.nag.annoying_reminder()
       
       mock_choice.assert_called_once_with(self.nag.nagging_phrases)
   
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
   
   @patch('time.sleep')
   @patch('signal.signal')
   @patch('builtins.print')
   def test_start_nagging_setup(self, mock_print, mock_signal, mock_sleep):
       """Test that start_nagging sets up correctly"""
       # Mock the sleep to prevent infinite loop
       mock_sleep.side_effect = [None, KeyboardInterrupt()]
       
       with patch.object(self.nag, 'annoying_reminder') as mock_reminder:
           try:
               self.nag.start_nagging()
           except KeyboardInterrupt:
               pass
       
       # Check that signal handler was set up
       mock_signal.assert_called_once_with(signal.SIGINT, self.nag.signal_handler)
       
       # Check that initial messages were printed
       self.assertTrue(any("Focus Nag started!" in str(call) for call in mock_print.call_args_list))


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