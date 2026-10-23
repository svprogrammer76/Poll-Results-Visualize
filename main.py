"""Run the Poll Results Visualizer from a CSV or with reproducible demo data."""
from __future__ import annotations

import argparse
from pathlib import Path

from src.poll_visualizer import run_analysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze poll responses and export charts/reports.")
    parser.add_argument("--input", type=Path, help="Optional input CSV. If omitted, synthetic responses are generated.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Folder for reports and charts.")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="Folder for generated demo data.")
    parser.add_argument("--respondents", type=int, default=600, help="Number of demo responses (minimum 20).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for repeatable demo data.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_analysis(args.input, args.output_dir, args.data_dir, args.respondents, args.seed)
