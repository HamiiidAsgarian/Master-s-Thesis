# Visuals Plan — Thesis Figures, Charts, and Diagrams

**Status:** Working plan. Operationalizes `Visual_Guide_north-star.md` for `0-Active Doc/Thesis_v9-3.md`.
Read both before touching any figure. `Visual_Guide_north-star.md` stays authoritative for visual
work; where this plan proposes something that contradicts it, the conflict is flagged as a
**decision item** below, not silently resolved.

> **Execution status (2026-08-16):** D2(a) DONE — v10 rebuilt from real `baseline_comparison.csv`
> data (Aloor + †estimated dropped); D3(a) DONE — v17 built from `analysis_support/qtab/*.npy`;
> v09 converted to Persian canonical schematic; all pre-flight checks passed; G1/G3/G4 doc sync
> complete. Remaining open items are below.

---

## 1. Current state (verified 2026-08-16)

**23 thesis figures** in the v9-3 فهرست اشکال. All 23 are embedded in the document body and all 23
have visible caption lines `**شکل (X-Y):** …`.

| Source family | Files | Shapes | Styling |
|---|---|---|---|
| `generate_all_Visuals2.py` → `results/figures/vNN_*.png` | v01–v16, v18, v2_1 (18 files) | 1-1, 2-1, 3-1…3-7, 4-1…4-6, 4-8, 4-9, 4-14 | canonical (see §4) |
| **MISSING v17** | — | 4-7 (Q-table heatmaps) | legacy `results/qtable_heatmaps.png` (advanced_analysis.py, default `YlOrRd`, not canonical) |
| legacy per-run plots | `results/baseline_{charbonnier_validation,kusatake_timing,behrunani_sanity,may_huang_sanity}/results_plot.png` | 4-10…4-13 | matplotlib defaults, **not** canonical |
| schematic (Latin) | `v09_tragedy_commons.png` | 1-1 | off-palette hexes (`#8B4513`, `#D4A574`, `#E8F5E9`, `#E3F2FD`), English text |

### 1.1 Ground-truth drift vs. the north-star (read before editing)

These facts are verified directly from the thesis file and the code; several contradict the
north-star and `Result_Help.md`. Each is either a decision item (§5) or a doc-sync item (§7).

1. **The thesis does NOT consume only `figures/vNN_*.png`.** Five thesis figures embed
   non-vNN files directly: `../results/qtable_heatmaps.png` (شکل ۴-۷, thesis line 1336) and the
   four `../results/baseline_*/…/results_plot.png` (شکل ۴-۱۰…۴-۱۳, lines 1455–1467).
   → North-star §1 is stale; see decision item D1.
2. **v10 / شکل ۴-۱۴ IS in the document.** It is listed in the فهرست اشکال (line 329) AND embedded
   in the body (lines 1513–1515) with a caption that explicitly describes Aloor et al. as
   context-only and the comparison values as estimated from source papers. This contradicts
   north-star §2 ("must stay out of the document") and `Result_Help.md` §E1. The decision was
   apparently already made to include it; it must be re-confirmed, not silently reversed.
   → Decision item D2.
3. **Result_Help.md §F is stale.** It claims figures have no visible captions and that 3 shapes are
   orphaned / only 2 are cited in prose. Verified current state: **all 23 have visible captions**,
   and prose call-outs exist for every shape except شکل ۲-۱ (the one added this session).
   → Doc-sync item G1.
4. **PROJECT_NORTH_STAR.md (referenced by north-star §0) is not present in the repo.**
   → Doc-sync item G2.

---

## 2. Scope and chain of command

- **In scope (proceed without asking):** styling, layout, fonts, colors, regenerating a figure from
  already-correct data, file naming that does not change thesis numbering, caption/call-out edits
  that add a reference without changing any number or claim.
- **Requires Lead decision (report with evidence, wait):** anything that changes what a figure
  *claims* — a value on an axis, a label that describes methodology, adding/removing a figure,
  renumbering a شکل, changing a data source feeding a figure.
- **Never touch:** `offgrid_marl.py` and the baseline/sensitivity logic (locked); any number that
  must trace to audited sources (`baseline_comparison.csv`, `gini_reanalysis.csv`,
  `cloud_sensitivity_reanalysis.csv`, `battery_sensitivity/summary.csv`, `statistical_tests.txt`,
  `.npy` arrays). `PROJECT_NORTH_STAR.md` wins over the north-star where they overlap.

## 3. Mandatory pre-flight before any data-figure work

1. Identify the exact data source for the figure (table in §8).
2. Pull the current value(s) from that source file — not from the chart, not from memory.
3. Cross-check against the thesis's own prose/table for the same result (Gini numbers vs Table 4-3 /
   §4-4; comfort vs §4-3; sharing frequency vs Table 4-4; scarcity vs Table 4-6; innovator stats vs
   §4-9 / Table 4-8; baselines vs Table 4-10).
4. Match → proceed with styling. Mismatch → stop, report both values + sources side by side.

Extra care for Gini / sharing-frequency / scarcity figures: they must reflect the corrected
**Method B** (per-episode cross-sectional Gini, time-averaged), not the old per-house framing.

---

## 4. Target style (the canonical spec — everything converges here)

From north-star §5 gen-3; used verbatim:

- Palette `C`: red `#e74c3c`, green `#2ecc71`, blue `#3498db`, purple `#9b59b6`, orange `#f39c12`,
  yellow `#f1c40f`, dark `#2c3e50`, grey `#7f8c8d`, teal `#1abc9c`. **No hardcoded hexes outside C.**
- `font.family='sans-serif'`; stack `['Helvetica','Arial','DejaVu Sans']`; `font.size=10`,
  `axes.titlesize=12`; `figure.dpi=150`.
- **Data figures:** `alpha≈0.85` fills with gray edges, `grid(alpha=0.3)`, bold titles, error bars
  `capsize=6`, value labels on bars.
- **Schematic figures:** axis-off, `FancyBboxPatch` rounded boxes (colored border + 15% tint fill +
  bold colored text) via the `_box`/`_arrow` helpers, straight arrows.
- **Persian figures:** `fa()` pipeline (`arabic_reshaper` + `bidi`), inside
  `plt.rc_context({'font.family': ['Geeza Pro','DejaVu Sans','Arial Unicode MS']})`. Never mix
  `$…$` mathtext into a `fa()` string; math lives in its own `ax.text()`. Copy the pipeline, don't
  improvise.

Current gaps against this spec (verified in code): v09 uses off-palette hexes + Latin text; v10 uses
the 5-entry `C_5` sub-palette (line 570) instead of full `C`; the four baseline plots and the Q-table
heatmap are not canonical at all; bar-edge/value-label/legend conventions need an audit per figure
(v13 has value labels, v15 has an annotation — v14/v16 must be checked).

---

## 5. Decision items for the Lead (content-affecting — do not act until answered)

| # | Question | Options | Recommended |
|---|---|---|---|
| D1 | The 5 non-vNN figures (4-7 heatmap + 4-10…4-13 baselines) violate the "ONLY vNN" rule. How to make them canonical? | (a) build vNN twins in `generate_all_Visuals2.py` reading the same data and re-point the thesis; (b) restyle in place in the source scripts (touches locked baseline scripts); (c) keep in place, just restyle plots | (a) — honors both the "only vNN" rule and "don't touch locked logic" |
| D2 | v10/شکل ۴-۱۴ is already in the thesis with an estimated-values + Aloor-context asterisk. Keep, rebuild from Table 4-10 reimplementation numbers (real audited data), or remove? | (a) rebuild from Table 4-10 real data, drop estimated + Aloor; (b) keep as-is; (c) remove figure + caption + LoF row | (a), if the professor's rejection of †estimated values still stands |
| D3 | v17 data source. Legacy `advanced_analysis.py` **retrains** agents for the heatmap; saved `results/analysis_support/qtab/*.npy` (6 scenarios) exist. Which feeds v17? | (a) saved `.npy` (deterministic, auditable); (b) re-run advanced_analysis logic | (a) |
| D4 | v09 (شکل ۱-۱) is the only Latin schematic among Persian ones. Persize it (text + labels) or keep bilingual? | persianize / keep | persianize, consistent with the other 8 schematics |
| D5 | Data-figure labels/titles: currently English ('Prosocial Agents', etc.) inside a Persian thesis. Persian-first with English terms in parentheses, or keep English? | Persian-first / keep English | Persian-first (presentation-only change) |

---

## 6. Workstreams

### A. Naming & registry integrity
- Adopt `vNN_<snake_case>.png` for all thesis files. v2_1 stays as-is (encodes shape 2-1).
- Create `v17_qtable_heatmaps.png` (north-star §7.1 mandates this; overrides the older
  "v17 does NOT exist" notes — reconcile those docs in G).
- If D1(a): create `v19_charbonnier_validation.png`, `v20_kusatake_timing.png`,
  `v21_behrunani_sanity.png`, `v22_may_huang_sanity.png` in `generate_all_Visuals2.py`, re-point
  thesis lines 1455–1467. If D1(c): skip.
- Never renumber a شکل — thesis numbering is cross-referenced; any naming change is file-level only.

### B. Gap fill — v17 (priority 1, per north-star §7)
- Block in `generate_all_Visuals2.py` reading the D3-approved data.
- Must reproduce the layout the thesis caption already describes: mean Q per hour, rows = agent 0 /
  counterpart (agent 3; agent 8 in innovator), y = the 3 share actions (0/50/100 %), x = hour 0–23,
  color = mean Q averaged over battery levels.
- Run with `-W error::UserWarning`; visually verify the PNG. REVERSED 2026-08-16: do NOT re-point
  thesis line 1336 → v17 — the thesis keeps the legacy `results/qtable_heatmaps.png`
  (`advanced_analysis.py`); v17 stays a canonical working-artifact variant only (agent selection differs).

### C. Consistency sweep (priority 2 — report before fixing)
- Run §3 pre-flight for every data figure (13 current + v17). Check each figure's displayed numbers
  against the thesis's own current prose/tables. Deliver a discrepancy report (both values + sources
  side by side). Do not fix silently.

### D. Styling standardization (priority 3)
- v09: replace off-palette hexes with `C`; persianize per D4; rebuild with `_box`/`_arrow` helpers.
- v10 (per D2) and v15/v16: unify onto full `C` palette; audit bar edges (`#2c3e50`-ish gray), value
  labels, legend placement.
- Baselines (per D1) and Q-heatmap: bring onto canonical style.
- Sweep every data figure for the §4 spec (edges, alpha, grid, capsize, value labels).

### E. Readability pass
- Persian-first labels/titles per D5 (data figures), English technical terms kept parenthesized.
- Numeric formatting: consistent Persian decimal forms (`۰٫۹`) or ASCII, decided once; apply across
  figures and axis ticks (must stay traceable to source CSVs — formatting only, never re-rounding).
- Colorblind-safe practice within palette C (red/green distinction is used in v14/v18 — verify a
  paired high-contrast fallback or dash style if needed).
- Legend/tick font sizes, padding, `bbox_inches='tight'` trim, no clipped labels at 150 dpi.

### F. Placement & citation fixes in the thesis (text-only)
- Add a «شکل (۲-۱)» in-text call-out in §2-5-1 (currently the only figure with zero prose reference).
- Re-verify the collective ۴-۱۰…۴-۱۳ call-out (exists, §4-10 line 1453) and each caption line stays
  synced to its List-of-Figures entry.
- After any re-pointing (D1), update the image paths in the thesis body.

### G. Documentation sync
- G1: `Result_Help.md` — §A counts, §B tree (v17 + v19–v22), §C registry (2-1 already added; update
  4-7 source, statuses), §D sources, §E (rewrite items 1–2 per decisions D2/D3), **§F rewritten** to
  the verified state (captions exist; only ۲-۱ lacks a call-out), §H index.
- G2: flag missing `PROJECT_NORTH_STAR.md`; restore or re-reference it if it exists elsewhere.
- G3: `Important_considerations.md` §9/§12 — v17 now exists; update counts and the "do not create
  v17" wording.
- G4: `Code_Output_data_visuals_Map.md` — add v17/v19–v22 blocks, styling notes.
- G5: propose a small patch to `Visual_Guide_north-star.md` §1, §2, §7.4 to reflect verified reality
  (D1/D2) — north-star stays authoritative; the Lead applies the patch.

---

## 7. Figure-by-figure task matrix

Legend — **Type:** S=schematic, D=data. **Family:** P=Persian, L=Latin (until D4), E=English labels (until D5).
**Style status:** ✅ canonical / ⚠️ minor gaps / ❌ not canonical / 🚫 missing.

| File | شکل | Type/Family | Status | Data source | Checks / actions |
|---|---|---|---|---|---|
| v2_1_conceptual_framework.png | 2-1 | S/P | ✅ | none | Add «شکل ۲-۱» call-out in §2-5-1 |
| v09_tragedy_commons.png | 1-1 | S/L | ⚠️ | none | D4: persianize; replace off-palette hexes with C |
| v12_system_architecture.png | 3-1 | S/P | ✅ | none | — |
| v02_ring_topology.png | 3-2 | S/P | ✅ | none | — |
| v05_solar_curve.png | 3-3 | D | ✅ | analytic half-sine | verify curve matches Eq. 3-1 params (Gmax=1.3 kW, 0.5 factor) |
| v04_demand_profiles.png | 3-4 | D | ✅ | in-code profiles | labels Persian-first (D5); decimals |
| v01_ocean_to_rl_mapping.png | 3-5 | S/P | ✅ | none | — |
| v03_two_phase_sharing.png | 3-6 | S/P | ✅ | none | — |
| v06_community_compositions.png | 3-7 | S/P | ✅ | scenario lists | — |
| v13_community_metrics.png | 4-1 | D | ✅ | seed `final_metrics.csv` | pre-flight vs §4-1/Table 4-1 (comfort 0.920 mixed, innovator 0.902±0.008, F(4,20)=3.362 p=0.0293); value labels present |
| v14_agent_comfort_split.png | 4-2 | D | ✅ | seed `final_metrics.csv` | pre-flight vs §4-3 (0.935±0.007 vs 0.905±0.010, t(4)=8.487 p=0.0011; varied 0.924 vs 0.904 p=0.0472; innovator 0.912 vs 0.892); red/green contrast (E) |
| v07_reciprocity_cycle.png | 4-3 | S/P | ✅ | none | — |
| v11_lorenz_curve.png | 4-4 | D | ✅ | `analysis_support/house_comfort/lorenz_curves.npy` | pre-flight vs §4-4/Table 4-4 (mixed Gini 0.079, innovator 0.096; t=-2.84 p=0.047) |
| v15_gini_comparison.png | 4-5 | D | ⚠️ | `gini_reanalysis.csv` + `gini_more_scenarios.csv` | pre-flight vs Table 4-3 (Method B values); unify `freq_colors`/C_5 → C |
| v16_sharing_frequency.png | 4-6 | D | ⚠️ | `analysis_support/qtab/*.npy` | pre-flight vs Table 4-4 (SDs 2.00–3.16%); unify palette; check value labels |
| **v17_qtable_heatmaps.png** | 4-7 | D | ✅ | D3 decision (.npy) | **built**; thesis NOT re-pointed (reversed 2026-08-16) — شکل ۴-۷ = legacy `results/qtable_heatmaps.png`; v17 = working artifact |
| v18_scarcity_sensitivity.png | 4-8 | D | ✅ | `cloud_sensitivity_reanalysis.csv` | pre-flight vs Table 4-6 (§4-7); red/green contrast |
| v08_innovator_effect.png | 4-9 | S/P | ✅ | none (mechanism only) | mechanism must show **unpredictability**, not reduced sharing |
| baseline ×4 (v19–v22 or in-place) | 4-10…4-13 | D | ❌ | baseline run histories / `baseline_comparison.csv` | D1 decision; restyle to canonical; pre-flight vs Table 4-10 |
| v10_sota_comparison.png | 4-14 | D | ⚠️ | hardcoded/†estimated | D2 decision; if kept, pre-flight vs Table 4-10/4-11; if rebuilt, drop estimated + Aloor |

---

## 8. Execution order and gates

1. **Lead answers D1–D5.**
2. **B (v17)** → verified PNG; thesis re-point REVERSED 2026-08-16 (keeps legacy `results/qtable_heatmaps.png`); docs synced (G1/G3/G4).
3. **C (consistency sweep)** → deliver discrepancy report → **Lead triages** → fix only approved items.
4. **D + E (styling + readability)** per decisions.
5. **F (thesis call-outs / re-pointing)** — text edits after figure work settles.
6. **G (doc sync)** — last, so nothing goes stale again.

**Gate rule:** after each regenerated figure, run `python generate_all_Visuals2.py -W error::UserWarning`
(deliberate UserWarning-as-error) and visually read the output PNG. For any content-affecting change,
paste before/after and cite the data source in the report.

## 9. Reporting standard

Same as every other agent here: paste the actual before/after, cite the data source for every number
touched, report mismatches with both values side by side, one task at a time — flag extras
separately and let them be triaged.
