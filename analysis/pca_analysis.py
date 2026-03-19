import numpy as np
from sklearn.decomposition import PCA

def perform_pca(feature_matrix: np.ndarray, n_components: int = 2) -> dict:
    """Perform Principal Component Analysis."""
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(feature_matrix)
    
    return {
        'transformed': transformed,
        'explained_variance': pca.explained_variance_ratio_,
        'components': pca.components_
    }
