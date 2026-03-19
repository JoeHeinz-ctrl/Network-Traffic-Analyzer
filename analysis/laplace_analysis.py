import numpy as np

def analyze_frequency_spectrum(time_series: np.ndarray, sampling_rate: float = 1.0) -> dict:
    """Perform FFT to extract frequency components."""
    n = len(time_series)
    
    fft_values = np.fft.fft(time_series)
    fft_freq = np.fft.fftfreq(n, d=1.0/sampling_rate)
    
    positive_freq_idx = fft_freq > 0
    frequencies = fft_freq[positive_freq_idx]
    magnitudes = np.abs(fft_values[positive_freq_idx])
    
    top_5_idx = np.argsort(magnitudes)[-5:][::-1]
    top_5_frequencies = frequencies[top_5_idx].tolist()
    
    return {
        'frequencies': frequencies,
        'magnitudes': magnitudes,
        'top_5_frequencies': top_5_frequencies
    }
