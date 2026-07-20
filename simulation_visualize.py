#!/usr/bin/env python3
"""Visualize the fungal bio-battery electron transport graph."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from electron_transport_graph import FungalMFCGraph, FARADAY

mfc = FungalMFCGraph(strain="T_pubescens")
G = mfc.G

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

pos = nx.spring_layout(G, k=2.5, iterations=100)

capacities = []
for u, v, d in G.edges(data=True):
    if d.get("capacity", 0) > 0:
        cap_uA = d["capacity"] * FARADAY * 1e6
        capacities.append(cap_uA)
    else:
        capacities.append(0)

node_colors = []
for node, data in G.nodes(data=True):
    ntype = data.get("type", "")
    if ntype == "substrate": node_colors.append("#2ecc71")
    elif ntype == "electrode": node_colors.append("#f39c12")
    elif ntype == "enzyme": node_colors.append("#e74c3c")
    elif ntype == "mediator": node_colors.append("#9b59b6")
    elif ntype == "electron_carrier": node_colors.append("#3498db")
    elif ntype == "electrical": node_colors.append("#1abc9c")
    elif ntype == "product": node_colors.append("#95a5a6")
    else: node_colors.append("#bdc3c7")

edge_colors = []
edge_widths = []
max_cap = max(capacities) if capacities else 1
for cap in capacities:
    if cap > 0:
        edge_colors.append("#e74c3c")
        w = max(1, cap / max_cap * 15)
        edge_widths.append(w)
    else:
        edge_colors.append("#bdc3c7")
        edge_widths.append(0.5)

nx.draw(G, pos, ax=ax1, with_labels=True, node_color=node_colors,
        edge_color=edge_colors, width=edge_widths, node_size=2000,
        font_size=9, font_weight="bold", arrows=True,
        arrowsize=20)

ax1.set_title("Electron Transport Graph\n(edge width = capacity)", fontsize=14)

results = mfc.bottleneck_analysis()
edges_sorted = results["critical_path_ranking"]

names = [e["edge"].replace(" → ", "\n→\n") for e in edges_sorted]
vals = [e["current_uA"] for e in edges_sorted]
colors = ["#e74c3c" if i == 0 else "#3498db" for i in range(len(vals))]

bars = ax2.barh(range(len(names)), vals, color=colors)
ax2.set_yticks(range(len(names)))
ax2.set_yticklabels(names, fontsize=8)
ax2.set_xlabel("Max Current (µA)")
ax2.set_title(f"Bottleneck: {results['bottleneck_edge']}\n{results['max_power_density_uW_cm2']:.1f} µW/cm² max", fontsize=12)
ax2.set_xscale("log")
ax2.grid(axis="x", alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, vals)):
    ax2.text(val * 1.1, bar.get_y() + bar.get_height()/2,
             f"{val:.1f} µA", va="center", fontsize=7)

plt.tight_layout()
plt.savefig("/home/weissto_local/workspace/shrooms/simulation/electron_transport_graph.png", dpi=150, bbox_inches="tight")
print("Saved: electron_transport_graph.png")

# Power vs Internal Resistance curve
resistances = np.logspace(2, 5, 50)
v_oc = 0.45
powers = [v_oc**2 * r / (r + 10e3)**2 * 1e6 for r in resistances]

fig2, ax3 = plt.subplots(figsize=(8, 5))
ax3.semilogx(resistances, powers, "b-", linewidth=2)
ax3.axvline(10e3, color="r", linestyle="--", alpha=0.5, label="R_internal = 10 kΩ")
ax3.axhline(12.5, color="g", linestyle="--", alpha=0.5, label="Empa baseline (12.5 µW/cm²)")
ax3.set_xlabel("Load Resistance (Ω)")
ax3.set_ylabel("Power Density (µW/cm²)")
ax3.set_title("Power vs Load Resistance at V_oc = 0.45V")
ax3.legend()
ax3.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("/home/weissto_local/workspace/shrooms/simulation/power_curve.png", dpi=150, bbox_inches="tight")
print("Saved: power_curve.png")
