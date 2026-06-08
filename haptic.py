import numpy as np
import matplotlib.pyplot as plt

# Normalized displacement
x = np.linspace(-1, 1, 500)

# -----------------------------
# Effect 1: Bump
# F_bump(x) = A (x-x0) exp(-(x-x0)^2 / (2 sigma^2))
# -----------------------------
A = 4.0
x0 = 0.0
sigma = 0.20

F_bump = A * (x - x0) * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

# Normalize to [-1, 1]
F_bump = F_bump / np.max(np.abs(F_bump))

# -----------------------------
# Effect 2: Detent / Toggle-like
# F_detent(x) = kx - b x^3
# -----------------------------
k = 2.0
b = 4.0

F_detent = k * x - b * x**3

# Normalize to [-1, 1]
F_detent = F_detent / np.max(np.abs(F_detent))

# -----------------------------
# Plot 1: Bump
# -----------------------------
plt.figure(figsize=(7, 4))
plt.plot(x, F_bump, linewidth=2)
plt.axhline(0, linewidth=1)
plt.axvline(0, linewidth=1)
plt.title("Haptic Effect 1: Bump")
plt.xlabel("Normalized Displacement")
plt.ylabel("Normalized Desired Force")
plt.grid(True)
plt.tight_layout()
plt.savefig("hw18_bump_curve.png", dpi=200)
plt.show()

# -----------------------------
# Plot 2: Detent / Toggle-like
# -----------------------------
plt.figure(figsize=(7, 4))
plt.plot(x, F_detent, linewidth=2)
plt.axhline(0, linewidth=1)
plt.axvline(0, linewidth=1)
plt.title("Haptic Effect 2: Detent / Toggle-like")
plt.xlabel("Normalized Displacement")
plt.ylabel("Normalized Desired Force")
plt.grid(True)
plt.tight_layout()
plt.savefig("hw18_detent_curve.png", dpi=200)
plt.show()