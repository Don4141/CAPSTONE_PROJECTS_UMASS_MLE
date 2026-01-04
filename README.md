![Python](https://img.shields.io/badge/Python-3.9+-blue)
![ML](https://img.shields.io/badge/Machine%20Learning-XGBoost%20%7C%20Keras-green)

# Structure-Informed Prediction of Missense Variant Pathogenicity

### Overview

This project implements an end-to-end applied machine learning system for predicting the pathogenicity of human missense variants using protein structural information derived from AlphaFold-predicted 3D structures. The motivation is to overcome the limitations of existing variant-effect predictors that rely on static, precomputed scores and cannot evaluate previously uncharacterized variants.
The pipeline dynamically generates mutation-specific structural energy features using FoldX, constructs a reproducible feature matrix, and trains supervised ML models to classify variants as benign or pathogenic. The system is designed with a strong emphasis on reproducibility, scalability, model interpretability, and deployability, culminating in a production-grade web application built with FastAPI and Streamlit.
Pipeline

The workflow consists of five modular stages:
### 1. Data Preparation

	Input variants sourced from ClinVar-labeled benign/pathogenic datasets.

	Variants parsed from HGVSp notation into reference residue, position, and mutant residue.

	Variants split into Train/Test × Benign/Pathogenic subsets using predefined dataset labels.

### 2. Structure Resolution

	Gene symbols resolved to UniProt accession IDs.

	AlphaFold-predicted protein structures downloaded programmatically.

	Variants mapped to corresponding protein structures.

### 3. Feature Engineering (Structural)

	FoldX BuildModel used to compute mutation-induced stability changes (ΔΔG).

	FoldX PositionScan used to assess energetic sensitivity across mutation sites.

	Raw energy outputs parsed and aggregated into structured feature tables.

	Wild-type and mutant energies aligned and differenced to produce final features.

### 4. Model Training & Evaluation

	Dimensionality reduction performed using an autoencoder (TensorFlow/Keras).

	Final classification performed using XGBoost.

	Model evaluation conducted using held-out test data and independent deep mutational scanning (DMS) benchmarks.

	Feature importance analyzed to assess biological interpretability.

### 5. Inference & Deployment

	Trained model artifacts versioned and loaded by a FastAPI backend.

	Predictions served via a REST API and visualized through a Streamlit frontend.

### Results

The final model demonstrates strong discriminative performance in classifying missense variants:

	AUROC: ~0.93 on labeled test data

	Accuracy: ~0.85 
	Independent validation: High Spearman correlation with functional scores from deep mutational scanning experiments

	Key contributors: Relative solvent accessibility and mutation-induced stability changes (ΔΔG)

Feature importance analysis confirms that structurally meaningful variables drive predictions, supporting biological plausibility in addition to predictive accuracy.

### Deployment & System Architecture

This project is deployed as a two-tier applied ML system separating inference logic from user interaction.

### Architecture Diagram (Conceptual)
+--------------------+
|   Streamlit UI     |
|  (User Interface)  |
+---------+----------+
          |
          | HTTP POST (JSON)
          v
+---------+----------+
|   FastAPI Backend  |
|  - Input validation|
|  - Preprocessing   |
|  - Autoencoder     |
|  - XGBoost model   |
+---------+----------+
          |
          | Prediction (JSON)
          v
+--------------------+
|  Model Artifacts   |
| (versioned files)  |
+--------------------+

### System Components
### FastAPI Backend (Render)
	Validates inputs using Pydantic schemas.

	Applies scaling and dimensionality reduction.

	Runs XGBoost inference and returns predictions (0 = Benign, 1 = Pathogenic).

### Streamlit Frontend (Streamlit Community Cloud)

	Collects user inputs.

	Displays predictions and visual feedback in real time.

### Model Artifacts

	Autoencoder (.keras), XGBoost model (.pkl), scaler, and feature metadata.

	Versioned for reproducibility and rollback.

## 1. Create environment
conda env create -f environment.yml

conda activate sigma-ml

## 2. Prepare variant datasets
python parse_HGVSp_col.py

bash remove_HGVSp_col.sh

## 3. Download AlphaFold structures
python fetch_uniprot_ids.py

python download_alphafold_pdbs.py

## 4. Run FoldX feature generation
bash run_FoldX.sh

## 5. Train and evaluate model
python train_model.py

## 6. Launch frontend (optional)
streamlit run app.py

### Limitations

	Dependence on AlphaFold-predicted structures introduces uncertainty for highly flexible or disordered regions.

	FoldX computations are CPU-intensive and limit large-scale real-time inference.

	Current model focuses on missense variants and does not handle indels or splice-site variants.

### Future Work

	Replace FoldX-based features with learned structural embeddings (e.g., graph neural networks).

	Add batch inference and caching to support large-scale variant screening.

	Integrate uncertainty quantification and calibration analysis.

	Extend support to additional variant classes and multi-isoform handling.

	Containerize services for cloud-native scaling (Docker/Kubernetes).

### Why This Project Matters (Applied ML Perspective)

	Demonstrates end-to-end ML ownership: data → features → model → deployment

	Emphasizes reproducibility, validation, and interpretability

	Integrates domain-specific feature engineering with modern ML tools

	Designed as a production-style system, not a research notebook
