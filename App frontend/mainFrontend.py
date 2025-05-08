import os
import subprocess
import sys
import shutil

# Define project directory
PROJECT_DIR = os.path.expanduser("../App frontend")

def run_command(command, cwd=PROJECT_DIR, shell=True):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, check=True, text=True, capture_output=True)
        print(result.stdout)
        return result  # Return the result so it can be used by the caller
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        sys.exit(1)

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

    # Step 2: Serve the Angular application
    print("Starting Angular application...")
    run_command("ng serve -o")

if __name__ == "__main__":
    main()