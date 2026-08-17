# Sutton & Barto, Chapter 2 — Multi-armed Bandits

One notebook per section, in reading order. Each one is self-contained: LaTeX statements
of the section's formulas, a derivation where the book gives one, "predict first" prompts
before every experiment, and collapsible answers you open after you have committed to a
guess.

| Notebook | Section | Core idea | Book figure / exercise |
|---|---|---|---|
| `01_sec2.1_k_armed_bandit_problem.ipynb` | 2.1 | $q_*(a)$, explore vs. exploit, regret | Ex. 2.1 |
| `02_sec2.2_action_value_methods.ipynb` | 2.2 | sample averages, $\varepsilon$-greedy, maximisation bias | Ex. 2.2 |
| `03_sec2.3_the_10_armed_testbed.ipynb` | 2.3 | the benchmark; horizon-dependence of $\varepsilon$ | **Fig. 2.2**, Ex. 2.3 |
| `04_sec2.4_incremental_implementation.ipynb` | 2.4 | $Q_{n+1} = Q_n + \frac1n[R_n - Q_n]$, step-size weights | — |
| `05_sec2.5_tracking_a_nonstationary_problem.ipynb` | 2.5 | constant $\alpha$, recency weighting, tracking | Ex. 2.4, **Ex. 2.5** |
| `06_sec2.6_optimistic_initial_values.ipynb` | 2.6 | optimism as an exploration driver, and its limits | **Fig. 2.3**, Ex. 2.6 |
| `07_sec2.7_upper_confidence_bound.ipynb` | 2.7 | $Q_t(a) + c\sqrt{\ln t / N_t(a)}$ | **Fig. 2.4**, Ex. 2.8 |
| `08_sec2.8_gradient_bandit_algorithms.ipynb` | 2.8 | preferences, soft-max, baselines as variance reduction | **Fig. 2.5**, Ex. 2.7 |
| `09_sec2.9_associative_search.ipynb` | 2.9 | contextual bandits; the value of state | Ex. 2.10 |
| `10_sec2.10_summary_parameter_study.ipynb` | 2.10 | fair comparison, regret growth, Thompson sampling | **Fig. 2.6** |

`bandit_utils.py` holds the shared vectorised testbed and plotting helpers. Every
experiment simulates all runs simultaneously with numpy, so nothing here takes more than
a few seconds.

## Running

```bash
pip install numpy matplotlib jupyter ipywidgets
jupyter lab
```

Notebooks assume they are launched from this directory (they add the working directory to
`sys.path` to import `bandit_utils`).

### FAST vs. FULL

`bandit_utils` defaults to 500 runs per experiment — noisier curves, near-instant cells.
For the book-faithful 2000 runs, set the environment variable **before** launching:

```bash
RL_MODE=FULL jupyter lab
```

or in the first cell of a notebook, before the import:

```python
import os; os.environ["RL_MODE"] = "FULL"
```

The qualitative shape of every plot is identical in both modes; FULL just smooths them.

## How to use these

The predict-then-reveal cells are the point. Reading the answer before guessing costs you
most of the value — the surprise is what makes the concept stick. Concretely:

1. Read the markdown, including the derivation.
2. At a **Predict first** cell, commit to an answer. Say it out loud or type it in.
3. Run the experiment.
4. *Then* open the Reveal block and see whether your model of the algorithm was right.

The interactive sliders are for after you finish a section — go back and break things.
The most instructive settings are the extreme ones.

## The five ideas that outlive this chapter

1. **NewEstimate ← OldEstimate + StepSize [Target − OldEstimate]** — every learning rule
   in the book is this with a different target.
2. **Step size is memory length.** $1/n$ remembers everything; constant $\alpha$ has an
   effective window of $1/\alpha$. Nonstationary targets need the latter.
3. **Optimism in the face of uncertainty** — explore where you are uncertain, not at random.
4. **Baselines cut variance for free**, because $\sum_a \partial\pi(a)/\partial H = 0$.
   This becomes the advantage function and the critic in Chapter 13.
5. **Exploration must be sustained.** Any mechanism tied to $t = 0$ dies exactly when the
   world starts changing.
