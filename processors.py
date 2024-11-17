import pandas as pd
import numpy as np
from typing import List

class DataProcessor:
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Remove duplicate rows based on selected columns."""
        return df.drop_duplicates(subset=columns)

    @staticmethod
    def fill_missing_values(df: pd.DataFrame, columns: List[str], method: str) -> pd.DataFrame:
        """Fill missing values in selected columns."""
        df_copy = df.copy()
        for col in columns:
            if method == "mean" and pd.api.types.is_numeric_dtype(df[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
            elif method == "median" and pd.api.types.is_numeric_dtype(df[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].median())
            else:
                df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
        return df_copy

    @staticmethod
    def normalize_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Normalize selected numeric columns to 0-1 range."""
        df_copy = df.copy()
        for col in columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                min_val = df_copy[col].min()
                max_val = df_copy[col].max()
                if min_val != max_val:
                    df_copy[col] = (df_copy[col] - min_val) / (max_val - min_val)
        return df_copy

    @staticmethod
    def remove_outliers(df: pd.DataFrame, columns: List[str], threshold: float = 3) -> pd.DataFrame:
        """Remove outliers from selected columns using z-score method."""
        df_copy = df.copy()
        for col in columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                z_scores = np.abs((df_copy[col] - df_copy[col].mean()) / df_copy[col].std())
                df_copy = df_copy[z_scores < threshold]
        return df_copy
