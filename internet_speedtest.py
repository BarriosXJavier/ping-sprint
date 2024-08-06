#!/usr/bin/python3

import tkinter as tk
import speedtest
import threading


class SpeedTestApp:
    """
    A class representing an Internet Speed Test application.

    Attributes:
        root (tk.Tk): The root window of the application.

    Methods:
        __init__(self, root): Initializes the SpeedTestApp object.
        setup_ui(self): Sets up the user interface of the application.
        create_speed_label(self, parent, text): Creates a speed label widget.
        setup_animations(self): Sets up the animations for the gauge.
        draw_gauge(self): Draws the gauge on the canvas.
        run_speed_test(self): Runs the speed test.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("500x700")
        self.root.configure(bg="#282c34")

        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#282c34")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Internet Speed Test",
            font=("Helvetica", 24, "bold"),
            fg="#61afef",
            bg="#282c34",
        )
        title_label.pack(pady=20)

        # Speed gauge
        self.gauge_canvas = tk.Canvas(
            main_frame, width=300, height=300, bg="#282c34", highlightthickness=0
        )
        self.gauge_canvas.pack(pady=20)

        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Helvetica", 16),
            fg="#98c379",
            bg="#282c34",
        )
        self.status_label.pack(pady=10)

        # Speed labels
        self.speed_frame = tk.Frame(main_frame, bg="#282c34")
        self.speed_frame.pack(pady=10)

        self.download_label = self.create_speed_label(
            self.speed_frame, "Download")
        self.upload_label = self.create_speed_label(self.speed_frame, "Upload")
        self.ping_label = self.create_speed_label(self.speed_frame, "Ping")

        # Test button
        self.test_button = tk.Button(
            main_frame,
            text="Start Test",
            font=("Helvetica", 16),
            command=self.run_speed_test,
            bg="#61afef",
            fg="#ffffff",
            activebackground="#61afef",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=10,
        )
        self.test_button.pack(pady=20)

    def create_speed_label(self, parent, text):
        frame = tk.Frame(parent, bg="#282c34")
        frame.pack(side=tk.LEFT, padx=10)

        label = tk.Label(
            frame,
            text=text,
            font=("Helvetica", 14),
            fg="#dcdfe4",
            bg="#282c34",
        )
        label.pack()

        value = tk.Label(
            frame,
            text="--",
            font=("Helvetica", 16, "bold"),
            fg="#98c379",
            bg="#282c34",
        )
        value.pack()

        return value

    def setup_animations(self):
        self.gauge_value = 0
        self.gauge_target = 0
        self.gauge_speed = 0
        self.draw_gauge()

    def draw_gauge(self):
        self.gauge_canvas.delete("all")
        center_x, center_y = 150, 150
        radius = 120

        # Draw background arc
        self.gauge_canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=135,
            extent=270,
            style="arc",
            width=20,
            outline="#3e4451"
        )

        # Draw foreground arc
        self.gauge_canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=135,
            extent=self.gauge_value * 2.7,
            style="arc",
            width=20,
            outline="#61afef"
        )

        # Draw speed text
        self.gauge_canvas.create_text(
            center_x,
            center_y,
            text=f"{self.gauge_value:.1f}",
            font=("Helvetica", 48, "bold"),
            fill="#61afef"
        )
        self.gauge_canvas.create_text(
            center_x,
            center_y + 50,
            text="Mbps",
            font=("Helvetica", 18),
            fill="#dcdfe4"
        )

        # Animate gauge
        if abs(self.gauge_value - self.gauge_target) > 0.1:
            self.gauge_value += (self.gauge_target - self.gauge_value) * 0.1
            self.root.after(16, self.draw_gauge)

    def run_speed_test(self):
        self.test_button.config(state=tk.DISABLED)
        self.download_label.config(text="--")
        self.upload_label.config(text="--")
        self.ping_label.config(text="--")
        self.status_label.config(text="Test Started")

        def test():
            try:
                st = speedtest.Speedtest()
                st.get_best_server()

                # Test download speed
                self.root.after(0, lambda: self.status_label.config(
                    text="Test Running: Download"))
                self.gauge_target = 0
                download_speed = st.download() / 1_000_000  # Convert to Mbps
                self.gauge_target = download_speed
                self.root.after(0, self.draw_gauge)
                self.root.after(0, lambda: self.download_label.config(
                    text=f"{download_speed:.2f} Mbps"))

                # Test upload speed
                self.root.after(0, lambda: self.status_label.config(
                    text="Test Running: Upload"))
                self.gauge_target = 0
                upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                self.gauge_target = upload_speed
                self.root.after(0, self.draw_gauge)
                self.root.after(0, lambda: self.upload_label.config(
                    text=f"{upload_speed:.2f} Mbps"))

                # Get ping
                ping = st.results.ping
                self.root.after(0, lambda: self.ping_label.config(
                    text=f"{ping:.2f} ms"))

                self.root.after(
                    0, lambda: self.status_label.config(text="Test Complete"))
            except Exception as e:
                self.root.after(0, lambda e=e: self.status_label.config(
                    text=f"Error: {e}"))
            finally:
                self.root.after(
                    0, lambda: self.test_button.config(state=tk.NORMAL))

        threading.Thread(target=test).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()
