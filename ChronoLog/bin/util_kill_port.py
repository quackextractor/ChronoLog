import argparse
import subprocess
import sys


def kill_port_process(port):
    """Find and kill process listening on a specific port."""
    print(f"Checking for process on port {port}...")
    
    if sys.platform == "win32":
        _kill_port_windows(port)
    elif sys.platform.startswith("linux"):
        _kill_port_linux(port)
    else:
        print(f"[WARNING] Auto-kill not supported on this OS: {sys.platform}")

def _kill_port_windows(port):
    """Windows implementation using netstat and taskkill."""
    try:
        # Run netstat to find process using the port
        output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
        
        if not output:
             print(f"No process found on port {port}.")
             return

        # Parse lines to find the PID
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 5 and f":{port}" in parts[1]:
                pid = parts[-1]
                print(f"Found process {pid} listening on port {port}. Killing it...")
                try:
                    subprocess.check_call(f"taskkill /F /PID {pid}", shell=True)
                    print(f"[OK] Process {pid} terminated.")
                except subprocess.CalledProcessError:
                    print(f"[FAILED] Could not kill process {pid}.")
                return # Only kill one, usually enough
    except subprocess.CalledProcessError:
        # netstat returns error if no match found
        print(f"No process found on port {port}.")
        pass 
    except Exception as e:
        print(f"[WARNING] Error checking port {port}: {e}")

def _kill_port_linux(port):
    """Linux implementation using lsof and kill."""
    try:
        # Ty lsof first (list open files) to get PID simply
        # -t: terse mode (only PIDs)
        # -i: Internet files
        # :{port}: Select by port
        try:
            pid = subprocess.check_output(f"lsof -t -i:{port}", shell=True).decode().strip()
            if pid:
                print(f"Found process {pid} listening on port {port}. Killing it...")
                subprocess.check_call(f"kill -9 {pid}", shell=True)
                print(f"[OK] Process {pid} terminated.")
                return
        except subprocess.CalledProcessError:
            # lsof returns >0 exit code if no files found
            pass
        
    except Exception as e:
        print(f"[WARNING] Error checking/killing port {port} on Linux: {e}")
        print("Ensure 'lsof' is installed.")

def main():
    parser = argparse.ArgumentParser(description="Kill process on specific port")
    parser.add_argument("--port", type=str, default="5000", help="Port to check and kill process on")
    args = parser.parse_args()
    
    kill_port_process(args.port)

if __name__ == "__main__":
    main()
