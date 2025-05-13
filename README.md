# Survey of Filtered Approximate Nearest Neighbor Search over the Vector-Scalar Hybrid Data

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
- Exploring the above dataset contents
- Reproducing the experimental results presented in the survey

## Environment Setup

To set up the environment using `conda`, run:

```bash
source env.sh
```

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

To download and extract all datasets specified in `config.yml`, run `dataset_download.py`.

### 2. Dataset Overview

To inspect dataset structure and basic contents, run `dataset_overview.ipynb`.

### 3. Dataset Analysis

To reproduce the experiments presented in the survey, run `dataset_analysis.ipynb`. 

## Citation

If you find this project helpful in your research, please consider citing:

```bibtex
@misc{lin2025surveyfilteredapproximatenearest,
      title={Survey of Filtered Approximate Nearest Neighbor Search over the Vector-Scalar Hybrid Data}, 
      author={Yanjun Lin and Kai Zhang and Zhenying He and Yinan Jing and X. Sean Wang},
      year={2025},
      eprint={2505.06501},
      archivePrefix={arXiv},
      primaryClass={cs.DB},
      url={https://arxiv.org/abs/2505.06501}, 
}
```
