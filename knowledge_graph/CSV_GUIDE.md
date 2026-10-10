# What the example CSV files mean

The example data pretends to be **one TruLaser machine in a factory over 3 weeks (1 to 19 Sep 2026)**. It is all made up, but it is built to look like the records a real factory keeps.

The easiest way to understand it is to follow **one job** through every file. We use job **J0071**: one part cut on 5 Sep, on the afternoon the gas supply went wrong.

---

## The 7 files in one picture

Think of the files as answers to three questions:

| Question | Files |
|---|---|
| **What happened on the machine, and when?** | `events.csv`, `jobs.csv` |
| **What did the cameras see?** | `photos.csv`, `videos.csv` |
| **What does the manual say?** | `knowledge.csv`, `alarm_causes.csv`, `component_causes.csv` |

The knowledge graph joins these three groups together. That joining is the whole point of your MMKG.

---

## Group 1: what happened on the machine

### `events.csv`: the machine's diary (494 rows)

One row is **one thing that happened**, with the time it happened. It is like a logbook, in time order. There are 4 kinds of event (column `type`):

| type | What it means | Rows |
|---|---|---|
| `Job` | The machine started cutting a part | 240 |
| `Inspection` | Someone checked the finished part and wrote down the result | 240 |
| `Alarm` | The machine showed a warning | 9 |
| `Maintenance` | A technician repaired or replaced something | 5 |

Here is the diary around job J0071:

```
event_id  type        timestamp         job_id  result  code   text                                  
EV0141    Alarm       2026-09-05 10:28  J0071           E_GAS  assist gas pressure below set value
EV0142    Job         2026-09-05 10:28  J0071                                                        
EV0143    Inspection  2026-09-05 10:51  J0071   dross                                                
```

In plain words: at 10:28 the machine started cutting J0071 and at the same moment warned that the gas pressure was too low. At 10:51 an inspector found **dross** (melted metal stuck under the cut edge).

And here is what maintenance rows look like:

```
EV0169  Maintenance  2026-09-08 08:00   action: gas supply regulator repaired   component: gas supply
EV0170  Maintenance  2026-09-08 08:00   action: nozzle replaced                 component: nozzle
```

The columns:
- `event_id`: a unique name for the event.
- `type`: one of the four kinds above.
- `timestamp`: date and time.
- `job_id`: which part it belongs to (empty for maintenance).
- `result`: the inspection result (`ok` or a defect name).
- `code` and `text`: the alarm code and its message.
- `action` and `component`: what was repaired, and which machine part.

**Why it matters:** this file is what makes the graph *event-centric*. Because every row has a time, the graph can ask "what happened just before this defect?"

### `jobs.csv`: the settings for each cut (240 rows)

One row is **one part that was cut**, with the machine settings used.

```
job_id  start             material   thickness_mm  laser_power_w  cutting_speed_mm_min  gas_pressure_bar  bevel_angle_deg  nozzle_jobs_since_change  glass_jobs_since_clean  defect
J0071   2026-09-05 10:28  stainless  12.0          4754           1354                  8.25              0.0              70                        70                      dross
```

| Column | Meaning | J0071 |
|---|---|---|
| `material`, `thickness_mm` | What sheet was cut | 12 mm stainless steel |
| `laser_power_w` | Laser power in watts | 4754 W |
| `cutting_speed_mm_min` | How fast the head moved | 1354 mm per minute |
| `gas_pressure_bar` | Pressure of the gas that blows molten metal out of the cut | **8.25 bar, but stainless normally uses about 15**, so it is too low |
| `bevel_angle_deg` | 0 means a straight cut, 30 or 45 means an angled (bevel) cut | 0, straight |
| `nozzle_jobs_since_change` | How many parts the nozzle has cut since it was last replaced (wear) | 70, an old nozzle |
| `glass_jobs_since_clean` | How many parts since the protective glass was cleaned (dirt) | 70 |
| `defect` | The inspection result (the "answer") | dross |

**Why it matters:** these are the numbers your **table model** learns from.

---

## Group 2: what the cameras saw

### `photos.csv`: one photo of each finished part (240 rows)

```
photo_id  job_id  file                     model_label  confidence  embedding
PJ0071    J0071   media/photos/J0071.png   dross        0.56        0.866;0.101;0.975; ... (64 numbers)
```

- `file`: where the picture is, in the `media/photos` folder. Open it to see it.
- `model_label`: what the **image model** thinks the defect is from the photo. Here it is dross.
- `confidence`: how sure the model is, from 0 to 1. Here 0.56, so not very sure.
- `embedding`: 64 numbers that summarise what the photo looks like. Photos that look alike have similar numbers. This is what lets the graph find **similar past photos** (question Q5).

### `videos.csv`: one video of the cutting process (240 rows)

```
video_id  job_id  file                     model_label  unusual_signal
VJ0071    J0071   media/videos/J0071.mp4   ok           sparks fall below the cut
```

- `model_label`: what the **video model** thinks. Here it says `ok`, so it **disagrees** with the photo model. This happens in real life too, and it is why your pipeline has a fusion step and can answer "unknown".
- `unusual_signal`: what looked different from a normal cut, in words. "Sparks fall below the cut" is a typical sign of dross.

---

## Group 3: what the manual says

These files are the "textbook" knowledge. In the real project they come from the TRUMPF manual's troubleshooting section. Here they are placeholders.

### `knowledge.csv`: defect, then cause, then fix (25 rows)

Each row is one fact, written as **subject, relation, object**, plus where it came from (`source`).

```
subject           relation   object              source
dross             CAUSED_BY  low_gas_pressure    Troubleshooting guide, section 'Dross on the bottom edge'
dross             CAUSED_BY  speed_too_high      ...
dross             CAUSED_BY  focus_too_high      ...
dross             CAUSED_BY  worn_nozzle         ...
low_gas_pressure  FIXED_BY   adjust_gas_pressure ...
```

Read it as sentences: "Dross can be caused by low gas pressure, too high speed, wrong focus or a worn nozzle", and "low gas pressure is fixed by adjusting the gas pressure".

### `alarm_causes.csv`: what each alarm points to (3 rows)

```
code    cause
E_GAS   low_gas_pressure
E_AXIS  bevel_axis_drift
E_TEMP  power_too_high
```

This is the **bridge between the diary and the manual**. It is how the graph knows that an `E_GAS` alarm in `events.csv` is evidence for the cause `low_gas_pressure` in `knowledge.csv`.

### `component_causes.csv`: which machine part can cause what (4 rows)

```
component         cause
nozzle            worn_nozzle
protective glass  dirty_protective_glass
gas supply        low_gas_pressure
bevel axis        bevel_axis_drift
```

This is the bridge for maintenance. "Nozzle replaced" in the diary means the cause `worn_nozzle` has just been fixed.

---

## Putting J0071 together

This is what the graph can say about J0071 by joining all the files. The pipeline would do this automatically:

1. **Inspection** (`events.csv`) found **dross** at 10:51.
2. **Photo** (`photos.csv`) agrees it is dross, but the model is only 56% sure. **Video** (`videos.csv`) says ok, but saw sparks falling below the cut.
3. The **manual** (`knowledge.csv`) says dross has 4 possible causes.
4. Which cause is it? **Machine settings** (`jobs.csv`) show gas pressure 8.25 bar, about half the normal value. The **diary** (`events.csv`) shows an `E_GAS` alarm at 10:28. `alarm_causes.csv` links E_GAS to `low_gas_pressure`.
5. So the most likely cause is **low gas pressure**, and the fix from `knowledge.csv` is **adjust gas pressure**.
6. The diary also shows that the E_GAS alarms happened only on 5 Sep and that the gas regulator was repaired on 8 Sep. That fits the story of a gas-supply fault.

No single file could tell you this. Only the files **linked together** can, and the knowledge graph is what links them.

---

## How this maps to your real data later

| Example file | What it will be in the real project |
|---|---|
| `jobs.csv` | The TruLaser machine-database export (one row per job) |
| `events.csv` | The machine's alarm log, maintenance records and quality-inspection records, all with times |
| `photos.csv`, `videos.csv` | Your cut-edge photos and process videos, plus what your trained models say about them |
| `knowledge.csv`, `alarm_causes.csv`, `component_causes.csv` | Facts taken from the TRUMPF manuals and checked by an engineer |
