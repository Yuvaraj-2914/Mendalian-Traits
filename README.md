# 🧬 Mendalian Traits
### Evolutionary Game Theory in Mendelian Genetics

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Research](https://img.shields.io/badge/Research-Evolutionary%20Game%20Theory-purple)](https://doi.org/10.1371/journal.pone.0331044)
[![Status](https://img.shields.io/badge/Project-Academic%20Research-green)]()

## 📌 Overview

**Mendalian Traits** is an interactive simulation project that explores the relationship between Mendelian genetics and Evolutionary Game Theory.

The project is based on the research paper *"Matrix Games Between Full Siblings in Mendelian Populations"* (2025). It investigates how genetic inheritance, sibling cooperation and defection, and survival probabilities influence genotype distributions and population evolution.

The system combines mathematical modelling and computational simulation to demonstrate how game-theoretic interactions can influence genetic population dynamics.

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

### Simulation and Results
Generates numerical outputs and result files for comparing the different inheritance patterns.

## 📐 Mathematical Model

The implementation combines Mendelian inheritance probabilities with game-theoretic survival calculations.

The payoff matrix used in the selected donation-game example is:

\[
A_3 =
\begin{pmatrix}
0.7 & 0.1\\
0.8 & 0.2
\end{pmatrix}
\]

The population dynamics are represented by:

\[
\dot{x}_k = V_k(x) - x_k\sum_j V_j(x)
\]

Where:

- \(x_k\) represents the frequency of genotype \(k\).
- \(V_k(x)\) represents the production rate of genotype \(k\).
- The equation describes how genotype frequencies change over time.

Numerical integration is used to solve the population dynamics equations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| NumPy | Numerical calculations |
| SciPy | Differential equation solving |
| Pandas | Data processing |
| Matplotlib | Data visualisation |
| HTML, CSS, JavaScript | Web interface |

## 📁 Repository Structure

```text
Mendalian-Traits/
│
├── web/ 
│   └── Web application files
│
├── GT.py
│   └── Core game-theoretic and genetic simulation
│
├── export_benchmark.py
│   └── Benchmark result generation
│
├── benchmark_data.json
│   └── Benchmark data
│
├── dominant_results.csv
│   └── Dominant inheritance results
│
├── recessive_results.csv
│   └── Recessive inheritance results
│
├── intermediate_results.csv
│   └── Intermediate inheritance results
│
└── README.md
```

## ⚙️ Installation and Execution

### Prerequisites

- Python 3.x
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/Yuvaraj-2914/Mendalian-Traits.git
```

Navigate into the project directory:

```bash
cd Mendalian-Traits
```

### Install Dependencies

```bash
pip install numpy scipy pandas matplotlib
```

### Run the Simulation

```bash
python GT.py
```

The simulation executes the mathematical model and generates the corresponding results based on the implementation.

**Note:** The web interface is maintained separately in the `web/` directory. Follow its application-specific setup instructions to launch it.

## 📊 Expected Outcomes

The project is designed to demonstrate:

- Mendelian offspring genotype distributions.
- Differences between dominant, recessive, and intermediate inheritance.
- The influence of sibling strategies on survival probabilities.
- Changes in genotype frequencies over time.
- The relationship between inheritance patterns and evolutionary population dynamics.

## 🔬 Research Paper

The primary research publication used for this implementation is:

Garay, J., Varga, T., Csiszár, V., Móri, T. F., and Szilágyi, A. (2025). "Matrix Games Between Full Siblings in Mendelian Populations." *PLOS ONE*, 20(9), e0331044.

**DOI:** https://doi.org/10.1371/journal.pone.0331044

## 🚀 Future Enhancements

- Multiple genetic loci and recombination.
- Biased allele transmission and meiotic drive.
- Stochastic finite-population simulations.
- Additional evolutionary game strategies.
- Enhanced interactive visualisations.
- Comparison with additional genetic population models.

## 👨‍💻 Project Purpose

This project was developed as part of an academic research study on the application of Game Theory to biological systems.

It aims to provide an accessible computational demonstration of how Mendelian inheritance and evolutionary game-theoretic interactions can be combined to study population evolution.

---

**Keywords:** Mendelian Genetics · Evolutionary Game Theory · Population Dynamics · Genotype · Phenotype · Cooperation · Defection · Genetic Inheritance
