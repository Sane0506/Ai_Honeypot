import socket
import threading
import logging
import json
from datetime import datetime
from typing import Dict, Any
import numpy as np
from sklearn.ensemble import IsolationForest
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import sqlite3
from fastapi import FastAPI, HTTPException
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('honeypot.log'),
        logging.StreamHandler()
    ]
)

class AIDrivenHoneypot:
    def __init__(self, host: str = 'localhost', ports: Dict[str, int] = None):
        self.host = host
        self.ports = ports or {
            'ssh': 2222,
            'http': 8080,
            'ftp': 2121
        }
        self.running = False
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
        self.setup_database()
        self.initialize_models()

    def setup_database(self):
        conn = sqlite3.connect('honeypot.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                source_ip TEXT,
                port INTEGER,
                payload TEXT,
                anomaly_score REAL,
                threat_level TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def initialize_models(self):
        # Initialize anomaly detector with some baseline data
        baseline_data = np.random.randn(100, 5)  # Example baseline data
        self.anomaly_detector.fit(baseline_data)

    def log_attack(self, source_ip: str, port: int, payload: str, anomaly_score: float):
        conn = sqlite3.connect('honeypot.db')
        cursor = conn.cursor()
        threat_level = 'HIGH' if anomaly_score > 0.7 else 'MEDIUM' if anomaly_score > 0.3 else 'LOW'
        
        cursor.execute('''
            INSERT INTO attacks (timestamp, source_ip, port, payload, anomaly_score, threat_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now(), source_ip, port, payload, anomaly_score, threat_level))
        
        conn.commit()
        conn.close()
        logging.info(f"Attack logged from {source_ip} on port {port}")

    def analyze_payload(self, payload: str) -> float:
        # Convert payload to features for anomaly detection
        features = np.array([
            len(payload),
            payload.count(';'),
            payload.count('|'),
            payload.count('&'),
            payload.count('>')
        ]).reshape(1, -1)
        
        # Get anomaly score
        anomaly_score = self.anomaly_detector.score_samples(features)[0]
        return anomaly_score

    def handle_connection(self, client_socket: socket.socket, address: tuple, port: int):
        try:
            client_socket.settimeout(30)
            data = client_socket.recv(1024).decode('utf-8', errors='ignore')
            
            if data:
                anomaly_score = self.analyze_payload(data)
                self.log_attack(address[0], port, data, anomaly_score)
                
                # Send fake response based on port
                if port == self.ports['ssh']:
                    client_socket.send(b'SSH-2.0-OpenSSH_7.9p1\r\n')
                elif port == self.ports['http']:
                    client_socket.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
                elif port == self.ports['ftp']:
                    client_socket.send(b'220 FTP Server Ready\r\n')
            
        except Exception as e:
            logging.error(f"Error handling connection from {address}: {str(e)}")
        finally:
            client_socket.close()

    def start_service(self, port: int):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, port))
        server_socket.listen(5)
        
        logging.info(f"Listening on port {port}")
        
        while self.running:
            try:
                client_socket, address = server_socket.accept()
                logging.info(f"Connection from {address}")
                threading.Thread(
                    target=self.handle_connection,
                    args=(client_socket, address, port)
                ).start()
            except Exception as e:
                logging.error(f"Error in service on port {port}: {str(e)}")

    def start(self):
        self.running = True
        for service, port in self.ports.items():
            threading.Thread(target=self.start_service, args=(port,)).start()
        logging.info("Honeypot started successfully")

    def stop(self):
        self.running = False
        logging.info("Honeypot stopped")

# FastAPI application
app = FastAPI(title="AI Honeypot API")
honeypot = AIDrivenHoneypot()

@app.get("/")
async def root():
    return {"message": "AI Honeypot API is running"}

@app.get("/stats")
async def get_stats():
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as total_attacks,
               AVG(anomaly_score) as avg_anomaly_score,
               threat_level,
               COUNT(*) as count
        FROM attacks
        GROUP BY threat_level
    ''')
    
    stats = cursor.fetchall()
    conn.close()
    
    return {
        "total_attacks": stats[0][0] if stats else 0,
        "average_anomaly_score": stats[0][1] if stats else 0,
        "threat_levels": [{"level": row[2], "count": row[3]} for row in stats]
    }

if __name__ == "__main__":
    # Start the honeypot
    honeypot.start()
    
    # Start the FastAPI server
    uvicorn.run(app, host="localhost", port=8000) 