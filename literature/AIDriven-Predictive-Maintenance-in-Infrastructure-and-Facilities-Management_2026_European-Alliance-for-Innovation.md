# AI-Driven Predictive Maintenance in Infrastructure and Facilities Management

- **Citation (IEEE):** S. B. Masud, H. M. Sozib, K. P. Mishu, et al., "AI-Driven Predictive Maintenance in Infrastructure and Facilities Management," *EAI Endorsed Transactions on AI and Robotics*, vol. 5, 2026, doi: 10.4108/airo.9975.
- **Domain:** Industrial predictive maintenance / tabular machine-failure classification
- **Relevance to FYP (1-5):** 3 - classic ML on machine operating data (torque, speed, temperature, tool wear) with failure-mode labels; a practical baseline for the tabular branch, though no images, LLM or laser-specific data.

## Problem
Reactive or fixed-schedule maintenance causes unexpected downtime and cost; the study evaluates ML models for proactive prediction of failure occurrence and failure type.

## Data & modalities
Tabular sensor/operational data: UCI synthetic predictive-maintenance dataset (10,000 instances, 14 features): product type (low/medium/high), air and process temperature, rotational speed, torque, tool wear, with failure modes (tool wear failure, heat dissipation, power failure, overstrain, random failures). Strong class imbalance.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Preprocessing: feature scaling, label/custom encoding, SMOTE oversampling for minority failure classes.
- Models: logistic regression, K-Nearest Neighbours, Support Vector Classifier, Random Forest, XGBoost for multiclass failure prediction.
- Interpretability: PCA (3D) visualisation of failure-mode separability and permutation feature importance.
- No deep learning, LLM or multimodal fusion.

## Results (key numbers and metrics)
- XGBoost best: 98.9% accuracy, AUC near 1.0, F1 above 0.98 on validation and test sets.
- RFC and SVC: precision and recall above 95%; KNN about 96.6% accuracy with fast inference.
- Torque, rotational speed and tool wear most important; product type contributes little. PCA shows tool-wear failures separate on a tool-wear component, power failures on a power component.

## Limitations
Synthetic dataset (not real plant data), so near-perfect scores may not transfer; no temporal modelling or remaining-useful-life estimation; integration, cybersecurity and interoperability challenges noted but not tested.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** use XGBoost/Random Forest on TruLaser job/parameter tables (laser power, feed rate, gas pressure, nozzle hours, lens hours, sheet thickness) as a fast, strong baseline predictor of defect/failure class.
- **Data ingestion:** apply scaling, categorical encoding and SMOTE for rare fault classes; keep a real (not synthetic) hold-out test.
- **LLM reasoning:** pass permutation feature importances and PCA cluster membership to the LLM as explanatory evidence ("tool wear / nozzle age is the top contributor").
- **Deployment:** KNN-style light models where real-time inference on an edge PC is required; XGBoost for accuracy.
