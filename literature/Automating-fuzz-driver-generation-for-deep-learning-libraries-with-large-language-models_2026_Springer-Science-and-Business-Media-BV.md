# Automating Fuzz Driver Generation for Deep Learning Libraries with Large Language Models

- **Citation (IEEE):** T. Zheng, F. Meng, P. Yi, et al., "Automating fuzz driver generation for deep learning libraries with large language models," *Cybersecurity*, vol. 9, art. 7, 2026, doi: 10.1186/s42400-025-00532-9.
- **Domain:** Software security / LLM-based code generation and fuzz testing
- **Relevance to FYP (1-5):** 2 - unrelated domain (software testing), but its staged multi-agent pipeline with verification, issue diagnosis and repair loop is a transferable design for reliable LLM workflows.

## Problem
Prior LLM-based testers of deep-learning libraries (TitanFuzz, FuzzGPT) generate hard-coded test programs with low validity, and some approaches require continual LLM calls throughout testing, which is costly and impractical.

## Data & modalities
Text/code only: API documentation and source of PyTorch and TensorFlow (Python and native C/C++ layers); generated fuzz-driver programs; runtime logs, crashes, sanitizer reports and coverage data.

## Method
FD-FACTORY, inspired by an industrial production line, splits generation into eight stages: Preparation (extract API usage constraints), Initial Fuzz Driver Generation, Early Stop Checks, Verification (static analysis + execution), Issue Diagnosis, Decision Making, Repair Loop, and Deployment. Each stage is handled by a dedicated LLM agent or tool, with prompt templates per agent. Main experiments use gpt4-0613 (temperature 0.5); extended experiments with deepseek-chat-v3-0324 and Grok-Code-Fast-1. LLMs are used only before deployment - generated drivers are reused by the fuzzing engine without further LLM calls. Compared against TitanFuzz, FuzzGPT and LLM4FDG-DL.

## Results
Fuzz-driver generation success of 73.67% (PyTorch) and 65.33% (TensorFlow), 34.66-54.66% higher than prior approaches. Total line coverage of 308,351 (PyTorch) and 528,427 (TensorFlow) including native code. In LLM4FDG-DL, only 24.07% (58/241) of PyTorch drivers it considered valid passed the authors' stricter verification. Across 300 extended runs, average success was 91.67% for deepseek-chat-v3-0324 and 84.8% for Grok-Code-Fast-1; DeepSeek gave the best cost-performance trade-off.

## Limitations
Rediscovered existing bugs but found no new ones; empty seed banks; number of APIs and fuzzing time limited by token cost of multi-agent orchestration; oracles limited to crashes/exceptions/sanitizers (no semantic or numerical oracles); LLM security and data-leakage concerns.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** structure diagnosis as explicit stages (evidence gathering -> hypothesis -> verification against machine data/manual -> issue diagnosis -> decision -> repair/re-query loop), each a dedicated agent or tool with its own prompt, instead of one monolithic prompt.
- **Evaluation:** add automatic verification gates (e.g. check that cited parameter values exist in the machine database, units are valid, recommended settings lie in the TruLaser's allowed ranges) and count "valid output" rates, as the paper does with stricter verification exposing false positives.
- **Deployment:** use the LLM offline to generate reusable artefacts (e.g. diagnostic rules, SQL queries, checklists) so routine runtime checks on the machine do not need LLM calls; compare cost vs success across LLM providers.
