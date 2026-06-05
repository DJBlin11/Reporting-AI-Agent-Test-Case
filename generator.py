import numpy as np
import pandas as pd


class DataGenerator:

    def __init__(self, n_users=1000, months=12):
        self.n_users = n_users
        self.months = months
        np.random.seed(42)

    def generate(self):

        plans = np.random.choice(
            ["basic", "standard", "premium"],
            size=self.n_users,
            p=[0.6, 0.3, 0.1],
        )

        price_map = {
            "basic": 10,
            "standard": 20,
            "premium": 40,
        }

        churn_map = {
            "basic": 0.07,
            "standard": 0.05,
            "premium": 0.03,
        }

        rows = []

        for user_id, plan in enumerate(plans, start=1):

            active = True

            for month in range(1, self.months + 1):

                if active and month > 1:
                    if np.random.rand() < churn_map[plan]:
                        active = False

                if active:
                    paid = np.random.rand() < 0.97
                    amount = price_map[plan] if paid else 0
                    status = "paid" if paid else "failed"
                else:
                    status = "failed"
                    amount = 0

                rows.append({
                    "user_id": user_id,
                    "month": month,
                    "plan": plan,
                    "monthly_price": price_map[plan],
                    "payment_status": status,
                    "amount_paid": amount,
                    "is_active": int(active),
                })

        return pd.DataFrame(rows)