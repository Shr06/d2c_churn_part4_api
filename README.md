# d2c_churn_part4_api
# D2C Customer Churn Prediction API

## Project Overview

This project implements a production-ready FastAPI service for predicting customer churn in a Direct-to-Consumer (D2C) business.

The API uses a trained Logistic Regression pipeline to estimate the probability that a customer will churn based on behavioral, transactional, engagement, and support-related features.

The trained model was developed using the `rfm_modeling_snapshot.csv` dataset and exported as `model.pkl`.

---

## Business Objective

Customer retention is significantly less expensive than customer acquisition. This API helps identify customers at risk of churn so that retention teams can proactively engage them with targeted interventions.

The API returns:

* Churn probability
* Predicted churn class
* Risk level
* Risk explanation

---

## Model Information

| Attribute   | Value                 |
| ----------- | --------------------- |
| Model Type  | Logistic Regression   |
| Saved Model | model.pkl             |
| Threshold   | 0.40                  |
| Framework   | Scikit-Learn Pipeline |

### Model Performance

| Metric    | Value  |
| --------- | ------ |
| Accuracy  | 0.8155 |
| Precision | 0.7819 |
| Recall    | 0.8750 |
| F1 Score  | 0.8258 |
| ROC AUC   | 0.8856 |
| PR AUC    | 0.8793 |

Confusion Matrix:

|                 | Predicted No Churn | Predicted Churn |
| --------------- | ------------------ | --------------- |
| Actual No Churn | 127                | 41              |
| Actual Churn    | 21                 | 147             |

---

## Input Features

The API expects the exact features used by the trained model:

```text
city_tier
age_group
acquisition_channel
loyalty_tier
preferred_category
marketing_consent
recency_days
frequency_180d
monetary_180d
return_rate_180d
avg_discount_pct_180d
avg_rating_180d
category_diversity_180d
ticket_count_90d
negative_ticket_rate_90d
avg_resolution_hours_90d
days_since_signup
sessions_30d
product_views_30d
cart_adds_30d
wishlist_adds_30d
abandoned_carts_30d
email_opens_30d
campaign_clicks_30d
last_visit_days_ago
```

---

## API Endpoints

### GET /health

Health-check endpoint.

#### Response

```json
{
  "status": "ok"
}
```

---

### POST /predict

Predict churn risk for a single customer.

#### Example Request

```json
{
  "city_tier": "Tier 1",
  "age_group": "26-35",
  "acquisition_channel": "Organic",
  "loyalty_tier": "Gold",
  "preferred_category": "Electronics",
  "marketing_consent": "Yes",
  "recency_days": 15,
  "frequency_180d": 8,
  "monetary_180d": 12000,
  "return_rate_180d": 0.05,
  "avg_discount_pct_180d": 10,
  "avg_rating_180d": 4.5,
  "category_diversity_180d": 5,
  "ticket_count_90d": 1,
  "negative_ticket_rate_90d": 0,
  "avg_resolution_hours_90d": 8,
  "days_since_signup": 500,
  "sessions_30d": 20,
  "product_views_30d": 80,
  "cart_adds_30d": 10,
  "wishlist_adds_30d": 3,
  "abandoned_carts_30d": 1,
  "email_opens_30d": 12,
  "campaign_clicks_30d": 4,
  "last_visit_days_ago": 2
}
```

#### Example Response

```json
{
  "churn_probability": 0.72,
  "predicted_class": 1,
  "risk_level": "High",
  "risk_explanation": "Low recent activity and high support-ticket count indicate elevated churn risk."
}
```

---

### POST /batch_predict

Predict churn risk for multiple customers in a single request.

#### Example Response

```json
{
  "predictions": [
    {
      "churn_probability": 0.72,
      "predicted_class": 1,
      "risk_level": "High",
      "risk_explanation": "Low recent activity and high support-ticket count indicate elevated churn risk."
    },
    {
      "churn_probability": 0.15,
      "predicted_class": 0,
      "risk_level": "Low",
      "risk_explanation": "Customer engagement indicators appear healthy."
    }
  ]
}
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd fast_api
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

Execute:

```bash
pytest tests/test_api.py -v
```

The test suite validates:

* Health endpoint
* Single prediction endpoint
* Batch prediction endpoint

---

## Repository Structure

```text
fast_api/
│
├── app/
│   └── main.py
│
├── model/
│   └── model.pkl
│
├── tests/
│   └── test_api.py
│
├── metrics.json
├── requirements.txt
├── monitoring_plan.md
├── README.md
└── churn_model.ipynb
```

---

## Responsible Use

This API is intended to support customer-retention strategies and should not be used as the sole basis for customer treatment decisions.

Retention teams should:

* Use churn predictions as decision-support information.
* Combine model outputs with customer history and business context.
* Monitor prediction quality regularly.

Retention teams should not:

* Treat churn predictions as guaranteed outcomes.
* Automatically deny benefits or services based solely on model output.
* Use predictions without ongoing monitoring and validation.

The model provides probabilistic estimates and may occasionally produce incorrect predictions.
