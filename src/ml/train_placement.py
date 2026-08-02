"""Predict whether a horse will place (finish top 3).

    python3 -m src.ml.train_placement

This script runs, reports a high accuracy, and is not trustworthy. Everything wrong
with it is wrong on purpose:

  * `finish_position` is used as a feature. It IS the target. Textbook leakage.
  * Accuracy is the only metric reported, on an imbalanced problem.
  * `train_test_split` is random over rows, so entries from the same race land on
     both sides of the split.
  * No random seed on the split, so the number changes every run.

Do not fix these before you have found them. The exercise is to interrogate the
number, not to produce a better one.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "race_results.csv"

FEATURES = [
    "distance_f",
    "weight_kg",
    "finish_position",   # <-- this is the answer
]


def load() -> pd.DataFrame:
    frame = pd.read_csv(DATA)

    # Minimal cleaning: just enough to make the model fit.
    frame["distance_f"] = pd.to_numeric(frame["distance_f"], errors="coerce")
    frame["weight_kg"] = pd.to_numeric(
        frame["weight_kg"].astype(str).str.replace(",", ".", regex=False),
        errors="coerce",
    )
    frame["finish_position"] = pd.to_numeric(frame["finish_position"], errors="coerce")
    frame["placed"] = pd.to_numeric(frame["placed"], errors="coerce")

    return frame.dropna(subset=FEATURES + ["placed"])


def main() -> None:
    frame = load()
    X = frame[FEATURES]
    y = frame["placed"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"rows used:        {len(frame)}")
    print(f"features:         {', '.join(FEATURES)}")
    print(f"accuracy:         {accuracy_score(y_test, predictions):.3f}")
    print()
    print("Looks good. It isn't. Work out why before changing anything.")


if __name__ == "__main__":
    main()
