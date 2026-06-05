import pandas as pd


class MetricsCalculator:

    def calculate(self, df):

        df = df.sort_values(["user_id", "month"]).copy()

        # previous state per user
        df["prev_active"] = df.groupby("user_id")["is_active"].shift(1).fillna(0)

        # churn event: active -> inactive
        df["churn_event"] = (
            (df["prev_active"] == 1) &
            (df["is_active"] == 0)
        ).astype(int)

        grouped = df.groupby("month")

        metrics = pd.DataFrame({
            "month": grouped.size().index,
            "active_users": grouped["is_active"].sum().values,
            "paid_users": grouped.apply(
                lambda x: (x["payment_status"] == "paid").sum()
            ).values,
            "monthly_revenue": grouped["amount_paid"].sum().values,
            "churned_users": grouped["churn_event"].sum().values,
        })

        metrics["churn_rate"] = (
            metrics["churned_users"] /
            metrics["active_users"].shift(1)
        ).fillna(0)

        metrics["arpu"] = (
            metrics["monthly_revenue"] /
            metrics["active_users"]
        )

        return metrics