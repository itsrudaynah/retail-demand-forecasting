# Retail Demand Forecasting

## Project Overview

This project develops an end-to-end retail demand forecasting pipeline using the **Kaggle Store Sales — Time Series Forecasting** dataset from Ecuador.

The project covers:

- Data cleaning and exploratory analysis
- Time-series validation
- Baseline and machine-learning forecasting
- Hyperparameter tuning
- DeepAR probabilistic forecasting
- Demand-pattern evaluation and error analysis
- Final 15-day forecasting
- Replenishment analysis

Forecasting is performed at the **Store × Product Family** level.

### Final Forecast Setup

- Forecast horizon: **15 days**
- Validation period: **August 1–15, 2017**
- Final forecast period: **August 16–30, 2017**
- Evaluation/forecast series: **1,728 Store × Family series**
- Final forecast rows: **25,920**
- Primary metric: **RMSLE**
- Supporting metrics: **MAE, RMSE, WMAPE**

---

## Dataset

The project uses the Ecuadorian retail sales dataset containing:

- `train.csv` — historical sales
- `test.csv` — forecast dates and known features
- `stores.csv` — store metadata
- `oil.csv` — daily oil prices
- `holidays_events.csv` — holidays and events
- `transactions.csv` — store transaction counts
- `sample_submission.csv` — Kaggle submission format

The dataset contains **54 stores** and **33 product families**, giving **1,782 possible Store × Family combinations**.

The modeling and evaluation pipeline uses **1,728 supported series** according to the project's evaluation rules.

---

## Project Structure

```text
retail-demand-forecasting/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── deepar_full_trained.ckpt
│   └── epoch=4-step=22655.ckpt
│
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb
│   ├── 02_validation_evaluation_framework.ipynb
│   ├── 03_forecasting_models.ipynb
│   ├── 04_DeepAR_training.ipynb
│   ├── 05_DeepAR.ipynb
│   ├── 06_demand_pattern_evaluation.ipynb
│   ├── 07_final_forecast.ipynb
│   └── 08_replenishment_analysis.ipynb
│
├── outputs/
├── predictions/
├── src/
│   └── evaluation.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Notebook Execution Guide

The notebook numbers represent the recommended project workflow.

```text
01 Data Cleaning & EDA
        ↓
02 Validation & Evaluation Framework
        ↓
03 Forecasting Models
        ↓
04 DeepAR Training
        ↓
05 DeepAR Inference & Validation
        ↓
06 Demand Pattern Evaluation
        ↓
07 Final 15-Day Forecast
        ↓
08 Replenishment Analysis
```

For reproducibility, run notebooks from a clean kernel/session and use the execution environment specified for each notebook.

---

## 1. Data Cleaning & EDA

### `01_data_cleaning_eda.ipynb`

This notebook:

- Loads the raw datasets
- Checks missing values and duplicates
- Validates dates and sales
- Handles missing oil prices
- Explores sales trends and demand behaviour
- Analyzes product families, stores, weekdays, months, promotions, and holidays
- Classifies demand patterns
- Creates the prepared modeling datasets

### Main outputs

```text
data/processed/train_df.parquet
data/processed/valid_df.parquet
```

These files are used by the validation and forecasting notebooks.

---

## 2. Validation & Evaluation Framework

### `02_validation_evaluation_framework.ipynb`

This notebook verifies the shared validation and evaluation framework used by the forecasting stage.

It checks:

- Chronological train/validation splitting
- 15-day validation horizon
- Date separation and leakage checks
- Store × Family series coverage
- The documented evaluation-series exclusion rule
- Shared metric calculations
- Prediction handling rules

The shared implementation is located in:

```text
src/evaluation.py
```

### Output

This notebook is a **validation and verification stage**. It does not create a new modeling dataset. It verifies that the prepared datasets from Notebook 01 and the shared evaluation utilities are ready for the forecasting notebooks.

---

## 3. Forecasting Models

### `03_forecasting_models.ipynb`

This notebook evaluates:

- Seasonal Naive
- XGBoost
- LightGBM
- Tuned XGBoost
- Tuned LightGBM

The forecasting process uses chronological validation and recursive forecasting for the tree-based models.

The shared evaluation function calculates:

- RMSLE
- MAE
- RMSE
- WMAPE

### Main outputs

Model prediction and comparison files are saved under:

```text
outputs/forecasts/
```

These outputs are used by the demand-pattern evaluation stage.

---

## 4. DeepAR Training

### `04_DeepAR_training.ipynb`

This notebook trains the DeepAR model.

> **Execution Environment: Google Colab + GPU**

DeepAR training is performed in **Google Colab using a GPU runtime**. Google Drive is mounted to access the project files and save the trained checkpoints.

The training process uses two phases:

1. Internal chronological validation to determine the training duration.
2. Full training using the selected number of epochs.

The final validation period remains unseen during training.

### Main output

```text
models/deepar_full_trained.ckpt
```

---

## 5. DeepAR Inference & Validation

### `05_DeepAR.ipynb`

> **Execution Environment: Google Colab / compatible DeepAR environment**

This notebook:

1. Loads the trained DeepAR checkpoint.
2. Reconstructs the validation `TimeSeriesDataSet`.
3. Generates forecasts for the validation horizon.
4. Compares predictions with actual sales.
5. Evaluates DeepAR performance.
6. Saves the validation predictions.

### Main output

```text
predictions/deepar_predictions.parquet
```

---

## 6. Demand Pattern Evaluation

### `06_demand_pattern_evaluation.ipynb`

This notebook performs detailed model comparison and error analysis across:

- Regular demand
- Irregular demand
- Intermittent demand

It also evaluates:

- Model performance by demand pattern
- Intermittent-family performance
- Largest forecast errors
- Promotion, holiday, weekend, and sales-spike context
- Overall model comparison
- Baseline vs tuned models
- Final model comparison

The resulting evaluation files are saved under:

```text
outputs/
```

---

## 7. Final 15-Day Forecast

### `07_final_forecast.ipynb`

> **Execution Environment: Google Colab / compatible DeepAR environment**

This notebook uses the trained DeepAR model to generate the final 15-day forecast for:

```text
2017-08-16 → 2017-08-30
```

The final forecast contains:

- **1,728 Store × Family series**
- **25,920 forecast rows**
- 15 forecast dates

### Main outputs

```text
predictions/final_deepar_forecast.parquet
predictions/final_deepar_forecast.csv
```

---

## 8. Replenishment Analysis

### `08_replenishment_analysis.ipynb`

This notebook converts the final forecast into Store × Family replenishment recommendations.

### Assumptions

- Lead time: **3 days**
- Safety stock: **20% of expected lead-time demand**
- Current stock is not included in the dataset and is therefore not deducted from the recommendation.

### Main output

```text
outputs/replenishment_recommendations.csv
```

---

## Local vs Google Colab

Most project notebooks can be developed and executed locally using the project environment and `requirements.txt`.

The DeepAR notebooks use a compatible PyTorch / PyTorch Forecasting environment. **DeepAR training is run in Google Colab with a GPU**, and the DeepAR inference and final forecast notebooks are intended to use the compatible Colab environment as well.

The local notebooks and Colab notebooks use the same project structure and output paths.

---

## Installation

Create a virtual environment and install the project dependencies:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

Launch Jupyter:

```bash
jupyter notebook
```

---

## Streamlit Application

_To be completed after the Streamlit application is finalized._

---

## Reproducibility

For a clean project run:

1. Clone the repository.
2. Create a fresh virtual environment.
3. Install `requirements.txt`.
4. Run the notebooks in the documented order.
5. Use Google Colab with GPU for the DeepAR training stage.
6. Verify the generated outputs before running downstream notebooks.

The expected final forecast contains **25,920 rows across 1,728 Store × Family series and 15 forecast dates**.
