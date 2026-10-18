# Data handover: Laser Cell 2 (TruLaser 3000)

This folder is everything the production team handed over for the project. It covers six weeks of production, from 1 September to 10 October 2026, on one machine.

> **This data is synthetic.** It was generated to behave like a real factory export, including the gaps and inconsistencies. It contains no real company or TRUMPF data, and the guide in `documents/` is not a TRUMPF manual.

## What the team asked for

> "We get cut-quality problems every week and it takes too long to find out why. We would like a tool that looks at a job and tells us what went wrong, why, and what to change, with evidence we can check. Here is what we have."

Nobody has labelled the root causes. The team only knows what the inspectors wrote down.

## What you have

| File | What it is | Rows / files | Notes from the team |
|---|---|---|---|
| `machine/job_log.csv` | Export from the machine database, one row per job | ~530 jobs | Separator is `;` and decimals use a comma (German export). Times are `dd.mm.yyyy`. Gas pressure is the **set** value, not the measured one. |
| `machine/alarm_log.txt` | Every machine message with a timestamp | ~400 lines | Most are routine INFO messages. Not linked to job IDs, only to time. |
| `maintenance/maintenance_log.xlsx` | Maintenance book, typed up from the paper book on the machine | ~45 entries | Written by operators in their own words. Some entries have no time. Not every action was written down. |
| `quality/inspection_records.csv` | Quality inspection sheet | ~420 jobs | Not every job was inspected. Defect names are free text, so the same defect is spelled several ways. Some job IDs were typed differently. Dross height, Ra and bevel angle were only measured sometimes. |
| `quality/photos/` | Photo of a cut edge, named by job ID | ~380 images | Taken by phone on the inspection bench, so lighting varies and a few are blurry or named oddly. |
| `process_video/` | Short clip from the coaxial process camera, named by job ID | ~200 clips | The camera was installed on 14 September and only records when storage allows, so about half the jobs from then on have a clip. |
| `documents/troubleshooting_guide.pdf` | Internal cut-quality troubleshooting guide | 3 pages | Symptoms, causes, remedies, machine message codes, maintenance intervals. |
| `documents/cutting_table.csv` | Recommended cutting parameters per material and thickness | 13 rows | Starting values. Operators adjust them. |

## Words you will see

- **Dross**: molten metal that sticks to the bottom edge of the cut.
- **Striations**: the fine lines on a cut edge. Heavy or bent lines mean a rough cut.
- **Bevel**: cutting at an angle instead of straight down. This machine can tilt the head.
- **Protective glass**: a cheap window that protects the lens from spatter. When dirty it absorbs laser power.
- **Nozzle**: the copper tip the gas and beam come out of. It wears with use.
- **Ra**: surface roughness in micrometres. Higher is rougher.
- **NOK**: "not OK", a failed inspection.

## Things the team mentioned

- "Stainless jobs had a lot of dross at some point in September."
- "There was a head crash in October."
- "The late shift sometimes runs a faster program when an order is late."

## Rules

- Do not edit these files. Write cleaned or derived data somewhere else (for example a `data/processed/` folder), so you can always go back to the original.
- The repository is public. Real company data must never be committed; keep it in `data/`, which git ignores.
