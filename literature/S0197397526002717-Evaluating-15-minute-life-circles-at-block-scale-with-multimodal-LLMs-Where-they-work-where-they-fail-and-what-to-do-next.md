# Evaluating 15-minute life circles at block scale with multimodal LLMs: Where they work, where they fail, and what to do next

- **Citation (IEEE):** T. Wu, C. Shen, R. Wei, et al., "Evaluating 15-minute life circles at block scale with multimodal LLMs: Where they work, where they fail, and what to do next," *Habitat International*, vol. 178, Art. no. 103978, 2026, doi: 10.1016/j.habitatint.2026.103978.
- **Domain:** Urban planning / geospatial MLLM benchmarking
- **Relevance to FYP (1-5):** 2 — unrelated domain, but a useful protocol for benchmarking MLLMs on image + structured inputs and a clear finding that MLLMs are unreliable at metric/quantitative estimation.

## Problem
Block-scale evaluation of 15-minute life circles (15-LC) is fragmented between indicator computation, integrated interpretation and actionable recommendations. The authors ask whether MLLMs can perform integrated, auditable evaluation under the 5D framework (Density, Diversity, Design, Destination accessibility, Distance to transit), and where they fail.

## Data & modalities
216 policy-defined 15-LC units inside Shanghai's inner ring. GIS layers (POIs, road network, transit, land use, buildings) rendered as standardized semantic maps with fixed legend and ground sampling distance, plus textual task rules; expert ratings used as qualitative reference.

## Method
- Protocolized benchmark: standardized semantic-map image inputs, fixed prompts with explicit definitions/units, structured outputs covering quantitative metrics, qualitative 5D ratings and recommendations.
- Nine MLLMs across providers, generations and reasoning modes: GPT-4o, GPT-5.2 (thinking / non-thinking), Gemini (earlier generation and Gemini 3 thinking / non-thinking), Qwen2.5-VL, Qwen3-VL (thinking / non-thinking).
- Metrics: tolerance accuracy (TA/TR) and normalized error for quantitative tasks; rank agreement with experts for ratings. No fine-tuning or RAG.

## Results
- Best: Gemini-3 non-thinking, overall tolerance accuracy 0.682; Gemini-3 thinking TA 0.646.
- GPT models TA 0.570-0.584; Qwen3-VL non-thinking 0.506, Qwen2.5-VL 0.474.
- Counting/distribution-summary tasks most robust (TR = 0.73); scale-sensitive measurement worst (TR = 0.48-0.51).
- Newer generations better (TR 0.59 vs 0.54); "thinking" mode does not consistently improve quantitative accuracy but improves evidence organization.
- Ratings positively rank-correlated with experts but compressed (fewer extremes).

## Limitations
MLLMs unreliable for continuous ratio estimation, distance/area and network-geometric reasoning; errors rise with boundary complexity; score compression; authors state outputs must not drive regulatory decisions without GIS verification.

## Transferable ideas for the FYP pipeline
- **Vision / LLM reasoning:** do not let the MLLM estimate physical measurements (kerf width, dross height, bevel angle) from images; compute them with deterministic tools (OpenCV/metrology) and pass numbers to the LLM — the "tools anchor measurement, LLM integrates evidence" layered workflow.
- **Data ingestion:** standardize image inputs (fixed scale, legend, background, resolution) before prompting.
- **Evaluation:** benchmark several VLMs (proprietary vs open Qwen-VL) and reasoning on/off under one fixed protocol with tolerance-based accuracy and rank agreement with expert (technician) ratings.
- **Output design:** structured output schema (metrics, ratings, recommendations with evidence) for auditable process-optimisation advice.
