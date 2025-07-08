#!/usr/bin/env python3
"""
Test script to verify network monitor dependencies and basic functionality
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import psutil
        print("✓ psutil imported successfully")
    except ImportError as e:
        print(f"✗ psutil import failed: {e}")
        return False
    
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        print("✓ matplotlib imported successfully")
    except ImportError as e:
        print(f"✗ matplotlib import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    try:
        import tkinter as tk
        print("✓ tkinter imported successfully")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic network monitoring functionality"""
    print("\nTesting basic functionality...")
    
    try:
        import psutil
        
        # Test network connections
        connections = psutil.net_connections()
        print(f"✓ Found {len(connections)} network connections")
        
        # Test getting process info
        current_process = psutil.Process()
        print(f"✓ Current process: {current_process.name()}")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_network_monitor_import():
    """Test if the main network monitor module can be imported"""
    print("\nTesting network monitor import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Import the main module (without running GUI)
        import network_monitor
        print("✓ Network monitor module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Network monitor import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Network Monitor - Dependency and Functionality Test")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print()
    
    success = True
    
    success &= test_imports()
    success &= test_basic_functionality() 
    success &= test_network_monitor_import()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! Network monitor should work correctly.")
        print("\nTo run the network monitor:")
        if sys.platform == "win32":
            print("  - Double-click run_monitor.bat")
            print("  - Or run: python network_monitor.py")
        else:
            print("  - Run: python3 network_monitor.py")
            print("  - Note: Some features may be limited on non-Windows systems")
    else:
        print("✗ Some tests failed. Please install missing dependencies.")
        print("Run: python3 install_dependencies.py")
    
    print()

if __name__ == "__main__":
    main()