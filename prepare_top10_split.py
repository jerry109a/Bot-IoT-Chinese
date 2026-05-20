from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42
DATASET_DIR = Path("dataset")
OUTPUT_DIR = Path("Dataset_for_train_and_test")

TRAIN_OUTPUT = OUTPUT_DIR / "UNSW_2018_IoT_Botnet_Final_10_best_Training.csv"
TEST_OUTPUT = OUTPUT_DIR / "UNSW_2018_IoT_Botnet_Final_10_best_Testing.csv"

TOP10_FEATURES = [
    "seq",
    "stddev",
    "N_IN_Conn_P_SrcIP",
    "min",
    "state_number",
    "mean",
    "N_IN_Conn_P_DstIP",
    "drate",
    "srate",
    "max",
]

TARGET_COLUMNS = ["attack", "category", "subcategory"]
SELECTED_COLUMNS = TOP10_FEATURES + TARGET_COLUMNS


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(DATASET_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {DATASET_DIR.resolve()}")

    frames = []
    for csv_path in csv_files:
        df = pd.read_csv(csv_path, usecols=SELECTED_COLUMNS, low_memory=False)
        frames.append(df)
        print(f"Loaded {csv_path.name}: {len(df):,} rows")

    full_df = pd.concat(frames, ignore_index=True)
    print(f"Combined rows: {len(full_df):,}")

    stratify_key = (
        full_df["attack"].astype(str)
        + "_"
        + full_df["category"].astype(str)
        + "_"
        + full_df["subcategory"].astype(str)
    )

    train_df, test_df = train_test_split(
        full_df,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=stratify_key,
    )

    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    train_df.to_csv(TRAIN_OUTPUT, index=False)
    test_df.to_csv(TEST_OUTPUT, index=False)

    print(f"Saved train: {TRAIN_OUTPUT} ({len(train_df):,} rows)")
    print(f"Saved test : {TEST_OUTPUT} ({len(test_df):,} rows)")
    print("Selected TOP10 features:")
    print(", ".join(TOP10_FEATURES))


if __name__ == "__main__":
    main()