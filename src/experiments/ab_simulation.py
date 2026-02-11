"""Offline A/B simulation and ROI sensitivity analysis."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.config import PipelineConfig


@dataclass
class ABResult:
    uplift: float
    control_rate: float
    treatment_rate: float
    diff: float
    p_value: float
    ci_low: float
    ci_high: float


def _bootstrap_ci(control: np.ndarray, treatment: np.ndarray, n_boot: int = 500, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(n_boot):
        c = rng.choice(control, size=len(control), replace=True)
        t = rng.choice(treatment, size=len(treatment), replace=True)
        diffs.append(t.mean() - c.mean())
    return float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def _two_prop_p(control_success: int, control_n: int, treat_success: int, treat_n: int) -> float:
    p_pool = (control_success + treat_success) / (control_n + treat_n)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / control_n + 1 / treat_n))
    if se == 0:
        return 1.0
    z = (treat_success / treat_n - control_success / control_n) / se
    return float(2 * (1 - norm.cdf(abs(z))))


def run_ab_simulation(latest_predictions: pd.DataFrame, config: PipelineConfig) -> tuple[pd.DataFrame, str, pd.DataFrame]:
    top = latest_predictions.head(config.top_k_at_risk).copy()
    rng = np.random.default_rng(config.random_seed)
    top["group"] = np.where(rng.random(len(top)) < 0.5, "control", "treatment")
    top["base_pass_prob"] = (1 - top["risk_score"]).clip(0.05, 0.95)

    assignments = []
    results = []
    for uplift in [0.03, 0.05, 0.08]:
        sim = top.copy()
        sim["sim_pass_prob"] = sim["base_pass_prob"]
        sim.loc[sim["group"] == "treatment", "sim_pass_prob"] = (
            sim.loc[sim["group"] == "treatment", "sim_pass_prob"] + uplift
        ).clip(0, 1)
        sim["pass_outcome"] = rng.binomial(1, sim["sim_pass_prob"])
        sim["uplift_scenario"] = uplift
        assignments.append(sim)

        control = sim[sim["group"] == "control"]["pass_outcome"].to_numpy()
        treat = sim[sim["group"] == "treatment"]["pass_outcome"].to_numpy()
        c_rate, t_rate = control.mean(), treat.mean()
        ci_low, ci_high = _bootstrap_ci(control, treat, seed=config.random_seed)
        p_val = _two_prop_p(int(control.sum()), len(control), int(treat.sum()), len(treat))
        results.append(
            ABResult(
                uplift=uplift,
                control_rate=float(c_rate),
                treatment_rate=float(t_rate),
                diff=float(t_rate - c_rate),
                p_value=p_val,
                ci_low=ci_low,
                ci_high=ci_high,
            )
        )

    assignment_df = pd.concat(assignments, ignore_index=True)
    assignment_df.to_csv(config.experiments_dir / "assignment_latest.csv", index=False)

    report_lines = [
        "# Offline A/B Simulation Report",
        "",
        "Top-K at-risk students were randomized (seeded) to control/treatment and simulated under uplift scenarios.",
        "",
        "| Uplift | Control Pass Rate | Treatment Pass Rate | Diff | 95% Bootstrap CI | p-value |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        report_lines.append(
            f"| {r.uplift:.0%} | {r.control_rate:.2%} | {r.treatment_rate:.2%} | {r.diff:.2%} | [{r.ci_low:.2%}, {r.ci_high:.2%}] | {r.p_value:.4f} |"
        )

    report = "\n".join(report_lines)
    (config.reports_dir / "ab_test_report.md").write_text(report)

    grid_rows = []
    base = results[1]
    for uplift in [0.03, 0.05, 0.08, 0.10]:
        for cost in [50, 100, 150, 200, 300]:
            incremental_passes = len(top) * uplift
            roi = incremental_passes * config.value_per_pass - len(top) * cost
            grid_rows.append(
                {
                    "top_k_students": len(top),
                    "uplift_assumption": uplift,
                    "cost_per_student": cost,
                    "value_per_pass": config.value_per_pass,
                    "incremental_passes": incremental_passes,
                    "roi": roi,
                    "reference_diff_from_5pct_sim": base.diff,
                }
            )
    roi_df = pd.DataFrame(grid_rows)
    roi_df.to_csv(config.reports_dir / "roi_sensitivity.csv", index=False)
    return assignment_df, report, roi_df
