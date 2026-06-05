# Task Offloading in Fog Environments

A research framework for **learning and benchmarking task-offloading policies** in fog/edge
computing. It simulates the execution of streams of tasks across a network of edge nodes with
a SimPy-based discrete-event engine, and trains a range of policies — deep Q-learning,
genetic algorithms, PPO, and classic heuristics — to optimise the multi-objective trade-off
between **success rate**, **latency**, and **energy**.

The framework is built on top of the
[RayCloudSim](https://github.com/ZhangRui111/RayCloudSim) simulation environment.

---

## Requirements & Installation

Requires **Python ≥ 3.8** (developed and tested on 3.12).

```bash
conda create --name fog python=3.12
conda activate fog
pip install -r requirements.txt
```

Main dependencies: `networkx`, `simpy`, `numpy`, `pandas`, `torch`, `matplotlib`, `seaborn`,
`plotly`, `optuna` (+ `optuna-dashboard`), `scipy`, `tqdm`, `PyYAML`. See
[`requirements.txt`](requirements.txt) for the full list.

---

## Quick start

Everything runs through [`main.py`](main.py), which is driven by a single YAML config file:

```bash
python main.py configs/Pakistan/Tuple100K/DQL/NATE.yaml
```

A config selects the policy, the dataset/scenario, and all training/evaluation
hyperparameters. Training runs through epochs (or generations, for GA) with validation-based
early stopping, then evaluates on the held-out test set. Logs, metrics (CSV), checkpoints, and
plots are written under `logs/<dataset>/<flag>/<policy>/<timestamp>/`.

---

## Policies

Policies are registered in [`policies/__init__.py`](policies/__init__.py) and selected via the
`policy:` field in the config. Available policies:

| Key | Family | Description |
|-----|--------|-------------|
| `Random` | Heuristic | Offload to a uniformly random node. |
| `Greedy` | Heuristic | Offload to the node with the most available resources. |
| `RoundRobin` | Heuristic | Offload to nodes in round-robin order. |
| `MLP` / `T-MLP` | DQL | Deep Q-learning with an MLP Q-network (`T-` = task-aware input). |
| `NATE` / `T-NATE` | DQL | Node- And Task-aware Transformer Encoder (`T-` = task-aware). |
| `CT-NATE` | DQL | Conditional (task-modulated) NATE variant. |
| `NPGA` | GA | Niched Pareto Genetic Algorithm. |
| `NSGA2` | GA | Non-dominated Sorting Genetic Algorithm II (NSGA-II). |

The neural architectures live in [`policies/model/`](policies/model); the training logic for
each family is in `utils/dql.py` (DQL) and `utils/GA.py` (GA).

---

## Datasets & configs

Configs are organised as `configs/<dataset>/<flag>/<family>/<policy>.yaml`. The bundled
datasets (under [`eval/benchmarks/`](eval/benchmarks)) are:

- **Pakistan** — flags `Tuple30K`, `Tuple50K`, `Tuple100K`
- **Synthetic** — flags `50N100T150D`, `100N100T180D`
- **Topo4MEC**

Each config sets the `policy`, the `env` (dataset/flag/refresh rate), the `eval.lambda`
multi-objective weights, and the `training`/`model` hyperparameters. See any file under
`configs/` for a complete example.

---

## Advanced usage

### Hyperparameter search

Search over any config field with `--search "section.key=v1,v2,..."`:

```bash
python main.py configs/Pakistan/Tuple100K/DQL/T-NATE.yaml \
    --search "training.lr=1e-4,5e-5,2e-5" "training.batch_size=16,32,64" \
    --sampler qmc --n_samples 32 --num_workers 4 --device cuda
```

- `--sampler {grid,random,qmc}` — search strategy (`grid` = all combinations, `random` =
  uniform, `qmc` = Sobol low-discrepancy). Default: `random`.
- `--n_samples N` — number of trials (ignored for `grid`).
- `--num_workers N` — parallel worker processes (GPUs assigned round-robin).

Searches are resumable and backed by Optuna. See
[`docs/hparam_search.md`](docs/hparam_search.md) for the design.

> **Reproducing the paper.** [`docs/REPRODUCE.md`](docs/REPRODUCE.md) maps every
> table and figure to its config and command, including the scenario → config
> mapping (Pakistan 8N/20N, Synthetic 50N).

### Multi-seed evaluation

Report aggregate mean ± std over several seeds (resumable — completed seeds are skipped):

```bash
python main.py configs/Pakistan/Tuple100K/DQL/NATE.yaml --seeds 42 123 456
python main.py configs/Pakistan/Tuple100K/DQL/NATE.yaml --n_seeds 8   # shortcut for seeds 0..7
```

### Plotting from existing results

```bash
python main.py configs/.../some.yaml --plot lambda   # ternary plots from a lambda search
```

Standalone plotting/benchmarking scripts also live in [`utils/`](utils) (run from the repo
root), e.g. `python utils/benchmark_inference.py <config.yaml>` to benchmark `policy.act()`
inference speed.

---

## Project structure

```
core/            Discrete-event simulator: tasks, environment, infrastructure, logging
  vis/           Post-simulation visualisation
policies/        Offloading policies
  heuristics/    Random, Greedy, RoundRobin
  dql/           Deep Q-learning policies (MLP, NATE, CT-NATE)
  ga/            Genetic-algorithm policies (NSGA-II, NPGA)
  model/         Neural network architectures
eval/            Benchmark datasets and metrics
configs/         YAML run configs, grouped by dataset / flag / family
utils/           Training loops, hyperparameter search, plotting & benchmarking scripts
docs/            Additional documentation
main.py          Single entry point for training / search / evaluation
```

---

## License

Released under the [MIT License](LICENSE).

## Citation & credits

This framework is based on [RayCloudSim](https://github.com/ZhangRui111/RayCloudSim) — refer to
the original repository for details on the simulation environment.

Developed and maintained by **Arthur Garon** as part of his research project. Questions and
contributions are welcome — please open an issue or pull request.
