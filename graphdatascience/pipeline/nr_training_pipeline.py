from typing import Any, List, Union

from pandas import Series

from ..model.node_regression_model import NRModel
from ..query_runner.query_runner import QueryRunner
from .training_pipeline import TrainingPipeline


class NRTrainingPipeline(TrainingPipeline[NRModel]):
    """
    Represents a node regression training pipeline.
    Construct an instance of this class using :func:`graphdatascience.GraphDataScience.nr_pipe`.
    """

    def addLinearRegression(self, **config: Any) -> "Series[Any]":
        """
        Add a linear regression model candidate to the pipeline.

        Args:
            **config: The configuration for the linear regression model.

        Returns:
            The result of the query.

        """
        query = f"{self._query_prefix()}addLinearRegression($pipeline_name, $config)"
        params = {"pipeline_name": self.name(), "config": self._expand_ranges(config)}

        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    def addRandomForest(self, **config: Any) -> "Series[Any]":
        """
        Add a random forest regressor candidate to the pipeline.

        Args:
            **config: The configuration for the random forest regressor.

        Returns:
            The result of the query.

        """
        query = f"{self._query_prefix()}addRandomForest($pipeline_name, $config)"
        params = {"pipeline_name": self.name(), "config": self._expand_ranges(config)}

        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    def selectFeatures(self, node_properties: Union[str, List[str]]) -> "Series[Any]":
        """
        Select the node properties to use for training.

        Args:
            node_properties: The node properties to use for training.

        Returns:
            The result of the query.

        """
        query = f"{self._query_prefix()}selectFeatures($pipeline_name, $node_properties)"
        params = {"pipeline_name": self.name(), "node_properties": node_properties}

        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    def feature_properties(self) -> "Series[Any]":
        """
        Get the feature properties of the pipeline.

        Returns:
            A Series containing the feature properties of the pipeline.

        """
        pipeline_info = self._list_info()["pipelineInfo"][0]
        feature_properties: "Series[Any]" = Series(pipeline_info["featurePipeline"]["featureProperties"], dtype=object)
        return feature_properties

    def _query_prefix(self) -> str:
        return "CALL gds.alpha.pipeline.nodeRegression."

    def _create_trained_model(self, name: str, query_runner: QueryRunner) -> NRModel:
        return NRModel(name, query_runner, self._server_version)
