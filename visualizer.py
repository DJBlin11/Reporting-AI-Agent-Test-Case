from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:

    def __init__(self):
        sns.set_theme(style="whitegrid")

    def generate(self, metrics_df):

        Path("reports").mkdir(exist_ok=True)

        self._plot(metrics_df, "monthly_revenue", "Revenue Trend", "revenue_trend.png")
        self._plot(metrics_df, "churn_rate", "Churn Rate Trend", "churn_trend.png")
        self._plot(metrics_df, "arpu", "ARPU Trend", "arpu_trend.png")

    def _plot(self, df, y_col, title, filename):

        plt.figure(figsize=(10, 5))

        sns.lineplot(
            data=df,
            x="month",
            y=y_col,
            marker="o"
        )

        plt.title(title)
        plt.xlabel("Month")
        plt.ylabel(y_col)

        plt.tight_layout()

        plt.savefig(f"reports/{filename}", dpi=150)
        plt.close()