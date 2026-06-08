import serial
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

SERIAL_PORT = "COM5"   # 改成你的 Pico 端口
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

latest_time = 0
latest_raw = 0
latest_angle = 0.0

# -----------------------------
# Effect curves
# -----------------------------
x_curve = np.linspace(-1, 1, 500)

# Bump effect
A = 4.0
x0 = 0.0
sigma = 0.20
F_bump = A * (x_curve - x0) * np.exp(-((x_curve - x0) ** 2) / (2 * sigma ** 2))
F_bump = F_bump / np.max(np.abs(F_bump))

# Detent / toggle-like effect
k = 2.0
b = 4.0
F_detent = k * x_curve - b * x_curve**3
F_detent = F_detent / np.max(np.abs(F_detent))

current_effect = "bump"

# -----------------------------
# Figure layout
# -----------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

# ---- Left plot: paddle angle ----
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-1.2, 1.2)
ax1.set_aspect("equal")
ax1.grid(True)
ax1.set_title("Real-Time Paddle Angle")

circle = plt.Circle((0, 0), 1.0, fill=False)
ax1.add_patch(circle)

line_plot, = ax1.plot([0, 1], [0, 0], linewidth=3)
text_info = ax1.text(-1.1, 1.05, "", fontsize=11, va="top")

# ---- Right plot: haptic effect curve ----
curve_plot, = ax2.plot(x_curve, F_bump, linewidth=2, label="Bump Effect")
ax2.axhline(0, linewidth=1)
ax2.axvline(0, linewidth=1)
ax2.set_xlim(-1.05, 1.05)
ax2.set_ylim(-1.1, 1.1)
ax2.grid(True)
ax2.set_title("Haptic Effect Curve")
ax2.set_xlabel("Normalized Displacement")
ax2.set_ylabel("Normalized Desired Force")

point_plot, = ax2.plot([0], [0], 'ro', markersize=8)
effect_text = ax2.text(-0.98, 1.02, "Effect: bump", fontsize=11, va="top")

def angle_to_normalized_x(angle_deg):
    x = (angle_deg / 180.0) - 1.0
    if x < -1:
        x = -1
    if x > 1:
        x = 1
    return x

def bump_force(x):
    val = A * (x - x0) * math.exp(-((x - x0) ** 2) / (2 * sigma ** 2))
    return val / np.max(np.abs(F_bump))

def detent_force(x):
    val = k * x - b * x**3
    return val / np.max(np.abs(F_detent))

def on_key(event):
    global current_effect
    if event.key == 'b':
        current_effect = "bump"
    elif event.key == 'd':
        current_effect = "detent"

fig.canvas.mpl_connect("key_press_event", on_key)

def update(frame):
    global latest_time, latest_raw, latest_angle, current_effect

    while ser.in_waiting:
        line = ser.readline().decode(errors="ignore").strip()
        parts = line.split(",")

        if len(parts) == 3:
            try:
                latest_time = int(parts[0])
                latest_raw = int(parts[1])
                latest_angle = float(parts[2])
            except ValueError:
                pass

    # ---- Left plot update ----
    theta = math.radians(latest_angle)
    x = math.cos(theta)
    y = math.sin(theta)

    line_plot.set_data([0, x], [0, y])
    text_info.set_text(
        f"time_ms = {latest_time}\nraw = {latest_raw}\nangle = {latest_angle:.2f} deg"
    )

    # ---- Right plot update ----
    x_norm = angle_to_normalized_x(latest_angle)

    if current_effect == "bump":
        curve_plot.set_data(x_curve, F_bump)
        y_force = bump_force(x_norm)
        effect_text.set_text("Effect: bump   (press 'd' for detent)")
    else:
        curve_plot.set_data(x_curve, F_detent)
        y_force = detent_force(x_norm)
        effect_text.set_text("Effect: detent   (press 'b' for bump)")

    point_plot.set_data([x_norm], [y_force])

    return line_plot, text_info, curve_plot, point_plot, effect_text

ani = FuncAnimation(fig, update, interval=50, blit=False)
plt.tight_layout()
plt.show()

ser.close()