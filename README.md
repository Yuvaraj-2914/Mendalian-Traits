# Mendelian Sibling Matrix Games

Interactive research reproduction of the scientific paper:
> **"Matrix Games Between Full Siblings in Mendelian Populations"**  
> József Garay, Tamás Varga, Villő Csiszár, Tamás F. Móri, and András Szilágyi  
> *PLOS ONE*, September 2025 · **DOI:** [10.1371/journal.pone.0331044](https://doi.org/10.1371/journal.pone.0331044)

---

## 🚀 How to Run the Website

You have two easy ways to run the website on your machine:

### Option 1: Using Node.js (Recommended)
Open your terminal (PowerShell, Command Prompt, or VS Code terminal) in the project folder and run:

```bash
node web/server.mjs
```

Then open your browser and navigate to:
👉 **[http://127.0.0.1:3000/](http://127.0.0.1:3000/)**

---

### Option 2: Using Python
If you prefer Python, you can use its built-in HTTP server:

```bash
python -m http.server 3000 --directory web
```

Then open your browser and navigate to:
👉 **[http://127.0.0.1:3000/](http://127.0.0.1:3000/)**

---

## 🔬 Running the SciPy Mathematical Engine

To run the author's mathematical reproduction and generate simulation CSVs and stability analysis:

```bash
python GT.py
```

To re-export benchmark datasets for the web application:

```bash
python export_benchmark.py
```

---

## 📂 Project Structure

- `web/index.html` — Clean, decluttered interactive research dashboard.
- `web/engine.js` — Client-side Runge-Kutta 4 (RK4) differential equation solver and Mendelian genetics engine.
- `web/app.js` — Interactive UI state management, Punnett squares, and centered Plotly charts.
- `web/server.mjs` — Lightweight local HTTP server.
- `GT.py` — Authoritative SciPy differential equation solver (`solve_ivp` RK45) and stability conditions.
- `benchmark_data.json` — Precomputed numerical datasets verified against the original publication.
