#!/usr/bin/env python3
"""
Dependency installer for Network Monitor
Automatically installs required packages for the network monitoring application
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def check_admin_privileges():
    """Check if running with administrator privileges on Windows"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    print("Network Monitor - Dependency Installer")
    print("=" * 50)
    
    # Check if running on Windows
    if os.name != 'nt':
        print("Warning: This application is designed for Windows 10.")
        print("Some features may not work properly on other operating systems.")
    
    # Check for admin privileges
    if os.name == 'nt' and not check_admin_privileges():
        print("Warning: For full functionality, consider running as administrator.")
        print("Some network monitoring features may be limited without admin privileges.")
    
    # Required packages
    packages = [
        "psutil>=5.9.0",
        "matplotlib>=3.7.0", 
        "numpy>=1.24.0",
        "pandas>=2.0.0"
    ]
    
    print(f"\nInstalling {len(packages)} required packages...")
    print("-" * 30)
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("-" * 30)
    print(f"Installation complete: {success_count}/{len(packages)} packages installed successfully")
    
    if success_count == len(packages):
        print("✓ All dependencies installed successfully!")
        print("\nYou can now run the network monitor with:")
        print("  python network_monitor.py")
    else:
        print("✗ Some packages failed to install.")
        print("Please install them manually using:")
        print("  pip install -r requirements.txt")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()