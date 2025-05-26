import os
import subprocess
import sys
import shutil
import time

# Define project directory
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

def run_command(command, cwd=PROJECT_DIR, shell=True):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, check=True, text=True, capture_output=True)
        print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        sys.exit(1)

def check_prerequisites():
    """Check if required tools are installed."""
    if not shutil.which("node"):
        print("Node.js is not installed. Please install Node.js (version 18.x or 20.x) and try again.")
        sys.exit(1)
    node_version = run_command("node -v").stdout.strip()
    print(f"Node.js version: {node_version}")

    if not shutil.which("ng"):
        print("Angular CLI is not installed. Installing globally...")
        run_command("npm install -g @angular/cli")

    if not shutil.which("npx"):
        print("npx is not installed. Please install Node.js/npm properly.")
        sys.exit(1)

def launch_in_terminal(command, title="Terminal", log_file=None):
    """Try to launch a command in a new terminal window or fallback to background with optional logging."""
    terminal_cmds = [
        # Disabled due to GLIBC error:
        # ['gnome-terminal', '--', 'bash', '-c', f'cd {PROJECT_DIR} && {command}; exec bash'],
        ['xterm', '-T', title, '-e', f'cd {PROJECT_DIR} && {command}; bash'],
        ['konsole', '--hold', '-e', f'cd {PROJECT_DIR} && {command}'],
        ['xfce4-terminal', '--hold', '-e', f'cd {PROJECT_DIR} && {command}']
    ]
    for cmd in terminal_cmds:
        try:
            subprocess.Popen(cmd)
            print(f"Launched in terminal: {' '.join(cmd)}")
            return
        except FileNotFoundError:
            continue

    # Fallback: run in background with logging
    if log_file:
        log_path = os.path.join(PROJECT_DIR, log_file)
        with open(log_path, 'w') as f:
            subprocess.Popen(f'cd {PROJECT_DIR} && {command}', shell=True, stdout=f, stderr=subprocess.STDOUT)
        print(f"Started in background, logging to {log_path}")
    else:
        subprocess.Popen(f'cd {PROJECT_DIR} && {command}', shell=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Started in background without log file.")

def start_json_server():
    """Start json-server in a separate terminal."""
    print("Starting json-server on port 8081...")
    json_server_cmd = "npx json-server --watch src/db.json --port 8081"
    launch_in_terminal(json_server_cmd, title="JSON Server", log_file="json-server.log")
    time.sleep(2)

def start_angular_app():
    """Start Angular application in a separate terminal."""
    print("Starting Angular application on http://localhost:4200 ...")
    angular_cmd = "ng serve"
    launch_in_terminal(angular_cmd, title="Angular App", log_file="angular-app.log")

def main():
    check_prerequisites()

    if not os.path.exists(PROJECT_DIR):
        print(f"Project directory {PROJECT_DIR} does not exist.")
        sys.exit(1)

    print(f"Navigating to {PROJECT_DIR}")
    os.chdir(PROJECT_DIR)

    print("Installing dependencies with --legacy-peer-deps...")
    run_command("npm install --legacy-peer-deps")

    start_json_server()
    start_angular_app()

if __name__ == "__main__":
    main()

