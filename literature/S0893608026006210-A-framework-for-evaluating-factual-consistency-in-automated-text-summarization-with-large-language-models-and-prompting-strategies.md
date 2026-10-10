# A framework for evaluating factual consistency in automated text summarization with large language models and prompting strategies

- **Citation (IEEE):** M. M. Islam and M. Oussalah, "A framework for evaluating factual consistency in automated text summarization with large language models and prompting strategies," *Neural Networks*, vol. 204, Art. no. 109160, 2026, doi: 10.1016/j.neunet.2026.109160.
- **Domain:** NLP / LLM evaluation (summarization factuality, hallucination)
- **Relevance to FYP (1-5):** 3 — not industrial, but gives a ready recipe (prompting strategies + atomic-fact metrics) for checking that LLM-generated diagnosis reports are faithful to the retrieved evidence.

## Problem
LLM summaries can be fluent but factually inconsistent; ROUGE/BLEU/BERTScore do not measure factual accuracy. Prior factuality evaluations mostly used zero-shot prompting only. The paper builds a framework to compare prompting strategies and factuality metrics across LLMs and domains.

## Data & modalities
Text only. Five datasets: CNN & Daily Mail (~287k articles), BBC News (2,225 documents), AggreFACT (10,000 annotated document-summary pairs), DialogSum (12,960 dialogues), LongSciVerify (270 PubMed/arXiv articles). No fine-tuning on evaluation data.

## Method
- Eight LLMs: GPT-3.5-Turbo, GPT-4o-Mini, LLaMA-2 7B, LLaMA-3.2 3B, Mistral 7B, Phi-3.5-Mini, Orca-2 7B, Vicuna 7B.
- Five prompting strategies: Zero-shot, Few-shot, Chain-of-Thought (CoT), Structured CoT (SCoT), Chain-of-Verification (CoVe).
- Factuality metrics: FActScore (atomic fact precision, scored with an LLM), LongDocFACTScore (LDFActs), AlignScore; compared with ROUGE/BLEU/BARTScore and human summaries.
- Standardized templates, fixed low temperature (T = 0.0 vs 0.3 ablation), three runs for proprietary models.

## Results
- Few-shot best in most domains except scientific literature; zero-shot better for semantic alignment (AlignScore).
- LLM summaries outperform human references: 67-98% factual consistency vs 17.8-86.3% for human summaries; >95% FActScore on aggregated claims; AlignScore 0.77-0.84.
- LLMs generate 2-10× more atomic facts than human references (completeness vs precision trade-off).
- LDFActs peak correlation 0.43 with human judgements, above ROUGE/BLEU.
- Conversational data hardest (AlignScore 0.19-0.64). CoT, SCoT and CoVe reduced hallucinations.

## Limitations
Prompt-wording sensitivity; may not generalize to technical documentation, legal or medical domains; model-specific behaviours (e.g., Mistral 7B few-shot sensitivity); FActScore relies on an LLM judge; metrics correlate only moderately with humans.

## Transferable ideas for the FYP pipeline
- **Evaluation:** decompose each generated fault-diagnosis report into atomic claims ("nozzle is damaged", "gas pressure below spec") and verify each against retrieved machine data and TRUMPF manual chunks (FActScore-style); report precision of supported claims.
- **LLM reasoning:** use Chain-of-Verification — draft diagnosis, generate verification questions, answer from evidence, revise — to reduce hallucinated causes.
- **Prompting:** test zero-shot vs few-shot (with example diagnoses) vs structured CoT under a fixed temperature, since the best strategy depends on the metric.
- **Text/RAG:** AlignScore-type models can automatically check alignment between the answer and retrieved documentation chunks.
