import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
import re

class ProxychainsConfigurator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proxychain Manager")
        self.geometry("575x650")

        # Define color scheme
        self.bg_color = "#161A1D"  # Dark background color
        self.fg_color = "#ffffff"  # White text color
        self.button_color = "#85182a"  # Red button color
        self.active_color = "#00ff00"  # Green color for active status
        self.inactive_color = "#cf9c1d"  # Yellow color for inactive status
        self.scrollbar_color = "#b0b0b0"  # Gray color for scrollbar

        # Apply colors to the main window
        self.configure(bg=self.bg_color)

        # Create a frame with vertical scrollbar
        self.canvas = tk.Canvas(self, bg=self.bg_color, highlightthickness=0)
        self.frame = tk.Frame(self.canvas, bg=self.bg_color)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview, bg=self.scrollbar_color,
        troughcolor=self.bg_color, activebackground=self.button_color)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a window in the canvas to hold the frame
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Bind the frame size to the canvas scroll region
        self.frame.bind("<Configure>", self.on_frame_configure)

        # Enable mouse wheel scrolling on the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Create buttons for Tor control and editing Proxychains config
        self.create_button("Start Tor", self.start_tor)
        self.create_button("Stop Tor", self.stop_tor)
        self.create_button("Edit Proxychains Config", self.edit_proxychains)

        # Create label for Tor service status
        self.tor_status_label = self.create_label("Tor status: Unknown")

        # Section for running custom commands through Proxychains
        self.create_label("Enter command to run through Proxychains:")
        self.command_entry = self.create_entry()
        self.create_button("Run Command", self.run_proxychains_command)

        # Section for navigating to a URL using Proxychains
        self.create_label("Enter URL to navigate using Proxychains:")
        self.url_entry = self.create_entry()
        self.create_button("Navigate to URL", self.navigate_to_url)

        # Section for changing proxychain type
        self.create_label("Select proxychain type:")
        self.proxychain_var = tk.StringVar(value="dynamic_chain")

        # Dictionary to hold radio buttons for proxychain types
        self.radio_buttons = {}

        for chain_type in ["dynamic_chain", "strict_chain", "random_chain"]:
            radio_button = tk.Radiobutton(
                self.frame,
                text=chain_type.replace("_", " ").title(),
                variable=self.proxychain_var,
                value=chain_type,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor=self.button_color,
                indicatoron=True
            )
            radio_button.pack(anchor=tk.W)
            self.radio_buttons[chain_type] = radio_button

        self.create_button("Update Proxychain Type", self.update_proxychain_type)

        # Button to ping servers
        self.create_button("Ping Servers", self.ping_servers)

        # Log for displaying results and traffic
        self.log_text = scrolledtext.ScrolledText(self.frame, width=60, height=10, bg=self.bg_color, fg=self.fg_color,
        insertbackground=self.fg_color)
        self.log_text.pack(pady=10)

        # Terminal-like section for executing custom commands
        self.create_label("Terminal:")
        self.terminal_entry = self.create_entry()
        self.create_button("Execute Command", self.execute_custom_command)

        # Button to clear log
        self.create_button("Clear Log", self.clear_log)

        # Initial update of Tor status
        self.update_tor_status()

    def on_frame_configure(self, event):
        # Update scroll region when the frame is resized
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        # Scroll the canvas using the mouse wheel
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_button(self, text, command):
        button = tk.Button(self.frame, text=text, command=command, bg=self.button_color, fg=self.fg_color,
                           relief="groove")
        button.pack(pady=10, padx=10, anchor=tk.W)

    def create_label(self, text):
        label = tk.Label(self.frame, text=text, bg=self.bg_color, fg=self.fg_color)
        label.pack(pady=0,anchor=tk.W)
        return label

    def create_entry(self):
        entry = tk.Entry(self.frame, width=40, bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color)
        entry.pack(pady=0, anchor=tk.W)
        return entry

    def start_tor(self):
        try:
            self.run_command_with_sudo("systemctl start tor")
            messagebox.showinfo("Success", "Tor service started.")
            # Update Tor status
            self.update_tor_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Tor: {e}")

    def stop_tor(self):
        try:
            self.run_command_with_sudo("systemctl stop tor")
            messagebox.showinfo("Success", "Tor service stopped.")
            # Update Tor status
            self.update_tor_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop Tor: {e}")

    def edit_proxychains(self):
        try:
            # Execute the command to open the file /etc/proxychains.conf in a terminal text editor
            subprocess.Popen(["sudo", "vim", "/etc/proxychains.conf"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit Proxychains config: {e}")

    def update_proxychain_type(self):
        proxychain_type = self.proxychain_var.get()

        # Path to the Proxychains configuration file
        config_path = "/etc/proxychains.conf"

        # Use a temporary file to store the updated lines
        temp_filename = "/tmp/proxychains.conf.temp"

        # Read the existing content from the file
        with open(config_path, "r") as file:
            lines = file.readlines()

        # Update the proxychain type by commenting and uncommenting lines
        proxy_types = ["dynamic_chain", "strict_chain", "random_chain"]
        updated_lines = []

        for line in lines:
            # Comment/uncomment proxychain types based on the selected type
            if any(pt in line for pt in proxy_types):
                if proxychain_type in line:
                    # Uncomment the chosen proxychain type
                    updated_lines.append(line.lstrip("#"))
                else:
                    # Comment out other proxychain types
                    updated_lines.append("#" + line if not line.startswith("#") else line)
            else:
                updated_lines.append(line)

        # Write the updated content to the temporary file
        with open(temp_filename, "w") as temp_file:
            temp_file.writelines(updated_lines)

        # Use sudo to move the temporary file to /etc/proxychains.conf
        try:
            command = f"sudo mv {temp_filename} {config_path}"
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Success", f"Proxychain type updated to {proxychain_type}.")

            # Update the selected radio button to indicate the current proxychain type
            for chain_type, radio_button in self.radio_buttons.items():
                if chain_type == proxychain_type:
                    radio_button.select()
                else:
                    radio_button.deselect()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update proxychain type: {e}")

    def run_proxychains_command(self):
        command = self.command_entry.get()
        if command:
            try:
                # Run the command using Proxychains
                process = subprocess.Popen(f"proxychains {command}", shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()

                # Log the output and error if any
                if output:
                    self.log_text.insert(tk.END, f"Output from {command}:\n{output}\n")
                if error:
                    self.log_text.insert(tk.END, f"Error from {command}:\n{error}\n")

                messagebox.showinfo("Success", f"Command '{command}' run through Proxychains.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run command: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter a command to run.")

    def navigate_to_url(self):
        url = self.url_entry.get()
        if url:
            try:
                # Run the URL using Proxychains and a web browser (e.g., Firefox)
                subprocess.Popen(f"proxychains firefox {url}", shell=True)
                messagebox.showinfo("Success", f"Navigated to {url} using Proxychains.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to navigate to URL: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter a URL to navigate to.")

    def run_command_with_sudo(self, command):
        # Run the command with sudo and raise an exception if it fails
        try:
            process = subprocess.run(f"sudo {command}", shell=True, check=True, text=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Log the output
            if process.stdout:
                self.log_text.insert(tk.END, f"Output from {command}:\n{process.stdout}\n")
            if process.stderr:
                self.log_text.insert(tk.END, f"Error from {command}:\n{process.stderr}\n")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Command failed with exit code {e.returncode}: {e.output}")

    def execute_custom_command(self):
        command = self.terminal_entry.get()
        if command:
            try:
                # Execute the command in a subprocess
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()

                # Log the output and error if any
                if output:
                    self.log_text.insert(tk.END, f"Output from {command}:\n{output}\n")
                if error:
                    self.log_text.insert(tk.END, f"Error from {command}:\n{error}\n")

                messagebox.showinfo("Success", f"Command '{command}' executed.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute command: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter a command to execute.")

    def ping_servers(self):
        try:
            # Allow the user to specify the configuration file path
            config_path = "/etc/proxychains.conf"

            # Read the Proxychains configuration file to extract server IPs
            with open(config_path, "r") as file:
                lines = file.readlines()

            # Define a regular expression pattern to match IP addresses
            ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

            # Extract server IPs from the configuration file
            servers = []
            for line in lines:
                # Search for IP addresses in the line using the regex pattern
                match = ip_pattern.search(line)
                if match:
                    server_ip = match.group()
                    servers.append(server_ip)

            # Loop through each server IP and ping it
            for server in servers:
                # Run the ping command for the server with a timeout of 1 second
                command = f"ping -c 1 -W 1 {server}"
                process = subprocess.run(command, shell=True, capture_output=True, text=True)

                # Check the return code of the ping command
                if process.returncode == 0:
                    # Server is up
                    self.log_text.insert(tk.END, f"{server} is up.\n")
                else:
                    # Server is down
                    self.log_text.insert(tk.END, f"{server} is down.\n")

            messagebox.showinfo("Success", "Pinged specified servers.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to ping servers: {e}")

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def update_tor_status(self):
        try:
            # Run the command to check the status of Tor service
            process = subprocess.run("systemctl is-active tor", shell=True, capture_output=True, text=True)
            status = process.stdout.strip()

            # Update the Tor status label with color based on the status
            if status == "active":
                self.tor_status_label.config(text="Tor status: Active", fg=self.active_color)
            else:
                self.tor_status_label.config(text="Tor status: Inactive", fg=self.inactive_color)
        except Exception as e:
            self.tor_status_label.config(text=f"Tor status: Error checking status: {e}", fg=self.inactive_color)

# Create the application and start the main event loop
if __name__ == "__main__":
    app = ProxychainsConfigurator()
    app.mainloop()