import pandas as pd


class DataValidator:

    def validate(self, df: pd.DataFrame) -> list:

        errors = []

        required_cols = [
            "user_id",
            "month",
            "plan",
            "monthly_price",
            "payment_status",
            "amount_paid",
            "is_active",
        ]

        missing = [c for c in required_cols if c not in df.columns]

        if missing:
            errors.append(f"Missing columns: {missing}")

        if (df["amount_paid"] < 0).any():
            errors.append("Negative payments detected")

        if (df["amount_paid"] > df["monthly_price"]).any():
            errors.append("Overpayment detected")

        return errors