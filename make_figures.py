#!/usr/bin/env python3
"""Generate the two scaling figures for the engine-acceleration paper.

Data are the exact published table values (results.tex Tables 2-3). Outputs land in
manuscript/figures/ as PNG at 300 dpi (matching the companion paper's artwork format;
titles are omitted and supplied via the LaTeX \\caption, per the C&G artwork guidelines).
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

plt.rcParams.update({
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})

# ---- Figure: cross-hardware scaling (final engine, dedicated AWS instances) ----
# Self-relative speedup (each machine's own t1 -> N). Consistent final-engine re-run,
# one simulated year, daily channel_sd, best of two. (Workstation removed; AWS-only.)
n   = [2, 4, 6, 8, 10, 12, 16, 20, 24]
c8a = [1.70, 2.79, 3.48, 3.95, 4.30, 4.54, 4.90, 5.18, 5.33]   # AMD EPYC "Turin", 32 vCPU
c8i = [1.59, 2.41, 2.93, 3.29, 3.55, 3.75, 4.01, 3.73, 3.74]   # Intel Xeon "Granite Rapids", 32 vCPU
c5a = [1.62, 2.47, 2.89, 3.21, 3.42, 3.60, 3.81, 3.51, 3.58]   # AMD EPYC "Rome", 32 vCPU

fig, ax = plt.subplots(figsize=(5.4, 3.6))
ax.plot(n, c8a, marker="o", ms=4, lw=1.6, color="#c0392b", label="c8a (Turin)")
ax.plot(n, c8i, marker="s", ms=4, lw=1.6, color="#2c6fbb", label="c8i (Granite Rapids)")
ax.plot(n, c5a, marker="^", ms=4, lw=1.6, color="#27ae60", label="c5a (Rome)")
ax.annotate("Turin still climbing\nat 24 threads (5.33×)", xy=(24, 5.33), xytext=(13, 5.2),
            fontsize=8, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.8))
ax.annotate("others peak ~16,\nregress on SMT", xy=(16, 4.01), xytext=(8.5, 2.1),
            fontsize=8, color="#555",
            arrowprops=dict(arrowstyle="->", color="#555", lw=0.8))
ax.set_xlabel("Worker threads")
ax.set_ylabel("Speedup (each machine's own $1\\rightarrow N$)")
ax.set_xticks(n)
ax.set_ylim(1.2, 5.8)
ax.legend(frameon=False, loc="lower right", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "Figure_3.png"), dpi=300, bbox_inches="tight")
plt.close(fig)

print("WROTE", os.path.join(FIGDIR, "Figure_3.png"))

# ---- Figure: speedup configurator (total vs stock single-core, end-to-end) ----
# Directly measured R0(stock,1 thread) / R6FULL(N) on each dedicated AWS instance.
nn  = [2, 4, 6, 8, 10, 12, 16, 20, 24]
c8a_tot = [2.28, 3.74, 4.66, 5.29, 5.76, 6.09, 6.57, 6.95, 7.14]   # Turin
c8i_tot = [3.32, 5.05, 6.13, 6.88, 7.42, 7.85, 8.40, 7.80, 7.83]   # Granite Rapids
c5a_tot = [2.81, 4.28, 5.00, 5.56, 5.92, 6.23, 6.59, 6.08, 6.20]   # Rome
# c8a byte-identical (routing-serial) mode: directly measured vs-stock on the same box.
byte_n   = [2, 4, 8, 16]
c8a_byte = [1.98, 2.75, 3.37, 3.80]

fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.plot(nn, c8a_tot, marker="o", ms=4, lw=1.8, color="#c0392b", label="c8a Turin — full wavefront")
ax.plot(nn, c8i_tot, marker="s", ms=4, lw=1.6, color="#2c6fbb", label="c8i Granite Rapids — full")
ax.plot(nn, c5a_tot, marker="^", ms=4, lw=1.6, color="#27ae60", label="c5a Rome — full")
ax.plot(byte_n, c8a_byte, marker="o", ms=3, lw=1.4, color="#c0392b", ls="--",
        label="c8a Turin — byte-identical (routing-serial)")
ax.set_xlabel("Cores")
ax.set_ylabel("Total speedup vs. stock single core")
ax.set_xticks(nn)
ax.set_xlim(1.0, 25)
ax.set_ylim(1.0, 9.0)
ax.legend(frameon=False, loc="upper left", fontsize=7.5)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "Figure_5.png"), dpi=300, bbox_inches="tight")
plt.close(fig)
print("WROTE", os.path.join(FIGDIR, "Figure_5.png"))
