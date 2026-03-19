import numpy as np

def detect_anomalies(actual: np.ndarray, predicted: np.ndarray, 
                     timestamps: list, threshold: float = 2.0) -> list:
    """Detect anomalies using statistical deviation."""
    residuals = actual - predicted
    std_dev = np.std(residuals)
    
    anomalies = []
    for i, (act, pred, ts, res) in enumerate(zip(actual, predicted, timestamps, residuals)):
        if abs(res) > threshold * std_dev:
            anomalies.append({
                'timestamp': ts,
                'actual': float(act),
                'predicted': float(pred),
                'deviation': float(abs(res) / std_dev) if std_dev > 0 else 0,
                'residual': float(res)
            })
    
    return anomalies
