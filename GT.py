
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp


# ============================================================
# PAPER REPRODUCTION
#
# Matrix Games Between Full Siblings in Mendelian Populations
# Garay et al. (2025)
# PLOS ONE, 20(9), e0331044
# DOI: 10.1371/journal.pone.0331044
#
# Reproduction of the single-locus, two-allele model.
# ============================================================


# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

GENOTYPES = ["aa", "aA", "AA"]

# Published donation-game payoff matrix A3
PAYOFF_MATRIX = np.array([
    [0.7, 0.1],
    [0.8, 0.2]
], dtype=float)

# Initial genotype frequencies
INITIAL_STATE = np.array([0.33, 0.34, 0.33])

# Population and offspring scaling parameters
N = 1.0
n = 1.0

# Simulation settings
TIME_START = 0.0
TIME_END = 100.0
TIME_POINTS = 1000

# Numerical tolerance for equality conditions
TOL = 1e-9


# ============================================================
# 2. MENDELIAN GAMETE PROBABILITIES
# ============================================================

GAMETES = {
    "aa": {"a": 1.0, "A": 0.0},
    "aA": {"a": 0.5, "A": 0.5},
    "AA": {"a": 0.0, "A": 1.0}
}


def offspring_probabilities(parent1, parent2):
    """
    Mendelian offspring probabilities.

    Returns:
        [P(aa), P(aA), P(AA)]
    """

    probabilities = np.zeros(3)

    for allele1, p1 in GAMETES[parent1].items():

        for allele2, p2 in GAMETES[parent2].items():

            probability = p1 * p2

            number_of_A = (
                int(allele1 == "A")
                + int(allele2 == "A")
            )

            probabilities[number_of_A] += probability

    return probabilities


def create_mating_table():

    table = {}

    for parent1 in GENOTYPES:

        for parent2 in GENOTYPES:

            table[(parent1, parent2)] = (
                offspring_probabilities(parent1, parent2)
            )

    return table


MATINGS = create_mating_table()


# ============================================================
# 3. GENOTYPE-PHENOTYPE MAPPING
# ============================================================

def phenotype_strategies(mode):
    """
    Strategy 1 = Cooperation
    Strategy 2 = Defection

    Genotype order:
        aa, aA, AA
    """

    if mode == "recessive":

        # Cooperator phenotype is recessive
        return np.array([
            [1.0, 0.0],
            [0.0, 1.0],
            [0.0, 1.0]
        ])

    elif mode == "dominant":

        # Cooperator phenotype is dominant
        return np.array([
            [1.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0]
        ])

    elif mode == "intermediate":

        # Heterozygote uses mixed strategy
        return np.array([
            [1.0, 0.0],
            [0.5, 0.5],
            [0.0, 1.0]
        ])

    else:

        raise ValueError(
            "Mode must be recessive, dominant or intermediate."
        )


# ============================================================
# 4. GENOTYPE SURVIVAL TABLE
# ============================================================

def family_survival(
    parent1,
    parent2,
    mode,
    payoff_matrix
):
    """
    Expected number of surviving offspring per family.

    n_k(ij) = n * p_k(ij) *
              sum_l[p_l(ij) * s_k.T @ A @ s_l]

    This implements the general genotype-survival
    expression from the paper's Table 1.
    """

    probabilities = MATINGS[(parent1, parent2)]

    strategies = phenotype_strategies(mode)

    surviving = np.zeros(3)

    for k in range(3):

        expected_survival = 0.0

        for sibling in range(3):

            payoff = (
                strategies[k]
                @ payoff_matrix
                @ strategies[sibling]
            )

            expected_survival += (
                probabilities[sibling] * payoff
            )

        surviving[k] = (
            n
            * probabilities[k]
            * expected_survival
        )

    return surviving


def create_survival_table(mode):

    rows = []

    for parent1 in GENOTYPES:

        for parent2 in GENOTYPES:

            surviving = family_survival(
                parent1,
                parent2,
                mode,
                PAYOFF_MATRIX
            )

            rows.append({
                "Parents": f"{parent1} x {parent2}",
                "Surviving aa": surviving[0],
                "Surviving aA": surviving[1],
                "Surviving AA": surviving[2]
            })

    return pd.DataFrame(rows)


# ============================================================
# 5. GENOTYPE PRODUCTION RATES
# ============================================================

def production_rates(x, mode, payoff_matrix):

    V = np.zeros(3)

    for i, parent1 in enumerate(GENOTYPES):

        for j, parent2 in enumerate(GENOTYPES):

            # Panmictic mating
            mating_frequency = x[i] * x[j]

            surviving = family_survival(
                parent1,
                parent2,
                mode,
                payoff_matrix
            )

            V += (
                (N / 2.0)
                * mating_frequency
                * surviving
            )

    return V


# ============================================================
# 6. PAPER EQUATION (1): GENOTYPE DYNAMICS
# ============================================================

def genotype_dynamics(
    time,
    x,
    mode,
    payoff_matrix
):

    V = production_rates(
        x,
        mode,
        payoff_matrix
    )

    total_production = np.sum(V)

    # dx_i/dt = V_i(x) - x_i * sum(V_j(x))
    dx = V - x * total_production

    return dx


# ============================================================
# 7. STABILITY CONDITIONS
#    Based on published Tables 2 and 3
# ============================================================

def stability_conditions(payoff):

    a11, a12 = payoff[0]
    a21, a22 = payoff[1]

    def greater(a, b):
        return a > b + TOL

    def less(a, b):
        return a < b - TOL

    def equal(a, b):
        return abs(a - b) <= TOL

    # Common threshold expressions
    threshold_G1 = (
        a12 + 3 * a21 + a22
    ) / 5.0

    threshold_G3 = (
        a11 + 3 * a12 + a21
    ) / 5.0

    results = {}

    # --------------------------------------------------------
    # RECESSIVE INHERITANCE
    # --------------------------------------------------------

    recessive_G1 = (
        greater(2 * a11, a21 + a22)
        or (
            equal(2 * a11, a21 + a22)
            and (
                (
                    a11 >= 2 * a22
                    and greater(
                        a11 + 4 * a12,
                        3 * a22
                    )
                )
                or (
                    a11 < 2 * a22
                    and 7 * a11 <= 2 * a12
                )
            )
        )
    )

    recessive_G3 = greater(a22, threshold_G3)

    results["Recessive"] = {
        "G1_ESGD": recessive_G1,
        "G3_ESGD": recessive_G3,

        "G1_Repellor": less(
            2 * a11,
            a21 + a22
        ),

        "G1_Suspected_Repellor": (
            equal(2 * a11, a21 + a22)
            and less(
                a11 + 4 * a12,
                3 * a22
            )
        ),

        "G3_Suspected_Repellor": less(
            a22,
            threshold_G3
        )
    }

    # --------------------------------------------------------
    # DOMINANT INHERITANCE
    # --------------------------------------------------------

    dominant_G1 = greater(
        a11,
        threshold_G1
    )

    dominant_G3 = (
        greater(2 * a22, a11 + a12)
        or (
            equal(2 * a22, a11 + a12)
            and (
                (
                    a22 >= 2 * a11
                    and greater(
                        a22 + 4 * a21,
                        3 * a11
                    )
                )
                or (
                    a22 < 2 * a11
                    and 7 * a22 <= 2 * a21
                )
            )
        )
    )

    results["Dominant"] = {
        "G1_ESGD": dominant_G1,
        "G3_ESGD": dominant_G3,

        "G1_Suspected_Repellor": less(
            a11,
            threshold_G1
        ),

        "G3_Repellor": less(
            2 * a22,
            a11 + a12
        ),

        "G3_Suspected_Repellor": (
            equal(2 * a22, a11 + a12)
            and less(
                a22 + 4 * a21,
                3 * a11
            )
        )
    }

    # --------------------------------------------------------
    # INTERMEDIATE INHERITANCE
    # --------------------------------------------------------

    intermediate_G1 = (
        greater(a11, threshold_G1)
        or (
            equal(a11, threshold_G1)
            and 2 * a12 >= a21 + 3 * a22
        )
    )

    intermediate_G3 = (
        greater(a22, threshold_G3)
        or (
            equal(a22, threshold_G3)
            and 2 * a21 >= 3 * a11 + a12
        )
    )

    results["Intermediate"] = {
        "G1_ESGD": intermediate_G1,
        "G3_ESGD": intermediate_G3,

        "G1_Repellor": less(
            a11,
            threshold_G1
        ),

        "G1_Suspected_Repellor": (
            equal(a11, threshold_G1)
            and 3 * a12 + a21 <= 2 * a22
        ),

        "G3_Repellor": less(
            a22,
            threshold_G3
        ),

        "G3_Suspected_Repellor": (
            equal(a22, threshold_G3)
            and a12 + 3 * a21 <= 2 * a11
        )
    }

    return results


# ============================================================
# 8. NUMERICAL SIMULATION
# ============================================================

def simulate(
    mode,
    initial_state=INITIAL_STATE,
    payoff_matrix=PAYOFF_MATRIX
):

    x0 = np.asarray(initial_state, dtype=float)

    if x0.shape != (3,):
        raise ValueError("Three genotype frequencies are required.")

    if np.any(x0 < 0):
        raise ValueError("Frequencies cannot be negative.")

    if not np.isclose(np.sum(x0), 1.0):
        raise ValueError("Initial frequencies must sum to 1.")

    if payoff_matrix.shape != (2, 2):
        raise ValueError("Payoff matrix must be 2x2.")

    if np.any(payoff_matrix <= 0) or np.any(payoff_matrix > 1):
        raise ValueError("Payoffs must be in the interval (0, 1].")

    times = np.linspace(
        TIME_START,
        TIME_END,
        TIME_POINTS
    )

    result = solve_ivp(
        genotype_dynamics,
        (TIME_START, TIME_END),
        x0,
        t_eval=times,
        args=(mode, payoff_matrix),
        method="RK45",
        rtol=1e-9,
        atol=1e-11
    )

    if not result.success:
        raise RuntimeError(result.message)

    frequencies = result.y.T

    # Numerical validation
    if np.min(frequencies) < -1e-7:
        raise RuntimeError("Invalid negative genotype frequency.")

    if not np.allclose(
        frequencies.sum(axis=1),
        1.0,
        atol=1e-6
    ):
        raise RuntimeError("Genotype frequencies do not sum to one.")

    return result.t, frequencies


# ============================================================
# 9. PLOT GENOTYPE FREQUENCIES
# ============================================================

def plot_simulation(time, frequencies, mode):

    plt.figure(figsize=(10, 6))

    for i, genotype in enumerate(GENOTYPES):

        plt.plot(
            time,
            frequencies[:, i],
            linewidth=2,
            label=genotype
        )

    plt.xlabel("Time")
    plt.ylabel("Genotype Frequency")

    plt.title(
        f"Genotype Dynamics - {mode.title()} Inheritance"
    )

    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        f"{mode}_dynamics.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 10. COMPARE INHERITANCE MODES
# ============================================================

def compare_modes():

    modes = [
        "recessive",
        "dominant",
        "intermediate"
    ]

    results = {}

    fig, axes = plt.subplots(
        1, 3,
        figsize=(17, 5),
        sharey=True
    )

    for ax, mode in zip(axes, modes):

        time, frequencies = simulate(mode)

        results[mode] = frequencies

        for i, genotype in enumerate(GENOTYPES):

            ax.plot(
                time,
                frequencies[:, i],
                label=genotype,
                linewidth=2
            )

        ax.set_title(mode.title())
        ax.set_xlabel("Time")
        ax.set_ylim(0, 1)
        ax.grid(alpha=0.3)
        ax.legend()

    axes[0].set_ylabel("Genotype Frequency")

    fig.suptitle(
        "Comparison of Genotype Dynamics Across Inheritance Modes"
    )

    plt.tight_layout()
    plt.savefig(
        "inheritance_comparison.png",
        dpi=300
    )
    plt.show()

    print("\nFINAL GENOTYPE FREQUENCIES")

    for mode, frequencies in results.items():

        print(f"\n{mode.upper()}")

        for genotype, value in zip(
            GENOTYPES,
            frequencies[-1]
        ):
            print(f"{genotype}: {value:.8f}")

    return results


# ============================================================
# 11. DISPLAY ALL TABLES AND CONDITIONS
# ============================================================

def main():

    print("=" * 65)
    print("PAPER 2 - MATHEMATICAL REPRODUCTION")
    print("=" * 65)

    print("\nPAYOFF MATRIX A3:")
    print(PAYOFF_MATRIX)

    print("\nMENDELIAN MATING TABLE:")

    mating_rows = []

    for (parent1, parent2), probabilities in MATINGS.items():

        mating_rows.append({
            "Parents": f"{parent1} x {parent2}",
            "P(aa)": probabilities[0],
            "P(aA)": probabilities[1],
            "P(AA)": probabilities[2]
        })

    mating_df = pd.DataFrame(mating_rows)

    print(mating_df.to_string(index=False))

    mating_df.to_csv(
        "mendelian_mating_table.csv",
        index=False
    )

    for mode in ["recessive", "dominant", "intermediate"]:

        print("\n" + "=" * 65)
        print(f"{mode.upper()} INHERITANCE")
        print("=" * 65)

        print("\nGENOTYPE SURVIVAL TABLE:")

        survival_df = create_survival_table(mode)

        print(survival_df.to_string(index=False))

        survival_df.to_csv(
            f"{mode}_survival_table.csv",
            index=False
        )

        time, frequencies = simulate(mode)

        results_df = pd.DataFrame({
            "Time": time,
            "aa": frequencies[:, 0],
            "aA": frequencies[:, 1],
            "AA": frequencies[:, 2]
        })

        results_df.to_csv(
            f"{mode}_results.csv",
            index=False
        )

        print("\nFINAL FREQUENCIES:")
        print(results_df.tail(1).to_string(index=False))

        plot_simulation(
            time,
            frequencies,
            mode
        )

    # Published stability classifications
    print("\n" + "=" * 65)
    print("PUBLISHED STABILITY CONDITIONS - TABLES 2 AND 3")
    print("=" * 65)

    conditions = stability_conditions(PAYOFF_MATRIX)

    for mode, values in conditions.items():

        print(f"\n{mode.upper()}")

        for condition, value in values.items():

            print(
                f"{condition}: {value}"
            )

    # Compare all modes
    print("\nGENERATING COMPARISON GRAPH...")

    compare_modes()

    print("\n" + "=" * 65)
    print("PAPER REPRODUCTION MODULE COMPLETED")
    print("=" * 65)

    print("\nGenerated files:")
    print("- mendelian_mating_table.csv")
    print("- recessive_survival_table.csv")
    print("- dominant_survival_table.csv")
    print("- intermediate_survival_table.csv")
    print("- recessive_results.csv")
    print("- dominant_results.csv")
    print("- intermediate_results.csv")
    print("- recessive_dynamics.png")
    print("- dominant_dynamics.png")
    print("- intermediate_dynamics.png")
    print("- inheritance_comparison.png")


if __name__ == "__main__":
    main()
