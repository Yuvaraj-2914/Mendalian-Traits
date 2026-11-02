// =========================================================================
// MENDELIAN MATRIX GAMES ENGINE
// Garay et al. (2025) - PLOS ONE
// =========================================================================

export const GENOTYPES = ["aa", "aA", "AA"];

// Mendelian gamete output:
export const GAMETES = {
  aa: { a: 1.0, A: 0.0 },
  aA: { a: 0.5, A: 0.5 },
  AA: { a: 0.0, A: 1.0 }
};

// Calculate Mendelian offspring probabilities for any 2 parents [P(aa), P(aA), P(AA)]
export function getOffspringProbs(parent1, parent2) {
  const g1 = GAMETES[parent1];
  const g2 = GAMETES[parent2];
  const probs = [0.0, 0.0, 0.0];

  for (const [al1, p1] of Object.entries(g1)) {
    for (const [al2, p2] of Object.entries(g2)) {
      const prob = p1 * p2;
      const numA = (al1 === "A" ? 1 : 0) + (al2 === "A" ? 1 : 0);
      probs[numA] += prob;
    }
  }
  return probs;
}

// Full 9 mating combinations
export function getMatingTable() {
  const table = {};
  for (const p1 of GENOTYPES) {
    for (const p2 of GENOTYPES) {
      table[`${p1} x ${p2}`] = getOffspringProbs(p1, p2);
    }
  }
  return table;
}

export const MATINGS = getMatingTable();

// Strategy vector s_k = [prob_cooperate, prob_defect]
export function getPhenotypeStrategies(mode) {
  if (mode === "recessive") {
    // aa is Cooperator; aA and AA are Defectors
    return [
      [1.0, 0.0],
      [0.0, 1.0],
      [0.0, 1.0]
    ];
  } else if (mode === "dominant") {
    // aa and aA are Cooperators; AA is Defector
    return [
      [1.0, 0.0],
      [1.0, 0.0],
      [0.0, 1.0]
    ];
  } else if (mode === "intermediate") {
    // aa Cooperates; aA mixes (0.5, 0.5); AA Defects
    return [
      [1.0, 0.0],
      [0.5, 0.5],
      [0.0, 1.0]
    ];
  }
  throw new Error("Unknown inheritance mode: " + mode);
}

// Sibling expected payoff calculation:
// s_k^T * A * s_l
export function strategyPayoff(s_k, A, s_l) {
  // s_k is 1x2, A is 2x2, s_l is 1x2
  const r0 = s_k[0] * A[0][0] + s_k[1] * A[1][0];
  const r1 = s_k[0] * A[0][1] + s_k[1] * A[1][1];
  return r0 * s_l[0] + r1 * s_l[1];
}

// Genotype survival calculation per family (Table 1):
// n_k(ij) = n * p_k(ij) * sum_l [ p_l(ij) * (s_k^T A s_l) ]
export function familySurvival(p1, p2, mode, A, n = 1.0) {
  const probs = MATINGS[`${p1} x ${p2}`];
  const strats = getPhenotypeStrategies(mode);
  const surviving = [0.0, 0.0, 0.0];

  for (let k = 0; k < 3; k++) {
    let expectedSurvival = 0.0;
    for (let l = 0; l < 3; l++) {
      const payoff = strategyPayoff(strats[k], A, strats[l]);
      expectedSurvival += probs[l] * payoff;
    }
    surviving[k] = n * probs[k] * expectedSurvival;
  }
  return surviving;
}

// Genotype production rate V_k(x) = (N/2) * sum_i sum_j [ x_i * x_j * n_k(ij) ]
export function productionRates(x, mode, A, N = 1.0, n = 1.0) {
  const V = [0.0, 0.0, 0.0];

  for (let i = 0; i < 3; i++) {
    const p1 = GENOTYPES[i];
    for (let j = 0; j < 3; j++) {
      const p2 = GENOTYPES[j];
      const matingFreq = x[i] * x[j];
      const surv = familySurvival(p1, p2, mode, A, n);

      for (let k = 0; k < 3; k++) {
        V[k] += (N / 2.0) * matingFreq * surv[k];
      }
    }
  }
  return V;
}

// Vector field: dx_k/dt = V_k(x) - x_k * sum_j(V_j(x))
export function vectorField(x, mode, A) {
  const V = productionRates(x, mode, A);
  const totalV = V[0] + V[1] + V[2];
  return [
    V[0] - x[0] * totalV,
    V[1] - x[1] * totalV,
    V[2] - x[2] * totalV
  ];
}

// High-fidelity Runge-Kutta 4th Order (RK4) integrator with Simplex Invariant Manifold Projection
export function simulateRK4(mode, A, x0 = [0.33, 0.34, 0.33], tEnd = 100, dt = 0.05) {
  let t = 0.0;
  let state = [...x0];
  const steps = Math.floor(tEnd / dt);
  
  const time = [0.0];
  const aa = [state[0]];
  const aA = [state[1]];
  const AA = [state[2]];

  const saveInterval = Math.max(1, Math.floor(steps / 200));

  for (let s = 1; s <= steps; s++) {
    const k1 = vectorField(state, mode, A);

    const s2 = [
      state[0] + 0.5 * dt * k1[0],
      state[1] + 0.5 * dt * k1[1],
      state[2] + 0.5 * dt * k1[2]
    ];
    const k2 = vectorField(s2, mode, A);

    const s3 = [
      state[0] + 0.5 * dt * k2[0],
      state[1] + 0.5 * dt * k2[1],
      state[2] + 0.5 * dt * k2[2]
    ];
    const k3 = vectorField(s3, mode, A);

    const s4 = [
      state[0] + dt * k3[0],
      state[1] + dt * k3[1],
      state[2] + dt * k3[2]
    ];
    const k4 = vectorField(s4, mode, A);

    for (let i = 0; i < 3; i++) {
      state[i] += (dt / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
      if (state[i] < 0) state[i] = 0.0;
    }

    // Exact simplex re-normalization to guarantee sum=1
    const sum = state[0] + state[1] + state[2];
    if (sum > 0) {
      state[0] /= sum;
      state[1] /= sum;
      state[2] /= sum;
    }

    t += dt;

    if (s % saveInterval === 0 || s === steps) {
      time.push(Number(t.toFixed(2)));
      aa.push(Number(state[0].toFixed(6)));
      aA.push(Number(state[1].toFixed(6)));
      AA.push(Number(state[2].toFixed(6)));
    }
  }

  return {
    time,
    aa,
    aA,
    AA,
    finalState: { aa: state[0], aA: state[1], AA: state[2] }
  };
}

// Stability criteria directly from Garay et al. (2025) Tables 2 & 3
export function evaluateStability(A) {
  const [[a11, a12], [a21, a22]] = A;
  const TOL = 1e-9;

  const greater = (a, b) => a > b + TOL;
  const less = (a, b) => a < b - TOL;
  const equal = (a, b) => Math.abs(a - b) <= TOL;

  const threshG1 = (a12 + 3 * a21 + a22) / 5.0;
  const threshG3 = (a11 + 3 * a12 + a21) / 5.0;

  // 1. Recessive
  const recG1 = greater(2 * a11, a21 + a22) ||
    (equal(2 * a11, a21 + a22) && (
      (a11 >= 2 * a22 && greater(a11 + 4 * a12, 3 * a22)) ||
      (a11 < 2 * a22 && 7 * a11 <= 2 * a12)
    ));
  const recG3 = greater(a22, threshG3);
  const recG1Repellor = less(2 * a11, a21 + a22);
  const recG1SusRepellor = equal(2 * a11, a21 + a22) && less(a11 + 4 * a12, 3 * a22);
  const recG3SusRepellor = less(a22, threshG3);

  // 2. Dominant
  const domG1 = greater(a11, threshG1);
  const domG3 = greater(2 * a22, a11 + a12) ||
    (equal(2 * a22, a11 + a12) && (
      (a22 >= 2 * a11 && greater(a22 + 4 * a21, 3 * a11)) ||
      (a22 < 2 * a11 && 7 * a22 <= 2 * a21)
    ));
  const domG1SusRepellor = less(a11, threshG1);
  const domG3Repellor = less(2 * a22, a11 + a12);
  const domG3SusRepellor = equal(2 * a22, a11 + a12) && less(a22 + 4 * a21, 3 * a11);

  // 3. Intermediate
  const intG1 = greater(a11, threshG1) ||
    (equal(a11, threshG1) && 2 * a12 >= a21 + 3 * a22);
  const intG3 = greater(a22, threshG3) ||
    (equal(a22, threshG3) && 2 * a21 >= 3 * a11 + a12);
  const intG1Repellor = less(a11, threshG1);
  const intG1SusRepellor = equal(a11, threshG1) && (3 * a12 + a21 <= 2 * a22);
  const intG3Repellor = less(a22, threshG3);
  const intG3SusRepellor = equal(a22, threshG3) && (a12 + 3 * a21 <= 2 * a11);

  return {
    thresholds: {
      threshG1,
      threshG3
    },
    recessive: {
      G1_ESGD: recG1,
      G3_ESGD: recG3,
      G1_Repellor: recG1Repellor,
      G1_Suspected_Repellor: recG1SusRepellor,
      G3_Suspected_Repellor: recG3SusRepellor
    },
    dominant: {
      G1_ESGD: domG1,
      G3_ESGD: domG3,
      G1_Suspected_Repellor: domG1SusRepellor,
      G3_Repellor: domG3Repellor,
      G3_Suspected_Repellor: domG3SusRepellor
    },
    intermediate: {
      G1_ESGD: intG1,
      G3_ESGD: intG3,
      G1_Repellor: intG1Repellor,
      G1_Suspected_Repellor: intG1SusRepellor,
      G3_Repellor: intG3Repellor,
      G3_Suspected_Repellor: intG3SusRepellor
    }
  };
}

// Convert 3D simplex coordinate (x1, x2, x3) where sum=1 to 2D De Finetti equilateral triangle (u, v)
// Vertex G1 (aa) = (0, 0)
// Vertex G3 (AA) = (1, 0)
// Vertex G2 (aA) = (0.5, sqrt(3)/2)
export function simplexTo2D(x1, x2, x3) {
  const u = x3 + 0.5 * x2;
  const v = (Math.sqrt(3) / 2.0) * x2;
  return { u, v };
}

