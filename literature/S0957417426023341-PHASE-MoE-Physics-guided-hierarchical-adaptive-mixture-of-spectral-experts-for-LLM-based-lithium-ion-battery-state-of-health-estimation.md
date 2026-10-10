# PHASE-MoE: Physics-guided hierarchical adaptive mixture of spectral experts for LLM-based lithium-ion battery state of health estimation

- **Citation (IEEE):** Y. Jiang, J. Hou, P. Li, et al., "PHASE-MoE: Physics-guided hierarchical adaptive mixture of spectral experts for LLM-based lithium-ion battery state of health estimation," *Expert Systems With Applications*, vol. 331, Art. no. 133425, 2026, doi: n/a.
- **Domain:** Prognostics and health management (battery SOH) / LLM fine-tuning for time series
- **Relevance to FYP (1-5):** 2 - battery regression, but shows how to fine-tune an LLM on numeric sensor sequences with physics priors and parameter-efficient MoE-LoRA.

## Problem
LLM-based SOH estimation struggles with full-lifecycle data. The specific issues are heterogeneity across degradation stages, inefficient fine-tuning and physically inconsistent (non-monotonic) predictions.

## Data & modalities
Four public battery datasets (CALCE, HUST, TJU, XJTU). The inputs are charge/discharge cycle measurements and incremental-capacity (IC) curves, so the data are numeric time series only.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Incremental Capacity Analysis (ICA) features are clustered with K-means into degradation stages. The clusters give a probabilistic physical prior for routing.
- Numeric inputs are mapped by a linear projection directly into the Transformer hidden space, bypassing tokenisation.
- A hierarchical mixture of "spectral experts" is built in the residual SVD spectral space of the frozen LLM's weights. The experts are MoELoRA-style low-rank modules with SVD-based initialisation instead of random initialisation.
- The upper gate is aligned to the degradation stages via a KL-divergence constraint. The lower gate is sparse and data-driven to handle operating-condition fluctuations.
- A multi-level loss adds a global monotonicity penalty, hierarchical constraints and load balancing.
- Backbone: Qwen3-8B, with only 0.51% of its parameters trained. Llama3.1 and others were compared as backbones.

## Results (key numbers and metrics)
- Minimum RMSE is 0.003597, a 49.3% reduction versus the second-best model (Mamba) on that dataset. TJU RMSE is 0.003663 in the within-dataset setting.
- In the backbone comparison, Qwen3 gives the best results (TJU RMSE 0.005576 vs. 0.007261 for Llama3.1).
- Leave-one-dataset-out (LODO) cross-domain tests show strong generalisation. Ablations confirm each component.

## Limitations
- Restricted to SOH regression on lab datasets.
- Requires ICA features specific to battery chemistry.
- An 8B backbone is heavy for embedded BMS use.
- Cross-domain robustness is less stable in some settings (e.g., RMSE 0.042423, MAPE 4.96% in one LODO case).

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** project numeric machine-table features (laser power, feed rate, gas pressure, focal position) straight into LLM hidden space via a linear layer, instead of serialising them to text.
- **Fusion / LLM fine-tuning:** route MoE-LoRA experts by a physics or process-regime prior, e.g., material and thickness class or bevel vs. straight cut, so experts specialise per regime.
- **Evaluation:** add physics-consistency checks to the loss or post-hoc validation (e.g., monotonic trends in kerf width vs. power), and use LODO-style splits (per material or per machine) to test generalisation.
