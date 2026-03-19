# Network Traffic Flow Analysis and Anomaly Detection

A localhost Python web application demonstrating mathematical methods applied to network traffic analysis and anomaly detection. Built with FastAPI and interactive Plotly visualizations.

## Mathematical Concepts

### CO1 - Partial Differential Equations (PDE Smoothing)
Applies diffusion equation approximation using Gaussian filtering to remove noise from traffic data. The diffusion equation ∂u/∂t = α∇²u describes how values spread over time, approximated numerically via Gaussian convolution.

### CO2 - Linear Transformations
Treats traffic features as vectors and performs transformations including normalization and scaling using NumPy matrix operations. Min-max scaling transforms all features to [0, 1] range.

### CO3 - Orthonormal Bases / Dimensionality Reduction
Uses Principal Component Analysis (PCA) to reduce high-dimensional traffic features to 2 principal components for 2D visualization. PCA finds orthonormal basis vectors that maximize variance.

### CO4 - Laplace Transform / Frequency Analysis
Analyzes frequency components of network traffic using Fast Fourier Transform (FFT). Treats traffic as a discrete time signal to detect burst patterns and periodic behavior.

### CO5 - Least Squares Prediction
Uses linear regression based on least squares method to predict expected traffic values. Deviations exceeding 2 standard deviations from predictions are marked as anomalies.

## Features

- **CSV Upload**: Upload network traffic logs with columns: timestamp, source_ip, destination_ip, packet_size, protocol
- **PDE Smoothing**: Apply Gaussian filtering to remove noise
- **PCA Visualization**: 2D projection of high-dimensional traffic features
- **Frequency Analysis**: FFT-based detection of dominant frequencies
- **Anomaly Detection**: Statistical detection using least squares regression
- **Interactive Dashboards**: Plotly-based visualizations
- **Sample Data**: Automatic generation of realistic traffic data

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Then open your browser to:
```
http://127.0.0.1:8000
```

## Usage

1. **Upload Data**: Go to the landing page and upload a CSV file with network traffic logs
2. **View Dashboard**: Click "View Dashboard" to see all visualizations
3. **Analyze**: The system automatically applies all mathematical analyses
4. **Interpret Results**: 
   - Traffic chart shows original and PDE-smoothed data
   - PCA chart shows 2D projection of traffic features
   - Frequency chart shows dominant frequencies
   - Anomaly chart highlights unusual traffic patterns

## CSV Format

Required columns:
- `timestamp`: ISO 8601 format (e.g., "2024-01-15T10:30:00")
- `source_ip`: IPv4 address (e.g., "192.168.1.100")
- `destination_ip`: IPv4 address (e.g., "10.0.0.50")
- `packet_size`: Integer bytes (64-1500)
- `protocol`: "TCP", "UDP", or "ICMP"

## API Endpoints

- `POST /upload` - Upload CSV file
- `GET /visualize` - Get traffic visualization data
- `GET /pca` - Get PCA analysis results
- `GET /frequency` - Get FFT frequency spectrum
- `GET /anomalies` - Get detected anomalies

## Anomaly Detection

Anomalies are detected using statistical deviation from predicted values:
1. Fit linear regression model to traffic data
2. Calculate residuals (actual - predicted)
3. Compute standard deviation of residuals
4. Mark records as anomalies if |residual| > 2 × std_dev

## Project Structure

```
network-traffic-analysis/
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── analysis/                        # Analysis modules
│   ├── preprocessing.py             # CSV parsing, normalization
│   ├── pde_smoothing.py             # Gaussian filtering
│   ├── pca_analysis.py              # PCA dimensionality reduction
│   ├── laplace_analysis.py          # FFT frequency analysis
│   ├── least_squares.py             # Linear regression
│   └── anomaly_detection.py         # Anomaly detection
├── frontend/                        # Frontend files
│   ├── index.html                   # Landing page
│   ├── dashboard.html               # Visualization dashboard
│   ├── charts.js                    # Plotly rendering
│   └── style.css                    # Styling
└── data/                            # Data directory
    └── sample_network_traffic.csv   # Sample data
```

## Technologies

- **Backend**: FastAPI, Uvicorn
- **Data Processing**: NumPy, Pandas, SciPy, scikit-learn
- **Visualization**: Plotly
- **Frontend**: HTML5, CSS3, JavaScript

## Notes

- Application runs entirely on localhost (127.0.0.1:8000)
- No database required - data stored in memory
- Sample data automatically generated if no CSV uploaded
- All mathematical operations use NumPy for efficiency
- Suitable for classroom demonstrations and educational purposes
