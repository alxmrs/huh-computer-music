from scipy.io import wavfile

def wav_read(filename):
    """
    Import .wav files from current directory.
    """
    return wavfile.read(filename)[1]

def wav_write(filename, sample_rate, file):
    """
    Export array to .wav file in current directory.
    """
    return wavfile.write(filename, sample_rate, file)
