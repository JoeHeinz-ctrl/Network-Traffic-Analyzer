# Design Document: Network Traffic Analysis

## Overview

The Network Traffic Analysis system is a localhost Python web application that demonstrates mathematical methods applied to network traffic flow analysis and anomaly detection. The application is designed for classroom demonstration purposes and applies advanced mathematical concepts including partial differential equations (PDE smoothing), linear transformations, Principal Component Analysis (PCA), Fourier/Laplace transforms, and least squares regression.

The system consists of a FastAPI backend that performs mathematical analysis on network traffic data and a frontend that provides interactive visualizations using Plotly. The application runs entirely on localhost without requiring cloud deployment, authentication, or internet connectivity.

### Key Mathematical Concepts

1. **PDE Smoothing (CO1)**: Applies diffusion equation approximation using Gaussian filtering to remove noise from traffic data
2. **Linear Transformations (CO2)**: Uses matrix operations for normalization and feature scaling
3. **Orthonormal Bases (CO3)**: Implements PCA to project high-dimensional traffic features onto 2D principal components
4. **Laplace Transform (CO4)**: Uses FFT to analyze frequency components and detect burst traffic patterns
5. **Least Squares (CO5)**: Applies linear regression for traffic prediction and anomaly detection baseline

## Architecture

### System Components

The system follows a client-server architecture with clear separation between data processing, analysis, and presentation layers.

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  index.html  │  │dashboard.html│  │  charts.js   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP REST API
                            │
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    main.py                            │   │
│  │  - Route handlers                                     │   │
│  │  - File upload management                             │   │
│  │  - Data orchestration                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                     Analysis Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │preprocessing │  │pde_smoothing │  │ pca_analysis │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │laplace_      │  │least_squares │  │   anomaly_   │      │
│  │  analysis    │  │              │  │  detection   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  In-Memory Storage (global state)                     │   │
│  │  - Parsed traffic logs                                │   │
│  │  - Analysis results cache                             │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  data/sample_network_traffic.csv                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend Framework**: FastAPI (async Python web framework)
- **Web Server**: Uvicorn (ASGI server)
- **Numerical Computing**: NumPy (matrix operations, linear algebra)
- **Data Processing**: Pandas (CSV parsing, data manipulation)
- **Scientific Computing**: SciPy (Gaussian filtering, signal processing)
- **Machine Learning**: scikit-learn (PCA, linear regression)
- **Visualization**: Plotly (interactive charts)
- **File Upload**: python-multipart (multipart form data handling)

### Data Flow

1. **Upload Phase**: User uploads CSV → CSV_Parser validates and extracts Traffic_Log records → Store in memory
2. **Analysis Phase**: Traffic data → Preprocessing (normalization) → Parallel analysis pipelines (PDE, PCA, FFT, Regression) → Results aggregation
3. **Visualization Phase**: Frontend requests data via API → Backend returns JSON → Plotly renders interactive charts

## Components and Interfaces

### 1. Main Application (main.py)

**Responsibilities**:
- FastAPI application initialization
- Route endpoint definitions
- File upload handling
- Global state management
- CORS configuration for localhost

**Key Functions**:
```python
app = FastAPI()
traffic_data: Optional[pd.DataFrame] = None

@app.post("/upload")
async def upload_csv(file: UploadFile) -> dict

@app.get("/visualize")
async def get_visualization_data() -> dict

@app.get("/pca")
async def get_pca_analysis() -> dict

@app.get("/frequency")
async def get_frequency_analysis() -> dict

@app.get("/anomalies")
async def get_anomalies() -> dict
```

**State Management**:
- Global `traffic_data` variable stores parsed DataFrame
- Lazy loading: if no data uploaded, generate sample data on first request

### 2. CSV Parser (analysis/preprocessing.py)

**Responsibilities**:
- Validate CSV structure
- Parse CSV into structured DataFrame
- Generate sample data
- Normalize and scale features

**Interface**:
```python
def parse_csv(file_content: bytes) -> pd.DataFrame
    """
    Parse CSV file and validate required columns.
    
    Args:
        file_content: Raw bytes from uploaded file
        
    Returns:
        DataFrame with columns: timestamp, source_ip, destination_ip, 
                                packet_size, protocol
                                
    Raises:
        ValueError: If required columns are missing
    """

def generate_sample_data(num_records: int = 1000) -> pd.DataFrame
    """
    Generate realistic sample network traffic data.
    
    Returns:
        DataFrame with 1000+ records spanning 24 hours
    """

def normalize_features(df: pd.DataFrame) -> np.ndarray
    """
    Apply min-max scaling to transform features to [0, 1] range.
    
    Args:
        df: DataFrame with traffic features
        
    Returns:
        Normalized feature matrix (n_samples, n_features)
    """
```

**Validation Rules**:
- Required columns: timestamp, source_ip, destination_ip, packet_size, protocol
- File size limit: 50 MB
- Timestamp format: ISO 8601 or Unix timestamp

### 3. PDE Smoother (analysis/pde_smoothing.py)

**Responsibilities**:
- Model traffic as a matrix (time × features)
- Apply Gaussian filtering as diffusion equation approximation
- Preserve matrix dimensions

**Mathematical Foundation**:
The diffusion equation ∂u/∂t = α∇²u describes how values spread over time. We approximate this using Gaussian filtering, which is equivalent to solving the heat equation numerically.

**Interface**:
```python
def smooth_traffic_pde(traffic_matrix: np.ndarray, sigma: float = 2.0) -> np.ndarray
    """
    Apply PDE-based smoothing using Gaussian filter.
    
    The Gaussian filter approximates the solution to the diffusion equation:
    ∂u/∂t = α∇²u
    
    Args:
        traffic_matrix: Shape (n_time_intervals, n_features)
        sigma: Standard deviation for Gaussian kernel (controls smoothing strength)
        
    Returns:
        Smoothed matrix with same shape as input
    """
```

**Implementation Details**:
- Use `scipy.ndimage.gaussian_filter` for 2D Gaussian convolution
- Default sigma=2.0 provides moderate smoothing
- Apply to packet_size feature over time

### 4. PCA Transformer (analysis/pca_analysis.py)

**Responsibilities**:
- Reduce high-dimensional traffic features to 2 principal components
- Compute explained variance ratios
- Transform all traffic records to 2D coordinates

**Mathematical Foundation**:
PCA finds orthonormal basis vectors (principal components) that maximize variance. It uses eigenvalue decomposition of the covariance matrix to project data onto lower-dimensional subspace.

**Interface**:
```python
def perform_pca(feature_matrix: np.ndarray, n_components: int = 2) -> dict
    """
    Perform Principal Component Analysis for dimensionality reduction.
    
    Args:
        feature_matrix: Shape (n_samples, n_features)
        n_components: Number of components to keep (default: 2)
        
    Returns:
        {
            'transformed': np.ndarray,  # Shape (n_samples, 2)
            'explained_variance': list,  # [PC1_variance, PC2_variance]
            'components': np.ndarray     # Principal component vectors
        }
    """
```

**Feature Selection**:
- Input features: packet_size, protocol_encoded, hour_of_day, ip_hash
- Normalization applied before PCA
- 2 components for 2D visualization

### 5. FFT Analyzer (analysis/laplace_analysis.py)

**Responsibilities**:
- Treat traffic over time as discrete signal
- Compute Fast Fourier Transform
- Identify dominant frequencies
- Return frequency spectrum

**Mathematical Foundation**:
The Laplace transform analyzes signals in the frequency domain. For discrete signals, we use FFT (Fast Fourier Transform) which computes the Discrete Fourier Transform efficiently. This reveals periodic patterns and burst traffic.

**Interface**:
```python
def analyze_frequency_spectrum(time_series: np.ndarray, sampling_rate: float = 1.0) -> dict
    """
    Perform FFT to extract frequency components.
    
    Args:
        time_series: 1D array of traffic values over time
        sampling_rate: Samples per unit time (default: 1.0)
        
    Returns:
        {
            'frequencies': np.ndarray,  # Frequency values (Hz)
            'magnitudes': np.ndarray,   # Magnitude at each frequency
            'top_5_frequencies': list   # Top 5 dominant frequencies
        }
    """
```

**Implementation Details**:
- Use `numpy.fft.fft` for frequency analysis
- Apply to packet_size time series
- Filter out DC component (frequency = 0)
- Return positive frequencies only (real signal symmetry)

### 6. Regression Predictor (analysis/least_squares.py)

**Responsibilities**:
- Fit linear regression model using least squares
- Predict expected traffic values
- Compute R² coefficient of determination
- Provide baseline for anomaly detection

**Mathematical Foundation**:
Least squares minimizes the sum of squared residuals: min Σ(y_i - ŷ_i)². The solution is found by solving the normal equations: β = (X^T X)^(-1) X^T y.

**Interface**:
```python
def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> dict
    """
    Fit linear regression model using least squares method.
    
    Args:
        X: Independent variable (time), shape (n_samples, 1)
        y: Dependent variable (packet_size), shape (n_samples,)
        
    Returns:
        {
            'predictions': np.ndarray,  # Predicted values
            'coefficients': np.ndarray, # [intercept, slope]
            'r_squared': float,         # Coefficient of determination
            'residuals': np.ndarray     # y - predictions
        }
    """
```

**Model Specification**:
- Independent variable: time (seconds since start)
- Dependent variable: packet_size
- Model: packet_size = β₀ + β₁ × time

### 7. Anomaly Detector (analysis/anomaly_detection.py)

**Responsibilities**:
- Compare actual vs predicted traffic
- Identify deviations exceeding 2 standard deviations
- Return anomaly records with timestamps and deviation values

**Interface**:
```python
def detect_anomalies(actual: np.ndarray, predicted: np.ndarray, 
                     timestamps: np.ndarray, threshold: float = 2.0) -> list
    """
    Detect anomalies using statistical deviation from predictions.
    
    Args:
        actual: Actual traffic values
        predicted: Predicted values from regression
        timestamps: Corresponding timestamps
        threshold: Number of standard deviations for anomaly (default: 2.0)
        
    Returns:
        List of dicts: [
            {
                'timestamp': str,
                'actual': float,
                'predicted': float,
                'deviation': float,  # In standard deviations
                'residual': float
            },
            ...
        ]
    """
```

**Detection Algorithm**:
1. Compute residuals: r = actual - predicted
2. Calculate standard deviation: σ = std(residuals)
3. Mark as anomaly if |r| > threshold × σ

### 8. Frontend Components

#### index.html
- Landing page with file upload interface
- Navigation to dashboard
- Instructions for usage

#### dashboard.html
- Container for all visualizations
- Grid layout for multiple charts
- Responsive design

#### charts.js
**Responsibilities**:
- Fetch data from API endpoints
- Render Plotly visualizations
- Handle user interactions

**Key Functions**:
```javascript
async function loadTrafficVisualization()
async function loadPCAVisualization()
async function loadFrequencyVisualization()
async function loadAnomalyVisualization()
```

**Chart Types**:
1. Line chart: Traffic volume over time
2. Heatmap: Traffic intensity (time × IP addresses)
3. Scatter plot: PCA 2D projection
4. Line chart: Frequency spectrum
5. Dual line chart: Predicted vs actual traffic
6. Scatter plot: Anomalies highlighted

#### style.css
- Modern, clean design
- Color scheme for mathematical/technical theme
- Responsive grid layout

## Data Models

### Traffic Log Record

```python
{
    'timestamp': str,           # ISO 8601 format: "2024-01-15T10:30:00"
    'source_ip': str,           # IPv4 address: "192.168.1.100"
    'destination_ip': str,      # IPv4 address: "10.0.0.50"
    'packet_size': int,         # Bytes: 64-1500
    'protocol': str             # "TCP", "UDP", or "ICMP"
}
```

### Feature Matrix

After preprocessing, traffic logs are converted to numerical feature matrix:

```python
features = [
    packet_size,        # Original packet size
    protocol_encoded,   # One-hot: TCP=0, UDP=1, ICMP=2
    hour_of_day,        # 0-23
    ip_hash             # Hash of source_ip for numerical representation
]
```

Shape: (n_samples, 4)

### API Response Formats

#### /visualize Response
```json
{
    "traffic_over_time": {
        "timestamps": ["2024-01-15T00:00:00", ...],
        "packet_sizes": [512, 1024, ...],
        "smoothed_sizes": [510, 1020, ...]
    },
    "heatmap_data": {
        "time_intervals": ["00:00", "01:00", ...],
        "ip_addresses": ["192.168.1.1", ...],
        "intensity_matrix": [[10, 20, ...], ...]
    }
}
```

#### /pca Response
```json
{
    "transformed_coordinates": [[0.5, -0.3], [0.2, 0.8], ...],
    "explained_variance": [0.65, 0.25],
    "labels": ["TCP", "UDP", ...]
}
```

#### /frequency Response
```json
{
    "frequencies": [0.1, 0.2, 0.3, ...],
    "magnitudes": [100, 50, 25, ...],
    "top_5_frequencies": [0.1, 0.5, 1.2, 2.3, 3.1]
}
```

#### /anomalies Response
```json
{
    "anomalies": [
        {
            "timestamp": "2024-01-15T10:30:00",
            "actual": 1450,
            "predicted": 800,
            "deviation": 2.5,
            "residual": 650
        },
        ...
    ],
    "total_count": 15,
    "threshold": 2.0
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: CSV Parsing Completeness

*For any* valid CSV file containing Traffic_Log records, parsing should extract all records without loss, and the number of records in the output DataFrame should equal the number of data rows in the input CSV.

**Validates: Requirements 1.1**

### Property 2: Invalid CSV Error Messages

*For any* CSV file missing one or more required columns (timestamp, source_ip, destination_ip, packet_size, protocol), the parser should return an error message that specifically identifies which columns are missing.

**Validates: Requirements 1.2**

### Property 3: Parsed Data Persistence

*For any* successfully parsed CSV file, subsequent requests to analysis endpoints should use the parsed data rather than sample data, confirming that data is stored in memory.

**Validates: Requirements 1.4**

### Property 4: Sample Data Validity

*For any* generated sample dataset, all records should satisfy the constraints: at least 1000 records, timestamps spanning at least 24 hours, packet sizes between 64 and 1500 bytes, and all three protocol types (TCP, UDP, ICMP) present.

**Validates: Requirements 2.2, 2.3, 2.4**

### Property 5: PDE Smoothing Dimension Preservation

*For any* traffic matrix with shape (n_time_intervals, n_features), applying PDE smoothing should return a smoothed matrix with identical shape (n_time_intervals, n_features).

**Validates: Requirements 3.3**

### Property 6: Smoothed Data Availability

*For any* traffic dataset, the visualization endpoint should return both original and smoothed traffic data in the response.

**Validates: Requirements 3.4**

### Property 7: Min-Max Normalization Range

*For any* feature matrix, applying min-max normalization should transform all values to the range [0, 1], where the minimum value becomes 0 and the maximum value becomes 1.

**Validates: Requirements 4.2**

### Property 8: Original Data Preservation

*For any* traffic dataset, after applying transformations (normalization, PCA, etc.), the original raw data should remain accessible and unchanged.

**Validates: Requirements 4.4**

### Property 9: PCA Dimensionality Reduction

*For any* feature matrix with more than 2 dimensions, PCA transformation should produce output coordinates with exactly 2 dimensions (principal components).

**Validates: Requirements 5.1**

### Property 10: PCA Explained Variance

*For any* PCA transformation, the result should include explained variance ratios for each principal component, and the sum of all explained variance ratios should be less than or equal to 1.0.

**Validates: Requirements 5.2**

### Property 11: Transformation Completeness

*For any* input dataset with n records, all transformation operations (PCA, regression prediction, anomaly detection) should produce outputs with exactly n corresponding results.

**Validates: Requirements 5.3, 7.3**

### Property 12: FFT Minimum Data Requirement

*For any* traffic time series with at least 10 time intervals, the FFT analyzer should successfully compute and return frequency components; for time series with fewer than 10 intervals, it should handle gracefully.

**Validates: Requirements 6.2**

### Property 13: FFT Output Structure

*For any* FFT computation, the output should contain both frequency values and corresponding magnitude values, with equal-length arrays.

**Validates: Requirements 6.3**

### Property 14: Top Frequencies Identification

*For any* FFT frequency spectrum, exactly 5 dominant frequencies should be identified and returned, sorted by magnitude in descending order.

**Validates: Requirements 6.4**

### Property 15: Regression Model Fitting

*For any* traffic dataset with at least 20 records, the regression predictor should successfully fit a linear model and return predictions for all time points.

**Validates: Requirements 7.2**

### Property 16: R-Squared Calculation

*For any* fitted regression model, the coefficient of determination (R²) should be calculated and should fall within the range [-∞, 1.0], where 1.0 indicates perfect prediction.

**Validates: Requirements 7.4**

### Property 17: Anomaly Detection Threshold

*For any* traffic dataset with predictions, records where the absolute difference between actual and predicted values exceeds 2 standard deviations of the residuals should be marked as anomalies, and all such records should be included in the anomaly list.

**Validates: Requirements 8.2**

### Property 18: Anomaly Record Structure

*For any* detected anomaly, the output record should contain all required fields: timestamp, actual value, predicted value, deviation (in standard deviations), and residual.

**Validates: Requirements 8.3**

### Property 19: Sample Data Fallback

*For any* API endpoint request made before data is uploaded, the system should automatically generate and use sample data rather than returning an error, ensuring all endpoints remain functional.

**Validates: Requirements 10.6, 15.3**

### Property 20: CSV Parsing Error Status

*For any* CSV parsing error (invalid format, missing columns, etc.), the API should return HTTP status code 400 with a descriptive error message.

**Validates: Requirements 15.1**

### Property 21: Analysis Error Status

*For any* error occurring during mathematical analysis (PDE smoothing, PCA, FFT, regression, anomaly detection), the API should return HTTP status code 500 with details about which component failed.

**Validates: Requirements 15.2**

### Property 22: Error Logging

*For any* error that occurs in the system, an error message should be logged to the console with sufficient detail for debugging.

**Validates: Requirements 15.4**

## Error Handling

### Error Categories

1. **Input Validation Errors (HTTP 400)**
   - Invalid CSV format
   - Missing required columns
   - File size exceeds 50 MB
   - Invalid data types in CSV fields

2. **Analysis Errors (HTTP 500)**
   - PDE smoothing failure (e.g., invalid matrix dimensions)
   - PCA failure (e.g., insufficient data variance)
   - FFT failure (e.g., non-numeric time series)
   - Regression failure (e.g., insufficient data points)
   - Anomaly detection failure (e.g., missing predictions)

3. **System Errors (HTTP 500)**
   - File I/O errors
   - Memory allocation errors
   - Unexpected exceptions

### Error Response Format

All error responses follow a consistent JSON structure:

```json
{
    "error": true,
    "message": "Human-readable error description",
    "details": {
        "component": "CSV_Parser | PDE_Smoother | PCA_Transformer | ...",
        "error_type": "ValidationError | AnalysisError | SystemError",
        "missing_columns": ["timestamp", "packet_size"],  // For CSV errors
        "stack_trace": "..."  // In development mode only
    }
}
```

### Error Handling Strategy

1. **Graceful Degradation**: If one analysis component fails, other components should continue to work
2. **Informative Messages**: Error messages should guide users toward resolution
3. **Logging**: All errors logged to console with timestamp and context
4. **Sample Data Fallback**: Missing data triggers sample data generation rather than errors
5. **Validation First**: Input validation occurs before expensive computations

### Exception Handling in Components

Each analysis module implements try-except blocks:

```python
def perform_analysis(data):
    try:
        # Analysis logic
        result = compute_analysis(data)
        return {"success": True, "data": result}
    except ValueError as e:
        logger.error(f"Validation error in analysis: {e}")
        return {"success": False, "error": str(e), "component": "AnalysisModule"}
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {e}")
        return {"success": False, "error": "Internal analysis error", "component": "AnalysisModule"}
```

## Testing Strategy

### Dual Testing Approach

The Network Traffic Analysis system requires both unit testing and property-based testing to ensure correctness:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs
- Both approaches are complementary and necessary for comprehensive coverage

Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Unit Testing

**Framework**: pytest

**Test Organization**:
```
tests/
├── test_preprocessing.py
├── test_pde_smoothing.py
├── test_pca_analysis.py
├── test_laplace_analysis.py
├── test_least_squares.py
├── test_anomaly_detection.py
├── test_api_endpoints.py
└── fixtures/
    └── sample_data.py
```

**Unit Test Focus Areas**:

1. **Specific Examples**
   - Parse a known CSV file and verify exact output
   - Apply PDE smoothing to a small matrix and verify result
   - Test PCA on a 3-feature dataset and verify 2D output

2. **Edge Cases**
   - Empty CSV file
   - CSV with only header row
   - Single data point for regression
   - Time series with exactly 10 intervals (FFT boundary)
   - All traffic values identical (zero variance)

3. **Error Conditions**
   - Missing CSV columns
   - Invalid data types
   - File size exceeding 50 MB
   - Insufficient data for analysis (< 20 records for regression)

4. **Integration Points**
   - API endpoint responses
   - Data flow between components
   - Sample data generation on startup

**Example Unit Tests**:

```python
def test_parse_valid_csv():
    """Test parsing a valid CSV file with all required columns."""
    csv_content = b"timestamp,source_ip,destination_ip,packet_size,protocol\n2024-01-15T10:00:00,192.168.1.1,10.0.0.1,512,TCP\n"
    df = parse_csv(csv_content)
    assert len(df) == 1
    assert df.iloc[0]['packet_size'] == 512

def test_parse_missing_columns():
    """Test error handling for CSV missing required columns."""
    csv_content = b"timestamp,source_ip,packet_size\n2024-01-15T10:00:00,192.168.1.1,512\n"
    with pytest.raises(ValueError) as exc_info:
        parse_csv(csv_content)
    assert "destination_ip" in str(exc_info.value)
    assert "protocol" in str(exc_info.value)

def test_pde_smoothing_preserves_dimensions():
    """Test that PDE smoothing returns same-shaped matrix."""
    traffic_matrix = np.random.rand(100, 4)
    smoothed = smooth_traffic_pde(traffic_matrix)
    assert smoothed.shape == traffic_matrix.shape
```

### Property-Based Testing

**Framework**: Hypothesis (Python property-based testing library)

**Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each test tagged with comment referencing design document property
- Tag format: `# Feature: network-traffic-analysis, Property {number}: {property_text}`

**Property Test Focus Areas**:

1. **Data Transformation Properties**
   - Dimension preservation (PDE smoothing, normalization)
   - Range constraints (min-max scaling to [0, 1])
   - Completeness (output count matches input count)

2. **Mathematical Properties**
   - PCA explained variance sums to ≤ 1.0
   - R² coefficient in valid range [-∞, 1.0]
   - FFT output arrays have equal length

3. **Invariants**
   - Original data unchanged after transformations
   - Sample data always meets validity constraints
   - Error responses always include required fields

4. **Round-Trip Properties**
   - Parse CSV → extract records → count matches input rows

**Example Property Tests**:

```python
from hypothesis import given, strategies as st
import hypothesis.extra.numpy as npst

# Feature: network-traffic-analysis, Property 5: PDE Smoothing Dimension Preservation
@given(traffic_matrix=npst.arrays(
    dtype=np.float64,
    shape=st.tuples(st.integers(10, 1000), st.integers(2, 10))
))
def test_pde_smoothing_preserves_dimensions(traffic_matrix):
    """For any traffic matrix, PDE smoothing should preserve dimensions."""
    smoothed = smooth_traffic_pde(traffic_matrix)
    assert smoothed.shape == traffic_matrix.shape

# Feature: network-traffic-analysis, Property 7: Min-Max Normalization Range
@given(feature_matrix=npst.arrays(
    dtype=np.float64,
    shape=st.tuples(st.integers(10, 1000), st.integers(2, 10)),
    elements=st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
))
def test_normalization_range(feature_matrix):
    """For any feature matrix, normalization should produce values in [0, 1]."""
    normalized = normalize_features(feature_matrix)
    assert np.all(normalized >= 0.0)
    assert np.all(normalized <= 1.0)
    # Check that min and max are actually 0 and 1 (if not all values identical)
    if not np.all(feature_matrix == feature_matrix[0, 0]):
        assert np.min(normalized) == 0.0
        assert np.max(normalized) == 1.0

# Feature: network-traffic-analysis, Property 11: Transformation Completeness
@given(n_records=st.integers(20, 1000))
def test_transformation_completeness(n_records):
    """For any dataset with n records, transformations should produce n outputs."""
    # Generate sample data
    df = generate_sample_data(num_records=n_records)
    
    # Test PCA
    features = extract_features(df)
    pca_result = perform_pca(features)
    assert len(pca_result['transformed']) == n_records
    
    # Test regression
    X, y = prepare_regression_data(df)
    regression_result = fit_linear_regression(X, y)
    assert len(regression_result['predictions']) == n_records

# Feature: network-traffic-analysis, Property 17: Anomaly Detection Threshold
@given(
    actual=npst.arrays(dtype=np.float64, shape=st.integers(50, 500)),
    predicted=npst.arrays(dtype=np.float64, shape=st.integers(50, 500))
)
def test_anomaly_detection_threshold(actual, predicted):
    """For any actual and predicted values, anomalies should exceed 2 std devs."""
    # Ensure arrays have same length
    min_len = min(len(actual), len(predicted))
    actual = actual[:min_len]
    predicted = predicted[:min_len]
    
    timestamps = [f"2024-01-15T{i:02d}:00:00" for i in range(min_len)]
    anomalies = detect_anomalies(actual, predicted, timestamps, threshold=2.0)
    
    # Verify all detected anomalies actually exceed threshold
    residuals = actual - predicted
    std_dev = np.std(residuals)
    
    for anomaly in anomalies:
        assert abs(anomaly['residual']) > 2.0 * std_dev
```

### Test Coverage Goals

- **Line Coverage**: Minimum 85%
- **Branch Coverage**: Minimum 80%
- **Critical Paths**: 100% coverage for error handling and data validation

### Continuous Testing

- Run unit tests on every commit
- Run property tests (100 iterations) on every commit
- Run extended property tests (1000 iterations) nightly
- Monitor test execution time and optimize slow tests

### Test Data Management

**Fixtures**:
- Small CSV (10 records) for fast unit tests
- Medium CSV (100 records) for integration tests
- Large CSV (10,000 records) for performance tests
- Invalid CSVs (missing columns, wrong types) for error testing

**Generators**:
- Hypothesis strategies for random traffic data
- Custom generators for edge cases (zero variance, extreme values)
- Reproducible random seeds for debugging


## Implementation Details

### File Structure

```
network-traffic-analysis/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── analysis/                        # Analysis modules
│   ├── __init__.py
│   ├── preprocessing.py             # CSV parsing, normalization, sample data
│   ├── pde_smoothing.py             # Gaussian filtering for diffusion smoothing
│   ├── pca_analysis.py              # Principal Component Analysis
│   ├── laplace_analysis.py          # FFT frequency analysis
│   ├── least_squares.py             # Linear regression predictor
│   └── anomaly_detection.py         # Anomaly detection logic
├── frontend/                        # Frontend files
│   ├── index.html                   # Landing page with upload
│   ├── dashboard.html               # Visualization dashboard
│   ├── charts.js                    # Plotly chart rendering
│   └── style.css                    # Styling
├── data/                            # Data directory
│   └── sample_network_traffic.csv   # Pre-generated sample data
└── tests/                           # Test suite
    ├── test_preprocessing.py
    ├── test_pde_smoothing.py
    ├── test_pca_analysis.py
    ├── test_laplace_analysis.py
    ├── test_least_squares.py
    ├── test_anomaly_detection.py
    ├── test_api_endpoints.py
    └── fixtures/
        └── sample_data.py
```

### Module Implementation Details

#### main.py

**Key Responsibilities**:
- Initialize FastAPI application
- Define API routes
- Manage global state (uploaded traffic data)
- Handle file uploads
- Coordinate analysis pipeline
- Serve static frontend files

**Global State**:
```python
traffic_data: Optional[pd.DataFrame] = None  # Stores uploaded/generated data
analysis_cache: Dict[str, Any] = {}          # Cache analysis results
```

**Route Handlers**:

```python
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Handle CSV file upload.
    
    Returns:
        {"success": True, "records": count} or error response
    """
    global traffic_data
    try:
        content = await file.read()
        traffic_data = parse_csv(content)
        analysis_cache.clear()  # Invalidate cache
        return {"success": True, "records": len(traffic_data)}
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": str(e), "component": "CSV_Parser"}
        )

@app.get("/visualize")
async def get_visualization_data():
    """
    Get processed traffic data for visualization.
    
    Returns:
        {
            "traffic_over_time": {...},
            "heatmap_data": {...}
        }
    """
    data = ensure_data_loaded()
    
    # Extract time series
    timestamps = data['timestamp'].tolist()
    packet_sizes = data['packet_size'].tolist()
    
    # Apply PDE smoothing
    traffic_matrix = prepare_traffic_matrix(data)
    smoothed_matrix = smooth_traffic_pde(traffic_matrix)
    smoothed_sizes = smoothed_matrix[:, 0].tolist()  # First column is packet_size
    
    # Prepare heatmap data
    heatmap = generate_heatmap_data(data)
    
    return {
        "traffic_over_time": {
            "timestamps": timestamps,
            "packet_sizes": packet_sizes,
            "smoothed_sizes": smoothed_sizes
        },
        "heatmap_data": heatmap
    }

@app.get("/pca")
async def get_pca_analysis():
    """Get PCA analysis results."""
    data = ensure_data_loaded()
    features = extract_features(data)
    normalized = normalize_features(features)
    pca_result = perform_pca(normalized)
    
    return {
        "transformed_coordinates": pca_result['transformed'].tolist(),
        "explained_variance": pca_result['explained_variance'].tolist(),
        "labels": data['protocol'].tolist()
    }

@app.get("/frequency")
async def get_frequency_analysis():
    """Get FFT frequency spectrum."""
    data = ensure_data_loaded()
    time_series = data['packet_size'].values
    freq_result = analyze_frequency_spectrum(time_series)
    
    return {
        "frequencies": freq_result['frequencies'].tolist(),
        "magnitudes": freq_result['magnitudes'].tolist(),
        "top_5_frequencies": freq_result['top_5_frequencies']
    }

@app.get("/anomalies")
async def get_anomalies():
    """Get detected anomalies."""
    data = ensure_data_loaded()
    
    # Prepare regression data
    X = np.arange(len(data)).reshape(-1, 1)  # Time as independent variable
    y = data['packet_size'].values
    
    # Fit regression model
    regression_result = fit_linear_regression(X, y)
    
    # Detect anomalies
    anomalies = detect_anomalies(
        actual=y,
        predicted=regression_result['predictions'],
        timestamps=data['timestamp'].tolist(),
        threshold=2.0
    )
    
    return {
        "anomalies": anomalies,
        "total_count": len(anomalies),
        "threshold": 2.0,
        "r_squared": regression_result['r_squared']
    }

def ensure_data_loaded() -> pd.DataFrame:
    """Ensure traffic data is available, generate sample if needed."""
    global traffic_data
    if traffic_data is None:
        traffic_data = generate_sample_data()
    return traffic_data
```

#### analysis/preprocessing.py

**Key Functions**:

```python
def parse_csv(file_content: bytes) -> pd.DataFrame:
    """
    Parse CSV file and validate structure.
    
    Validation:
    - Required columns present
    - Valid data types
    - File size within limits
    """
    # Read CSV
    df = pd.read_csv(io.BytesIO(file_content))
    
    # Validate columns
    required_columns = ['timestamp', 'source_ip', 'destination_ip', 'packet_size', 'protocol']
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    
    # Validate data types
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['packet_size'] = df['packet_size'].astype(int)
    
    return df

def generate_sample_data(num_records: int = 1000) -> pd.DataFrame:
    """
    Generate realistic sample network traffic data.
    
    Constraints:
    - At least 1000 records
    - Timestamps span 24+ hours
    - Packet sizes: 64-1500 bytes
    - Protocols: TCP, UDP, ICMP
    """
    np.random.seed(42)  # Reproducible sample data
    
    # Generate timestamps (24 hours)
    start_time = pd.Timestamp('2024-01-15 00:00:00')
    timestamps = [start_time + pd.Timedelta(seconds=i*86.4) for i in range(num_records)]
    
    # Generate packet sizes (realistic distribution)
    packet_sizes = np.random.choice(
        [64, 128, 256, 512, 1024, 1500],
        size=num_records,
        p=[0.1, 0.15, 0.2, 0.25, 0.2, 0.1]
    )
    
    # Generate protocols
    protocols = np.random.choice(['TCP', 'UDP', 'ICMP'], size=num_records, p=[0.7, 0.25, 0.05])
    
    # Generate IP addresses
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
    """
    Apply min-max scaling to transform features to [0, 1].
    
    Formula: x_normalized = (x - x_min) / (x_max - x_min)
    """
    min_vals = feature_matrix.min(axis=0)
    max_vals = feature_matrix.max(axis=0)
    
    # Avoid division by zero for constant features
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1.0
    
    normalized = (feature_matrix - min_vals) / range_vals
    return normalized

def extract_features(df: pd.DataFrame) -> np.ndarray:
    """
    Extract numerical features from traffic data.
    
    Features:
    - packet_size
    - protocol_encoded (TCP=0, UDP=1, ICMP=2)
    - hour_of_day
    - ip_hash (hash of source_ip)
    """
    protocol_map = {'TCP': 0, 'UDP': 1, 'ICMP': 2}
    
    features = np.column_stack([
        df['packet_size'].values,
        df['protocol'].map(protocol_map).values,
        pd.to_datetime(df['timestamp']).dt.hour.values,
        df['source_ip'].apply(lambda x: hash(x) % 1000).values
    ])
    
    return features
```

#### analysis/pde_smoothing.py

```python
from scipy.ndimage import gaussian_filter

def smooth_traffic_pde(traffic_matrix: np.ndarray, sigma: float = 2.0) -> np.ndarray:
    """
    Apply PDE-based smoothing using Gaussian filter.
    
    Mathematical basis:
    The diffusion equation ∂u/∂t = α∇²u describes how values spread over time.
    Gaussian filtering is equivalent to solving this equation numerically.
    
    Args:
        traffic_matrix: Shape (n_time_intervals, n_features)
        sigma: Standard deviation for Gaussian kernel
        
    Returns:
        Smoothed matrix with same shape
    """
    # Apply 2D Gaussian filter
    smoothed = gaussian_filter(traffic_matrix, sigma=sigma, mode='reflect')
    
    return smoothed

def prepare_traffic_matrix(df: pd.DataFrame) -> np.ndarray:
    """
    Convert traffic DataFrame to matrix for PDE smoothing.
    
    Rows: time intervals (1-minute bins)
    Columns: aggregated features (mean packet_size, count)
    """
    # Bin by time intervals
    df['time_bin'] = pd.to_datetime(df['timestamp']).dt.floor('1min')
    
    # Aggregate by time bin
    aggregated = df.groupby('time_bin').agg({
        'packet_size': ['mean', 'count'],
        'protocol': lambda x: (x == 'TCP').sum()
    }).values
    
    return aggregated
```

#### analysis/pca_analysis.py

```python
from sklearn.decomposition import PCA

def perform_pca(feature_matrix: np.ndarray, n_components: int = 2) -> dict:
    """
    Perform Principal Component Analysis.
    
    Mathematical basis:
    PCA finds orthonormal basis vectors (principal components) that maximize
    variance. Uses eigenvalue decomposition of covariance matrix.
    
    Args:
        feature_matrix: Shape (n_samples, n_features)
        n_components: Number of components (default: 2)
        
    Returns:
        {
            'transformed': np.ndarray,      # (n_samples, 2)
            'explained_variance': np.ndarray, # [PC1_ratio, PC2_ratio]
            'components': np.ndarray        # Principal component vectors
        }
    """
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(feature_matrix)
    
    return {
        'transformed': transformed,
        'explained_variance': pca.explained_variance_ratio_,
        'components': pca.components_
    }
```

#### analysis/laplace_analysis.py

```python
def analyze_frequency_spectrum(time_series: np.ndarray, sampling_rate: float = 1.0) -> dict:
    """
    Perform FFT to extract frequency components.
    
    Mathematical basis:
    The Laplace transform analyzes signals in frequency domain. For discrete
    signals, FFT computes the Discrete Fourier Transform efficiently.
    
    Args:
        time_series: 1D array of traffic values
        sampling_rate: Samples per unit time
        
    Returns:
        {
            'frequencies': np.ndarray,
            'magnitudes': np.ndarray,
            'top_5_frequencies': list
        }
    """
    n = len(time_series)
    
    # Compute FFT
    fft_values = np.fft.fft(time_series)
    fft_freq = np.fft.fftfreq(n, d=1.0/sampling_rate)
    
    # Take positive frequencies only (real signal symmetry)
    positive_freq_idx = fft_freq > 0
    frequencies = fft_freq[positive_freq_idx]
    magnitudes = np.abs(fft_values[positive_freq_idx])
    
    # Find top 5 dominant frequencies
    top_5_idx = np.argsort(magnitudes)[-5:][::-1]
    top_5_frequencies = frequencies[top_5_idx].tolist()
    
    return {
        'frequencies': frequencies,
        'magnitudes': magnitudes,
        'top_5_frequencies': top_5_frequencies
    }
```

#### analysis/least_squares.py

```python
from sklearn.linear_model import LinearRegression

def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> dict:
    """
    Fit linear regression using least squares method.
    
    Mathematical basis:
    Least squares minimizes Σ(y_i - ŷ_i)².
    Solution: β = (X^T X)^(-1) X^T y
    
    Args:
        X: Independent variable (time), shape (n_samples, 1)
        y: Dependent variable (packet_size), shape (n_samples,)
        
    Returns:
        {
            'predictions': np.ndarray,
            'coefficients': np.ndarray,  # [intercept, slope]
            'r_squared': float,
            'residuals': np.ndarray
        }
    """
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
```

#### analysis/anomaly_detection.py

```python
def detect_anomalies(actual: np.ndarray, predicted: np.ndarray, 
                     timestamps: list, threshold: float = 2.0) -> list:
    """
    Detect anomalies using statistical deviation.
    
    Algorithm:
    1. Compute residuals: r = actual - predicted
    2. Calculate std dev: σ = std(residuals)
    3. Mark as anomaly if |r| > threshold × σ
    
    Args:
        actual: Actual traffic values
        predicted: Predicted values
        timestamps: Corresponding timestamps
        threshold: Number of standard deviations (default: 2.0)
        
    Returns:
        List of anomaly records
    """
    residuals = actual - predicted
    std_dev = np.std(residuals)
    
    anomalies = []
    for i, (act, pred, ts, res) in enumerate(zip(actual, predicted, timestamps, residuals)):
        if abs(res) > threshold * std_dev:
            anomalies.append({
                'timestamp': ts,
                'actual': float(act),
                'predicted': float(pred),
                'deviation': float(abs(res) / std_dev),
                'residual': float(res)
            })
    
    return anomalies
```

### Frontend Implementation

#### charts.js

```javascript
// Fetch and render all visualizations
async function loadAllVisualizations() {
    await loadTrafficVisualization();
    await loadPCAVisualization();
    await loadFrequencyVisualization();
    await loadAnomalyVisualization();
}

async function loadTrafficVisualization() {
    const response = await fetch('/visualize');
    const data = await response.json();
    
    // Line chart: Traffic over time
    const trace1 = {
        x: data.traffic_over_time.timestamps,
        y: data.traffic_over_time.packet_sizes,
        mode: 'lines',
        name: 'Original',
        line: {color: '#1f77b4'}
    };
    
    const trace2 = {
        x: data.traffic_over_time.timestamps,
        y: data.traffic_over_time.smoothed_sizes,
        mode: 'lines',
        name: 'PDE Smoothed',
        line: {color: '#ff7f0e', dash: 'dash'}
    };
    
    const layout = {
        title: 'Network Traffic Over Time (PDE Smoothing)',
        xaxis: {title: 'Time'},
        yaxis: {title: 'Packet Size (bytes)'}
    };
    
    Plotly.newPlot('traffic-chart', [trace1, trace2], layout);
    
    // Heatmap: Traffic intensity
    const heatmapTrace = {
        z: data.heatmap_data.intensity_matrix,
        x: data.heatmap_data.time_intervals,
        y: data.heatmap_data.ip_addresses,
        type: 'heatmap',
        colorscale: 'Viridis'
    };
    
    const heatmapLayout = {
        title: 'Traffic Intensity Heatmap',
        xaxis: {title: 'Time Interval'},
        yaxis: {title: 'IP Address'}
    };
    
    Plotly.newPlot('heatmap-chart', [heatmapTrace], heatmapLayout);
}

async function loadPCAVisualization() {
    const response = await fetch('/pca');
    const data = await response.json();
    
    const trace = {
        x: data.transformed_coordinates.map(c => c[0]),
        y: data.transformed_coordinates.map(c => c[1]),
        mode: 'markers',
        type: 'scatter',
        text: data.labels,
        marker: {
            size: 8,
            color: data.labels.map(l => l === 'TCP' ? 0 : l === 'UDP' ? 1 : 2),
            colorscale: 'Viridis'
        }
    };
    
    const layout = {
        title: `PCA 2D Projection (Explained Variance: PC1=${(data.explained_variance[0]*100).toFixed(1)}%, PC2=${(data.explained_variance[1]*100).toFixed(1)}%)`,
        xaxis: {title: 'Principal Component 1'},
        yaxis: {title: 'Principal Component 2'}
    };
    
    Plotly.newPlot('pca-chart', [trace], layout);
}

async function loadFrequencyVisualization() {
    const response = await fetch('/frequency');
    const data = await response.json();
    
    const trace = {
        x: data.frequencies,
        y: data.magnitudes,
        mode: 'lines',
        line: {color: '#2ca02c'}
    };
    
    const layout = {
        title: `Frequency Spectrum (Top 5: ${data.top_5_frequencies.map(f => f.toFixed(2)).join(', ')})`,
        xaxis: {title: 'Frequency (Hz)'},
        yaxis: {title: 'Magnitude'}
    };
    
    Plotly.newPlot('frequency-chart', [trace], layout);
}

async function loadAnomalyVisualization() {
    const response = await fetch('/anomalies');
    const data = await response.json();
    
    // Extract data for plotting
    const timestamps = data.anomalies.map(a => a.timestamp);
    const actual = data.anomalies.map(a => a.actual);
    const predicted = data.anomalies.map(a => a.predicted);
    
    const trace1 = {
        x: timestamps,
        y: actual,
        mode: 'markers',
        name: 'Anomalies (Actual)',
        marker: {color: 'red', size: 10}
    };
    
    const trace2 = {
        x: timestamps,
        y: predicted,
        mode: 'markers',
        name: 'Expected (Predicted)',
        marker: {color: 'blue', size: 8}
    };
    
    const layout = {
        title: `Detected Anomalies (${data.total_count} found, R²=${data.r_squared.toFixed(3)})`,
        xaxis: {title: 'Time'},
        yaxis: {title: 'Packet Size (bytes)'}
    };
    
    Plotly.newPlot('anomaly-chart', [trace1, trace2], layout);
}

// Load visualizations on page load
document.addEventListener('DOMContentLoaded', loadAllVisualizations);
```

### Deployment and Execution

**Installation**:
```bash
pip install -r requirements.txt
```

**Running the Application**:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Accessing the Application**:
- Landing page: http://127.0.0.1:8000/
- Dashboard: http://127.0.0.1:8000/dashboard.html
- API docs: http://127.0.0.1:8000/docs (FastAPI auto-generated)

**Development Mode**:
```bash
uvicorn main:app --reload --log-level debug
```

### Performance Considerations

1. **Data Size Limits**:
   - CSV upload: 50 MB maximum
   - In-memory storage: Suitable for datasets up to 100,000 records
   - For larger datasets, consider database storage

2. **Analysis Optimization**:
   - Cache analysis results to avoid recomputation
   - Use NumPy vectorized operations (avoid Python loops)
   - Lazy loading: compute analysis only when requested

3. **Frontend Performance**:
   - Plotly handles up to 10,000 points efficiently
   - For larger datasets, downsample for visualization
   - Use Plotly's built-in zoom and pan for interactivity

### Security Considerations

Since this is a localhost demonstration application:

1. **No Authentication Required**: Application runs on localhost only
2. **File Upload Validation**: Validate CSV structure and size limits
3. **Input Sanitization**: Validate all user inputs before processing
4. **Error Messages**: Don't expose internal system details in production
5. **CORS**: Restrict to localhost origins only

### Future Enhancements

Potential extensions beyond the current requirements:

1. **Real-time Analysis**: Stream network traffic in real-time
2. **Multiple Datasets**: Compare multiple traffic captures
3. **Export Results**: Download analysis results as PDF/CSV
4. **Advanced Anomaly Detection**: Machine learning models (Isolation Forest, Autoencoders)
5. **Database Integration**: PostgreSQL for persistent storage
6. **Distributed Processing**: Dask for large-scale data processing

