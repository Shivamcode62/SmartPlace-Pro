#!/usr/bin/env python3
"""
SmartPlace Pro - Placement Preparation Platform
Main Application Launcher
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket
import platform

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print application banner"""
    banner = f"""
{Colors.BLUE}{'='*70}{Colors.ENDC}
{Colors.GREEN}{' ' * 15}SMARTPLACE PRO - PLACEMENT PREPARATION PLATFORM{Colors.ENDC}
{Colors.BLUE}{'='*70}{Colors.ENDC}
{Colors.YELLOW}
    ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗██████╗ ██╗      █████╗  ██████╗███████╗
    ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝
    ███████╗██╔████╔██║███████║██████╔╝   ██║   ██████╔╝██║     ███████║██║     █████╗  
    ╚════██║██║╚██╔╝██║██╔══██║██╔═══╝    ██║   ██╔═══╝ ██║     ██╔══██║██║     ██╔══╝  
    ███████║██║ ╚═╝ ██║██║  ██║██║        ██║   ██║     ███████╗██║  ██║╚██████╗███████╗
    ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝
{Colors.ENDC}
{Colors.BLUE}{'='*70}{Colors.ENDC}
{Colors.BOLD}Version: 1.0.0 | Author: SmartPlace Team | AI-Powered Platform{Colors.ENDC}
{Colors.BLUE}{'='*70}{Colors.ENDC}
    """
    print(banner)

def check_python_version():
    """Check Python version"""
    print(f"{Colors.BOLD}📌 Checking Python version...{Colors.ENDC}")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"{Colors.GREEN}✅ Python {version.major}.{version.minor}.{version.micro} - OK{Colors.ENDC}")
        return True
    else:
        print(f"{Colors.RED}❌ Python 3.7+ required. Current version: {version.major}.{version.minor}{Colors.ENDC}")
        return False

def check_requirements():
    """Check and install requirements"""
    print(f"\n{Colors.BOLD}📦 Checking dependencies...{Colors.ENDC}")
    
    required_packages = ['flask', 'flask_cors', 'flask_jwt_extended']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"{Colors.GREEN}✅ {package} - installed{Colors.ENDC}")
        except ImportError:
            print(f"{Colors.YELLOW}⚠️  {package} - missing{Colors.ENDC}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n{Colors.YELLOW}📥 Installing missing packages...{Colors.ENDC}")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{Colors.GREEN}✅ {package} - installed successfully{Colors.ENDC}")
            except subprocess.CalledProcessError:
                print(f"{Colors.RED}❌ Failed to install {package}{Colors.ENDC}")
                return False
        
        # Install from requirements.txt if exists
        if os.path.exists('requirements.txt'):
            print(f"\n{Colors.YELLOW}📥 Installing from requirements.txt...{Colors.ENDC}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    return True

def check_port_availability(port=5000):
    """Check if port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def create_directories():
    """Create necessary directories"""
    print(f"\n{Colors.BOLD}📁 Creating directories...{Colors.ENDC}")
    
    directories = ['data', 'static/images', 'static/js', 'frontend/css']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{Colors.GREEN}✅ Created: {directory}{Colors.ENDC}")
        else:
            print(f"{Colors.BLUE}📁 Already exists: {directory}{Colors.ENDC}")

def check_frontend_files():
    """Check if frontend files exist"""
    print(f"\n{Colors.BOLD}📄 Checking frontend files...{Colors.ENDC}")
    
    frontend_files = [
        'frontend/index.html',
        'frontend/aptitude.html',
        'frontend/coding.html',
        'frontend/interview.html',
        'frontend/resume.html',
        'frontend/dashboard.html',
        'frontend/profile.html',
        'frontend/css/style.css'
    ]
    
    missing_files = []
    for file in frontend_files:
        if os.path.exists(file):
            print(f"{Colors.GREEN}✅ {file}{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  Missing: {file}{Colors.ENDC}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n{Colors.YELLOW}⚠️  Some frontend files are missing. Creating basic structure...{Colors.ENDC}")
    
    return True

def check_backend_files():
    """Check if backend files exist"""
    print(f"\n{Colors.BOLD}📄 Checking backend files...{Colors.ENDC}")
    
    backend_files = [
        'backend/app.py',
        'backend/database.py',
        'backend/models.py'
    ]
    
    for file in backend_files:
        if os.path.exists(file):
            print(f"{Colors.GREEN}✅ {file}{Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ Missing: {file}{Colors.ENDC}")
            return False
    
    return True

def open_browser():
    """Open browser after delay"""
    time.sleep(2)
    url = "http://localhost:5000"
    print(f"\n{Colors.GREEN}🌐 Opening browser at {url}{Colors.ENDC}")
    webbrowser.open(url)

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def print_startup_info():
    """Print startup information"""
    local_ip = get_local_ip()
    
    info = f"""
{Colors.BOLD}{Colors.GREEN}✨ SERVER STARTING...{Colors.ENDC}
{Colors.BLUE}{'='*60}{Colors.ENDC}
{Colors.YELLOW}📍 Local Access:{Colors.ENDC}    http://localhost:5000
{Colors.YELLOW}📍 Network Access:{Colors.ENDC}  http://{local_ip}:5000
{Colors.YELLOW}📍 API Endpoint:{Colors.ENDC}    http://localhost:5000/api
{Colors.YELLOW}📍 Database:{Colors.ENDC}        ./data/smartplace.db
{Colors.BLUE}{'='*60}{Colors.ENDC}

{Colors.BOLD}📊 Available Features:{Colors.ENDC}
  • User Authentication (JWT)
  • Aptitude Tests with Timer
  • Coding Challenges with Editor
  • AI-Powered Interview Practice
  • Resume Analyzer with ATS Score
  • Dashboard with Analytics
  • User Profile Management

{Colors.BOLD}🔧 Admin Access:{Colors.ENDC}
  • View Database: sqlite3 ./data/smartplace.db
  • Backup Data: Copy ./data/smartplace.db

{Colors.BOLD}💡 Tips:{Colors.ENDC}
  • Press CTRL+C to stop the server
  • All data is stored in SQLite database
  • Use the login modal to register new users

{Colors.BLUE}{'='*60}{Colors.ENDC}
    """
    print(info)

def run_server():
    """Run the Flask server"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}🚀 Starting SmartPlace Pro Server...{Colors.ENDC}\n")
    
    # Add backend to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        from backend.app import app
        
        # Open browser after delay
        import threading
        timer = threading.Timer(2, open_browser)
        timer.start()
        
        # Run server
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Server stopped by user{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error starting server: {e}{Colors.ENDC}")
        sys.exit(1)

def main():
    """Main function"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    # Print banner
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check and install requirements
    if not check_requirements():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check files
    check_frontend_files()
    if not check_backend_files():
        print(f"\n{Colors.RED}❌ Critical backend files missing. Please ensure all backend files exist.{Colors.ENDC}")
        sys.exit(1)
    
    # Check port availability
    if not check_port_availability():
        print(f"\n{Colors.RED}❌ Port 5000 is already in use. Please free the port and try again.{Colors.ENDC}")
        sys.exit(1)
    
    # Print startup info
    print_startup_info()
    
    # Run server
    run_server()

if __name__ == "__main__":
    main()