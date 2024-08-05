import tkinter as tk
from tkinter import ttk
import speedtest
import threading
import time


class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("400x400")
        self.root.configure(bg="282c34")
                            
        
        #frame for the content
        frame = tk.Frame(self.root, bg="282c34")
        frame.pack(expand=True)

        #label for the title
        self.title_label = tk.Label(
            frame, text="Internet Speed Test", 
            font=("Helvetica", 18, "bold"),
            fg="#61afef", bg="#282c34"
        )
        self.title_label.pack(pady=20)
        self.test_button = tk.Button(
            frame, text="Start Test", font=("Helvetica", 14), command=self.run_speed_test, bg="#61afef", fg="#ffffff", activebackground="#61afef", activeforeground="#ffffff"
        )
        self.test_button.pack(pady=10)

        # Create a label to display results
        self.result_label = tk.Label(frame, text="", font=(
            "Helvetica", 14), fg="#dcdfe4", bg="#282c34")
        self.result_label.pack(pady=20)

        # Create a canvas for animation
        self.canvas = tk.Canvas(
            frame, width=100, height=100, bg="#282c34", highlightthickness=0)
        self.arc = self.canvas.create_arc(
            10, 10, 90, 90, start=0, extent=150, outline="#61afef", width=5)
        self.canvas.pack(pady=10)

        # Animation variables
        self.angle = 0
        self.animating = False

    def animate_arc(self):
        """Animate the arc to create a spinning effect."""
        if self.animating:
            self.angle = (self.angle + 10) % 360
            self.canvas.itemconfig(self.arc, start=self.angle)
            self.root.after(50, self.animate_arc)

    def toggle_animation(self, start=True):
        """Start or stop the spinning animation."""
        self.animating = start
        if start:
            self.animate_arc()
        else:
            self.canvas.itemconfig(self.arc, start=0)

    def run_speed_test(self):
        """Run the internet speed test and update the GUI with results."""
        self.test_button.config(state=tk.DISABLED)
        self.result_label.config(text="Testing...")
        self.toggle_animation(True)

        def test():
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000      # Convert to Mbps
            ping = st.results.ping

            # Update the GUI with the results
            result_text = (
                f"Download Speed: {download_speed:.2f} Mbps\n"
                f"Upload Speed: {upload_speed:.2f} Mbps\n"
                f"Ping: {ping:.2f} ms"
            )
            self.result_label.config(text=result_text)
            self.toggle_animation(False)
            self.test_button.config(state=tk.NORMAL)

        # Run in a separate thread to prevent UI blocking
        threading.Thread(target=test).start()


root = tk.Tk()
app = SpeedTestApp(root)

root.mainloop()

class SpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("400x400")
        self.root.configure(bg="282c34")
                            
        
        #frame for the content
        frame = tk.Frame(self.root, bg="282c34")
        frame.pack(expand=True)

        #label for the title
        self.title_label = tk.Label(
            frame, text="Internet Speed Test", 
            font=("Helvetica", 18, "bold"),
            fg="#61afef", bg="#282c34"
        )
        self.title_label.pack(pady=20)
        # Create a button to start the speed test
        self.test_button = tk.Button(
            frame, text="Start Test", font=("Helvetica", 14), command=self.run_speed_test, bg="#61afef", fg="#ffffff", activebackground="#61afef", activeforeground="#ffffff"
        )
        self.test_button.pack(pady=10)

        # Create a label to display results
        self.result_label = tk.Label(frame, text="", font=(
            "Helvetica", 14), fg="#dcdfe4", bg="#282c34")
        self.result_label.pack(pady=20)

        # Create a canvas for animation
        self.canvas = tk.Canvas(
            frame, width=100, height=100, bg="#282c34", highlightthickness=0)
        self.arc = self.canvas.create_arc(
            10, 10, 90, 90, start=0, extent=150, outline="#61afef", width=5)
        self.canvas.pack(pady=10)

        # Animation variables
        self.angle = 0
        self.animating = False

    def animate_arc(self):
        """Animate the arc to create a spinning effect."""
        if self.animating:
            self.angle = (self.angle + 10) % 360
            self.canvas.itemconfig(self.arc, start=self.angle)
            self.root.after(50, self.animate_arc)

    def toggle_animation(self, start=True):
        """Start or stop the spinning animation."""
        self.animating = start
        if start:
            self.animate_arc()
        else:
            self.canvas.itemconfig(self.arc, start=0)

    def run_speed_test(self):
        """Run the internet speed test and update the GUI with results."""
        self.test_button.config(state=tk.DISABLED)
        self.result_label.config(text="Testing...")
        self.toggle_animation(True)

        def test():
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000      # Convert to Mbps
            ping = st.results.ping

            # Update the GUI with the results
            result_text = (
                f"Download Speed: {download_speed:.2f} Mbps\n"
                f"Upload Speed: {upload_speed:.2f} Mbps\n"
                f"Ping: {ping:.2f} ms"
            )
            self.result_label.config(text=result_text)
            self.toggle_animation(False)
            self.test_button.config(state=tk.NORMAL)

        # Run in a separate thread to prevent UI blocking
        threading.Thread(target=test).start()


root = tk.Tk()
app = SpeedTestApp(root)

root.mainloop()
