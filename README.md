# HumanvsMachine

A lightweight repository for reproducing figures and tables used in the paper Human vs. machine -- 1:3. Joint analysis of classical and ML-based summary statistics of the Lyman-α forest (https://arxiv.org/abs/2508.03264).

## Project Overview

This project contains code to load posterior chain data, generate publication-style plots, and compute summary tables for model comparison.

- `figures/fig02.py` — generate `Figure2.png`
- `figures/fig03.py` — generate `Figure3.png`
- `figures/fig04.py` — generate `Figure4.png`
- `figures/tables.py` — compute FoM/RCI tables and print summary output
- `src/hVsFigures/plotting.py` — reusable plotting utilities
- `src/hVsFigures/config.py` — central data and output paths plus plotting settings

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Optionally install the package for editable imports:

```bash
python3 -m pip install -e .
```

## Data

The scripts expect data under the repository `data/` directory.

- `data/ind_chains_Nspectra=500.pkl`
- `data/joint_chains_Nspectra=500/*.parquet`

If these files are missing, place them in the `data/` folder before running the scripts.

## Usage

Generate each figure with:

```bash
python3 figures/fig02.py
python3 figures/fig03.py
python3 figures/fig04.py
```

Generate tables and print results with:

```bash
python3 figures/tables.py
```

Generated figures are saved to the `outputs/` directory.

## Project Structure

- `figures/` — runnable scripts that produce figure and table outputs
- `src/hVsFigures/` — reusable plotting and configuration modules
- `data/` — input datasets for posterior chain analysis
- `outputs/` — generated figure files

## Notes

- Plotting uses `chainconsumer` and matplotlib.
- Figure scripts load pickled chains and additional joint chain data from parquet files.
- `tables.py` computes figure-of-merit ratios and relative contribution indices.
