# Anti-APhish: A robust and adaptive detection approach against evolving AI-powered phishing URLs

- **Citation (IEEE):** Z. Zhang, Y. Yang, N. Lu, et al., "Anti-APhish: A robust and adaptive detection approach against evolving AI-powered phishing URLs," *Expert Systems With Applications*, vol. 331, Art. no. 133324, 2026, doi: 10.1016/j.eswa.2026.133324.
- **Domain:** Cybersecurity; URL-based phishing detection under adversarial mutation and concept drift.
- **Relevance to FYP (1-5):** 1 - Unrelated domain; only the concept-drift detection and LoRA-based incremental update with clustered core samples are loosely transferable to machine-data drift.

## Problem
LLM/AI-generated phishing URLs (A-PURLs) systematically mutate URL structure, defeating blacklists, handcrafted-feature ML, and DL detectors that rely on surface semantics. Detectors must handle spatial adversarial shift and temporal concept drift simultaneously ("dual distribution shifts").

## Data & modalities
URL strings only. Pools: 4.6M benign URLs (Alexa domains), 3.3M phishing URLs (PhishTank, OpenPhish, Kaggle, 2023 to Apr 2026), 2.1M A-PURLs (wild, PMG-synthesised, and LLM-generated under a controlled attacker-prompt protocol). Multiple datasets with strict distributional, temporal and attack-pattern separation.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
(1) Phishing Mutation Grammar (PMG): character-, token- and structure-level mutation operators (homoglyphs, typosquatting, subword insertion/exchange, domain concatenation) for controlled adversarial augmentation. (2) MASCoNet: convolution-attention network with Token-Property embeddings marking nine URL structural roles (protocol, subdomain, domain, TLD, paths, query name/value, fragment). (3) Drift-aware incremental adaptation: sliding windows (s=800, stride 200) over streaming data; drift flagged by chi-square test (<0.05) plus magnitude thresholds (mean diff >0.1 or variance diff >0.15) on block features; uncertain samples clustered, centroid-nearest core samples manually labelled; LoRA updates on global attention layers. LLMs used only to generate test attacks; baselines include URLNet, LSTM, URLBert.

## Results (key numbers and metrics)
- 97.57% accuracy, 0.9517 MCC under 20% A-PURL exposure.
- Zero-shot on LLM-generated PURLs: 94.76% accuracy, 0.8976 MCC.
- Without PMG augmentation, LSTM recall 12.47%, URLNet 18.87%, MASCoNet/URLBert ~35% on LLM-PURLs; PMG augmentation lifts recall 40-50% across all models.
- Incremental adaptation cuts manual labelling by 88% while maintaining performance; incremental updates take few epochs (e.g., 3 epochs, tens of seconds) vs. full retraining (50 epochs, thousands of seconds).

## Limitations
PMG is a bounded proxy and does not cover all unconstrained LLM generation; URL-only (no page content); drift thresholds calibrated once on a validation set; still requires some manual labels.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series / deployment:** Sliding-window drift detection combining a significance test with effect-size thresholds - useful to flag when TruLaser sensor/parameter distributions shift (new material batch, worn nozzle) before trusting diagnoses.
- **Vision/LLM fine-tuning:** Active selection of representative uncertain samples (clustering) for technician labelling, then LoRA updates rather than full retraining.
- **Data ingestion:** Structural role tagging of tokens (here URL parts) - analogous to tagging fields in machine logs/tables before encoding.
- **Evaluation:** Keep strict temporal splits to test generalization to future data, not random splits.
