// Plotly theme configuration
const plotlyTheme = {
    paper_bgcolor: '#1e293b',
    plot_bgcolor: '#1e293b',
    font: {
        family: 'Inter, sans-serif',
        color: '#cbd5e1'
    },
    xaxis: {
        gridcolor: 'rgba(99, 102, 241, 0.1)',
        zerolinecolor: 'rgba(99, 102, 241, 0.2)'
    },
    yaxis: {
        gridcolor: 'rgba(99, 102, 241, 0.1)',
        zerolinecolor: 'rgba(99, 102, 241, 0.2)'
    }
};

function showChartLoading(chartId, message) {
    document.getElementById(chartId).innerHTML = `
        <div class="chart-loading">
            <div class="spinner"></div>
            <div class="loading-message">${message}</div>
        </div>
    `;
}

function updateLoadingMessage(chartId, message) {
    const loadingElement = document.getElementById(chartId).querySelector('.loading-message');
    if (loadingElement) {
        loadingElement.textContent = message;
    }
}

async function loadAllVisualizations() {
    // Check data status first
    try {
        const statusResponse = await fetch('/data-status');
        const statusData = await statusResponse.json();
        
        const banner = document.getElementById('dataStatusBanner');
        const subtitle = document.getElementById('dashboardSubtitle');
        
        if (!statusData.has_uploaded_data || statusData.record_count === 0) {
            // No data - show no-data state for all charts
            banner.classList.remove('hidden');
            subtitle.textContent = 'No Data - Upload CSV to Begin Analysis';
            
            // Show no-data state for all charts immediately
            const noDataHTML = (icon, title) => `
                <div class="chart-no-data">
                    <div class="no-data-icon">${icon}</div>
                    <div class="no-data-title">No Data Available</div>
                    <div class="no-data-message">${title}</div>
                    <a href="/" class="no-data-button">Upload Data</a>
                </div>
            `;
            
            document.getElementById('traffic-chart').innerHTML = noDataHTML('🌊', 'Upload CSV to see traffic analysis');
            document.getElementById('heatmap-chart').innerHTML = noDataHTML('🔥', 'Upload CSV to see traffic heatmap');
            document.getElementById('pca-chart').innerHTML = noDataHTML('🎯', 'Upload CSV to see PCA analysis');
            document.getElementById('frequency-chart').innerHTML = noDataHTML('📡', 'Upload CSV to see frequency analysis');
            document.getElementById('anomaly-chart').innerHTML = noDataHTML('⚠️', 'Upload CSV to see anomaly detection');
            
            // Update stats to show no data
            document.getElementById('totalRecords').textContent = '0';
            document.getElementById('anomalyCount').textContent = '0';
            document.getElementById('modelAccuracy').textContent = '-';
            document.getElementById('pcaVariance').textContent = '-';
            
            return; // Stop here - don't try to load charts
        } else {
            // Hide banner for uploaded data
            banner.classList.add('hidden');
            subtitle.textContent = `Analysis of ${statusData.record_count.toLocaleString()} Traffic Records`;
        }
    } catch (error) {
        console.error('Error checking data status:', error);
    }
    
    // Show initial loading states
    showChartLoading('traffic-chart', '🌊 Loading traffic data...');
    showChartLoading('heatmap-chart', '🔥 Loading heatmap...');
    showChartLoading('normalization-chart', '📊 Loading normalization...');
    showChartLoading('pca-chart', '🎯 Loading PCA analysis...');
    showChartLoading('frequency-chart', '📡 Loading frequency analysis...');
    showChartLoading('anomaly-chart', '⚠️ Loading anomaly detection...');
    
    // Load all visualizations immediately (no delays)
    loadTrafficVisualization();
    loadNormalizationVisualization();
    loadPCAVisualization();
    loadFrequencyVisualization();
    loadAnomalyVisualization();
}

async function loadTrafficVisualization() {
    try {
        updateLoadingMessage('traffic-chart', '📊 Fetching traffic data...');
        const response = await fetch('/visualize');
        
        if (response.status === 404) {
            // No data uploaded
            document.getElementById('traffic-chart').innerHTML = `
                <div class="chart-no-data">
                    <div class="no-data-icon">📊</div>
                    <div class="no-data-title">No Data Available</div>
                    <div class="no-data-message">Upload a CSV file to see traffic analysis</div>
                    <a href="/" class="no-data-button">Upload Data</a>
                </div>
            `;
            document.getElementById('heatmap-chart').innerHTML = `
                <div class="chart-no-data">
                    <div class="no-data-icon">🔥</div>
                    <div class="no-data-title">No Data Available</div>
                    <div class="no-data-message">Upload a CSV file to see traffic heatmap</div>
                    <a href="/" class="no-data-button">Upload Data</a>
                </div>
            `;
            return;
        }
        
        const data = await response.json();
        
        updateLoadingMessage('traffic-chart', '🧮 Applying Gaussian filtering...');
        
        // Update stats
        document.getElementById('totalRecords').textContent = data.traffic_over_time.timestamps.length.toLocaleString();
        
        const trace1 = {
            x: data.traffic_over_time.timestamps,
            y: data.traffic_over_time.packet_sizes,
            mode: 'lines',
            name: 'Original Traffic',
            line: {
                color: '#818cf8',
                width: 2
            },
            hovertemplate: '<b>Time:</b> %{x}<br><b>Size:</b> %{y} bytes<extra></extra>'
        };
        
        const trace2 = {
            x: data.traffic_over_time.timestamps,
            y: data.traffic_over_time.smoothed_sizes,
            mode: 'lines',
            name: 'PDE Smoothed',
            line: {
                color: '#ec4899',
                width: 3,
                dash: 'dash'
            },
            hovertemplate: '<b>Time:</b> %{x}<br><b>Smoothed:</b> %{y} bytes<extra></extra>'
        };
        
        const layout = {
            ...plotlyTheme,
            title: {
                text: 'Network Traffic Flow Analysis',
                font: { size: 16, color: '#fff' }
            },
            xaxis: {
                ...plotlyTheme.xaxis,
                title: 'Timestamp',
                showgrid: true
            },
            yaxis: {
                ...plotlyTheme.yaxis,
                title: 'Packet Size (bytes)',
                showgrid: true
            },
            hovermode: 'x unified',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(30, 41, 59, 0.8)',
                bordercolor: 'rgba(99, 102, 241, 0.3)',
                borderwidth: 1
            }
        };
        
        updateLoadingMessage('traffic-chart', '📈 Rendering visualization...');
        // Clear loading state and render chart
        document.getElementById('traffic-chart').innerHTML = '';
        Plotly.newPlot('traffic-chart', [trace1, trace2], layout, {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['lasso2d', 'select2d']
        });
        
        // Heatmap visualization
        updateLoadingMessage('heatmap-chart', '🔥 Building intensity matrix...');
        // Clear loading state
        document.getElementById('heatmap-chart').innerHTML = '';
        const heatmapTrace = {
                z: data.heatmap_data.intensity_matrix,
                x: data.heatmap_data.time_intervals,
                y: data.heatmap_data.ip_addresses,
                type: 'heatmap',
                colorscale: [
                    [0, '#0f172a'],
                    [0.25, '#6366f1'],
                    [0.5, '#8b5cf6'],
                    [0.75, '#ec4899'],
                    [1, '#f59e0b']
                ],
                colorbar: {
                    title: 'Traffic<br>Count',
                    titleside: 'right',
                    tickmode: 'linear',
                    tick0: 0,
                    dtick: 1,
                    thickness: 15,
                    len: 0.7,
                    bgcolor: 'rgba(30, 41, 59, 0.8)',
                    bordercolor: 'rgba(99, 102, 241, 0.3)',
                    borderwidth: 1
                },
                hovertemplate: '<b>Time:</b> %{x}<br><b>IP:</b> %{y}<br><b>Count:</b> %{z}<extra></extra>'
            };
            
            const heatmapLayout = {
                ...plotlyTheme,
                title: {
                    text: 'Traffic Distribution Matrix',
                    font: { size: 16, color: '#fff' }
                },
                xaxis: {
                    ...plotlyTheme.xaxis,
                    title: 'Time Interval',
                    side: 'bottom'
                },
                yaxis: {
                    ...plotlyTheme.yaxis,
                    title: 'Destination IP',
                    automargin: true
                },
                hovermode: 'closest'
            };
            
            Plotly.newPlot('heatmap-chart', [heatmapTrace], heatmapLayout, {
                responsive: true,
                displayModeBar: true
            });
    } catch (error) {
        console.error('Error loading traffic visualization:', error);
        document.getElementById('traffic-chart').innerHTML = '<div class="chart-error">❌ Failed to load traffic data</div>';
        document.getElementById('heatmap-chart').innerHTML = '<div class="chart-error">❌ Failed to load heatmap</div>';
    }
}

async function loadNormalizationVisualization() {
    try {
        updateLoadingMessage('normalization-chart', '📊 Computing transformations...');
        const response = await fetch('/normalization');
        
        if (response.status === 404) {
            document.getElementById('normalization-chart').innerHTML = `
                <div class="chart-no-data">
                    <div class="no-data-icon">📊</div>
                    <div class="no-data-title">No Data Available</div>
                    <div class="no-data-message">Upload a CSV file to see normalization</div>
                    <a href="/" class="no-data-button">Upload Data</a>
                </div>
            `;
            return;
        }
        
        const data = await response.json();
        
        const trace1 = {
            x: data.indices,
            y: data.original,
            mode: 'lines+markers',
            name: 'Original Data',
            line: {
                color: '#ef4444',
                width: 2
            },
            marker: {
                size: 4,
                color: '#ef4444'
            },
            hovertemplate: '<b>Original:</b> %{y:.2f}<extra></extra>'
        };
        
        const trace2 = {
            x: data.indices,
            y: data.normalized,
            mode: 'lines+markers',
            name: 'Min-Max Normalized',
            line: {
                color: '#10b981',
                width: 2
            },
            marker: {
                size: 4,
                color: '#10b981'
            },
            hovertemplate: '<b>Normalized:</b> %{y:.3f}<extra></extra>'
        };
        
        const trace3 = {
            x: data.indices,
            y: data.standardized,
            mode: 'lines+markers',
            name: 'Z-Score Standardized',
            line: {
                color: '#1e90ff',
                width: 2
            },
            marker: {
                size: 4,
                color: '#1e90ff'
            },
            hovertemplate: '<b>Standardized:</b> %{y:.3f}<extra></extra>'
        };
        
        const layout = {
            ...plotlyTheme,
            title: {
                text: `Linear Transformations Applied<br><sub>Original: [${data.stats.original_min.toFixed(0)}, ${data.stats.original_max.toFixed(0)}] → Normalized: [0, 1] | Standardized: μ=0, σ=1</sub>`,
                font: { size: 16, color: '#fff' }
            },
            xaxis: {
                ...plotlyTheme.xaxis,
                title: 'Data Point Index',
                showgrid: true
            },
            yaxis: {
                ...plotlyTheme.yaxis,
                title: 'Value',
                showgrid: true
            },
            hovermode: 'x unified',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(30, 41, 59, 0.8)',
                bordercolor: 'rgba(99, 102, 241, 0.3)',
                borderwidth: 1
            }
        };
        
        document.getElementById('normalization-chart').innerHTML = '';
        Plotly.newPlot('normalization-chart', [trace1, trace2, trace3], layout, {
            responsive: true,
            displayModeBar: true
        });
    } catch (error) {
        console.error('Error loading normalization visualization:', error);
        document.getElementById('normalization-chart').innerHTML = '<div class="chart-error">❌ Failed to load normalization visualization</div>';
    }
}

async function loadPCAVisualization() {
    try {
        updateLoadingMessage('pca-chart', '🎯 Computing covariance matrix...');
        const response = await fetch('/pca');
        
        if (response.status === 404) {
            document.getElementById('pca-chart').innerHTML = `
                <div class="chart-no-data">
                    <div class="no-data-icon">🎯</div>
                    <div class="no-data-title">No Data Available</div>
                    <div class="no-data-message">Upload a CSV file to see PCA analysis</div>
                    <a href="/" class="no-data-button">Upload Data</a>
                </div>
            `;
            return;
        }
        
        const data = await response.json();
        
        updateLoadingMessage('pca-chart', '🔍 Finding principal components...');
        
        // Update PCA variance stat
        const totalVariance = ((data.explained_variance[0] + data.explained_variance[1]) * 100).toFixed(1);
        document.getElementById('pcaVariance').textContent = totalVariance + '%';
        
        const protocolColors = {
            'TCP': '#6366f1',
            'UDP': '#8b5cf6',
            'ICMP': '#ec4899'
        };
        
        const trace = {
            x: data.transformed_coordinates.map(c => c[0]),
            y: data.transformed_coordinates.map(c => c[1]),
            mode: 'markers',
            type: 'scatter',
            text: data.labels,
            marker: {
                size: 10,
                color: data.labels.map(l => protocolColors[l] || '#64748b'),
                opacity: 0.8,
                line: {
                    color: '#fff',
                    width: 1
                }
            },
            hovertemplate: '<b>Protocol:</b> %{text}<br><b>PC1:</b> %{x:.3f}<br><b>PC2:</b> %{y:.3f}<extra></extra>'
        };
        
        const layout = {
            ...plotlyTheme,
            title: {
                text: `Principal Component Analysis<br><sub>PC1: ${(data.explained_variance[0]*100).toFixed(1)}% | PC2: ${(data.explained_variance[1]*100).toFixed(1)}%</sub>`,
                font: { size: 16, color: '#fff' }
            },
            xaxis: {
                ...plotlyTheme.xaxis,
                title: 'Principal Component 1',
                zeroline: true
            },
            yaxis: {
                ...plotlyTheme.yaxis,
                title: 'Principal Component 2',
                zeroline: true
            },
            hovermode: 'closest'
        };
        
        updateLoadingMessage('pca-chart', '📊 Rendering 2D projection...');
        // Clear loading state and render chart
        document.getElementById('pca-chart').innerHTML = '';
        Plotly.newPlot('pca-chart', [trace], layout, {
            responsive: true,
            displayModeBar: true
        });
    } catch (error) {
        console.error('Error loading PCA visualization:', error);
        document.getElementById('pca-chart').innerHTML = '<div class="chart-error">❌ Failed to load PCA analysis</div>';
    }
}

async function loadFrequencyVisualization() {
    try {
        updateLoadingMessage('frequency-chart', '📡 Computing FFT transform...');
        const response = await fetch('/frequency');
        
        if (response.status === 404) {
            document.getElementById('frequency-chart').innerHTML = `
                <div class="chart-no-data">
                    <div class="no-data-icon">📡</div>
                    <div class="no-data-title">No Data Available</div>
                    <div class="no-data-message">Upload a CSV file to see frequency analysis</div>
                    <a href="/" class="no-data-button">Upload Data</a>
                </div>
            `;
            return;
        }
        
        const data = await response.json();
        
        updateLoadingMessage('frequency-chart', '🔍 Identifying dominant frequencies...');
        
        const trace = {
            x: data.frequencies,
            y: data.magnitudes,
            mode: 'lines',
            fill: 'tozeroy',
            line: {
                color: '#10b981',
                width: 3
            },
            fillcolor: 'rgba(16, 185, 129, 0.2)',
            hovertemplate: '<b>Frequency:</b> %{x:.3f} Hz<br><b>Magnitude:</b> %{y:.2f}<extra></extra>'
        };
        
        const layout = {
            ...plotlyTheme,
            title: {
                text: `Frequency Domain Analysis<br><sub>Top 5: ${data.top_5_frequencies.map(f => f.toFixed(2)).join(', ')} Hz</sub>`,
                font: { size: 16, color: '#fff' }
            },
            xaxis: {
                ...plotlyTheme.xaxis,
                title: 'Frequency (Hz)',
                showgrid: true
            },
            yaxis: {
                ...plotlyTheme.yaxis,
                title: 'Magnitude',
                showgrid: true
            },
            hovermode: 'x unified'
        };
        
        updateLoadingMessage('frequency-chart', '📈 Rendering spectrum...');
        // Clear loading state and render chart
        document.getElementById('frequency-chart').innerHTML = '';
        Plotly.newPlot('frequency-chart', [trace], layout, {
            responsive: true,
            displayModeBar: true
        });
    } catch (error) {
        console.error('Error loading frequency visualization:', error);
        document.getElementById('frequency-chart').innerHTML = '<div class="chart-error">❌ Failed to load frequency analysis</div>';
    }
}

async function loadAnomalyVisualization() {
    try {
        updateLoadingMessage('anomaly-chart', '📈 Fitting regression model...');
        const response = await fetch('/anomalies');
        
        if (response.status === 404) {
            document.getElementById('anomaly-chart').innerHTML = `
                <div class="chart-no-data">
                    <div class="no-data-icon">⚠️</div>
                    <div class="no-data-title">No Data Available</div>
                    <div class="no-data-message">Upload a CSV file to see anomaly detection</div>
                    <a href="/" class="no-data-button">Upload Data</a>
                </div>
            `;
            return;
        }
        
        const data = await response.json();
        
        updateLoadingMessage('anomaly-chart', '🔍 Computing residuals and thresholds...');
        
        // Update stats
        document.getElementById('anomalyCount').textContent = data.total_count;
        document.getElementById('anomalyChange').textContent = `${((data.total_count / 1000) * 100).toFixed(1)}% of traffic`;
        document.getElementById('modelAccuracy').textContent = data.r_squared.toFixed(3);
        
        const timestamps = data.anomalies.map(a => a.timestamp);
        const actual = data.anomalies.map(a => a.actual);
        const predicted = data.anomalies.map(a => a.predicted);
        
        const trace1 = {
            x: timestamps,
            y: actual,
            mode: 'markers',
            name: 'Anomalies Detected',
            marker: {
                color: '#ef4444',
                size: 12,
                symbol: 'x',
                line: {
                    color: '#fff',
                    width: 2
                }
            },
            hovertemplate: '<b>Time:</b> %{x}<br><b>Actual:</b> %{y} bytes<br><b>Status:</b> Anomaly<extra></extra>'
        };
        
        const trace2 = {
            x: timestamps,
            y: predicted,
            mode: 'markers',
            name: 'Expected Values',
            marker: {
                color: '#6366f1',
                size: 8,
                opacity: 0.6
            },
            hovertemplate: '<b>Time:</b> %{x}<br><b>Predicted:</b> %{y} bytes<extra></extra>'
        };
        
        const layout = {
            ...plotlyTheme,
            title: {
                text: `Anomaly Detection Results<br><sub>${data.total_count} anomalies found | R² = ${data.r_squared.toFixed(3)} | Threshold: ${data.threshold}σ</sub>`,
                font: { size: 16, color: '#fff' }
            },
            xaxis: {
                ...plotlyTheme.xaxis,
                title: 'Timestamp',
                showgrid: true
            },
            yaxis: {
                ...plotlyTheme.yaxis,
                title: 'Packet Size (bytes)',
                showgrid: true
            },
            hovermode: 'closest',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(30, 41, 59, 0.8)',
                bordercolor: 'rgba(99, 102, 241, 0.3)',
                borderwidth: 1
            }
        };
        
        updateLoadingMessage('anomaly-chart', '📊 Rendering anomaly detection...');
        // Clear loading state and render chart
        document.getElementById('anomaly-chart').innerHTML = '';
        Plotly.newPlot('anomaly-chart', [trace1, trace2], layout, {
            responsive: true,
            displayModeBar: true
        });
    } catch (error) {
        console.error('Error loading anomaly visualization:', error);
        document.getElementById('anomaly-chart').innerHTML = '<div class="chart-error">❌ Failed to load anomaly detection</div>';
    }
}

document.addEventListener('DOMContentLoaded', loadAllVisualizations);

// Update mathematical analysis section with computed values
async function updateMathematicalAnalysis() {
    try {
        // Fetch all analysis data
        const [pcaResponse, freqResponse, anomalyResponse] = await Promise.all([
            fetch('/pca'),
            fetch('/frequency'),
            fetch('/anomalies')
        ]);
        
        if (pcaResponse.ok) {
            const pcaData = await pcaResponse.json();
            const totalVariance = ((pcaData.explained_variance[0] + pcaData.explained_variance[1]) * 100).toFixed(1);
            document.getElementById('pcaVarianceExplained').textContent = `${totalVariance}% (PC1: ${(pcaData.explained_variance[0]*100).toFixed(1)}%, PC2: ${(pcaData.explained_variance[1]*100).toFixed(1)}%)`;
        }
        
        if (freqResponse.ok) {
            const freqData = await freqResponse.json();
            const topFreqs = freqData.top_5_frequencies.slice(0, 3).map(f => f.toFixed(3)).join(', ');
            document.getElementById('topFrequencies').textContent = `${topFreqs} Hz`;
        }
        
        if (anomalyResponse.ok) {
            const anomalyData = await anomalyResponse.json();
            document.getElementById('rSquaredValue').textContent = anomalyData.r_squared.toFixed(4);
            document.getElementById('anomaliesFound').textContent = `${anomalyData.total_count} (${anomalyData.threshold}σ threshold)`;
        }
    } catch (error) {
        console.error('Error updating mathematical analysis:', error);
    }
}

// Call this after all visualizations are loaded
document.addEventListener('DOMContentLoaded', () => {
    loadAllVisualizations().then(() => {
        updateMathematicalAnalysis();
    });
});
