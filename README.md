# Network Traffic Analysis

Advanced Mathematical Methods for Anomaly Detection using PDEs, Linear Algebra, PCA, FFT, and Least Squares

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory:**
```bash
cd D:\Acc\Projects\Maths
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

**Start the server:**
```bash
python main.py
```

The server will start on `http://127.0.0.1:8001`

**Access the application:**
- Open your browser and go to: **http://127.0.0.1:8001/**
- Or directly to dashboard: **http://127.0.0.1:8001/dashboard.html**

**Stop the server:**
- Press `Ctrl + C` in the terminal

---

## 📊 Mathematical Analysis Pipeline

### CO1 - PDE Smoothing
Gaussian filtering for noise reduction using diffusion equations
- **Heat Equation:** ∂u/∂t = α∇²u
- **Gaussian Kernel:** G(x,y,σ) = (1/2πσ²)e^(-(x²+y²)/2σ²)
- **Visualizations:** Traffic Over Time, Traffic Intensity Heatmap

### CO2 - Linear Transformations
Feature normalization and scaling for uniform data representation
- **Min-Max Normalization:** x' = (x - x_min) / (x_max - x_min)
- **Z-Score Standardization:** z = (x - μ) / σ
- **Visualization:** Before/After Normalization Comparison

### CO3 - PCA (Principal Component Analysis)
Dimensionality reduction to 2D principal components
- **Covariance Matrix:** Σ = (1/n)X^T X
- **Eigenvalue Decomposition:** Σv = λv
- **PCA Projection:** Z = XW
- **Visualization:** 2D PCA Projection

### CO4 - FFT Analysis
Frequency domain analysis for burst detection
- **Discrete Fourier Transform:** X(k) = Σ x(n)e^(-i2πkn/N)
- **Power Spectral Density:** P(f) = |X(f)|²
- **Visualization:** Frequency Spectrum

### CO5 - Least Squares
Linear regression for anomaly baseline prediction
- **Normal Equations:** β = (X^T X)^(-1) X^T y
- **Prediction Model:** ŷ = Xβ
- **Anomaly Detection:** |y - ŷ| > k·σ (k=2 for 95% confidence)
- **Visualization:** Anomaly Detection Chart

---

## 📁 Project Structure

```
Maths/
├── main.py                      # FastAPI server (port 8001)
├── requirements.txt             # Python dependencies
├── analysis/                    # Analysis modules
│   ├── preprocessing.py         # CSV parsing, normalization
│   ├── pde_smoothing.py         # Gaussian filtering
│   ├── pca_analysis.py          # PCA dimensionality reduction
│   ├── laplace_analysis.py      # FFT frequency analysis
│   ├── least_squares.py         # Linear regression
│   └── anomaly_detection.py     # Anomaly detection
├── frontend/                    # Web interface
│   ├── index.html               # Upload page
│   ├── dashboard_fixed.html     # Analytics dashboard
│   ├── style.css                # Styling
│   └── charts.js                # Plotly visualizations
└── data/                        # Sample datasets
    ├── sample_network_traffic.csv
    └── test_network_traffic_5mb.csv
```

---

## 📝 Usage

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Open browser:**
   Navigate to `http://127.0.0.1:8001/`

3. **Upload CSV file:**
   - Required columns: `timestamp`, `source_ip`, `destination_ip`, `packet_size`, `protocol`
   - Format: CSV with headers

4. **View analysis:**
   - Automatic redirect to dashboard after upload
   - All 5 mathematical analyses applied automatically
   - Interactive Plotly charts for each CO

---

## 🔧 Troubleshooting

### Port already in use
If port 8001 is busy, edit `main.py` (last line):
```python
uvicorn.run(app, host="127.0.0.1", port=8002)  # Change port number
```

### Module not found error
```bash
pip install -r requirements.txt
```

### Browser shows old version
Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)

### Server won't start
Make sure you're in the correct directory:
```bash
cd D:\Acc\Projects\Maths
python main.py
```

---

## 🎓 Research-Grade Analytics

This project implements advanced mathematical methods for network traffic anomaly detection, suitable for:
- Academic research and coursework
- Network security analysis
- Traffic pattern recognition
- Anomaly detection demonstrations

## 🛠️ Technologies

- **Backend:** FastAPI, Uvicorn
- **Data Processing:** NumPy, Pandas, SciPy, scikit-learn
- **Visualization:** Plotly.js
- **Frontend:** HTML5, CSS3, JavaScript

---

## 📊 CSV Format Example

```csv
timestamp,source_ip,destination_ip,packet_size,protocol
2024-01-15T10:30:00,192.168.1.100,10.0.0.50,1024,TCP
2024-01-15T10:30:01,192.168.1.101,10.0.0.51,512,UDP
2024-01-15T10:30:02,192.168.1.102,10.0.0.52,256,ICMP
```

---

## 🚀 Every Time You Want to Run:

1. Open terminal/command prompt
2. Navigate to project: `cd D:\Acc\Projects\Maths`
3. Run: `python main.py`
4. Open browser: `http://127.0.0.1:8001/`
5. Stop server: `Ctrl + C`

That's it! 🎉
