import json
import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# ==================================================
# LOAD MODEL
# ==================================================

model = joblib.load("model.pkl")
with open("metrics.json", "r") as f:
    metrics = json.load(f)
CHURN_THRESHOLD = float(metrics["threshold"])
FEATURES = list(model.feature_names_in_)

# ==================================================
# FASTAPI APP
# ==================================================
app = FastAPI(title="D2C Customer Churn Prediction API",
    version="1.0")

# ==================================================
# RISK LOGIC
# ==================================================

def get_risk_level(probability):
  if probability < 0.30:
      return "Low"
  elif probability < 0.70:
      return "Medium"
  return "High"

def generate_risk_explanation(customer, probability):
  reasons = []
  if customer.recency_days > 60:
      reasons.append("high recency")
  if customer.sessions_30d < 5:
      reasons.append("low recent activity")
  if customer.ticket_count_90d > 3:
      reasons.append("high support-ticket count")
  if customer.negative_ticket_rate_90d > 0.30:
      reasons.append("negative support experience")
  if reasons:
    return (
            ", ".join(reasons).capitalize()
            + " indicate elevated churn risk."
        )

    if probability >= 0.70:
        return (
            "Customer shows several patterns associated "
            "with churn risk."
        )

    return (
        "Customer engagement indicators appear healthy."
    )

# ==================================================
# PYDANTIC SCHEMAS
# ==================================================

class CustomerData(BaseModel):

    city_tier: str
    age_group: str
    acquisition_channel: str
    loyalty_tier: str
    preferred_category: str
    marketing_consent: str

    recency_days: float
    frequency_180d: float
    monetary_180d: float
    return_rate_180d: float
    avg_discount_pct_180d: float
    avg_rating_180d: float
    category_diversity_180d: float

    ticket_count_90d: float
    negative_ticket_rate_90d: float
    avg_resolution_hours_90d: float

    days_since_signup: float
    sessions_30d: float
    product_views_30d: float
    cart_adds_30d: float
    wishlist_adds_30d: float
    abandoned_carts_30d: float

    email_opens_30d: float
    campaign_clicks_30d: float
    last_visit_days_ago: float


class BatchCustomerData(BaseModel):
    customers: List[CustomerData]

# ==================================================
# HEALTH
# ==================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }

# ==================================================
# SINGLE PREDICTION
# ==================================================

@app.post("/predict")
def predict(customer: CustomerData):

    try:

        df = pd.DataFrame(
            [customer.model_dump()]
        )

        probability = float(
            model.predict_proba(df)[0][1]
        )

        prediction = int(
            probability >= CHURN_THRESHOLD
        )

        return {
            "churn_probability": round(probability, 4),
            "predicted_class": prediction,
            "risk_level": get_risk_level(probability),
            "risk_explanation": generate_risk_explanation(
                customer,
                probability
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ==================================================
# BATCH PREDICTION
# ==================================================

@app.post("/batch_predict")
def batch_predict(batch: BatchCustomerData):

    try:

        customers = [
            c.model_dump()
            for c in batch.customers
        ]

        df = pd.DataFrame(customers)

        probabilities = model.predict_proba(df)[:, 1]

        results = []

        for customer, prob in zip(
            batch.customers,
            probabilities
        ):

            results.append(
                {
                    "churn_probability": round(
                        float(prob), 4
                    ),
                    "predicted_class": int(
                        prob >= CHURN_THRESHOLD
                    ),
                    "risk_level": get_risk_level(
                        float(prob)
                    ),
                    "risk_explanation":
                        generate_risk_explanation(
                            customer,
                            float(prob)
                        )
                }
            )

        return {
            "predictions": results
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
