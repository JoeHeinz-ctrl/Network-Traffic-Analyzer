#!/usr/bin/env python3
"""
Generate a 5MB network traffic dataset for testing the analysis system.
Creates realistic network traffic patterns with anomalies.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_5mb_dataset(filename="test_network_traffic_5mb.csv"):
    """Generate a 5MB network traffic dataset with realistic patterns."""
    
    print(f"🚀 Generating 5MB network traffic dataset...")
    
    # Estimate records needed (approximately 150 bytes per record)
    target_size_mb = 5
    estimated_records = (target_size_mb * 1024 * 1024) // 150
    print(f"📊 Target records: ~{estimated_records:,}")
    
    # Set random seed for reproducible results
    np.random.seed(42)
    random.seed(42)
    
    # Time range: 2 days of traffic data
    start_time = datetime(2024, 1, 15, 0, 0, 0)
    end_time = start_time + timedelta(days=2)
    
    # Network configuration
    internal_subnets = [
        "192.168.1", "192.168.2", "10.0.0", "10.0.1"
    ]
    
    external_ips = [
        "8.8.8.8", "1.1.1.1", "208.67.222.222", 
        "74.125.224.72", "151.101.193.140"
    ]
    
    protocols = ["TCP", "UDP", "ICMP"]
    protocol_weights = [0.75, 0.20, 0.05]
    
    # Packet size distributions
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
    
    # Generate records
    for i in range(estimated_records):
        # Time progression
        time_increment = random.uniform(0.5, 10.0)
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
            if protocol == "TCP":
                packet_size = random.choice([32, 2048, 4096])
            elif protocol == "UDP":
                packet_size = random.choice([32, 2048])
            else:
                packet_size = random.choice([32, 512])
        
        # Business hours pattern
        hour = current_time.hour
        if 9 <= hour <= 17:
            # Peak hours - occasional bursts
            if random.random() < 0.2:
                for _ in range(random.randint(2, 5)):
                    burst_time = current_time + timedelta(milliseconds=random.randint(10, 100))
                    records.append({
                        'timestamp': burst_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                        'source_ip': source_ip,
                        'destination_ip': destination_ip,
                        'packet_size': packet_size + random.randint(-30, 30),
                        'protocol': protocol
                    })
        
        # Weekend pattern (less traffic)
        if current_time.weekday() >= 5:
            if random.random() < 0.5:
                continue
        
        records.append({
            'timestamp': current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
            'source_ip': source_ip,
            'destination_ip': destination_ip,
            'packet_size': max(32, packet_size),
            'protocol': protocol
        })
        
        if (i + 1) % 10000 == 0:
            print(f"📈 Generated {i + 1:,} records...")
    
    print(f"✅ Generated {len(records):,} total records")
    
    # Create DataFrame and sort by timestamp
    print("🔄 Creating DataFrame and sorting...")
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f').str[:-3]
    
    # Add DDoS attack simulation
    print("🎯 Adding DDoS attack simulation...")
    attack_start = start_time + timedelta(hours=30)
    attack_duration = timedelta(minutes=10)
    
    ddos_records = []
    attack_time = attack_start
    attacker_ip = "203.0.113.100"
    target_ip = "192.168.1.100"
    
    while attack_time < attack_start + attack_duration:
        ddos_records.append({
            'timestamp': attack_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
            'source_ip': attacker_ip,
            'destination_ip': target_ip,
            'packet_size': random.choice([32, 64, 128]),
            'protocol': random.choice(['TCP', 'UDP'])
        })
        attack_time += timedelta(milliseconds=random.randint(5, 20))
    
    # Add DDoS records
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
    
    print(f"\n✅ Dataset created successfully!")
    print(f"📁 Filename: {filename}")
    print(f"📊 Records: {len(df):,}")
    print(f"💾 File size: {file_size_mb:.2f} MB")
    print(f"📅 Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"🌐 Unique source IPs: {df['source_ip'].nunique():,}")
    print(f"🎯 Unique destination IPs: {df['destination_ip'].nunique():,}")
    print(f"\n📦 Protocol distribution:")
    print(df['protocol'].value_counts())
    print(f"\n📏 Packet size stats:")
    print(f"   Min: {df['packet_size'].min()} bytes")
    print(f"   Max: {df['packet_size'].max()} bytes")
    print(f"   Mean: {df['packet_size'].mean():.1f} bytes")
    print(f"   Median: {df['packet_size'].median():.1f} bytes")
    
    return filename, len(df), file_size_mb

if __name__ == "__main__":
    print("=" * 60)
    print("  5MB Network Traffic Dataset Generator")
    print("=" * 60)
    print()
    
    # Generate the dataset
    filename, record_count, file_size = generate_5mb_dataset()
    
    print(f"\n{'=' * 60}")
    print(f"🎉 Dataset ready for testing!")
    print(f"{'=' * 60}")
    print(f"\n📂 Upload '{filename}' to the web application")
    print(f"\n🔬 This dataset contains:")
    print(f"   • {record_count:,} network traffic records")
    print(f"   • {file_size:.2f} MB file size")
    print(f"   • 2 days of traffic data")
    print(f"   • Normal business traffic patterns")
    print(f"   • Weekend/weekday variations")
    print(f"   • Burst traffic during peak hours")
    print(f"   • Simulated DDoS attack (10 minutes)")
    print(f"   • Anomalous traffic patterns (5% of data)")
    print(f"\n🚀 Ready to test your application!")
    print()
