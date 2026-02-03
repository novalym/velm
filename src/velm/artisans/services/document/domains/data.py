import os
import json
from typing import Any, List, Dict


class DataEngine:
    """[THE DATA TRANSMUTER] Powered by Pandas."""

    def _get_pandas(self):
        try:
            import pandas as pd
            return pd
        except ImportError:
            raise ImportError("Pandas not found. Run `pip install pandas openpyxl`.")

    def parse(self, path: str, format: str) -> List[Dict]:
        pd = self._get_pandas()
        if format == "csv":
            df = pd.read_csv(path)
        elif format == "xlsx":
            df = pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported parse format: {format}")

        # Convert NaN to None for JSON safety
        return df.where(pd.notnull(df), None).to_dict(orient="records")

    def generate(self, data: List[Dict], path: str, format: str):
        pd = self._get_pandas()
        df = pd.DataFrame(data)

        if format == "csv":
            df.to_csv(path, index=False)
        elif format == "xlsx":
            df.to_excel(path, index=False)