# Motion Prediction through Physical Laws — project page

A static academic demo site for Dong Wang, Purdue University.

Intended free GitHub Pages URL: https://aabbccdkg.github.io/Video_prediction_through_physical_laws/

## Features

- All four evaluation clips, with synchronized observed-video / physics / baseline lanes.
- Playback, slow motion, single-frame stepping, loop and annotated contact jumps.
- Contacts enabled/disabled and deceleration rules; quadratic, linear, persistence and all three ConvLSTM seeds.
- Same observed prefix in every lane, followed by the saved future predictions.
- English / Chinese, responsive layout, keyboard access and reduced-motion support.
- Real experiment tables at 15/30/60-frame horizons, scientific scope, paper, source, experimental ZIP, CSV and citation.

Recorded video starts at1280×720. Saved model frames are160×90 and enlarged for the player; upscaling does not add model detail. Classical videos use the fixed observed-patch renderer from the experiment. All metrics are generated from stored outputs; no experimental result is recalculated or changed for the site.

## Development

```bash
npm install
npm run dev
npm run build
```

Run from the website/ folder. Vite uses relative asset URLs so dist/ works in the GitHub Pages repository subpath. No paid service or backend is required.

To regenerate video assets, run from the project root:

```bash
experiments/.venv/bin/python website/scripts/build_media.py
```

Requires the existing experiment environment plus imageio-ffmpeg. The script encodes40 H.264 files (4clips×10lanes) at source fps, verifies decodability and frame counts, and writes the media/provenance manifest.

## Publication layout

- docs/: production site (Vite dist output) served by free GitHub Pages.
- website/: source files, Vite build configuration and media-generation script.
- paper/: synchronized LaTeX manuscript and PDF.

The existing research source/data files are preserved. A GitHub workflow builds future site edits and deploys the resulting artifact to Pages. The initial docs directory includes the validated static build. Internal source records, credentials, local caches and virtual environments are excluded.

The design follows the academic project-page structure requested by the user, referencing https://introspective-diffusion.github.io/orl-dlm/ without copying its code or research claims.
