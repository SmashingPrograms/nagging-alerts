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


class TestFocusNag(unittest.TestCase):
   
   def setUp(self):
       self.nag = FocusNag()
   
   def test_initialization(self):
       """Test that FocusNag initializes correctly"""
       self.assertTrue(self.nag.running)
       self.assertEqual(len(self.nag.nagging_phrases), 2)
       self.assertIn("CODE. WRITE CODE. RIGHT NOW.", self.nag.nagging_phrases)
       self.assertIn("What were you supposed to be working on again?", self.nag.nagging_phrases)
   
   @patch('subprocess.run')
   @patch('os.system')
   @patch('builtins.print')
   @patch('time.strftime')
   def test_annoying_reminder(self, mock_strftime, mock_print, mock_os_system, mock_subprocess):
       """Test that annoying_reminder calls all the right functions"""
       mock_strftime.return_value = "12:34:56"
       
       self.nag.annoying_reminder()
       
       # Check that subprocess.run was called for notification
       mock_subprocess.assert_called_once()
       self.assertTrue(mock_subprocess.call_args[0][0][0] == 'osascript')
       
       # Check that sound was played
       mock_os_system.assert_called_once_with('afplay /System/Library/Sounds/Funk.aiff')
       
       # Check that print was called with timestamp
       mock_print.assert_called()
       print_call = mock_print.call_args[0][0]
       self.assertIn("[12:34:56]", print_call)
       self.assertIn("🚨", print_call)
   
   def test_actual_sound_playback(self):
       """Test that actually plays the sound so you can hear it"""
       print("\n🔊 Testing actual sound playback - you should hear the Funk sound!")
       
       # Don't mock anything - let it actually play
       with patch('subprocess.run'), patch('builtins.print'):
           # Only mock the notification and print, but let sound play
           message = "TEST SOUND - Can you hear this?"
           
           # Play the actual sound
           os.system('afplay /System/Library/Sounds/Funk.aiff')
           
           # Give it a moment to play
           time.sleep(1)
           
           print("🎵 Sound test completed!")
       
       # This always passes - it's just for hearing the sound
       self.assertTrue(True)
   
   @patch('random.choice')
   def test_message_selection(self, mock_choice):
       """Test that messages are selected from the phrase list"""
       expected_message = "CODE. WRITE CODE. RIGHT NOW."
       mock_choice.return_value = expected_message
       
       with patch('subprocess.run'), patch('os.system'), patch('builtins.print'), patch('time.strftime'):
           self.nag.annoying_reminder()
       
       mock_choice.assert_called_once_with(self.nag.nagging_phrases)
   
   def test_signal_handler(self):
       """Test that signal handler stops the nag"""
       self.assertTrue(self.nag.running)
       
       with patch('sys.exit') as mock_exit:
           with patch('builtins.print'):
               self.nag.signal_handler(signal.SIGINT, None)
       
       self.assertFalse(self.nag.running)
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
   
   @patch('time.sleep')
   @patch('signal.signal')
   @patch('builtins.print')
   def test_nagging_loop(self, mock_print, mock_signal, mock_sleep):
       """Test that the nagging loop calls reminder after sleep"""
       call_count = 0
       
       def side_effect(*args):
           nonlocal call_count
           call_count += 1
           if call_count >= 2:  # Stop after 2 calls
               self.nag.running = False
           return None
       
       mock_sleep.side_effect = side_effect
       
       with patch.object(self.nag, 'annoying_reminder') as mock_reminder:
           self.nag.start_nagging()
       
       # Should sleep 300 seconds (5 minutes) each time
       mock_sleep.assert_called_with(300)
       # Should call reminder once (stopped before second call)
       mock_reminder.assert_called_once()


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