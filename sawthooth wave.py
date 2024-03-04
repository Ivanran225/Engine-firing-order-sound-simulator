import pyaudio
import numpy as np
from keyboard import is_pressed  # Import for key press detection

# Define parameters
w_pressed_frequency = 150  # Hz (target frequency when 'w' is pressed)
default_frequency = 30  # Hz (default frequency)
increment = 2.5  # Hz per step for smooth transition
duration = 0.3  # seconds
volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz
current_frequency = default_frequency  # Initialize current frequency

def generate_sawtooth(frequency):
  """Generates sawtooth wave samples at the given frequency."""
  samples = np.modf(np.arange(fs * duration) * frequency / fs)[0] * 2.0 - 1.0
  samples = samples.astype(np.float32)  # Ensure float32 format
  return samples

# Create PyAudio object
p = pyaudio.PyAudio()

# Open audio stream (outside the loop for continuous operation)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# Main loop for sound generation and frequency control
while True:
  # Check for 'w' key press
  is_w_down = is_pressed('w')

  # Update frequency based on key press and smooth transition
  if is_w_down and current_frequency < w_pressed_frequency:
    current_frequency = min(current_frequency + increment, w_pressed_frequency)
  elif not is_w_down and current_frequency > default_frequency:
    current_frequency = max(current_frequency - increment, default_frequency)

  # Generate and play sawtooth wave with adjusted frequency
  samples = generate_sawtooth(current_frequency)
  stream.write(volume * samples)
  print(f'Frequency: {current_frequency:.2f} Hz')
  # Check for 'q' key press to terminate
  if is_pressed('q'):
    break

# Close stream and terminate PyAudio after loop exits
stream.stop_stream()
stream.close()
p.terminate()