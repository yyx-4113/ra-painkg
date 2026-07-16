# Supplementary Table S1: Complete Benchmark Results

Mean Pearson r (+/- SD) across 10 independent train/test splits (80%/20%). Random values are mean of 5 independent graph realizations each averaged over 10 splits.

| Knowledge Graph | PPI Edges | All-Genes r | Pain-Genes r | Non-Pain r | Track A r | Track B r | Track Dual r |
|---|---|---|---|---|---|---|---|
| GO | 673,899 | 0.589 +/- 0.051 | 0.542 +/- 0.058 | 0.590 +/- 0.051 | 0.098 +/- 0.114 | 0.436 +/- 0.099 | 0.542 +/- 0.056 |
| RA_PainKG | 2,400 | 0.551 +/- 0.057 | 0.503 +/- 0.055 | 0.552 +/- 0.057 | 0.097 +/- 0.143 | 0.451 +/- 0.075 | 0.503 +/- 0.059 |
| RA_PainKG_degPreserved | 2,400 | 0.546 +/- 0.049 | 0.483 +/- 0.057 | 0.547 +/- 0.049 | 0.069 +/- 0.084 | 0.460 +/- 0.088 | 0.487 +/- 0.058 |
| GO_painCentric | 121,543 | 0.603 +/- 0.054 | 0.523 +/- 0.065 | 0.604 +/- 0.054 | 0.055 +/- 0.085 | 0.555 +/- 0.183 | 0.518 +/- 0.063 |
| Random_R0 | 673,899 | 0.652 +/- 0.042 | 0.589 +/- 0.044 | 0.652 +/- 0.042 | 0.101 +/- 0.083 | 0.568 +/- 0.122 | 0.591 +/- 0.043 |
| Random_R1 | 673,899 | 0.667 +/- 0.045 | 0.620 +/- 0.046 | 0.667 +/- 0.045 | 0.070 +/- 0.070 | 0.540 +/- 0.121 | 0.621 +/- 0.043 |
| Random_R2 | 673,899 | 0.640 +/- 0.052 | 0.570 +/- 0.060 | 0.641 +/- 0.052 | 0.056 +/- 0.125 | 0.518 +/- 0.141 | 0.569 +/- 0.061 |
| Random_R3 | 673,899 | 0.656 +/- 0.045 | 0.591 +/- 0.035 | 0.657 +/- 0.045 | 0.076 +/- 0.086 | 0.587 +/- 0.113 | 0.590 +/- 0.035 |
| Random_R4 | 673,899 | 0.648 +/- 0.053 | 0.586 +/- 0.045 | 0.648 +/- 0.053 | 0.097 +/- 0.116 | 0.550 +/- 0.109 | 0.588 +/- 0.046 |
| STRING | 0 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 |
| Identity | 0 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 |

*Track A: n=3 genes (immune-inflammation). Track B: n=5 genes (nociception-pain transduction). Track Dual: n=96 genes spanning both tracks. Note: Track A/B measurements are noise-dominated due to small sample sizes.*