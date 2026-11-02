import json
import numpy as np
import pandas as pd
from GT import (
    GENOTYPES,
    PAYOFF_MATRIX,
    MATINGS,
    phenotype_strategies,
    family_survival,
    create_survival_table,
    stability_conditions,
    simulate
)

# Additional published matrices from Garay et al. (2025)
# A1: Prisoner's Dilemma
# A2: Snowdrift / Hawk-Dove
# A3: Donation game (0.7, 0.1; 0.8, 0.2)
MATRICES = {
    "A3_donation": {
        "name": "A3: Donation Game (Published Benchmark)",
        "matrix": [[0.7, 0.1], [0.8, 0.2]],
        "description": "Published main example in Section 4. aa and aA dynamics vs AA."
    },
    "A1_prisoners_dilemma": {
        "name": "A1: Classic Prisoner's Dilemma",
        "matrix": [[0.6, 0.1], [0.9, 0.2]],
        "description": "Standard PD payoff ranking T > R > P > S where sibling relatedness can alter ESS."
    },
    "A2_snowdrift": {
        "name": "A2: Snowdrift Game",
        "matrix": [[0.8, 0.4], [0.9, 0.1]],
        "description": "Cooperation can be mutually beneficial even with defection temptation."
    },
    "harmony_game": {
        "name": "Harmony Game",
        "matrix": [[0.9, 0.5], [0.6, 0.2]],
        "description": "Cooperation is strictly dominant for individual and sibling."
    }
}

export_data = {
    "paper": {
        "title": "Matrix Games Between Full Siblings in Mendelian Populations",
        "authors": "József Garay, Tamás Varga, Villő Csiszár, Tamás F. Móri, András Szilágyi",
        "journal": "PLOS ONE",
        "year": 2025,
        "volume": "20(9)",
        "article_id": "e0331044",
        "doi": "https://doi.org/10.1371/journal.pone.0331044"
    },
    "genotypes": GENOTYPES,
    "matings": {},
    "survival_tables": {},
    "simulations": {},
    "stability_analysis": {},
    "preset_matrices": MATRICES
}

# 1. Mendelian Mating Probabilities
for (p1, p2), probs in MATINGS.items():
    export_data["matings"][f"{p1} x {p2}"] = {
        "p1": p1,
        "p2": p2,
        "aa": float(probs[0]),
        "aA": float(probs[1]),
        "AA": float(probs[2])
    }

# 2. Survival Tables for each mode with A3
modes = ["recessive", "dominant", "intermediate"]
for mode in modes:
    st = create_survival_table(mode)
    export_data["survival_tables"][mode] = st.to_dict(orient="records")

# 3. Simulations for A3 with standard initial condition [0.33, 0.34, 0.33]
for mode in modes:
    t, freqs = simulate(mode, initial_state=[0.33, 0.34, 0.33], payoff_matrix=PAYOFF_MATRIX)
    # Sample 100 points for compact JSON storage
    indices = np.linspace(0, len(t) - 1, 100, dtype=int)
    export_data["simulations"][mode] = {
        "time": [round(float(t[idx]), 3) for idx in indices],
        "aa": [round(float(freqs[idx, 0]), 6) for idx in indices],
        "aA": [round(float(freqs[idx, 1]), 6) for idx in indices],
        "AA": [round(float(freqs[idx, 2]), 6) for idx in indices],
        "final": {
            "aa": float(freqs[-1, 0]),
            "aA": float(freqs[-1, 1]),
            "AA": float(freqs[-1, 2])
        }
    }

# 4. Stability conditions for all preset matrices
for key, item in MATRICES.items():
    mat = np.array(item["matrix"], dtype=float)
    stab = stability_conditions(mat)
    # Convert numpy bools to python bools
    clean_stab = {}
    for m, conds in stab.items():
        clean_stab[m] = {k: bool(v) for k, v in conds.items()}
    export_data["stability_analysis"][key] = clean_stab

with open("benchmark_data.json", "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=2)

print("Exported benchmark_data.json successfully!")

