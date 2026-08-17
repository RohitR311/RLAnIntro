# Reinforcement Learning: An Introduction — study notes

Working through Sutton & Barto's *Reinforcement Learning: An Introduction* (2nd edition),
one chapter at a time. For each chapter I build a set of notebooks that reproduce the
figures, derive the formulas, and poke at the algorithms until the ideas stick — plus a
quiz to check whether they actually did.

This is a personal study repo, made public in case it's useful to someone working through
the same book. It is not a library, and nothing here is meant to be imported into real
projects.

## Chapters

| Chapter | Topic | Contents | Status |
|---|---|---|---|
| [2](Chpt2/) | Multi-armed Bandits | 10 notebooks, 56-question quiz | Done |
| 3 | Finite Markov Decision Processes | — | Next |

Each chapter folder has its own README with a per-notebook breakdown. Start there rather
than here once you've picked a chapter.

### Chapter 2 — Multi-armed Bandits

One notebook per section (2.1 through 2.10), covering ε-greedy, incremental updates,
tracking nonstationary problems, optimistic initialisation, UCB, gradient bandits,
contextual bandits, and a parameter study comparing all of them fairly. Book exercises
2.1–2.8 and 2.10 are worked through in code. Ends with Thompson sampling as a
"where next" exercise.

→ [`Chpt2/README.md`](Chpt2/README.md)

## How a chapter folder is laid out

Every chapter follows the same shape, so once you've found your way around one you've
found your way around all of them:

```
ChptN/
  README.md                  index for the chapter, with a per-notebook table
  01_*.ipynb .. NN_*.ipynb   one notebook per section, in reading order
  *_utils.py                 shared simulation code for that chapter
  chapterN_quiz.html         self-test, opens in a browser
```

Notebooks import their chapter's utils module from the working directory, so launch
Jupyter from inside the chapter folder (or open the folder from a root-level Jupyter).
Chapters are self-contained — there's no cross-chapter package to install.

## Running it

```bash
git clone https://github.com/RohitR311/RLAnIntro.git
cd RLAnIntro
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
jupyter lab
```

`requirements.txt` at the root covers every chapter. If a later chapter needs something
extra, it gets added there.

## Conventions

A few things hold across all chapters:

**Predict first.** Each experiment is preceded by a cell asking what you think will
happen. Committing to a guess before running the code is the point — the explanation
below lands differently when you've just been wrong about something. Reading straight
through works, but you'll get much less out of it. Answers sit in collapsed blocks you
open afterwards.

**Fast by default.** Simulations run a reduced number of trials so cells return almost
immediately. Set `RL_MODE=FULL` before launching Jupyter for the book-faithful counts:

```bash
RL_MODE=FULL jupyter lab
```

Plots have the same shape either way; FULL just smooths them out.

**Sliders are for afterwards.** Once you've finished a section, go back and break things.
The extreme parameter settings are the instructive ones.

**Quizzes reshuffle.** Questions and answer options are randomised on every page load, so
the position of the correct answer tells you nothing and a second attempt is a real
retest. Selecting an option reveals the explanation immediately, right or wrong, plus a
note on why the specific distractor you chose was wrong.

## On AI use

I use Claude (Anthropic) to generate the notebooks and quizzes. Being specific about that,
since "AI-assisted" can mean anything:

- The **structure, code, prose, and explanations** are AI-generated, from my prompts, over
  several rounds of back-and-forth.
- The **quiz questions, answers, and explanations** are likewise AI-generated.
- The **numerical claims are checked by running them**, not taken on trust. Every notebook
  executes end-to-end without errors, and empirical assertions are verified against actual
  simulation output before they go in.

That verification step is the part worth knowing about, because it catches real errors. In
Chapter 2 a fact-checking pass over the quiz found five, one of which was also present in
the Section 2.5 notebook: I'd claimed the sample-average method's performance *declines*
over time on the nonstationary testbed. It doesn't — running it to 40,000 steps, it rises
and then plateaus near 45% while constant-α keeps climbing past 80%. The stated mechanism
was right and the predicted symptom was wrong. Both were corrected, and the notebook now
flags "declines" explicitly as the tempting wrong answer.

I mention this not as a disclaimer but as the actual lesson: **plausible-sounding
explanations of simulation results are exactly where this stuff goes wrong**, and the only
defence is running the simulation. If you spot something here that looks off, it may well
be. Open an issue.

The mathematical content — definitions, derivations, exercise answers — tracks the book
closely and I check it against the text. The empirical numbers come from this repo's own
code, so you can re-run anything you doubt.

## Attribution

All concepts, notation, figure designs, and exercises are from:

> Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.).
> MIT Press.

The authors make the book [freely available](http://incompleteideas.net/book/the-book.html).
Buy a copy if it's useful to you. Nothing in this repo substitutes for reading it — these
notebooks assume you've read the corresponding section and want to see it move.

The code here is mine (and Claude's) to do with as you like. The ideas are Sutton and
Barto's.
