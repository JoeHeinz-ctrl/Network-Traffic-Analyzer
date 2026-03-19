#!/usr/bin/env python3
"""
Generate a large network traffic dataset (~30MB) for testing the analysis system.
Creates realistic network traffic patterns with anomalies for demonstration.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import csv

def generate_large_network_dataset(target_size_mb=30, filename="large_network_traffic.csv"):
    """Generate a large network traffic dataset with realistic patterns."""
    
    print(f"🚀 Generating large network traffic dataset (~{target_size_mb}MB)...")
    
    # Estimate records needed (approximately 150 bytes per record)
    estimated_records = (target_size_mb * 1024 * 1024) // 150
    print(f"📊 Target records: ~{estimated_records:,}")
    
    # Set random seed for reproducible results
    np.random.seed(42)
    random.seed(42)
    
    # Time range: 7 days of traffic data
    start_time = datetime(2024, 1, 15, 0, 0, 0)
    end_time = start_time + timedelta(days=7)
    
    # Network configuration
    internal_subnets = [
        "192.168.1", "192.168.2", "10.0.0", "10.0.1", 
        "172.16.1", "172.16.2", "10.10.0", "10.10.1"
    ]
    
    external_ips = [
        "8.8.8.8", "1.1.1.1", "208.67.222.222", "9.9.9.9",
        "74.125.224.72", "151.101.193.140", "104.16.249.249",
        "13.107.42.14", "52.96.0.0", "23.185.0.2"
    ]
    
    protocols = ["TCP", "UDP", "ICMP"]
    protocol_weights = [0.75, 0.20, 0.05]  # TCP dominant
    
    # Packet size distributions (realistic)
    packet_sizes = {
        "TCP": [64, 128, 256, 512, 1024, 1500],
        "UDP": [64, 128, 256, 512, 1024],
        "ICMP": [64, 128, 256]
    }
    
    packet_weights = {
        "TCP": [0.15, 0.20, 0.25, 0.25, 0.10, 0.05],
        "UDP": [0.20, 0.25, 0.30, 0.20, 0.05],
        "ICMP": [0.60, 0.30, 0.10]
    }
    
    print("🔄 Generating traffic records...")
    
    records = []
    current_time = start_time
    
    # Generate records in batches to manage memory
    batch_size = 10000
    total_generated = 0
    
    while total_generated < estimated_records:
        batch_records = []
        
        for _ in range(min(batch_size, estimated_records - total_generated)):
            # Time progression (not perfectly sequential for realism)
            time_increment = random.uniform(0.1, 5.0)  # 0.1 to 5 seconds
            current_time += timedelta(seconds=time_increment)
            
            if current_time > end_time:
                current_time = start_time + timedelta(
                    seconds=random.uniform(0, (end_time - start_time).total_seconds())
                )
            
            # Protocol selection
            protocol = np.random.choice(protocols, p=protocol_weights)
            
            # Packet size based on protocol
            packet_size = np.random.choice(
                packet_sizes[protocol], 
                p=packet_weights[protocol]
            )
            
            # IP address generation
            if random.random() < 0.7:  # 70% internal to external
                source_subnet = random.choice(internal_subnets)
                source_ip = f"{source_subnet}.{random.randint(10, 254)}"
                destination_ip = random.choice(external_ips)
            elif random.random() < 0.5:  # 15% external to internal
                source_ip = random.choice(external_ips)
                dest_subnet = random.choice(internal_subnets)
                destination_ip = f"{dest_subnet}.{random.randint(10, 254)}"
            else:  # 15% internal to internal
                source_subnet = random.choice(internal_subnets)
                dest_subnet = random.choice(internal_subnets)
                source_ip = f"{source_subnet}.{random.randint(10, 254)}"
                destination_ip = f"{dest_subnet}.{random.randint(10, 254)}"
            
            # Add some anomalies (5% of traffic)
            if random.random() < 0.05:
                # Anomalous packet sizes
                if protocol == "TCP":
                    packet_size = random.choice([32, 2048, 4096, 8192])
                elif protocol == "UDP":
                    packet_size = random.choice([32, 2048, 4096])
                else:  # ICMP
                    packet_size = random.choice([32, 512, 1024])
            
            # Business hours pattern (more traffic 9-17)
            hour = current_time.hour
            if 9 <= hour <= 17:
                # Peak hours - more traffic
                if random.random() < 0.3:  # 30% chance of burst
                    # Generate burst of similar traffic
                    for _ in range(random.randint(2, 8)):
                        burst_time = current_time + timedelta(milliseconds=random.randint(10, 100))
                        batch_records.append({
                            'timestamp': burst_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                            'source_ip': source_ip,
                            'destination_ip': destination_ip,
                            'packet_size': packet_size + random.randint(-50, 50),
                            'protocol': protocol
                        })
            
            # Weekend pattern (less traffic)
            if current_time.weekday() >= 5:  # Saturday/Sunday
                if random.random() < 0.6:  # Skip 60% of weekend traffic
                    continue
            
            batch_records.append({
                'timestamp': current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                'source_ip': source_ip,
                'destination_ip': destination_ip,
                'packet_size': max(32, packet_size),  # Minimum packet size
                'protocol': protocol
            })
        
        records.extend(batch_records)
        total_generated += len(batch_records)
        
        if total_generated % 50000 == 0:
            print(f"📈 Generated {total_generated:,} records...")
    
    print(f"✅ Generated {len(records):,} total records")
    
    # Create DataFrame and sort by timestamp
    print("🔄 Creating DataFrame and sorting by timestamp...")
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f').str[:-3]
    
    # Add some DDoS attack simulation (concentrated anomalies)
    print("🎯 Adding DDoS attack simulation...")
    attack_start = start_time + timedelta(days=2, hours=14, minutes=30)
    attack_duration = timedelta(minutes=15)
    
    ddos_records = []
    attack_time = attack_start
    attacker_ip = "203.0.113.100"  # RFC5737 test IP
    target_ip = "192.168.1.100"
    
    while attack_time < attack_start + attack_duration:
        # High frequency small packets (typical DDoS)
        ddos_records.append({
            'timestamp': attack_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
            'source_ip': attacker_ip,
            'destination_ip': target_ip,
            'packet_size': random.choice([32, 64, 128]),
            'protocol': random.choice(['TCP', 'UDP'])
        })
        attack_time += timedelta(milliseconds=random.randint(1, 10))
    
    # Add DDoS records to main dataset
    ddos_df = pd.DataFrame(ddos_records)
    df = pd.concat([df, ddos_df], ignore_index=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f').str[:-3]
    
    print(f"🎯 Added {len(ddos_records):,} DDoS attack records")
    
    # Save to CSV
    print(f"💾 Saving to {filename}...")
    df.to_csv(filename, index=False)
    
    # Calculate actual file size
    import os
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    
    print(f"✅ Dataset created successfully!")
    print(f"📁 Filename: {filename}")
    print(f"📊 Records: {len(df):,}")
    print(f"💾 File size: {file_size_mb:.2f} MB")
    print(f"📅 Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"🌐 Unique source IPs: {df['source_ip'].nunique():,}")
    print(f"🎯 Unique destination IPs: {df['destination_ip'].nunique():,}")
    print(f"📦 Protocol distribution:")
    print(df['protocol'].value_counts())
    print(f"📏 Packet size range: {df['packet_size'].min()} - {df['packet_size'].max()} bytes")
    
    return filename, len(df), file_size_mb

if __name__ == "__main__":
    # Generate the large dataset
    filename, record_count, file_size = generate_large_network_dataset(
        target_size_mb=30,
        filename="large_network_traffic_30mb.csv"
    )
    
    print(f"\n🎉 Large dataset ready for testing!")
    print(f"📂 Upload '{filename}' to the web application")
    print(f"🔬 This dataset contains realistic traffic patterns with:")
    print(f"   • Normal business traffic patterns")
    print(f"   • Weekend/weekday variations") 
    print(f"   • Burst traffic during peak hours")
    print(f"   • Simulated DDoS attack (15 minutes)")
    print(f"   • Various packet sizes and protocols")
    print(f"   • Anomalous traffic patterns (5% of data)")