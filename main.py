import tkinter as tk
from tkinter import messagebox
import math
import time


class PhantomApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PHANTOM")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0a0f")

        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 450
        y = (self.root.winfo_screenheight() // 2) - 300
        self.root.geometry(f"900x600+{x}+{y}")

        # Animation state
        self.alpha = 0
        self.pulse_angle = 0
        self.particles = []
        self.loading_progress = 0
        self.loading_done = False

        self._create_loading_screen()
        self._animate_loading()

    def _create_loading_screen(self):
        """Create the loading screen with canvas for animations."""
        self.loading_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(
            self.loading_frame,
            width=900,
            height=600,
            bg="#0a0a0f",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Bind click event to entire canvas
        self.canvas.bind("<Button-1>", self._on_loading_click)

        # Initialize particles
        import random

        for _ in range(50):
            self.particles.append(
                {
                    "x": random.randint(0, 900),
                    "y": random.randint(0, 600),
                    "speed": random.uniform(0.3, 1.5),
                    "size": random.randint(1, 3),
                    "alpha": random.randint(50, 200),
                }
            )

    def _animate_loading(self):
        """Animate the loading screen."""
        self.canvas.delete("all")

        # Draw floating particles
        import random

        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < 0:
                p["y"] = 600
                p["x"] = random.randint(0, 900)

            gray = int(p["alpha"] * 0.4)
            color = f"#{gray:02x}{gray:02x}{max(gray + 30, 255) if gray + 30 < 256 else 255:02x}"
            self.canvas.create_oval(
                p["x"] - p["size"],
                p["y"] - p["size"],
                p["x"] + p["size"],
                p["y"] + p["size"],
                fill=color,
                outline="",
            )

        # Draw glowing circle behind logo
        self.pulse_angle += 0.05
        pulse_radius = 120 + math.sin(self.pulse_angle) * 20
        pulse_alpha = int(30 + math.sin(self.pulse_angle) * 15)

        for i in range(3):
            r = pulse_radius + i * 15
            alpha_val = max(10, pulse_alpha - i * 10)
            color = f"#{alpha_val:02x}{alpha_val:02x}{min(alpha_val + 40, 255):02x}"
            self.canvas.create_oval(
                450 - r, 220 - r, 450 + r, 220 + r, outline=color, width=2
            )

        # Draw PHANTOM title
        self.canvas.create_text(
            450,
            200,
            text="PHANTOM",
            font=("Courier New", 52, "bold"),
            fill="#e0e0ff",
        )

        # Draw subtitle
        self.canvas.create_text(
            450, 260, text="Multi Tool", font=("Courier New", 16), fill="#7070a0"
        )

        # Loading bar
        if self.loading_progress < 100:
            self.loading_progress += 0.8

        bar_width = 300
        bar_x = 300
        bar_y = 350
        bar_height = 4

        # Background bar
        self.canvas.create_rectangle(
            bar_x, bar_y, bar_x + bar_width, bar_y + bar_height, fill="#1a1a2e", outline=""
        )

        # Progress bar with gradient effect
        progress_width = (self.loading_progress / 100) * bar_width
        gradient_color = self._get_gradient_color(self.loading_progress)
        self.canvas.create_rectangle(
            bar_x, bar_y, bar_x + progress_width, bar_y + bar_height,
            fill=gradient_color, outline=""
        )

        # Loading percentage text
        self.canvas.create_text(
            450,
            380,
            text=f"{int(self.loading_progress)}%",
            font=("Courier New", 12),
            fill="#5050a0",
        )

        # "Click to continue" text (pulsing)
        if self.loading_progress >= 100:
            if not self.loading_done:
                self.loading_done = True

            text_alpha = int(128 + math.sin(self.pulse_angle * 2) * 127)
            text_color = f"#{text_alpha:02x}{text_alpha:02x}{min(text_alpha + 30, 255):02x}"
            self.canvas.create_text(
                450,
                450,
                text="[ Click anywhere to continue ]",
                font=("Courier New", 14),
                fill=text_color,
            )

        # Draw decorative corner elements
        self._draw_corners()

        # Bottom text
        self.canvas.create_text(
            450, 570, text="v1.0.0", font=("Courier New", 10), fill="#303050"
        )

        self.root.after(30, self._animate_loading)

    def _get_gradient_color(self, progress):
        """Get a color based on progress (blue to purple gradient)."""
        r = int(40 + (progress / 100) * 80)
        g = int(40 + (progress / 100) * 20)
        b = int(120 + (progress / 100) * 100)
        return f"#{min(r, 255):02x}{min(g, 255):02x}{min(b, 255):02x}"

    def _draw_corners(self):
        """Draw decorative corner brackets."""
        corner_color = "#3030a0"
        size = 30
        offset = 20

        # Top-left
        self.canvas.create_line(
            offset, offset, offset + size, offset, fill=corner_color, width=2
        )
        self.canvas.create_line(
            offset, offset, offset, offset + size, fill=corner_color, width=2
        )

        # Top-right
        self.canvas.create_line(
            900 - offset, offset, 900 - offset - size, offset, fill=corner_color, width=2
        )
        self.canvas.create_line(
            900 - offset, offset, 900 - offset, offset + size, fill=corner_color, width=2
        )

        # Bottom-left
        self.canvas.create_line(
            offset, 600 - offset, offset + size, 600 - offset, fill=corner_color, width=2
        )
        self.canvas.create_line(
            offset, 600 - offset, offset, 600 - offset - size, fill=corner_color, width=2
        )

        # Bottom-right
        self.canvas.create_line(
            900 - offset, 600 - offset, 900 - offset - size, 600 - offset,
            fill=corner_color, width=2,
        )
        self.canvas.create_line(
            900 - offset, 600 - offset, 900 - offset, 600 - offset - size,
            fill=corner_color, width=2,
        )

    def _on_loading_click(self, event):
        """Handle click on loading screen - transition to login."""
        if self.loading_done:
            self._transition_to_login()

    def _transition_to_login(self):
        """Fade out loading screen and show login page."""
        self.loading_frame.destroy()
        self._create_login_page()

    def _create_login_page(self):
        """Create the login page UI."""
        self.login_frame = tk.Frame(self.root, bg="#0a0a0f")
        self.login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Login canvas for background effects
        self.login_canvas = tk.Canvas(
            self.login_frame, width=900, height=600, bg="#0a0a0f", highlightthickness=0
        )
        self.login_canvas.pack(fill="both", expand=True)

        # Draw decorative background lines
        for i in range(0, 900, 40):
            self.login_canvas.create_line(
                i, 0, i, 600, fill="#0f0f1a", width=1
            )
        for i in range(0, 600, 40):
            self.login_canvas.create_line(
                0, i, 900, i, fill="#0f0f1a", width=1
            )

        # Draw login card background
        card_x, card_y = 250, 100
        card_w, card_h = 400, 420

        # Card shadow
        self.login_canvas.create_rectangle(
            card_x + 3, card_y + 3, card_x + card_w + 3, card_y + card_h + 3,
            fill="#050508", outline="",
        )

        # Card body
        self.login_canvas.create_rectangle(
            card_x, card_y, card_x + card_w, card_y + card_h,
            fill="#12121f", outline="#2a2a4a", width=1,
        )

        # Card header accent line
        self.login_canvas.create_rectangle(
            card_x, card_y, card_x + card_w, card_y + 3, fill="#5050dd", outline=""
        )

        # Title on card
        self.login_canvas.create_text(
            450, 160, text="PHANTOM", font=("Courier New", 28, "bold"), fill="#d0d0ff"
        )
        self.login_canvas.create_text(
            450, 195, text="Sign in to continue", font=("Courier New", 11), fill="#5050a0"
        )

        # Username label
        self.login_canvas.create_text(
            320, 245, text="USERNAME", font=("Courier New", 9, "bold"), fill="#7070b0", anchor="w"
        )

        # Username entry
        self.username_entry = tk.Entry(
            self.login_frame,
            font=("Courier New", 13),
            bg="#1a1a30",
            fg="#c0c0e0",
            insertbackground="#8080ff",
            relief="flat",
            highlightthickness=1,
            highlightcolor="#4040aa",
            highlightbackground="#2a2a4a",
        )
        self.login_canvas.create_window(450, 275, window=self.username_entry, width=260, height=35)

        # Password label
        self.login_canvas.create_text(
            320, 325, text="PASSWORD", font=("Courier New", 9, "bold"), fill="#7070b0", anchor="w"
        )

        # Password entry
        self.password_entry = tk.Entry(
            self.login_frame,
            font=("Courier New", 13),
            bg="#1a1a30",
            fg="#c0c0e0",
            insertbackground="#8080ff",
            relief="flat",
            show="•",
            highlightthickness=1,
            highlightcolor="#4040aa",
            highlightbackground="#2a2a4a",
        )
        self.login_canvas.create_window(450, 355, window=self.password_entry, width=260, height=35)

        # Login button
        self.login_btn = tk.Button(
            self.login_frame,
            text="LOGIN",
            font=("Courier New", 12, "bold"),
            bg="#3535aa",
            fg="#ffffff",
            activebackground="#4545cc",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self._on_login,
        )
        self.login_canvas.create_window(450, 420, window=self.login_btn, width=260, height=40)

        # Footer text
        self.login_canvas.create_text(
            450, 480, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font=("Courier New", 8), fill="#202040"
        )
        self.login_canvas.create_text(
            450, 560, text="© 2026 Phantom Systems", font=("Courier New", 9), fill="#303050"
        )

        # Bind Enter key to login
        self.root.bind("<Return>", lambda e: self._on_login())

    def _on_login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Phantom", "Please enter both username and password.")
            return

        messagebox.showinfo("Phantom", f"Welcome, {username}!")

    def run(self):
        """Start the application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PhantomApp()
    app.run()
