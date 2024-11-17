import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
import io

def validate_csv(file) -> Tuple[bool, str, Optional[pd.DataFrame]]:
    """Validate uploaded CSV file and return DataFrame if valid."""
    try:
        if file is None:
            return False, "No file uploaded", None
        
        # Read CSV file
        df = pd.read_csv(file)
        
        # Basic validation checks
        if df.empty:
            return False, "The uploaded file is empty", None
        
        if len(df.columns) < 1:
            return False, "The file must contain at least one column", None
            
        return True, "File is valid", df
        
    except pd.errors.EmptyDataError:
        return False, "The uploaded file is empty", None
    except pd.errors.ParserError:
        return False, "Invalid CSV format", None
    except Exception as e:
        return False, f"Error processing file: {str(e)}", None

def get_downloadable_csv(df: pd.DataFrame) -> str:
    """Convert DataFrame to CSV string for download."""
    return df.to_csv(index=False)

def get_column_dtypes(df: pd.DataFrame) -> dict:
    """Get data types for each column in the DataFrame."""
    return {col: str(dtype) for col, dtype in df.dtypes.items()}

def generate_summary_stats(df: pd.DataFrame) -> dict:
    """Generate basic summary statistics for numerical columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats = {}
    
    for col in numeric_cols:
        stats[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max()
        }
    
    return stats
