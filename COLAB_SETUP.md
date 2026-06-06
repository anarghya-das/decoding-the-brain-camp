# Getting started

Each notebook runs in **Google Colab** and sets itself up automatically — there's
nothing to install or download by hand.

## Steps

1. In the [README](README.md), pick a notebook and click its **Open in Colab** badge.
2. Run the **▶ Step 0** cell (the first one). It will:
   - install the `mne` library,
   - download the camp toolbox,
   - download the data file (~470 MB — takes ~1–2 minutes the first time).
3. When it asks to **connect Google Drive**, click **Connect** and choose your
   account. (This is so your figures are *saved* for your poster. You can skip it,
   but then your figures won't persist after you close Colab.)
4. Wait for **✅ Setup complete**, then run the rest of the notebook top to bottom.

Do this once per notebook — each Colab session is a fresh machine. Your figures are
saved to a **DecodingBrain_outputs** folder in your own Drive, so your poster images
build up across the weeks.

## Troubleshooting

- **Download is slow / fails** — re-run Step 0; the data file is large, so give it
  a minute. If it ever says the file can't be downloaded right now, wait a bit and
  retry (Google rate-limits very busy files).
- **Drive connect pop-up didn't appear** — re-run Step 0; allow pop-ups for
  colab.research.google.com. (Skipping it is fine; figures just won't be saved.)
- **`mne` / unpickle error** — Step 0 pins `mne==1.10.1` to match the data file.
  If Colab asks to *Restart runtime* after install, do it and re-run Step 0.
