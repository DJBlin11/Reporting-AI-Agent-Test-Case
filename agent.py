from generator import DataGenerator
from validator import DataValidator
from metrics import MetricsCalculator
from metrics_validator import MetricsValidator
from report_agent import ReportAgent
from visualizer import Visualizer


def main():

    #DATA
    generator = DataGenerator()
    df = generator.generate()
    df.to_csv("synthetic_users.csv", index=False)

    #VALIDATION
    validator = DataValidator()
    data_checks = validator.validate(df)

    if data_checks:
        raise ValueError(f"Data errors: {data_checks}")

    #METRICS
    metrics_calc = MetricsCalculator()
    metrics = metrics_calc.calculate(df)

    metrics_validator = MetricsValidator()
    metric_checks = metrics_validator.validate(metrics)

    if metric_checks:
        raise ValueError(f"Metric errors: {metric_checks}")

    metrics.to_csv("monthly_metrics.csv", index=False)

    #VISUALS
    visualizer = Visualizer()
    visualizer.generate(metrics)

    #REPORT (ONLY LLM STEP)
    report_agent = ReportAgent()

    report = report_agent.generate(
        metrics_df=metrics,
        data_checks=data_checks,
        metric_checks=metric_checks,
    )

    #SAVE REPORT
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("DONE")


if __name__ == "__main__":
    main()