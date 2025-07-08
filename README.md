# Real-Time Network Connection Monitor for Windows 10

A Python application that visualizes all incoming and outgoing network connections in real-time on Windows 10.

## Features

- **Real-time monitoring** of network connections
- **Interactive visualization** with graphs and charts
- **Detailed connection information** including process names, ports, and addresses
- **Statistics dashboard** with connection counts and port usage
- **Easy-to-use GUI** built with tkinter and matplotlib
- **Tabbed interface** for different views (graphs, connections, statistics)

## Screenshots

The application provides:
- Real-time line graphs showing incoming/outgoing connection counts over time
- Bar chart of most frequently used ports
- Detailed table of active connections with process information
- Statistics panel with connection summaries

## Requirements

- **Operating System**: Windows 10 (designed specifically for Windows)
- **Python**: 3.7 or higher
- **Administrator Privileges**: Recommended for full functionality

## Dependencies

- `psutil` - For system and network monitoring
- `matplotlib` - For data visualization
- `numpy` - For numerical operations
- `pandas` - For data handling
- `tkinter` - For GUI (included with Python)

## Installation

### Option 1: Automatic Installation

1. Clone or download this repository
2. Run the dependency installer:
   ```bash
   python install_dependencies.py
   ```

### Option 2: Manual Installation

1. Install dependencies manually:
   ```bash
   pip install -r requirements.txt
   ```

### Option 3: Individual Package Installation

```bash
pip install psutil>=5.9.0
pip install matplotlib>=3.7.0
pip install numpy>=1.24.0
pip install pandas>=2.0.0
```

## Usage

### Running the Application

1. **Basic usage**:
   ```bash
   python network_monitor.py
   ```

2. **With administrator privileges** (recommended):
   - Right-click Command Prompt → "Run as administrator"
   - Navigate to the project directory
   - Run: `python network_monitor.py`

### Using the Interface

1. **Start Monitoring**: Click the "Start Monitoring" button to begin real-time monitoring
2. **View Graphs**: The "Connection Graphs" tab shows:
   - Connection count over time (incoming vs outgoing)
   - Top 10 most used ports
3. **View Connections**: The "Active Connections" tab displays all current connections
4. **View Statistics**: The "Statistics" tab provides detailed summaries
5. **Stop Monitoring**: Click "Stop Monitoring" to pause data collection
6. **Clear Data**: Use "Clear Data" to reset all collected information

## Understanding the Data

### Connection Types
- **Incoming**: Connections where your system is the server (typically ports < 1024)
- **Outgoing**: Connections where your system is the client

### Connection Information
- **PID**: Process ID
- **Process**: Application name making the connection
- **Local Address/Port**: Your system's IP and port
- **Remote Address/Port**: External system's IP and port
- **Status**: Connection state (ESTABLISHED, LISTENING, etc.)
- **Type**: Incoming or Outgoing classification

### Statistics
- Active connection counts
- Port usage frequency
- Process connection summaries
- Real-time updates every 2 seconds

## Important Notes

### Administrator Privileges
- **Required for**: Full process information and system-level connections
- **Without admin**: Some process names may show as "Unknown"
- **Security**: The application only reads network information, doesn't modify anything

### Performance
- **Memory usage**: Limited to last 100 connections and 50 time points
- **Update frequency**: Every 2 seconds (configurable in code)
- **CPU impact**: Minimal - designed for continuous monitoring

### Privacy and Security
- All monitoring is **local only** - no data is sent anywhere
- Only reads existing network connection information
- Does not intercept or modify network traffic
- Does not store personal data

## Troubleshooting

### Common Issues

1. **"Access Denied" errors**:
   - Run as administrator
   - Check antivirus software isn't blocking the application

2. **Missing dependencies**:
   - Run `python install_dependencies.py`
   - Or manually install with `pip install -r requirements.txt`

3. **Blank or empty data**:
   - Ensure you have active network connections
   - Try running as administrator
   - Check Windows Firewall settings

4. **Application won't start**:
   - Verify Python 3.7+ is installed
   - Check all dependencies are installed
   - Run from command line to see error messages

### Error Messages
- **"Module not found"**: Install missing dependencies
- **"Permission denied"**: Run as administrator
- **"No connections found"**: Normal if no active network connections exist

## Customization

### Modifying Update Frequency
Edit `network_monitor.py`, line with `time.sleep(2)` - change 2 to desired seconds.

### Changing Data Retention
Edit the `maxlen` parameters in the `__init__` method:
- `connection_data = deque(maxlen=100)` - number of connection records
- `connection_counts = {'incoming': deque(maxlen=50), ...}` - time series length

### Adding New Features
The modular design makes it easy to add:
- Export functionality
- Alert systems
- Additional visualizations
- Network traffic analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## Disclaimer

This tool is for monitoring your own system's network connections. Use responsibly and in accordance with your organization's policies and local laws.
