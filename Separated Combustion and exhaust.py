import time
import numpy as np
import pyaudio

def play_tone(f, volume=0.5, fs=44100, duration=0.01):
    """
    Plays a tone with the specified frequency, volume, sampling rate, and duration.

    Args:
        f: The frequency of the tone (Hz).
        volume: The volume of the tone (range [0.0, 1.0]).
        fs: The sampling rate (Hz).
        duration: The duration of the tone (seconds).
    """

    # Generate samples
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

    # Convert to bytes
    output_bytes = (volume * samples).tobytes()

    # Open audio stream (outside the function)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # Play the sound
    stream.write(output_bytes)

    # Close the stream (outside the with block)
    stream.stop_stream()
    #stream.close()

if __name__ == "__main__":
  # Example usage: Play three tones with different frequencies
  #Frecuencies for each cilinder,
  C1 = 440
  C2 = 450
  C3 = 460
  C4 = 470

  E1 = 300
  E2 = 310
  E3 = 320
  E4 = 330

  combustion_frequencies = [C1, C2, C3, C4]
  exhaust_frequencies = [E1, E2, E3, E4]
  # Specify firing order in a separate list
  firing_order = [1, 3, 2, 4]
  total_duration = 3  # Duration in seconds (adjust as needed)
  start_time = time.time()
  while time.time() - start_time < total_duration:
      for index in firing_order:
        play_tone(combustion_frequencies[firing_order[index - 1] - 1])  # Play combustion
        play_tone(exhaust_frequencies[firing_order[index - 1] - 1])  # Play exhaust