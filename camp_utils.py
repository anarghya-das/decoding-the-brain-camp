"""
camp_utils — helper toolbox for the "Decoding the Brain" summer camp
=====================================================================

This file contains small, well-tested helpers so your notebooks can focus
on the science instead of boilerplate. You will *build* simplified versions
of some of these functions yourself during Week 1 — afterwards you can use
the versions here so everyone's results match.

Quick start (in any notebook in this folder):

    import camp_utils as cu
    data = cu.load_camp_data()

Everything you need to know about the data file is in the camp README.
"""

import os
from pathlib import Path

import numpy as np


# =============================================================================
# 1. Finding and loading the data
# =============================================================================

DATA_FILENAME = "synapse_preprocessed.pkl"

# Places we look for the data file, relative to this folder.
# Your instructor will tell you where to put the file — usually notebooks/data/
_SEARCH_DIRS = [
    Path("data"),
    Path("."),
    Path(".."),
    Path("../data"),
    Path("../../processed_data"),   # when running inside the research repo
]


def find_data_file():
    """Look for the camp data file. Returns a Path or None.

    Checks the CAMP_DATA_PATH environment variable first (the Colab/GitHub setup
    cell sets this to the data file it located in the mounted Drive), then falls
    back to the usual folders next to this file.
    """
    env = os.environ.get("CAMP_DATA_PATH")
    if env and Path(env).exists():
        return Path(env)
    here = Path(__file__).parent
    for d in _SEARCH_DIRS:
        candidate = (here / d / DATA_FILENAME).resolve()
        if candidate.exists():
            return candidate
    return None


def load_camp_data(path=None, verbose=True):
    """
    Load the preprocessed SYNAPSE dataset.

    Returns a dict with (among others) these keys:
      exp_epochs   : dict[task] -> list of mne.Epochs (one per EXP subject)
      ctrl_epochs  : dict[task] -> list of mne.Epochs (one per CTRL subject)
      exp_subjects : list of 18 EXP subject IDs (aligned with the lists above)
      ctrl_subjects: list of 10 CTRL subject IDs
      clinical_scores: dict[subject] -> dict of questionnaire totals (EXP only)
    """
    import pickle

    if path is None:
        path = find_data_file()
    if path is None:
        raise FileNotFoundError(
            f"Could not find {DATA_FILENAME}. Put it in a 'data' folder next to "
            "your notebooks, or pass the full path: load_camp_data('path/to/file.pkl')"
        )

    with open(path, "rb") as f:
        data = pickle.load(f)

    if verbose:
        print(f"Loaded {Path(path).name}")
        print(f"  EXP  (sound-sensitive) subjects: {len(data['exp_subjects'])}")
        print(f"  CTRL (healthy control) subjects: {len(data['ctrl_subjects'])}")
        for task in TASKS:
            n_exp = sum(1 for e in data["exp_epochs"][task] if e is not None)
            n_ctrl = sum(1 for e in data["ctrl_epochs"][task] if e is not None)
            print(f"  {task.upper():4s}: {n_exp} EXP + {n_ctrl} CTRL recordings")
    return data


def iter_subjects(data, group, task):
    """
    Loop over (subject_id, epochs) pairs for one group and task,
    automatically skipping subjects whose recording is missing (None).

    Example:
        for subject, epochs in cu.iter_subjects(data, "exp", "let"):
            print(subject, len(epochs))
    """
    subjects = data[f"{group}_subjects"]
    epochs_list = data[f"{group}_epochs"][task]
    for subject, epochs in zip(subjects, epochs_list):
        if epochs is not None:
            yield subject, epochs


# =============================================================================
# 2. The experiment: tasks, timing, frequency bands
# =============================================================================

TASKS = ["pmt", "let", "hlt", "ast"]

TASK_NAMES = {
    "pmt": "Pupil Muscular Test",
    "let": "Listening Effort Test",
    "hlt": "Hearing Loudness Test",
    "ast": "Aversive Sound Test",
}

# How long the sound lasts in each task (seconds). Sound starts at t = 0.
STIM_DURATIONS = {"pmt": 2, "let": 2, "hlt": 2, "ast": 5}

# The quiet period before the sound that we compare against ("baseline").
BASELINE_WINDOW = (-4, -1)

# Classic EEG frequency bands (Hz)
BANDS = {
    "delta": (1, 4),
    "theta": (4, 8),
    "alpha": (8, 13),
    "beta": (13, 30),
    "gamma": (30, 50),
}
BAND_ORDER = ["delta", "theta", "alpha", "beta", "gamma"]

HLT_INTENSITIES = ["3dB", "5dB", "10dB", "20dB", "40dB"]


def get_time_windows(task):
    """
    Time windows (in seconds) used to slice up each trial.
    The sound plays from 0 to 2 s (PMT/LET/HLT) or 0 to 5 s (AST).
    """
    if STIM_DURATIONS[task] == 2:
        return {
            "early_stim": (0, 0.5),
            "mid_stim": (0.5, 1.5),
            "late_stim": (1.5, 2.0),
            "full_stim": (0, 2.0),
            "poststim": (2.0, 7.0),
        }
    else:  # AST: 5-second sounds
        return {
            "early_stim": (0, 0.5),
            "mid_stim": (0.5, 4.5),
            "late_stim": (4.5, 5.0),
            "full_stim": (0, 5.0),
            "poststim": (5.0, 10.0),
        }


# =============================================================================
# 3. ERP components (the "bumps" in the averaged brain wave)
# =============================================================================
# window: where to look (seconds after sound onset)
# polarity: +1 = look for a peak (bump up), -1 = look for a trough (dip down)

ERP_COMPONENTS = {
    "n1":  {"window": (0.08, 0.15), "polarity": -1},  # sound detection
    "p2":  {"window": (0.15, 0.25), "polarity": +1},  # early processing
    "p3":  {"window": (0.25, 0.40), "polarity": +1},  # attention
    "lsp": {"window": (0.40, 0.60), "polarity": -1},  # late processing
    "lpp": {"window": (0.30, 0.60), "polarity": +1},  # emotional processing
    "vlc": {"window": (0.60, 0.80), "polarity": -1},  # very late (aversive sounds)
}

# Which components make sense for which task
TASK_COMPONENTS = {
    "let": ["n1", "p2", "p3", "lsp"],
    "hlt": ["n1", "p2", "lsp"],
    "ast_neutral": ["n1", "p2", "lpp"],
    "ast_trigger": ["n1", "p2", "lpp", "vlc"],
}


def erp_amplitude_and_latency(epochs, component):
    """
    Measure one ERP component for one subject.

    Averages all trials into one wave (the "evoked response"), averages
    across channels, then finds the peak (or trough) inside the
    component's time window.

    Returns (amplitude_in_microvolts, latency_in_ms).
    You will build this yourself in Notebook 05 — this is the tested version.
    """
    comp = ERP_COMPONENTS[component]
    t0, t1 = comp["window"]

    evoked = epochs.average()                       # average over trials
    cropped = evoked.copy().crop(tmin=t0, tmax=t1)  # keep only the window
    wave = cropped.data.mean(axis=0)                # average over channels

    idx = np.argmax(wave) if comp["polarity"] > 0 else np.argmin(wave)
    amplitude_uv = wave[idx] * 1e6      # volts -> microvolts
    latency_ms = cropped.times[idx] * 1000
    return amplitude_uv, latency_ms


# =============================================================================
# 4. Band power (how strong each brain rhythm is)
# =============================================================================

def band_power_db(epochs, band, stim_window, baseline_window=BASELINE_WINDOW):
    """
    Baseline-normalized band power, in decibels (dB).

    Positive = this rhythm got STRONGER during the sound.
    Negative = this rhythm got WEAKER during the sound.

    This mirrors the SYNAPSE study pipeline:  10 * log10(stim / baseline)
    using Welch's method with 0.5-second windows.
    You will build this yourself in Notebook 03 — this is the tested version.
    """
    fmin, fmax = BANDS[band] if isinstance(band, str) else band
    sfreq = epochs.info["sfreq"]
    n_fft = min(64, int(sfreq * 0.5))

    try:
        baseline = epochs.copy().crop(tmin=baseline_window[0], tmax=baseline_window[1])
        stim = epochs.copy().crop(tmin=stim_window[0], tmax=stim_window[1])
    except Exception:
        return np.nan

    bl_psd = baseline.compute_psd(method="welch", fmin=fmin, fmax=fmax,
                                  n_fft=n_fft, verbose=False)
    st_psd = stim.compute_psd(method="welch", fmin=fmin, fmax=fmax,
                              n_fft=n_fft, verbose=False)

    bl_power = bl_psd.get_data().mean()
    st_power = st_psd.get_data().mean()
    if bl_power <= 0:
        return np.nan
    return 10 * np.log10(st_power / bl_power)


def band_power_db_per_channel(epochs, band, stim_window,
                              baseline_window=BASELINE_WINDOW):
    """
    Same as band_power_db, but returns one dB value PER CHANNEL
    (a numpy array matching epochs.ch_names) instead of one number.
    Used for the Tier 1 spatial-map notebook.
    """
    fmin, fmax = BANDS[band] if isinstance(band, str) else band
    sfreq = epochs.info["sfreq"]
    n_fft = min(64, int(sfreq * 0.5))

    try:
        baseline = epochs.copy().crop(tmin=baseline_window[0], tmax=baseline_window[1])
        stim = epochs.copy().crop(tmin=stim_window[0], tmax=stim_window[1])
    except Exception:
        return None

    bl = baseline.compute_psd(method="welch", fmin=fmin, fmax=fmax,
                              n_fft=n_fft, verbose=False).get_data()
    st = stim.compute_psd(method="welch", fmin=fmin, fmax=fmax,
                          n_fft=n_fft, verbose=False).get_data()

    bl_power = bl.mean(axis=(0, -1))   # average over trials and frequencies
    st_power = st.mean(axis=(0, -1))
    with np.errstate(divide="ignore", invalid="ignore"):
        db = 10 * np.log10(st_power / bl_power)
    db[bl_power <= 0] = np.nan
    return db


# =============================================================================
# 4b. Feature matrices for machine learning (Tier 3)
# =============================================================================
# A "PSD feature spec" is a (task, period, band) triple, e.g.
# ("let", "early_stim", "gamma"). build_psd_feature_matrix turns a list of
# specs into a ready-to-model X / y. Used in Notebooks 13 & 14.

# The 5 features the *SYNAPSE study* used in its best simple classifier
# ("PSD-5-fixed", AUC ~0.84). Note the early_stim (0-0.5s) onset windows —
# that's the key ingredient the simplified Week-2 table was missing.
PAPER_PSD5 = [
    ("ast", "early_stim", "delta"),
    ("let", "early_stim", "gamma"),
    ("let", "full_stim",  "gamma"),
    ("let", "early_stim", "beta"),
    ("let", "full_stim",  "beta"),
]


def feature_label(spec):
    """('let','early_stim','gamma') -> 'LET early gamma' for nice axis labels."""
    task, period, band = spec
    return f"{task.upper()} {period.replace('_stim', '')} {band}"


def build_psd_feature_matrix(data, specs, impute=True):
    """Turn a list of (task, period, band) specs into a model-ready matrix.

    Returns
    -------
    X : ndarray (n_subjects, n_specs)   baseline-normalized band power (dB)
    y : ndarray (n_subjects,)           1 = EXP, 0 = CTRL
    names : list[str]                   human-readable column labels

    Subjects are stacked CTRL-first then EXP (so y is [0...0, 1...1]).
    Missing values are filled with the column mean when impute=True (keeps
    every subject), matching how we handle gaps elsewhere in the camp.
    """
    def rows(group):
        out = []
        subjects = data[f"{group}_subjects"]
        for i in range(len(subjects)):
            r = []
            for task, period, band in specs:
                ep = data[f"{group}_epochs"][task][i]
                if ep is None:
                    r.append(np.nan)
                else:
                    window = get_time_windows(task)[period]
                    r.append(band_power_db(ep, band, window))
            out.append(r)
        return np.array(out, dtype=float)

    X_ctrl, X_exp = rows("ctrl"), rows("exp")
    X = np.vstack([X_ctrl, X_exp])
    y = np.array([0] * len(X_ctrl) + [1] * len(X_exp))

    if impute:
        col_mean = np.nanmean(X, axis=0)
        nan_idx = np.where(np.isnan(X))
        X[nan_idx] = np.take(col_mean, nan_idx[1])

    names = [feature_label(s) for s in specs]
    return X, y, names


def loocv_auc(X, y, return_predictions=False):
    """Leakage-safe Leave-One-Out logistic-regression AUC.

    Scaling is fit on the training subjects only, inside each fold — the
    golden rule you learn in Notebook 13. Returns the AUC, or
    (auc, true_labels, predicted_probs) if return_predictions=True.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import LeaveOneOut
    from sklearn.metrics import roc_auc_score

    X = np.asarray(X, dtype=float)
    true, probs = [], []
    for train_idx, test_idx in LeaveOneOut().split(X):
        scaler = StandardScaler().fit(X[train_idx])
        model = LogisticRegression(max_iter=1000).fit(
            scaler.transform(X[train_idx]), y[train_idx])
        probs.append(model.predict_proba(scaler.transform(X[test_idx]))[0, 1])
        true.append(y[test_idx][0])
    true, probs = np.array(true), np.array(probs)
    auc = roc_auc_score(true, probs)
    if return_predictions:
        return auc, true, probs
    return auc


# =============================================================================
# 5. Electrodes: names and anatomical regions
# =============================================================================
# Each ear has 8 electrodes. Numbers 03 and 06 are skipped (hardware layout),
# so the names are: L01 L02 L04 L05 L07 L08 L09 L10 (same for R).
# NOTE: a few subjects have fewer channels — bad ones were removed during
# preprocessing. Always use epochs.ch_names instead of assuming all 16.

REGION_GROUPS = {
    "Tragus/Periauricular": [1, 2],     # in front of the ear canal
    "Mastoid": [4, 5, 7],               # the bone behind the ear
    "Temporal": [8, 9, 10],             # up toward the temple
}


def get_electrode_region(ch_name):
    """'L04' or 'R10' -> anatomical region name (or None if unknown)."""
    num = int(ch_name[1:])
    for region, members in REGION_GROUPS.items():
        if num in members:
            return region
    return None


# =============================================================================
# 6. Clinical questionnaires (EXP subjects only)
# =============================================================================

CLINICAL_MEASURES = {
    "HQ_Total": "Hyperacusis Questionnaire (overall sound sensitivity)",
    "HQ_Fear": "HQ subscale: fear of sounds",
    "HQ_Sensitivity": "HQ subscale: sensitivity",
    "HQ_Emotional": "HQ subscale: emotional impact",
    "GAD_Total": "GAD-7 (anxiety)",
    "THI_Total": "Tinnitus Handicap Inventory",
    "Iowa_Total": "Iowa misophonia composite",
    "Miso_Section1": "Misophonia Questionnaire part 1",
    "Miso_Section2": "Misophonia Questionnaire part 2",
    "Miso_Section3": "Misophonia Questionnaire part 3",
}

# Score at or above the cutoff = clinically significant
CLINICAL_CUTOFFS = {
    "HQ_Total": 28,        # hyperacusis
    "GAD_Total": 10,       # moderate-severe anxiety
    "THI_Total": 38,       # moderate+ tinnitus handicap
    "Miso_Section1": 7,    # moderate+ misophonia
}


def get_clinical_score(data, subject, measure):
    """One questionnaire score for one subject, or None if missing."""
    score = data.get("clinical_scores", {}).get(subject, {}).get(measure)
    if score is None or (isinstance(score, float) and np.isnan(score)):
        return None
    return score


# =============================================================================
# 7. Subgroups within the EXP group (for Tier 2)
# =============================================================================
# Not everyone in the EXP group is the same! Based on their diagnoses:

SUBGROUPS = {
    # only hyperacusis, nothing else
    "pure_hyperacusis": ["EXP02", "EXP05", "EXP07", "EXP13",
                         "EXP16", "EXP18", "EXP21"],
    # hyperacusis PLUS other conditions (tinnitus, hearing loss, misophonia)
    "comorbid_hyperacusis": ["EXP01", "EXP03", "EXP11", "EXP15",
                             "EXP22", "EXP23", "EXP29"],
    # sound-sensitive but NOT hyperacusis (our "negative control")
    "non_hyperacusis": ["EXP04", "EXP06", "EXP25", "EXP28"],
}
SUBGROUP_NAMES = {
    "pure_hyperacusis": "Pure Hyperacusis",
    "comorbid_hyperacusis": "Comorbid Hyperacusis",
    "non_hyperacusis": "Non-Hyperacusis",
}


# =============================================================================
# 8. Camp style: colors (colorblind-safe Wong palette, same as the paper)
# =============================================================================

EXP_COLOR = "#D55E00"    # orange  = sound-sensitive group
CTRL_COLOR = "#0072B2"   # blue    = healthy controls
GROUP_COLORS = {"EXP": EXP_COLOR, "CTRL": CTRL_COLOR}

BAND_COLORS = {
    "delta": "#0072B2", "theta": "#009E73", "alpha": "#E69F00",
    "beta": "#D55E00", "gamma": "#CC79A7",
}
REGION_COLORS = {
    "Tragus/Periauricular": "#56B4E9",
    "Mastoid": "#E69F00",
    "Temporal": "#009E73",
}
SUBGROUP_COLORS = {
    "pure_hyperacusis": "#E69F00",
    "comorbid_hyperacusis": "#009E73",
    "non_hyperacusis": "#0072B2",
}


# =============================================================================
# 9. Statistics helpers (you build these in Week 2; tested versions here)
# =============================================================================

def hedges_g(group1, group2):
    """
    Effect size: how far apart are two groups, in units of their
    combined spread? Includes the small-sample correction.
    Rule of thumb: 0.2 small, 0.5 medium, 0.8 large.
    """
    g1, g2 = np.asarray(group1, float), np.asarray(group2, float)
    g1, g2 = g1[~np.isnan(g1)], g2[~np.isnan(g2)]
    n1, n2 = len(g1), len(g2)
    if n1 < 2 or n2 < 2:
        return np.nan
    pooled_sd = np.sqrt(((n1 - 1) * g1.var(ddof=1) + (n2 - 1) * g2.var(ddof=1))
                        / (n1 + n2 - 2))
    if pooled_sd == 0:
        return np.nan
    d = (g1.mean() - g2.mean()) / pooled_sd
    correction = 1 - 3 / (4 * (n1 + n2) - 9)   # small-sample correction
    return d * correction


# =============================================================================
# 10. Friendly self-checks for the notebooks
# =============================================================================

def check(condition, success_msg="Looks good!", fail_msg="Not quite — re-read the hint and try again."):
    """Print a friendly pass/fail message instead of crashing the notebook."""
    if condition:
        print(f"✅ {success_msg}")
    else:
        print(f"❌ {fail_msg}")
    return bool(condition)


# Where notebooks save figures and tables.
# On Colab the shared camp folder is read-only, so the setup cell sets the
# CAMP_OUTPUT_DIR environment variable to a writable folder in the student's own
# Drive. Locally, CAMP_OUTPUT_DIR is unset and we use ./outputs next to this file.
def _resolve_output_dir():
    env = os.environ.get("CAMP_OUTPUT_DIR")
    return Path(env) if env else Path(__file__).parent / "outputs"


OUTPUT_DIR = _resolve_output_dir()


def save_path(filename):
    """Get a path inside the outputs folder (created if needed).

    Re-reads CAMP_OUTPUT_DIR each call so a Colab setup cell can redirect output
    even if it runs after camp_utils was first imported.
    """
    out = _resolve_output_dir()
    out.mkdir(parents=True, exist_ok=True)
    return out / filename
