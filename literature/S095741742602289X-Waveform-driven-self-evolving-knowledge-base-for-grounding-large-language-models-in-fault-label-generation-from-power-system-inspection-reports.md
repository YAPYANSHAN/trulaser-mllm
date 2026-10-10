# Waveform-driven self-evolving knowledge base for grounding large language models in fault label generation from power system inspection reports

- **Citation (IEEE):** H. Wu, Q. Cui, J. Wang, et al., "Waveform-driven self-evolving knowledge base for grounding large language models in fault label generation from power system inspection reports," *Expert Systems With Applications*, vol. 331, Art. no. 133380, 2026, doi: 10.1016/j.eswa.2026.133380.
- **Domain:** Industrial (power system) fault diagnosis / LLM text labelling grounded by signals
- **Relevance to FYP (1-5):** 4 - a local LLM that reasons over maintenance text, grounded by physical sensor evidence that automatically refines its knowledge base. This maps directly onto using machine data to ground LLM fault diagnosis.

## Problem
Transmission-line inspection reports (IRs) are unstructured and inconsistently worded, so fault-cause labelling depends on experts. LLMs hallucinate in specialised domains. Expert-written knowledge bases (KBs) are often misaligned with how LLMs reason, and utilities are unwilling to send sensitive data to cloud LLMs.

## Data & modalities
- Real-world inspection reports (text) labelled into four fault causes: conductor galloping (CG), lightning strike (LS), insulator flashover (IF) and foreign object (FO). The historical set includes 279 LS, 200 IF and 222 FO cases plus CG cases.
- An independent unseen test set of 221 IRs (59 CG, 60 LS, 30 IF, 72 FO).
- Fault waveforms are physics-based simulated signals (e.g., lightning current amplitude drawn from a probability distribution, arc and resistance parameters) paired with the reports.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Inspection Report Analysis Framework (IRAF):
1. A Noise-Robust Chain-of-Thought (NR-CoT) prompt guides a locally deployed LLM (DeepSeek-R1:7B, temperature 0.1) to produce latent labels despite noisy wording.
2. Waveforms grouped under each latent label are clustered with K-means (elbow method). Representative samples from inconsistent clusters trigger LLM re-evaluation.
3. The LLM rewrites or updates the expert KB (fault definitions and priority rules, e.g., "explicit lightning evidence outranks flashover traces") over iterative rounds, with no manual rule edits.
4. Final labels are generated with the evolved KB.
There is no fine-tuning; the approach relies on prompting and KB evolution.

## Results (key numbers and metrics)
- **Historical IRs:** IRAF reaches 91.23% ± 1.75% overall accuracy and 91.19% macro recall, compared with:
  - vanilla LLM: 42.58%
  - NR-CoT only: 64.78%
  - static expert KB: 22.82 points below IRAF
  - random KB evolution: 81.29%
- **Generalisation:** the updated KB generalises to the unseen IRs; 94.57% accuracy is reported in one setting.
- **Robustness:** it stays robust under class imbalance (88.75% at imbalance ratio 2) and under label noise (88.49% when the noise is set to 10%).

## Limitations
- The waveforms are simulated, not field-measured.
- Only four fault classes are covered.
- Broad class definitions (e.g., foreign object vs. bird-related flashover) still cause confusion.
- KB evolution depends on clustering quality and on the reasoning of a small LLM.
- Future work: more autonomous KB evolution.

## Transferable ideas for the FYP pipeline
- **LLM reasoning + text/RAG:** keep a structured fault-rule KB for TruLaser (dross, burr, incomplete cut, bevel-angle error) in the prompt, and let it self-evolve. Cluster machine-table signatures (laser power, feed, gas pressure, alarm sequences) within each LLM-assigned label, then send inconsistent clusters back to the LLM to revise rule definitions and priorities.
- **Tabular/time-series:** use physical process data as an independent "evidence channel" that checks the text- or image-based diagnosis.
- **Deployment:** a local 7B reasoning model (DeepSeek-R1-distill) at low temperature for data-privacy-sensitive factory data.
- **Evaluation:** ablation ladder of vanilla, CoT, static KB and evolved KB; test on unseen reports; stress-test imbalance and label noise.
