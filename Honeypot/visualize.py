import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns

class ThreatVisualizer:
    def __init__(self, db_path='honeypot.db'):
        self.db_path = db_path

    def get_attack_data(self):
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT 
                timestamp,
                source_ip,
                port,
                anomaly_score,
                threat_level
            FROM attacks
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def plot_attack_timeline(self):
        df = self.get_attack_data()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Resample to hourly counts
        hourly_attacks = df.resample('H').size()
        
        plt.figure(figsize=(12, 6))
        hourly_attacks.plot(kind='line')
        plt.title('Attack Frequency Over Time')
        plt.xlabel('Time')
        plt.ylabel('Number of Attacks')
        plt.grid(True)
        plt.savefig('attack_timeline.png')
        plt.close()

    def plot_threat_distribution(self):
        df = self.get_attack_data()
        
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='threat_level', order=['LOW', 'MEDIUM', 'HIGH'])
        plt.title('Distribution of Threat Levels')
        plt.xlabel('Threat Level')
        plt.ylabel('Count')
        plt.savefig('threat_distribution.png')
        plt.close()

    def plot_port_analysis(self):
        df = self.get_attack_data()
        
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='port')
        plt.title('Attack Distribution by Port')
        plt.xlabel('Port')
        plt.ylabel('Number of Attacks')
        plt.savefig('port_analysis.png')
        plt.close()

    def plot_anomaly_scores(self):
        df = self.get_attack_data()
        
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='anomaly_score', bins=30)
        plt.title('Distribution of Anomaly Scores')
        plt.xlabel('Anomaly Score')
        plt.ylabel('Count')
        plt.savefig('anomaly_scores.png')
        plt.close()

    def generate_all_visualizations(self):
        self.plot_attack_timeline()
        self.plot_threat_distribution()
        self.plot_port_analysis()
        self.plot_anomaly_scores()
        print("All visualizations have been generated and saved as PNG files.")

if __name__ == "__main__":
    visualizer = ThreatVisualizer()
    visualizer.generate_all_visualizations() 