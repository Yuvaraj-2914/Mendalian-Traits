# 🧬 Mendalian Traits
### Evolutionary Game Theory in Mendelian Genetics

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Research](https://img.shields.io/badge/Research-Evolutionary%20Game%20Theory-purple)](https://doi.org/10.1371/journal.pone.0331044)
[![Status](https://img.shields.io/badge/Project-Academic%20Research-green)]()

## 📌 Overview

**Mendalian Traits** is an interactive simulation project that explores the relationship between Mendelian genetics and Evolutionary Game Theory.

The project is based on the research paper *"Matrix Games Between Full Siblings in Mendelian Populations"* (2025). It investigates how genetic inheritance, sibling cooperation and defection, and survival probabilities influence genotype distributions and population evolution.

The system combines mathematical modelling and computational simulation to demonstrate how game-theoretic interactions can influence genetic population dynamics.

---

## 🚀 How to Run the Web Dashboard

You can run the interactive website locally using either **Node.js** or **Python**:

### Option 1: Using Node.js (Recommended)
Open your terminal inside the project directory and run:

```bash
node web/server.mjs
```

Then open your browser and navigate to:  
👉 **[http://127.0.0.1:3000/](http://127.0.0.1:3000/)**

### Option 2: Using Python
If you prefer Python:

```bash
python -m http.server 3000 --directory web
```

Then open your browser and navigate to:  
👉 **[http://127.0.0.1:3000/](http://127.0.0.1:3000/)**

---

## 🎯 Objectives

- Simulate Mendelian inheritance and offspring genotype probabilities.
- Explore dominant, recessive, and intermediate inheritance patterns.
- Model cooperation and defection between siblings.
- Apply game-theoretic payoff matrices to sibling survival.
- Study changes in genotype frequencies over time.
- Visualise population evolution through computational simulations.

## 🧪 Key Features

### Mendelian Inheritance
Models the inheritance of two alleles, `a` and `A`, producing three possible genotypes:

- `aa` – Homozygous recessive
- `aA` – Heterozygous
- `AA` – Homozygous dominant

Calculates offspring genotype probabilities using Mendelian segregation principles.

### Genotype–Phenotype Mapping
Maps genotypes to behavioural strategies under three inheritance patterns:

- Dominant inheritance
- Recessive inheritance
- Intermediate inheritance

### Evolutionary Game Theory
Models sibling interactions using two strategies:

- Cooperation
- Defection

A payoff matrix represents the survival outcomes associated with different sibling interactions.

### Population Dynamics
Uses genotype production and survival probabilities to model changes in genotype frequencies over time.

---

## 📐 Mathematical Model

The implementation combines Mendelian inheritance probabilities with game-theoretic survival calculations.

The payoff matrix used in the selected donation-game example is:

$$A_3 = \begin{pmatrix} 0.7 & 0.1 \\ 0.8 & 0.2 \end{pmatrix}$$

The population dynamics are represented by:

$$\dot{x}_k = V_k(x) - x_k\sum_j V_j(x)$$

Where:
- $x_k$ represents the frequency of genotype $k$.
- $V_k(x)$ represents the production rate of genotype $k$.
- The equation describes how genotype frequencies change over time.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core mathematical implementation |
| NumPy & SciPy | Differential equation solving (RK45) |
| Pandas | Data processing & CSV exports |
| HTML, Tailwind CSS, JavaScript | Interactive web dashboard |
| Plotly.js | Dynamic scientific visualizations |
| KaTeX | Mathematical formula rendering |

---

## 📁 Repository Structure

```text
Mendalian-Traits/
│
├── web/ 
│   ├── index.html        # Interactive scientific dashboard
│   ├── app.js            # UI logic, Plotly charts & interactions
│   ├── engine.js         # Client-side numerical RK4 solver
│   ├── server.mjs        # Lightweight web server
│   └── benchmark_data.json
│
├── GT.py                 # Core SciPy game-theoretic simulation
├── export_benchmark.py   # Benchmark result exporter
├── benchmark_data.json   # Validated paper benchmark datasets
├── dominant_results.csv  # Dominant inheritance results
├── recessive_results.csv # Recessive inheritance results
├── intermediate_results.csv # Intermediate inheritance results
└── README.md
```

---

## ⚙️ Running the Python Simulation

### Install Dependencies:

```bash
pip install numpy scipy pandas matplotlib
```

### Run Python Mathematical Engine:

```bash
python GT.py
```

### Re-export Benchmark Data:

```bash
python export_benchmark.py
```

---

## 🔬 Research Paper Reference

Garay, J., Varga, T., Csiszár, V., Móri, T. F., and Szilágyi, A. (2025). "Matrix Games Between Full Siblings in Mendelian Populations." *PLOS ONE*, 20(9), e0331044.  
**DOI:** [10.1371/journal.pone.0331044](https://doi.org/10.1371/journal.pone.0331044)
