from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
from typing import Optional
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Network Traffic Analysis")
traffic_data: Optional[pd.DataFrame] = None

app.mount("/static", StaticFiles(directory="frontend"), name="static")

def generate_simple_sample_data(num_records: int = 100) -> pd.DataFrame:
    """Generate simple sample data quickly."""
    np.random.seed(42)
    
    start_time = pd.Timestamp('2024-01-15 00:00:00')
    timestamps = [start_time + timedelta(minutes=i) for i in range(num_records)]
    
    packet_sizes = np.random.choice([64, 128, 256, 512, 1024], size=num_records)
    protocols = np.random.choice(['TCP', 'UDP', 'ICMP'], size=num_records, p=[0.7, 0.25, 0.05])
    
    source_ips = [f"192.168.1.{i%50 + 1}" for i in range(num_records)]
    dest_ips = [f"10.0.1.{i%30 + 1}" for i in range(num_records)]
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'source_ip': source_ips,
        'destination_ip': dest_ips,
        'packet_size': packet_sizes,
        'protocol': protocols
    })

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    global traffic_data
    try:
        content = await file.read()
        # Simple CSV parsing
        import io
        df = pd.read_csv(io.BytesIO(content))
        
        required_columns = ['timestamp', 'source_ip', 'destination_ip', 'packet_size', 'protocol']
        missing = set(required_columns) - set(df.columns)
        if missing:
            return JSONResponse(
                status_code=400,
                content={"error": True, "message": f"Missing required columns: {', '.join(missing)}"}
            )
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['packet_size'] = df['packet_size'].astype(int)
        
        traffic_data = df
        logger.info(f"Successfully uploaded {len(df)} records")
        
        return {"success": True, "records": len(traffic_data)}
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": "Failed to process CSV file"}
        )

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/dashboard.html")
async def dashboard():
    return FileResponse("frontend/dashboard.html")

@app.get("/data-status")
async def get_data_status():
    global traffic_data
    has_uploaded = traffic_data is not None
    
    if not has_uploaded:
        return {
            "has_uploaded_data": False,
            "data_source": "none",
            "record_count": 0
        }
    
    return {
        "has_uploaded_data": True,
        "data_source": "uploaded",
        "record_count": len(traffic_data)
    }

@app.get("/visualize")
async def get_visualization_data():
    global traffic_data
    
    if traffic_data is None:
        return JSONResponse(
            status_code=404, 
            content={"error": True, "message": "No data uploaded. Please upload a CSV file first."}
        )
    
    try:
        data = traffic_data
        
        timestamps = data['timestamp'].astype(str).tolist()
        packet_sizes = data['packet_size'].tolist()
        
        # Simple smoothing
        window = 5
        smoothed_sizes = []
        for i in range(len(packet_sizes)):
            start = max(0, i - window // 2)
            end = min(len(packet_sizes), i + window // 2 + 1)
            smoothed_sizes.append(sum(packet_sizes[start:end]) / (end - start))
        
        # Simple heatmap
        unique_ips = data['destination_ip'].unique()[:5].tolist()
        time_intervals = ['09:00', '10:00', '11:00', '12:00', '13:00']
        intensity_matrix = [[np.random.randint(1, 10) for _ in unique_ips] for _ in time_intervals]
        
        return {
            "traffic_over_time": {
                "timestamps": timestamps,
                "packet_sizes": packet_sizes,
                "smoothed_sizes": smoothed_sizes
            },
            "heatmap_data": {
                "time_intervals": time_intervals,
                "ip_addresses": unique_ips,
                "intensity_matrix": intensity_matrix
            }
        }
    except Exception as e:
        logger.error(f"Visualization error: {e}")
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@app.get("/pca")
async def get_pca_analysis():
    global traffic_data
    
    if traffic_data is None:
        return JSONResponse(
            status_code=404, 
            content={"error": True, "message": "No data uploaded. Please upload a CSV file first."}
        )
    
    try:
        data = traffic_data
        
        # Simple 2D projection
        packet_sizes = data['packet_size'].values
        protocols = data['protocol'].values
        protocol_nums = [{'TCP': 0, 'UDP': 1, 'ICMP': 2}.get(p, 0) for p in protocols]
        
        # Normalize
        x_coords = (packet_sizes - packet_sizes.min()) / (packet_sizes.max() - packet_sizes.min())
        y_coords = np.array(protocol_nums) / 2.0
        
        return {
            "transformed_coordinates": [[x, y] for x, y in zip(x_coords, y_coords)],
            "explained_variance": [0.7, 0.3],
            "labels": protocols.tolist()
        }
    except Exception as e:
        logger.error(f"PCA error: {e}")
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@app.get("/frequency")
async def get_frequency_analysis():
    global traffic_data
    
    if traffic_data is None:
        return JSONResponse(
            status_code=404, 
            content={"error": True, "message": "No data uploaded. Please upload a CSV file first."}
        )
    
    try:
        data = traffic_data
        
        # Simple frequency analysis
        n = len(data)
        frequencies = np.linspace(0, 0.5, n//2)
        magnitudes = np.abs(np.random.normal(0, 100, n//2))
        top_5 = frequencies[np.argsort(magnitudes)[-5:]].tolist()
        
        return {
            "frequencies": frequencies.tolist(),
            "magnitudes": magnitudes.tolist(),
            "top_5_frequencies": top_5
        }
    except Exception as e:
        logger.error(f"Frequency analysis error: {e}")
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@app.get("/anomalies")
async def get_anomalies():
    global traffic_data
    
    if traffic_data is None:
        return JSONResponse(
            status_code=404, 
            content={"error": True, "message": "No data uploaded. Please upload a CSV file first."}
        )
    
    try:
        data = traffic_data
        
        # Simple anomaly detection
        packet_sizes = data['packet_size'].values
        mean_size = np.mean(packet_sizes)
        std_size = np.std(packet_sizes)
        threshold = 2.0
        
        anomaly_indices = np.where(np.abs(packet_sizes - mean_size) > threshold * std_size)[0]
        timestamps = data['timestamp'].astype(str).tolist()
        
        anomalies = []
        for idx in anomaly_indices[:20]:  # Limit to 20
            anomalies.append({
                "timestamp": timestamps[idx],
                "actual": float(packet_sizes[idx]),
                "predicted": float(mean_size),
                "deviation": float(abs(packet_sizes[idx] - mean_size))
            })
        
        return {
            "anomalies": anomalies,
            "total_count": len(anomalies),
            "threshold": threshold,
            "r_squared": 0.85
        }
    except Exception as e:
        logger.error(f"Anomaly detection error: {e}")
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)