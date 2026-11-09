# Adversarial replication and data-acquisition gate (16 October 2026)

**Scope:** audit the findings in draft PR #10, not a second independent human reviewer. Self-reported ChatGPT GPT-6 session operating through `levyio`. **Status:** new quantitative reproduction from published device-level data; authors have **not** been contacted. **No clinical conclusions.**

## 1. Wood et al. 2024: reproduced published p-values, but interpretation is fragile

Original source: Felix N. R. Wood et al., *International Journal of Circumpolar Health* 83 (2024), article 2367273, [DOI:10.1080/22423982.2024.2367273](https://doi.org/10.1080/22423982.2024.2367273), [public primary article with Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11182065/). Source is published under **CC BY-NC 4.0**, so this repository does **not** reproduce its original 24-row table; any commercial reuse requires rights review.

The authors analyzed **12 expired EpiPen and 12 expired Jext autoinjectors**. Each brand had three devices assigned to each 0, 1, 5 or 15 cycle group. The endpoint was **mass of liquid discharged into a receptacle** after thawing, not epinephrine potency, sterility, or actual dose injected into tissue.

Independent recomputation from the 24 individual values printed in the **original Table 1** (with local SciPy/statsmodels checks) returns:

| Brand | Mean ejected mass at 0/1/5/15 cycles (g), derived | Welch ANOVA p (published and reproduced) | Ordinary one-way ANOVA p (sensitivity only) |
| --- | --- | --- | --- |
| EpiPen | 0.29567 / 0.30467 / 0.30533 / 0.29833 | 0.15410 | 0.22868 |
| Jext | 0.29667 / 0.32000 / 0.32000 / 0.33333 | 0.20664 | 0.04685 |

**Independent computations:** Welch F for EpiPen = 3.1423115 (df = 3, 3.82665), and for Jext = 2.3219758 (df = 3, 4.36681). Ordinary F = 1.7797228 (df=3,8) for EpiPen, and 4.1833333 (df=3,8) for Jext. These replicate the original **Welch** p-values to three decimal places. The conventional ANOVA result for Jext crosses a nominal 0.05 threshold, illustrating **assumption sensitivity**, **NOT** proving a genuine treatment effect; ordinary equal-variance assumptions may be inappropriate. Do not selectively promote one p-value.

**Crucial confound in original Table 1:** for Jext, the three no-freeze controls have expiry dates **July 2020 / July 2021**, whereas all three 15-cycle devices expire **August 2022**. EpiPen expiry dates likewise trend later across cycle conditions. The study does **not** establish equal device ages, independent production lots, baseline physical condition, or uniform pre-experiment storage histories across assigned groups. Since expiry date also corresponds to possible formulation/batch variation, **cycle effects cannot reliably be isolated**. This is an observed imbalance, not proof of bias direction. Source does not state randomized allocation. The two brands were also tested at different geographic locations with different freezers, so pooling without site/brand effects would not be justified.

**Conclusion:** all 24 devices fired in this experiment; the preliminary data do not show conclusive dose-mass deterioration under this test, but **absence of statistical significance does not demonstrate equivalence, noninferiority, full-dose accuracy, or safety**. Different valid analyses can yield different p-values, and neither addresses expiry confounding with n=3/group.

### Reproduction without redistributing noncommercial-licensed source tables

Code: [`research/tools/wood_anova.py`](tools/wood_anova.py), plus [`tests/test_wood_anova.py`](../tests/test_wood_anova.py). Obtain the 24 raw measurements **from the original paper** and create a local CSV with header:

```csv
brand,freeze_thaw_cycles,expiry_ym,ejected_mass_g
```

Enter each device's published values with four fields, converting published `MM/YYYY` expiry into `YYYY-MM`. **Do not substitute simulated data for original measurements.** Run:

```bash
python research/tools/wood_anova.py your_locally_transcribed_wood_table1.csv
python -m unittest discover -s tests -v
```

Script calculates F/df using Python standard library; SciPy, if installed, provides both F-tail p-values. No original Wood device rows are stored in this repository. The four new tests use explicitly **synthetic mathematical fixtures**, not clinical/device evidence. A different analyst must independently transcribe Table 1, confirm the values, check calculations and assess study limitations before approval.

## 2. Lai et al. 2019: raw series acquisition and timepoint ambiguity

[Lai et al., original full text](https://link.springer.com/article/10.1186/s12954-019-0288-4) reports **Sandoz naloxone 0.4 mg/mL, 1 mL ampoules, lot GH3080**. Three 50 µL HPLC injections per sample are *technical replicates*. To avoid time-since-stress variation, different ampoules were exposed for different durations, ending together for HPLC analysis. **Not repeated measures of the same sealed ampoule, and only one named manufacturing lot.**

**Day 21 discrepancy:** Methods list day 21, while the caption of Figure 1 lists 0,1–7,14,28. The figure caption does not prove whether a day-21 data point was collected. Request original sample-level timepoint labels instead of imputing a value.

**Data access:** The paper explicitly says analyzed data can be provided **upon request to the corresponding author**. The publicly downloadable supplementary file is a *sample chromatogram*, **not** the entire longitudinal HPLC measurements. No author outreach has occurred.

**Requested metadata for independent eligibility:** timestamp, start/end thermal exposure, manufacturer lot ID, unopened physical ampoule ID, whether a separate ampoule was used per condition/day, HPLC run and injection identifiers, all parent naloxone AUC/concentrations and calibration curves, paraben/byproduct traces, replicate/error metadata, and documented rights for data reuse/publication. The precise identity of visible white precipitate was not established by that reported assay; do not label it a particular impurity.

## 3. Contradictory primary literature must be screened, not ignored

- [Gammon et al., 2008, DOI 10.1016/j.ajem.2007.09.004](https://doi.org/10.1016/j.ajem.2007.09.004) is an original prehospital thermal-cycling HPLC study. Lai et al. report its naloxone measurements declined to approximately **89.62%** after four weeks of −6/54°C cycling; this numerical figure is a **secondary quotation in Lai's original article**, not separately extracted from Gammon's full source.
- [Armenian et al., 2017, DOI 10.1080/10903127.2016.1258098](https://doi.org/10.1080/10903127.2016.1258098) is an original four-week multi-medication LC-QTOF/MS study. Its abstract reports heat-dependent **naloxone** degradation. Lai's discussion highlights **one vial per thermal condition sampled weekly**, with no included experimental control; this cannot establish independence across vials or lots. An original paper must be rechecked to resolve exact experimental units.
- **Important negative-data precedent:** Armenian et al. excluded **epinephrine, amiodarone and dexamethasone** from the analyzed set due to reported inter-batch calibration coefficients of variation above 20%. Excluded observations must **not** be silently treated as measured stability results or filled with hypothetical numbers.

Therefore even simple naloxone temperature-response trends conflict across formulations, vial reuse regimes, assays and conditions; cross-study pooling without identifiers and quality controls is premature.

## 4. Author contact draft — **NOT SENT**

Corresponding author (publicly listed by Lai et al.): Michael A. Beazely, University of Waterloo, `mbeazely@uwaterloo.ca`.

**Subject:** Request for underlying timepoint data and experimental-unit metadata — Lai et al. 2019 naloxone stability (DOI 10.1186/s12954-019-0288-4)

Dear Professor Beazely,

I am conducting a public, nonclinical evidence-review project that screens independently reusable rescue-medication stability datasets. Your 2019 *Harm Reduction Journal* study on Sandoz naloxone lot GH3080 appears particularly informative because it measures parent naloxone alongside preservative-related signals and physical changes.

Your data-availability statement invites requests for analyzed data. Would you be willing to share the numerical measurements underlying Figures 1–3, together with any available sampling metadata (physical ampoule IDs, exact treatment/day groups, number of biological/physical versus technical replicates, assay identifiers, uncertainty and units)? The Methods mention day 21, but the Figure 1 caption does not; could you clarify whether day-21 measurements exist?

Please also indicate any conditions for lawful reuse of the numerical data, including whether redistribution of the data with attribution in an openly visible research repository or subsequent commercial research would require specific permission. We will distinguish formulation/lot-specific analytical stability from sterility, delivered-dose or clinical claims, and will not treat technical replicates as independent lots.

Thank you for considering the request.

**Status:** Draft only, no communication transmitted. Human owner to approve before outreach.

## Review gates and handoff

1. Different contributor independently replicates 24-row Wood data transcription and both statistical tests; examines device age/group imbalance.
2. Primary-author written response resolves Lai timepoint/ampoule-count ambiguity and rights to redistribute/process measurements. If no response, retain `DATA_UNAVAILABLE`, do not fabricate.
3. Screen Gammon and Armenian full methods as explicit disagreement cases; preserve positive **and negative** findings.
4. Only after independent-lot data and rights are established, design a preregistered whole-lot held-out modeling experiment. Otherwise `INSUFFICIENT`.
5. **No claims about approved shelf life, expired emergency product use, clinical performance or safety.**

**HANDOFF |** `agent=gpt6-independent-eai-challenge-20261016 | achieved=published-Wood statistical reproduction + test-sensitivity challenge + dataset request prepared | blocked=independent human reviewer, Lai numerical data, rights/physical replicate IDs | next=independently audit and request source data after human approval | tests=4 synthetic code tests + local published-table Welch cross-check | status=DRAFT_NOT_MERGED`.
