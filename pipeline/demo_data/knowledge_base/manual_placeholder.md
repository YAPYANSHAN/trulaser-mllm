# Troubleshooting guide (PLACEHOLDER - replace with the real TRUMPF TruLaser 3000 documentation)

## Dross on the bottom edge
Symptom: droplets or a burr of re-solidified melt hanging under the cut.
Causes: gas pressure too low; cutting speed too high for the thickness; focus position too high; worn or damaged nozzle.
Remedy: increase gas pressure towards the cutting-table value; reduce cutting speed in steps of 5-10 %; lower the focus position; inspect the nozzle.

## Rough cut face / deep striations
Symptom: irregular drag lines, rough cut surface, roughness above tolerance.
Causes: cutting speed too low; focus position wrong; nozzle worn or off-centre; contaminated protective glass.
Remedy: adjust cutting speed towards the table value; check focus position; replace the nozzle after many operating hours; clean the protective glass.

## Incomplete cut / loss of cut
Symptom: the sheet is not cut through, sparks fly upward.
Causes: cutting speed too high relative to laser power; laser power too low; dirty protective glass reducing power at the workpiece.
Remedy: reduce cutting speed or increase laser power; clean or replace the protective glass.

## Burn-out / overheating
Symptom: wide kerf, burned corners, discoloured edges, temperature alarm E_TEMP.
Causes: cutting speed too low for the laser power; excessive heat input in corners.
Remedy: increase cutting speed or reduce laser power; check the cooling; review corner strategies.

## Bevel angle deviation
Symptom: bevel face angle or land outside tolerance, axis alarm E_AXIS.
Causes: bevel axis calibration drift; nozzle standoff incorrect; collision of the cutting head.
Remedy: recalibrate the bevel axis; set the nozzle standoff to the nominal value; re-measure the part.

## Alarm E_GAS
Meaning: assist-gas pressure fell below the set value during cutting.
Remedy: check the gas supply and regulator; re-run the job after the pressure is stable.
