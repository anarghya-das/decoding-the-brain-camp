# One-time setup (do this before the first notebook)

These notebooks read the camp's data from a shared **Google Drive** folder. Set
that up once and every notebook will find it automatically.

## Steps

1. Open the **shared camp data folder** link your instructor sent you.
2. Click **"Add shortcut to Drive"** and put the shortcut in **My Drive**
   (not inside another folder). This does **not** copy the 467 MB file — it's
   just a pointer, and uses none of your storage.
3. Go back to the [README](README.md), pick a notebook, and click its
   **Open in Colab** badge.
4. Run the **▶ Step 0** cell. Click **Connect** on the Google Drive pop-up.
5. Wait for **✅ Setup complete**, then run the rest of the notebook.

You do steps 4–5 once per notebook (each Colab session is a fresh machine). Your
figures are saved to a **DecodingBrain_outputs** folder in your own Drive, so your
poster images build up across the weeks.

## Troubleshooting

- **"Could not find synapse_preprocessed.pkl in your Drive"** — you didn't add the
  shortcut, or it isn't in *My Drive*. Redo step 2 and re-run Step 0.
- **Drive pop-up didn't appear** — re-run Step 0; allow pop-ups for
  colab.research.google.com.
- **`mne` / unpickle error** — Step 0 pins `mne==1.10.1` to
  match the data file. If Colab asks to *Restart runtime* after install, do it and
  re-run Step 0.
