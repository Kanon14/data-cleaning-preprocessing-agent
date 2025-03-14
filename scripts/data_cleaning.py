import pandas as pd
import numpy as np

class DataCleaning:
    def handle_missing_values(self, df, strategy="mean"):
        """Handle missing values in a DataFrame using specified strategy."""
        if strategy == "mean":
            df = df.fillna(df.mean(numeric_only=True))
        elif strategy == "median":
            df = df.fillna(df.median(numeric_only=True))
        elif strategy == "mode":
            mode_values = df.mode().iloc[0] if not df.mode().empty else None
            df = df.fillna(mode_values)
        elif strategy == "drop":
            df = df.dropna()
        else:
            raise ValueError("Invalid strategy. Choose from 'mean', 'median', 'mode', or 'drop'.")
        return df
    
    def remove_duplicates(self, df):
        """Removes duplicate rows."""
        df = df.drop_duplicates()
        return df
    
    def fix_data_type(self, df):
        """Attempts to convert columns to appropriate types."""
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            except ValueError:
                pass
        return df
    
    def clean_data(self, df):
        """Applies all cleaning steps."""
        df = self.handle_missing_values(df)
        df = self.remove_duplicates(df)
        df = self.fix_data_type(df)
        return df
