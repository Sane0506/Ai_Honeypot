# AI-Based Honeypot System

A dynamic honeypot system that uses AI to detect and analyze malicious behavior in real-time. This system implements multiple service traps (SSH, HTTP, FTP) and uses machine learning to identify and classify potential threats.

## Features

- Multiple service traps (SSH, HTTP, FTP)
- Real-time anomaly detection using Isolation Forest
- Pattern analysis using DistilBERT
- SQLite database for attack logging
- REST API for monitoring and statistics
- Visualization tools for threat analysis
- Dynamic threat level assessment

## Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the honeypot system:
```bash
python honeypot.py
```

2. The system will start listening on the following ports:
   - SSH: 2222
   - HTTP: 8080
   - FTP: 2121

3. Access the API at `http://localhost:8000`:
   - `/`: API status
   - `/stats`: Get attack statistics

4. Generate visualizations:
```bash
python visualize.py
```

## How It Works

1. **Service Traps**: The system creates fake services that appear to be vulnerable to attract attackers.

2. **Anomaly Detection**: Uses Isolation Forest to identify unusual patterns in incoming connections and payloads.

3. **Pattern Analysis**: DistilBERT model analyzes payload content for malicious patterns.

4. **Threat Assessment**: Combines anomaly scores and pattern analysis to determine threat levels.

5. **Data Logging**: All attacks are logged in SQLite database for analysis.

6. **Visualization**: Generate various plots to analyze attack patterns and trends.

## Security Considerations

- This system is designed for research and educational purposes
- Run in a controlled environment
- Monitor system resources
- Regularly update dependencies
- Consider using a firewall to limit access

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 