# When financial fine-tuning fails: A three-level detectability analysis of numerical hallucination in domain-adapted language models

- **Citation (IEEE):** X. Li and P. Liu, "When financial fine-tuning fails: A three-level detectability analysis of numerical hallucination in domain-adapted language models," *Neurocomputing*, vol. 706, Art. no. 135011, 2026, doi: 10.1016/j.neucom.2026.135011.
- **Domain:** NLP / financial LLMs, hallucination evaluation, domain fine-tuning
- **Relevance to FYP (1-5):** 3 — different domain, but a direct warning for the FYP: domain LoRA/QLoRA fine-tuning can make an LLM invent plausible numbers (e.g., laser power, pressures) not present in the evidence.

## Problem
Financial LLMs summarize reports where fabricated numbers are dangerous. It is commonly assumed that domain fine-tuning and numeracy training reduce numerical errors; the paper tests this under controlled fine-tuning.

## Data & modalities
Text only. Fine-tuning data: Category A (~1,000 domain-language samples, e.g., report/MD&A style), B (~500 financial concept QA), C (~2,000 numeracy-oriented samples). Evaluation set: 240 summarization samples (160 synthetic with controlled numerical grounding, 80 real-world 10-K excerpts).

## Method
- Base: Mistral-7B-Instruct-v0.2. Variants: FT-A (domain language) and FT-A+B+C (domain + concepts + numeracy), plus a volume-matched control (3,500 Category-A samples). All via QLoRA, single epoch, fixed hyperparameters.
- Three-level detectability taxonomy: L1 overt (currency-denominated fabrication), L2 covert-explicit (professional-convention numbers such as percentages/ratios), L3 covert-implicit (ungrounded quantitative claims).
- "Restraint gap" framework separating numerical competence (computing correctly) from numerical discipline (abstaining when ungrounded).

## Results
- Base: near-zero hallucination (5.4% L1, 3.8% L2, 17.9% L3*).
- FT-A: 82.5% L1 overt hallucination; FT-A+B+C: 90.8% L1 in the conclusion (abstract reports 98%).
- Numeracy supervision increased hallucination at every level despite improving arithmetic.
- Primary mechanism: template injection — memorized canonical values (e.g., "USD 3.3 billion", "growth of 11%") inserted regardless of input.

## Limitations
Single 7B model family; small evaluation set (240); partially synthetic data; single-epoch QLoRA only; no cross-scale analysis; mitigation methods (grounding-aware generation, abstention training) recommended but not tested.

## Transferable ideas for the FYP pipeline
- **Fine-tuning:** if LoRA-tuning an LLM on TRUMPF manuals or historical fault reports, always compare against the base model for ungrounded numbers; include "restraint" examples where the correct answer is "value not available in the data".
- **Evaluation:** adopt an L1/L2/L3-style check for the diagnosis reports: (L1) explicit parameter values with units not in the machine-database record, (L2) percentages/tolerances not in the documentation, (L3) vague quantitative claims ("pressure is too low") without supporting evidence.
- **LLM reasoning / RAG:** force every number in the output to be copied from retrieved tables or manual chunks (grounding check by string/value matching), else abstain.
- Prefer RAG over heavy domain fine-tuning for factual parameter recommendations.
