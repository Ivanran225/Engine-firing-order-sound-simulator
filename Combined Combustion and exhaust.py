import time
import numpy as np
import pyaudio

def play_tones(frequencies, volume=0.5, fs=44100, duration=0.01):
    """
    Plays multiple tones with the specified frequencies, volume, sampling rate, and duration.

    Args:
        frequencies: A list of frequencies (Hz) to play.
        volume: The volume of the tones (range [0.0, 1.0]).
        fs: The sampling rate (Hz).
        duration: The duration of each tone (seconds).
    """

    # Combine samples for multiple frequencies
    samples = np.zeros(int(fs * duration), dtype=np.float32)
    for f in frequencies:
        samples += np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)

    # Normalize for volume and convert to bytes
    output_bytes = (volume * samples / len(frequencies)).astype(np.float32).tobytes()

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
    stream.close()
    p.terminate()  # Close PyAudio instance (optional)

if __name__ == "__main__":
  # Example usage: Play three tones with different frequencies
  #Frecuencies for each cilinder,
  C1 = 440
  C2 = 460
  C3 = 480
  C4 = 500

  E1 = 700
  E2 = 720
  E3 = 740
  E4 = 760

  combustion_frequencies = [C1, C2, C3, C4]
  exhaust_frequencies = [E1, E2, E3, E4]
  # Specify firing order in a separate list
  firing_order = [1, 3, 2, 4]
  total_duration = 3  # Duration in seconds
  start_time = time.time()  # Track start time

while time.time() - start_time < total_duration:
    for index in firing_order:
        combined_frequencies = [combustion_frequencies[index - 1], exhaust_frequencies[index - 1]]
        play_tones(combined_frequencies)