"""
Shared utilities for the Sutton & Barto Chapter 2 notebooks.

Everything here is vectorised over runs: an "experiment" simulates `runs`
independent bandit problems simultaneously, so a full 2000-run / 1000-step
sweep takes about a second.

Set the environment variable RL_MODE=FULL (or pass runs= explicitly) to use
book-faithful settings. Default is FAST.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

FAST = dict(runs=500, steps=1000)
FULL = dict(runs=2000, steps=1000)

MODE = os.environ.get("RL_MODE", "FAST").upper()
CONFIG = FULL if MODE == "FULL" else FAST

RUNS = CONFIG["runs"]
STEPS = CONFIG["steps"]


def banner():
    print(f"mode={MODE}  runs={RUNS}  steps={STEPS}")
    print("switch with:  import os; os.environ['RL_MODE']='FULL'  (before importing)")


class Testbed:
    """The 10-armed testbed of Section 2.3.

    q_star[r, a] ~ N(0, 1) drawn once per run.
    Reward for pulling arm a on run r ~ N(q_star[r, a], 1).

    If drift_sigma > 0 the true values take an independent random walk each
    step (the nonstationary variant used in Exercise 2.5).
    """

    def __init__(self, k=10, runs=None, seed=0, mean_shift=0.0, drift_sigma=0.0,
                 reward_sigma=1.0, equal_start=False):
        self.k = k
        self.runs = RUNS if runs is None else runs
        self.rng = np.random.default_rng(seed)
        self.drift_sigma = drift_sigma
        self.reward_sigma = reward_sigma
        if equal_start:
            self.q_star = np.zeros((self.runs, k)) + mean_shift
        else:
            self.q_star = self.rng.normal(mean_shift, 1.0, size=(self.runs, k))

    def optimal(self):
        return self.q_star.argmax(axis=1)

    def step(self, actions):
        """actions: (runs,) integer array. Returns (runs,) rewards."""
        idx = np.arange(self.runs)
        true_q = self.q_star[idx, actions]
        rewards = self.rng.normal(true_q, self.reward_sigma)
        if self.drift_sigma > 0:
            self.q_star += self.rng.normal(0.0, self.drift_sigma,
                                           size=self.q_star.shape)
        return rewards


def argmax_random_tiebreak(Q, rng):
    """Row-wise argmax with ties broken uniformly at random.

    Matters more than people expect: with optimistic initial values every arm
    is tied at step 0, and a deterministic argmax would always pick arm 0.
    """
    noise = rng.random(Q.shape)
    best = Q.max(axis=1, keepdims=True)
    masked = np.where(Q == best, noise, -np.inf)
    return masked.argmax(axis=1)


def run_bandit(agent_fn, testbed_kwargs=None, steps=None, runs=None, seed=0):
    """Generic driver.

    agent_fn(k, runs, rng) must return an object with:
        .act()               -> (runs,) actions
        .update(a, r)        -> None
    Returns dict with 'rewards' (steps,) and 'optimal' (steps,) averages.
    """
    steps = STEPS if steps is None else steps
    runs = RUNS if runs is None else runs
    tb = Testbed(runs=runs, seed=seed, **(testbed_kwargs or {}))
    rng = np.random.default_rng(seed + 12345)
    agent = agent_fn(tb.k, runs, rng)

    avg_reward = np.zeros(steps)
    pct_optimal = np.zeros(steps)

    for t in range(steps):
        best = tb.optimal()
        a = agent.act()
        r = tb.step(a)
        agent.update(a, r)
        avg_reward[t] = r.mean()
        pct_optimal[t] = (a == best).mean()

    return {"rewards": avg_reward, "optimal": pct_optimal * 100.0}


def plot_pair(results, labels=None, title=None, figsize=(12, 4.2)):
    """results: list of dicts from run_bandit. Draws reward + %optimal panels."""
    labels = labels or [f"run {i}" for i in range(len(results))]
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    for res, lab in zip(results, labels):
        axes[0].plot(res["rewards"], label=lab, lw=1.2)
        axes[1].plot(res["optimal"], label=lab, lw=1.2)
    axes[0].set_xlabel("Steps")
    axes[0].set_ylabel("Average reward")
    axes[1].set_xlabel("Steps")
    axes[1].set_ylabel("% Optimal action")
    axes[1].set_ylim(0, 100)
    for ax in axes:
        ax.legend(loc="lower right", fontsize=9)
        ax.grid(alpha=0.3)
    if title:
        fig.suptitle(title)
    fig.tight_layout()
    return fig, axes


REVEAL_STYLE = (
    "background-color: #fff3cd;"
    "color: #664d03;"
    "padding: 15px 18px;"
    "border-radius: 8px;"
    "border: 1px solid #ffecb5;"
)

SUMMARY_STYLE = (
    "cursor: pointer;"
    "font-weight: 600;"
    "color: #664d03;"
    "background-color: #fff3cd;"
    "padding: 8px 14px;"
    "border-radius: 8px;"
    "border: 1px solid #ffecb5;"
    "display: inline-block;"
    "margin-bottom: 6px;"
    "list-style: none;"
)


def hide(text):
    """Collapsible answer block for the predict-then-reveal cells.

    Kept collapsed on purpose: the value of these notebooks is in committing to a
    prediction before reading the answer. To show answers inline instead, drop the
    <details>/<summary> wrapper below and keep only the styled div.
    """
    from IPython.display import display, HTML
    display(HTML(
        f"<details style='margin:6px 0'>"
        f"<summary style='{SUMMARY_STYLE}'>Reveal</summary>"
        f"<div style='{REVEAL_STYLE}'>{text}</div>"
        f"</details>"))
