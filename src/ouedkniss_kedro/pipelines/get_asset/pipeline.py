"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import *




def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=get_asset,
                inputs="data",
                outputs="asset",
                name="get_asset_node",
            ),
        ],
        namespace="data_processing",
        inputs=["data"],
        outputs="asset",
    )
