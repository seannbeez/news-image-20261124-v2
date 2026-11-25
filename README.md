# news-image-20261124 v2 — "TUESDAY 24 NOVEMBER 2026"

One-image broadsheet of Tuesday 24 November 2026's world news, built under
Fura's Master System Instruction (Classic Financial Broadsheet: cream
#F6F2E9, Deep Navy #1E293B, Terracotta #B91C1C, serif).

- **32 stories, all verified live 25 Nov 2026** (3 heroes + 5 secondary +
  24 ALSO, nos. 9–32). Heroes: China probes Shanghai party chief Chen
  Jining; Dow closes 50,018.70 above 50,000 as the AI rally fades; Sanofi
  buys Insmed for $41bn. Full verified list with sources:
  `V2_NEW_RULES_PREP.md` in the builder work dir (not vendored here).
- **Structure:** giant-date masthead → THE DAY IN UTC timeline → THE DAY
  IN NUMBERS (6 giant numbers: 50,019 / $41BN / 5,258 / 60 KM / +6.32% /
  24) → 3 hero cards with procedural inked vector art → 5 secondary cards
  (each with its own icon) → world map WHERE IT HAPPENED + ALSO index →
  DATE CHECK ribbon (incl. the Hormuz tanker-fire trap: a Wed 25 Nov
  claim, NOT 24 Nov news).
- **Candidates:** `cand_v2_A.png` (editorial — Chen focal) and
  `cand_v2_B.png` (market — Dow 50,019 chart focal). `entry.png` is
  currently candidate A; the A/B blind duel could not run in the build
  session because the Gemini judge pool was 429-exhausted for the UTC day
  (see report) — **status: HOLD, do not submit this repo as-is.**
- **Program:** `main.py` (Python 3.13, stdlib only) copies `entry.png` to
  the output dir. No network, deterministic, byte-identical across runs.
- **Build:** `python3 build_v2.py` regenerates both candidates from
  scratch (Pillow only) and fails the build on any text overflow,
  truncation or overlap. Verified: two rebuilds byte-identical;
  184,500 / 185,465 bytes (≤1 MiB); 1024×1024.

## License

MIT — see `LICENSE`.
