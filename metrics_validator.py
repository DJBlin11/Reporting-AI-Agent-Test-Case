import numpy as np
class MetricsValidator:

    def validate(self, metrics):

        errors = []

        if metrics["monthly_revenue"].isna().any():
            errors.append("Missing revenue values")

        if (metrics["churn_rate"] < 0).any():
            errors.append("Negative churn")

        if (metrics["arpu"] <= 0).any():
            errors.append("Invalid ARPU")

        return errors