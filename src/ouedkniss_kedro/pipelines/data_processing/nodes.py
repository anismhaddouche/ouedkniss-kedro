"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.4
"""

import pandas as pd 



def preprocess_announcements(data) -> pd.DataFrame:
    """Preprocesses the data for announcements.

    Args:
        announcements: Raw data.
    Returns:
       
    """
    announcements = pd.DataFrame(data['search']['announcements']['data'])
    return announcements