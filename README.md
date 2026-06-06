# Decoding the Brain 🧠
### EEG Data Science for Sound Sensitivity Research — University at Buffalo

Hands-on notebooks for the summer camp. Each notebook opens in **Google Colab** with one click — no install needed.

> **First time? Read [COLAB_SETUP.md](COLAB_SETUP.md).** You'll add the shared data folder to your Drive once, then every notebook just works.

---

## Week 1 — The Brain & The Data

| Notebook | Open |
|---|---|
| Meet the Data | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week1/01_meet_the_data.ipynb) |
| Brain Waveforms (ERPs) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week1/02_brain_waveforms.ipynb) |
| Brain Rhythms (Spectral Power) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week1/03_spectral_power.ipynb) |
| First Group Comparison · Checkpoint 1 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week1/04_first_group_comparison.ipynb) |

## Week 2 — Measuring the Differences

| Notebook | Open |
|---|---|
| Feature Extraction | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week2/05_feature_extraction.ipynb) |
| Publication-Quality Figures | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week2/06_publication_figures.ipynb) |
| Statistical Testing | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week2/07_statistical_testing.ipynb) |
| Effect Sizes & FDR | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week2/08_effect_sizes_fdr.ipynb) |
| Clinical Correlations · Checkpoint 2 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week2/09_clinical_correlations.ipynb) |

## Week 3 — Deep Dive (pick your tier)

| Notebook | Open |
|---|---|
| Tier 1 · Spatial Maps | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week3/10_tier1_spatial_maps.ipynb) |
| Tier 2 · Subgroup Profiling | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week3/11_tier2_subgroup_profiles.ipynb) |
| Tier 2 · Temporal Dynamics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week3/12_tier2_temporal_dynamics.ipynb) |
| Tier 3 · Building a Classifier | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week3/13_tier3_classification.ipynb) |
| Tier 3 · Permutation & ROC | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week3/14_tier3_permutation_roc.ipynb) |
| Wrap-Up & Poster Figures · Checkpoint 3 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anarghya-das/decoding-the-brain-camp/blob/main/week3/15_wrapup_poster_figures.ipynb) |

---

## What you need before you start

Just a **Google account** (for Colab). Open any notebook above with its **Open in Colab** badge, run the **▶ Step 0** cell — it downloads the data automatically — and go. See [COLAB_SETUP.md](COLAB_SETUP.md) for details.

## For instructors

Notebooks are generated from the camp sources with `summer_camp/tools/build_github.py`. The data file itself (`synapse_preprocessed.pkl`, ~470 MB) is **not** in this repo — it lives on Google Drive and the Step 0 cell downloads it via `gdown`. Note the Drive link is referenced in the setup cell, so the data is reachable by anyone with this (public) repo; keep that in mind for sensitive data. Answer keys are kept separately and are not part of this repo.

