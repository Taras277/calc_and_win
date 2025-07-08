import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from collections import defaultdict, deque
import datetime
import numpy as np

class NetworkMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real-Time Network Connection Monitor - Windows 10")
        self.root.geometry("1200x800")
        
        # Data storage
        self.connection_data = deque(maxlen=100)
        self.connection_counts = {'incoming': deque(maxlen=50), 'outgoing': deque(maxlen=50)}
        self.timestamps = deque(maxlen=50)
        self.active_connections = {}
        self.port_stats = defaultdict(int)
        
        # Monitoring control
        self.monitoring = False
        self.monitor_thread = None
        
        self.setup_ui()
        self.setup_plots()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start Monitoring", 
                                     command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop Monitoring", 
                                    command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Status: Stopped", 
                                    foreground="red")
        self.status_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        self.clear_button = ttk.Button(control_frame, text="Clear Data", 
                                     command=self.clear_data)
        self.clear_button.pack(side=tk.LEFT)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Graph tab
        self.graph_frame = ttk.Frame(notebook)
        notebook.add(self.graph_frame, text="Connection Graphs")
        
        # Connection list tab
        self.list_frame = ttk.Frame(notebook)
        notebook.add(self.list_frame, text="Active Connections")
        
        # Statistics tab
        self.stats_frame = ttk.Frame(notebook)
        notebook.add(self.stats_frame, text="Statistics")
        
        self.setup_connection_list()
        self.setup_statistics()
        
    def setup_plots(self):
        """Setup matplotlib plots"""
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.suptitle('Network Connections Monitor', fontsize=14)
        
        # Connection count over time
        self.ax1.set_title('Connection Count Over Time')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Number of Connections')
        self.ax1.grid(True)
        self.ax1.legend(['Incoming', 'Outgoing'])
        
        # Port usage distribution
        self.ax2.set_title('Top 10 Most Used Ports')
        self.ax2.set_xlabel('Port Number')
        self.ax2.set_ylabel('Connection Count')
        self.ax2.grid(True)
        
        # Embed plot in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Animation for real-time updates
        self.ani = animation.FuncAnimation(self.fig, self.update_plots, 
                                         interval=1000, blit=False)
        
    def setup_connection_list(self):
        """Setup the connection list display"""
        # Create treeview for connection list
        columns = ('PID', 'Process', 'Local Address', 'Local Port', 
                  'Remote Address', 'Remote Port', 'Status', 'Type')
        
        self.connection_tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.connection_tree.heading(col, text=col)
            self.connection_tree.column(col, width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, 
                                  command=self.connection_tree.yview)
        h_scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.HORIZONTAL, 
                                  command=self.connection_tree.xview)
        
        self.connection_tree.configure(yscrollcommand=v_scrollbar.set, 
                                     xscrollcommand=h_scrollbar.set)
        
        # Pack elements
        self.connection_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_statistics(self):
        """Setup statistics display"""
        self.stats_text = scrolledtext.ScrolledText(self.stats_frame, 
                                                  width=80, height=30)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def get_network_connections(self):
        """Get current network connections"""
        try:
            connections = psutil.net_connections(kind='inet')
            current_time = datetime.datetime.now()
            
            incoming = 0
            outgoing = 0
            active_conns = []
            
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    try:
                        process = psutil.Process(conn.pid) if conn.pid else None
                        process_name = process.name() if process else "Unknown"
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        process_name = "Unknown"
                    
                    local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "Unknown"
                    remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "Unknown"
                    
                    # Determine if incoming or outgoing based on local port
                    if conn.laddr and conn.raddr:
                        if conn.laddr.port < 1024:  # System ports typically incoming
                            incoming += 1
                            conn_type = "Incoming"
                        else:
                            outgoing += 1
                            conn_type = "Outgoing"
                        
                        # Track port usage
                        self.port_stats[conn.laddr.port] += 1
                        
                        active_conns.append({
                            'pid': conn.pid or 'N/A',
                            'process': process_name,
                            'local_addr': conn.laddr.ip if conn.laddr else 'N/A',
                            'local_port': conn.laddr.port if conn.laddr else 'N/A',
                            'remote_addr': conn.raddr.ip if conn.raddr else 'N/A',
                            'remote_port': conn.raddr.port if conn.raddr else 'N/A',
                            'status': conn.status,
                            'type': conn_type
                        })
            
            self.connection_counts['incoming'].append(incoming)
            self.connection_counts['outgoing'].append(outgoing)
            self.timestamps.append(current_time)
            self.active_connections = active_conns
            
        except Exception as e:
            print(f"Error getting network connections: {e}")
    
    def update_plots(self, frame):
        """Update the plots with new data"""
        if not self.monitoring:
            return
        
        self.ax1.clear()
        self.ax2.clear()
        
        # Plot connection counts over time
        if len(self.timestamps) > 1:
            times = [t.strftime('%H:%M:%S') for t in list(self.timestamps)]
            incoming_counts = list(self.connection_counts['incoming'])
            outgoing_counts = list(self.connection_counts['outgoing'])
            
            self.ax1.plot(times, incoming_counts, 'b-', label='Incoming', linewidth=2)
            self.ax1.plot(times, outgoing_counts, 'r-', label='Outgoing', linewidth=2)
            self.ax1.set_title('Connection Count Over Time')
            self.ax1.set_xlabel('Time')
            self.ax1.set_ylabel('Number of Connections')
            self.ax1.legend()
            self.ax1.grid(True)
            
            # Rotate x-axis labels for better readability
            plt.setp(self.ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Plot top ports
        if self.port_stats:
            top_ports = sorted(self.port_stats.items(), key=lambda x: x[1], reverse=True)[:10]
            if top_ports:
                ports, counts = zip(*top_ports)
                self.ax2.bar(range(len(ports)), counts, color='green', alpha=0.7)
                self.ax2.set_xticks(range(len(ports)))
                self.ax2.set_xticklabels([str(p) for p in ports])
                self.ax2.set_title('Top 10 Most Used Ports')
                self.ax2.set_xlabel('Port Number')
                self.ax2.set_ylabel('Connection Count')
                self.ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        self.canvas.draw()
    
    def update_connection_list(self):
        """Update the connection list display"""
        # Clear existing items
        for item in self.connection_tree.get_children():
            self.connection_tree.delete(item)
        
        # Add current connections
        for conn in self.active_connections:
            self.connection_tree.insert('', 'end', values=(
                conn['pid'],
                conn['process'],
                conn['local_addr'],
                conn['local_port'],
                conn['remote_addr'],
                conn['remote_port'],
                conn['status'],
                conn['type']
            ))
    
    def update_statistics(self):
        """Update statistics display"""
        if not self.monitoring:
            return
        
        stats_text = f"""Network Connection Statistics
Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Active Connections: {len(self.active_connections)}
Incoming Connections: {self.connection_counts['incoming'][-1] if self.connection_counts['incoming'] else 0}
Outgoing Connections: {self.connection_counts['outgoing'][-1] if self.connection_counts['outgoing'] else 0}

Top 5 Most Used Ports:
"""
        
        if self.port_stats:
            top_ports = sorted(self.port_stats.items(), key=lambda x: x[1], reverse=True)[:5]
            for port, count in top_ports:
                stats_text += f"  Port {port}: {count} connections\n"
        
        stats_text += f"\nTotal Unique Ports Used: {len(self.port_stats)}\n"
        
        # Process statistics
        processes = {}
        for conn in self.active_connections:
            process = conn['process']
            if process in processes:
                processes[process] += 1
            else:
                processes[process] = 1
        
        stats_text += f"\nActive Processes with Network Connections:\n"
        for process, count in sorted(processes.items(), key=lambda x: x[1], reverse=True)[:10]:
            stats_text += f"  {process}: {count} connections\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            self.get_network_connections()
            
            # Update UI in main thread
            self.root.after(0, self.update_connection_list)
            self.root.after(0, self.update_statistics)
            
            time.sleep(2)  # Update every 2 seconds
    
    def start_monitoring(self):
        """Start network monitoring"""
        self.monitoring = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring", foreground="green")
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print("Network monitoring started...")
    
    def stop_monitoring(self):
        """Stop network monitoring"""
        self.monitoring = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", foreground="red")
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        
        print("Network monitoring stopped.")
    
    def clear_data(self):
        """Clear all collected data"""
        self.connection_data.clear()
        self.connection_counts['incoming'].clear()
        self.connection_counts['outgoing'].clear()
        self.timestamps.clear()
        self.active_connections = {}
        self.port_stats.clear()
        
        # Clear displays
        for item in self.connection_tree.get_children():
            self.connection_tree.delete(item)
        
        self.stats_text.delete(1.0, tk.END)
        
        print("Data cleared.")
    
    def run(self):
        """Start the application"""
        print("Starting Network Monitor...")
        print("Note: This application requires administrator privileges for full functionality.")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        if self.monitoring:
            self.stop_monitoring()
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    try:
        monitor = NetworkMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have the required permissions and dependencies installed.")