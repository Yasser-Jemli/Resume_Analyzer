import os
import subprocess
import sys
import shutil
import time

# Define project directory
PROJECT_DIR = os.path.expanduser("../App-frontend")

def run_command(command, cwd=PROJECT_DIR, shell=True):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, check=True, text=True, capture_output=True)
        print(result.stdout)
        return result  # Return the result so it can be used by the caller
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        sys.exit(1)

def run_background_command(command, cwd=PROJECT_DIR):
    """Run a command in the background and return the process."""
    process = subprocess.Popen(command, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(f"Started background process: {command}")
    return process

def check_prerequisites():
    """Check if required tools are installed."""
    # Check Node.js
    if not shutil.which("node"):
        print("Node.js is not installed. Please install Node.js (version 18.x or 20.x) and try again.")
        sys.exit(1)
    node_version = run_command("node -v").stdout.strip()
    print(f"Node.js version: {node_version}")

    # Check Angular CLI
    if not shutil.which("ng"):
        print("Angular CLI is not installed. Installing globally...")
        run_command("npm install -g @angular/cli")

    # Check json-server
    if not shutil.which("json-server"):
        print("json-server is not installed. Installing globally...")
        run_command("npm install -g json-server")

def main():
    # Check prerequisites
    check_prerequisites()

    # Ensure project directory exists
    if not os.path.exists(PROJECT_DIR):
        print(f"Project directory {PROJECT_DIR} does not exist.")
        sys.exit(1)

    print(f"Navigating to {PROJECT_DIR}")
    os.chdir(PROJECT_DIR)

    # Step 1: Install dependencies with --legacy-peer-deps
    print("Installing dependencies with --legacy-peer-deps...")
    run_command("npm install --legacy-peer-deps")

    # Step 2: Install bootstrap-icons
    print("Installing bootstrap-icons...")
    run_command("npm install bootstrap-icons --legacy-peer-deps")

    # Step 3: Start json-server in the background
    print("Starting json-server on port 8081...")
    json_server_process = run_background_command("npx json-server --watch src/db.json --port 8081")

    # Give json-server a moment to start
    time.sleep(2)

    # Step 4: Serve the Angular application
    print("Starting Angular application...")
    try:
        run_command("ng serve -o")
    finally:
        print("Shutting down json-server...")
        json_server_process.terminate()
        json_server_process.wait()

if __name__ == "__main__":
    main()