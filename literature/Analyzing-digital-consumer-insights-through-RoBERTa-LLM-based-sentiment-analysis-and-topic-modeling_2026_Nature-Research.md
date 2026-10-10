# Analyzing Digital Consumer Insights through RoBERTa LLM Based Sentiment Analysis and Topic Modeling

- **Citation (IEEE):** Q. Shasha, "Analyzing digital consumer insights through RoBERTa LLM based sentiment analysis and topic modeling," *Scientific Reports*, vol. 16, art. 18921, 2026, doi: 10.1038/s41598-026-48162-6.
- **Domain:** NLP / sentiment analysis / consumer behaviour analytics
- **Relevance to FYP (1-5):** 1 - review sentiment classification in e-commerce; only generic text-classification and SHAP/LIME explanation ideas transfer.

## Problem
Classical sentiment methods based on shallow lexical features miss contextual patterns in online reviews, and transformer approaches rarely provide interpretability for business decisions.

## Data & modalities
Text only: public Kaggle datasets - Amazon Fine Food Reviews and a Yelp review dataset.

## Method
Fine-tuned RoBERTa-Large (encoder transformer, described as an LLM) for sentiment classification. Baselines: classical ML and ensembles on TF-IDF features, deep models on sentence embeddings, and earlier transformers. Latent Dirichlet Allocation (LDA) for topic modelling of feedback themes. SHAP and LIME for global and local explanations. Phased training analysis and confidence-score visualisation.

## Results
RoBERTa-Large reached the highest accuracy, 93.59%, outperforming the TF-IDF ML, ensemble, sentence-embedding deep learning and earlier transformer baselines (per the abstract). Topic modelling identifies recurring themes in reviews.

## Limitations
Relies on public datasets that may not represent other domains or languages; computational cost limits very large-scale deployment; sentiment and topics modelled separately (a joint sentiment-topic model is future work); interpretability in multi-topic reviews is limited.

## Transferable ideas for the FYP pipeline
- **Text/RAG (ingestion):** LDA or BERTopic on operator logs / maintenance notes / service tickets to surface recurring fault themes for the TruLaser 3000 before building a fault taxonomy.
- **Tabular/text classification:** a fine-tuned encoder (RoBERTa-class) is a strong, cheap baseline for classifying free-text fault descriptions; compare against TF-IDF + classical ML as the paper does.
- **Evaluation / explainability:** SHAP and LIME token attributions as a baseline explanation method to contrast with LLM-generated reasoning.
