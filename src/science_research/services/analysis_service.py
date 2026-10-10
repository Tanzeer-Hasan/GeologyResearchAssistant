from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


class AnalysisService:
    """Generates reproducible analysis outputs for a research problem."""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def run(self, topic: str, domain: str = "general", variables: List[str] | None = None) -> Dict[str, Any]:
        variables = variables or ["x", "y", "z"]
        sample_x = [1, 2, 3, 4, 5, 6, 7, 8]
        sample_y = [12, 17, 15, 23, 28, 29, 34, 38]
        sample_z = [10, 13, 18, 22, 25, 31, 35, 37]

        df = pd.DataFrame({
            "sample_index": sample_x,
            variables[0] if len(variables) > 0 else "x": sample_x,
            variables[1] if len(variables) > 1 else "y": sample_y,
            variables[2] if len(variables) > 2 else "z": sample_z,
        })

        summary = {
            "mean_first": round(float(df.iloc[:, 1].mean()), 3),
            "mean_second": round(float(df.iloc[:, 2].mean()), 3),
            "mean_third": round(float(df.iloc[:, 3].mean()), 3),
            "n_samples": int(len(df)),
        }

        plot_path = self.output_dir / f"{topic.lower().replace(' ', '_')}_trend.png"
        self._generate_plot(sample_x, sample_y, title=f"{topic} trend analysis", save_path=plot_path)

        comparison_path = self.output_dir / f"{topic.lower().replace(' ', '_')}_comparison.png"
        self._generate_comparison_plot(sample_x, sample_y, sample_z, title=f"{topic} comparison", save_path=comparison_path)

        return {
            "topic": topic,
            "domain": domain,
            "input_variables": variables,
            "summary_statistics": summary,
            "generated_files": [
                str(plot_path),
                str(comparison_path),
            ],
            "tables": [
                {
                    "name": "summary_statistics",
                    "data": summary,
                }
            ],
        }

    def _generate_plot(self, x: List[int], y: List[int], title: str, save_path: Path) -> None:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, y, marker="o", linewidth=2)
        ax.set_title(title)
        ax.set_xlabel("Sample index")
        ax.set_ylabel("Value")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(save_path, dpi=200)
        plt.close(fig)

    def _generate_comparison_plot(self, x: List[int], y1: List[int], y2: List[int], title: str, save_path: Path) -> None:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, y1, marker="o", label="Variable 1", linewidth=2)
        ax.plot(x, y2, marker="s", label="Variable 2", linewidth=2)
        ax.set_title(title)
        ax.set_xlabel("Sample index")
        ax.set_ylabel("Value")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(save_path, dpi=200)
        plt.close(fig)
