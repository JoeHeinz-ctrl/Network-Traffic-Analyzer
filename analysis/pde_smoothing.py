import numpy as np
from scipy.ndimage import gaussian_filter

def smooth_traffic_pde(traffic_matrix: np.ndarray, sigma: float = 2.0) -> np.ndarray:
    """Apply PDE-based smoothing using Gaussian filter."""
    smoothed = gaussian_filter(traffic_matrix, sigma=sigma, mode='reflect')
    return smoothed
