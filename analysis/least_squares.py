import numpy as np
from sklearn.linear_model import LinearRegression

def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> dict:
    """Fit linear regression using least squares method."""
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    residuals = y - predictions
    r_squared = model.score(X, y)
    
    return {
        'predictions': predictions,
        'coefficients': np.array([model.intercept_, model.coef_[0]]),
        'r_squared': r_squared,
        'residuals': residuals
    }
