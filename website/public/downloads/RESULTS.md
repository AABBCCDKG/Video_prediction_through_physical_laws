# Existing-scene grouped experiment results

All results below were computed from fixed scene partitions: groups1–6 train,7–8 validation,9–10 evaluation. Both variants remain grouped. Existing scenes were examined in the earlier pilot, and neural training budget was extended from400 to2000 updates after validation loss continued improving. This is exploratory evaluation; no untouched external test set is claimed.

## 30-frame geometry comparison

Geometry is measured in1280×720 pixels against separate HSV segmentation/ellipse estimates and local tracking, with assistant-reviewed keyframes and explicit unavailable measurements. It is not exact simulator ground truth.

| Method | ADE px | FDE px | Moving ADE px | Pair-time overlap >10% |
|---|---:|---:|---:|---:|
| Persistence | 55.46 | 76.91 | 145.63 | 0.00% |
| Linear extrapolation | 51.70 | 89.51 | 116.59 | 1.39% |
| Quadratic extrapolation | 41.19 | 65.62 | 90.52 | 2.83% |
| Physics + constant acceleration | 16.58 | 35.95 | 39.72 | 0.00% |
| Physics + constant velocity | 12.42 | 21.24 | 28.91 | 0.00% |
| Same state, no contacts | 42.92 | 72.34 | 92.90 | 2.17% |
| Physics + deceleration | 14.02 | 26.76 | 34.56 | 0.00% |
| Deceleration, no contacts | 39.99 | 62.04 | 88.38 | 2.83% |

The moving cohort includes objects whose measured future displacement exceeds5px; this is a reporting stratum and does not provide inference inputs. Missing predictions are charged the image diagonal in archived end-to-end scores. Unavailable target measurements are excluded and their coverage is reported.

## Complete RGB comparison

All methods use160×90 RGB targets; classical methods share an observed-patch translation/inpainting renderer. ConvLSTM produces its own frames autoregressively.

| Method | RGB MSE | Mean per-clip PSNR dB |
|---|---:|---:|
| Persistence | 0.002162 | 26.80 |
| Linear extrapolation | 0.001953 | 27.37 |
| Quadratic extrapolation | 0.001804 | 27.62 |
| Physics + constant velocity | 0.001150 | 29.52 |
| Same state, no contacts | 0.001699 | 28.21 |
| Physics + deceleration | 0.001428 | 28.53 |
| ConvLSTM seed0 | 0.002475 | 26.19 |
| ConvLSTM seed1 | 0.002796 | 25.73 |
| ConvLSTM seed2 | 0.002910 | 25.64 |

ConvLSTM across seeds: MSE 0.002727 ± 0.000226; mean PSNR 25.85 ± 0.30 dB. Seed SD describes optimization variability, not uncertainty across scenes.

The frame background dominates RGB MSE; geometry and motion-object reporting remain necessary. Neural detector-based ADE is retained only in raw diagnostic files because blob-extraction failures make it detector-dependent. The primary neural comparison is complete RGB MSE/PSNR plus qualitative predictions.

## Per-scene results

| Scene | CV physics ADE px | Same state without contacts | Deceleration physics | Quadratic |
|---|---:|---:|---:|---:|
| 9 | 8.17 | 18.43 | 11.44 | 18.09 |
| 10 | 16.66 | 67.40 | 16.59 | 64.29 |

Do not claim statistical significance or broad generalization from two evaluation groups. Candidate near-contact metrics are descriptive and can count a pass-through as contact; they are not a substitute for displacement or penetration measurements. Full event counts, label coverage, training logs, checkpoints, and per-clip numbers are archived.
