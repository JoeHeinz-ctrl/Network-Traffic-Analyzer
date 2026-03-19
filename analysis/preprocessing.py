import io
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def parse_csv(file_content: bytes) -> pd.DataFrame:
    """Parse CSV file and validate structure."""
    df = pd.read_csv(io.BytesIO(file_content))
    
    required_columns = ['timestamp', 'source_ip', 'destination_ip', 'packet_size', 'protocol']
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['packet_size'] = df['packet_size'].astype(int)
    
    return df

def generate_sample_data(num_records: int = 500) -> pd.DataFrame:  # Reduced from 1000 to 500
    """Generate realistic sample network traffic data."""
    np.random.seed(42)
    
    start_time = pd.Timestamp('2024-01-15 00:00:00')
    timestamps = [start_time + timedelta(seconds=i*86.4) for i in range(num_records)]
    
    packet_sizes = np.random.choice(
        [64, 128, 256, 512, 1024, 1500],
        size=num_records,
        p=[0.1, 0.15, 0.2, 0.25, 0.2, 0.1]
    )
    
    protocols = np.random.choice(['TCP', 'UDP', 'ICMP'], size=num_records, p=[0.7, 0.25, 0.05])
    
    source_ips = [f"192.168.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}" 
                  for _ in range(num_records)]
    dest_ips = [f"10.0.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}" 
                for _ in range(num_records)]
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'source_ip': source_ips,
        'destination_ip': dest_ips,
        'packet_size': packet_sizes,
        'protocol': protocols
    })

def normalize_features(feature_matrix: np.ndarray) -> np.ndarray:
    """Apply min-max scaling to transform features to [0, 1]."""
    min_vals = feature_matrix.min(axis=0)
    max_vals = feature_matrix.max(axis=0)
    
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1.0
    
    normalized = (feature_matrix - min_vals) / range_vals
    return normalized

def extract_features(df: pd.DataFrame) -> np.ndarray:
    """Extract numerical features from traffic data."""
    protocol_map = {'TCP': 0, 'UDP': 1, 'ICMP': 2}
    
    features = np.column_stack([
        df['packet_size'].values,
        df['protocol'].map(protocol_map).values,
        pd.to_datetime(df['timestamp']).dt.hour.values,
        df['source_ip'].apply(lambda x: hash(x) % 1000).values
    ])
    
    return features

def prepare_traffic_matrix(df: pd.DataFrame) -> np.ndarray:
    """Convert traffic DataFrame to matrix for PDE smoothing."""
    df_copy = df.copy()
    df_copy['time_bin'] = pd.to_datetime(df_copy['timestamp']).dt.floor('1min')
    
    aggregated = df_copy.groupby('time_bin').agg({
        'packet_size': ['mean', 'count'],
        'protocol': lambda x: (x == 'TCP').sum()
    }).values
    
    return aggregated
