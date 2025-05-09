# A Survey of Filtered Approximate Nearest Neighbor Search over Vector-Scalar Hybrid Data

This repository contains the data analysis code for the paper.

## Overview

This project provides scripts for:

- Downloading datasets, including:
  - `sift-1m`
  - `gist-1m`
  - `deep-10m`
  - `mnist-8m`
  - `mtg-40k`
  - `glove-twitter-1m`
  - `glove-crawl-2m`
  - `laion-1m`
  - `youtube-6m`
- Exploring and summarizing dataset contents
- Reproducing the experimental results presented in the survey

## Environment Setup

To set up the environment using `conda`, run:

```bash
source env.sh
````

This script will:

- Create a new conda environment named `fanns`
- Install required system dependencies (e.g., `gcc`, `cmake`)
- Install all Python packages (e.g., `umap-learn`, `faiss-cpu`)

> **Important**: After installation, manually locate the `mahalanobis` package using
> `pip show mahalanobis`, and replace all occurrences of `np.linalg.inv` with `np.linalg.pinv`
> for numerical stability.

```python
# Python code to reload after modification:
import importlib
import mahalanobis
importlib.reload(mahalanobis)
```

## Usage

### 1. Dataset Download

```bash
cd script
python dataset_download.py
```

This will download and extract all datasets specified in `config.yml`.

### 2. Dataset Inspection

Run `dataset_overview.ipynb` to inspect dataset structure and basic statistics:

### 3. Reproduce Experiments

To reproduce the experiments and visualizations presented in the survey, run `dataset_analysis.ipynb`

## Citation

If you find this project helpful in your research, please consider citing:

```bibtex
TODO
```
