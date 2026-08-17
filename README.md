# Reinforcement Learning: An Introduction — study notes

Working through Sutton & Barto's *Reinforcement Learning: An Introduction* (2nd edition),
one chapter at a time. For each chapter I build a set of notebooks that reproduce the
figures, derive the formulas, and poke at the algorithms until the ideas stick — plus a
quiz to check whether they actually did.

This is a personal study repo, made public in case it's useful to someone working through
the same book. It is not a library, and nothing here is meant to be imported into real
projects.

## What's here

**Chapter 2 — Multi-armed Bandits.** Ten notebooks, one per section, in reading order.

| Notebook | Section | Topic |
|---|---|---|
| [`01_k_armed_bandit_problem`](Chpt2/01_k_armed_bandit_problem.ipynb) | 2.1 | `q*(a)`, explore vs. exploit, regret |
| [`02_action_value_methods`](Chpt2/02_action_value_methods.ipynb) | 2.2 | sample averages, ε-greedy, maximisation bias |
| [`03_the_10_armed_testbed`](Chpt2/03_the_10_armed_testbed.ipynb) | 2.3 | the benchmark; why the best ε depends on your horizon |
| [`04_incremental_implementation`](Chpt2/04_incremental_implementation.ipynb) | 2.4 | the update rule that runs through the whole book |
| [`05_tracking_a_nonstationary_problem`](Chpt2/05_tracking_a_nonstationary_problem.ipynb) | 2.5 | constant α, recency weighting, tracking a moving target |
| [`06_optimistic_initial_values`](Chpt2/06_optimistic_initial_values.ipynb) | 2.6 | optimism as an exploration driver, and where it breaks |
| [`07_upper_confidence_bound`](Chpt2/07_upper_confidence_bound.ipynb) | 2.7 | UCB, and why the step-11 spike is there |
| [`08_gradient_bandit_algorithms`](Chpt2/08_gradient_bandit_algorithms.ipynb) | 2.8 | preferences, soft-max, baselines as variance reduction |
| [`09_associative_search`](Chpt2/09_associative_search.ipynb) | 2.9 | contextual bandits; what state buys you |
| [`10_summary_parameter_study`](Chpt2/10_summary_parameter_study.ipynb) | 2.10 | fair comparison, regret growth, Thompson sampling |

`Chpt2/bandit_utils.py` holds the shared testbed. Everything is vectorised over runs, so a
full 2000-problem sweep takes a second or two rather than a minute.

**A quiz.** [`Chpt2/chapter2_quiz.html`](Chpt2/chapter2_quiz.html) — 56 multiple-choice
questions covering every section, medium to hard. Open it in a browser; no server needed.
Questions and answer options reshuffle on every reload, so the position of the correct
answer tells you nothing. Pick an option and you get the explanation immediately, right or
wrong, plus a note on why the specific distractor you chose was wrong.

## Running it

```bash
git clone https://github.com/RohitR311/RLAnIntro.git
cd RLAnIntro
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
jupyter lab
```

Launch Jupyter from inside `Chpt2/` (or start it at the repo root and open the folder) —
the notebooks add their working directory to `sys.path` to import `bandit_utils`.

By default the testbed runs 500 problems per experiment: slightly noisy curves, near-instant
cells. For the book-faithful 2000 runs, set the environment variable before launching:

```bash
RL_MODE=FULL jupyter lab
```

Every plot has the same shape either way; FULL just smooths them out.

## How these are meant to be used

Each experiment is preceded by a **Predict first** cell asking what you think will happen.
Committing to a guess before running the cell is the whole point — the explanation below
lands differently when you've just been wrong about something. Reading straight through
works, but you'll get much less out of it.

The interactive sliders are for afterwards. Go back and break things; the extreme settings
are the instructive ones.

## On AI use

I used Claude (Anthropic) to generate the notebooks and the quiz. Being specific about
that, since "AI-assisted" can mean anything:

- The **structure, code, prose, and explanations** in the notebooks are AI-generated, from
  my prompts, over several rounds of back-and-forth.
- The **quiz questions, answers, and explanations** are likewise AI-generated.
- The **numerical claims were checked by running them**, not taken on trust. Every notebook
  executes end-to-end without errors, and empirical assertions ("greedy plateaus around
  35%", "the parameter study ranks UCB first") were verified against actual simulation
  output.

That verification step caught real errors, which is the part worth knowing about. A
fact-checking pass over the quiz found five, one of which was also present in the Section
2.5 notebook: I'd claimed the sample-average method's performance *declines* over time on
the nonstationary testbed. It doesn't — running it to 40,000 steps, it rises and then
plateaus near 45% while constant-α keeps climbing past 80%. The stated mechanism was right
and the predicted symptom was wrong. Both have been corrected, and the notebook now flags
"declines" explicitly as the tempting wrong answer.

I mention this not as a disclaimer but as the actual lesson: **plausible-sounding
explanations of simulation results are exactly where this stuff goes wrong**, and the only
defence is running the simulation. If you spot something here that looks off, it may well
be. Open an issue.

The mathematical content — definitions, derivations, exercise answers — tracks the book
closely and I've checked it against the text. The empirical numbers come from this repo's
own code, so you can re-run anything you doubt.

## Attribution

All concepts, notation, figure designs, and exercises are from:

> Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.).
> MIT Press.

The authors make the book [freely available](http://incompleteideas.net/book/the-book.html).
Buy a copy if it's useful to you. Nothing in this repo substitutes for reading it — these
notebooks assume you've read the corresponding section and want to see it move.

The code here is mine (and Claude's) to do with as you like. The ideas are Sutton and
Barto's.

## Status

Chapter 2 done. Chapter 3 next, though value functions and Bellman backups don't lend
themselves to visualisation nearly as naturally as bandit curves do, so it may look
different.
