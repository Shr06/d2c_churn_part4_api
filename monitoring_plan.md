# Monitoring Plan

## Overview

This project deploys a Logistic Regression-based Customer Churn Prediction API for a Direct-to-Consumer (D2C) business. The API predicts the likelihood of customer churn using customer demographics, transaction history, engagement behavior, and customer support interactions.

The model was trained using the `rfm_modeling_snapshot.csv` dataset and achieved the following validation performance:

| Metric    | Value  |
| --------- | ------ |
| Accuracy  | 0.8155 |
| Precision | 0.7819 |
| Recall    | 0.8750 |
| F1 Score  | 0.8258 |
| ROC-AUC   | 0.8856 |
| Threshold | 0.40   |

To ensure the model remains reliable after deployment, the following monitoring strategy will be implemented.

---

# 1. Data Drift Monitoring

## Objective

Detect whether incoming customer data differs significantly from the training dataset.

## Key Features to Monitor

The following business-critical features should be tracked:

* recency_days
* frequency_180d
* monetary_180d
* last_visit_days_ago
* sessions_30d
* product_views_30d
* abandoned_carts_30d
* ticket_count_90d
* negative_ticket_rate_90d
* email_opens_30d
* campaign_clicks_30d

## Monitoring Approach

On a monthly basis:

* Compare feature distributions between training and production data.
* Monitor changes in:

  * Mean
  * Median
  * Standard deviation
  * Missing value rates
* Review new categories appearing in:

  * city_tier
  * acquisition_channel
  * loyalty_tier
  * preferred_category

## Alert Conditions

Investigation should be triggered if:

* Feature means change by more than 20%.
* Missing values increase significantly.
* New unseen categorical values appear frequently.
* Customer behavior patterns differ substantially from training data.

---

# 2. Prediction Distribution Monitoring

## Objective

Ensure model predictions remain stable and realistic over time.

## Metrics to Track

* Average churn probability
* Percentage of customers predicted as churners
* Distribution of risk levels:

  * Low Risk
  * Medium Risk
  * High Risk

## Monitoring Approach

Generate weekly reports showing:

* Mean predicted churn probability
* Churn classification rate
* Risk-level distribution

## Alert Conditions

Review the model if:

* Predicted churn rate changes by more than 25% from historical averages.
* High-risk customer percentage suddenly increases or decreases.
* Average churn probability shifts significantly.

---

# 3. Business Outcome Monitoring

## Objective

Measure whether predictions contribute to improved customer retention.

## Metrics to Track

* Actual customer churn rate
* Retention campaign conversion rate
* Revenue retained from intervention campaigns
* Percentage of predicted churners who actually churn
* Percentage of retained customers after intervention

## Monitoring Approach

Compare:

* Predicted churn outcomes
* Actual customer behavior

Evaluate model effectiveness monthly.

## Success Indicators

* Lower customer churn rate
* Increased customer retention
* Improved effectiveness of retention campaigns
* Increased customer lifetime value

---

# 4. API Monitoring

## Objective

Ensure API reliability, availability, and performance.

## Metrics to Track

### Availability

* API uptime percentage
* Service availability

### Performance

* Average response time
* Prediction latency

### Errors

* HTTP 4xx responses
* HTTP 5xx responses
* Failed prediction requests
* Validation failures

## Alert Conditions

Trigger alerts if:

* Uptime falls below 99%.
* Error rate exceeds 5%.
* Average response time increases significantly.

---

# 5. Model Performance Monitoring

## Objective

Ensure predictive performance remains close to training performance.

## Baseline Performance

| Metric    | Baseline |
| --------- | -------- |
| Accuracy  | 0.8155   |
| Precision | 0.7819   |
| Recall    | 0.8750   |
| F1 Score  | 0.8258   |
| ROC-AUC   | 0.8856   |

## Monitoring Frequency

Monthly evaluation using newly observed customer outcomes.

## Alert Conditions

Investigation is required if:

* Accuracy drops below 0.73
* Recall drops below 0.80
* ROC-AUC falls below 0.85

---

# 6. Retraining Triggers

The model should be retrained when one or more of the following conditions occur:

## Data Drift

* Significant shifts in recency_days, frequency_180d, monetary_180d, or engagement-related features.

## Performance Degradation

* Accuracy decreases by more than 10%.
* Recall falls below 0.80.
* ROC-AUC falls below 0.85.

## Business Performance Decline

* Retention campaign effectiveness decreases.
* Churn rates increase despite intervention efforts.

## Scheduled Retraining

* Retrain every 6 months using the latest customer data.
* Retrain earlier if major business changes occur.

---

# Responsible Use

This API should be used as a decision-support tool for customer retention teams.

The API output should:

* Help prioritize customer retention efforts.
* Support campaign targeting decisions.
* Be combined with business context and customer history.

The API output should not:

* Be treated as a guaranteed prediction of customer behavior.
* Be used as the sole basis for customer treatment decisions.
* Be used without periodic monitoring and validation.

Human review and business judgment should always accompany model predictions.

---

# Monitoring Summary

| Area                  | Metric                                           |
| --------------------- | ------------------------------------------------ |
| Data Drift            | Feature distribution changes                     |
| Prediction Monitoring | Churn probability and risk-level distribution    |
| Business Outcomes     | Actual churn and retention effectiveness         |
| API Health            | Uptime, latency, and error rates                 |
| Model Quality         | Accuracy, Recall, Precision, F1, ROC-AUC         |
| Retraining            | Drift, performance decline, or scheduled updates |

This monitoring strategy helps ensure that the churn prediction API remains accurate, reliable, and aligned with business objectives after deployment.
