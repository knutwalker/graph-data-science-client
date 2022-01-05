from ..query_runner.query_runner import QueryRunner
from .lp_pipeline_create_runner import LPPipelineCreateRunner


class PipelineEndpoints:
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    @property
    def linkPrediction(self) -> LPPipelineCreateRunner:
        return LPPipelineCreateRunner(
            self._query_runner, f"{self._namespace}.linkPrediction"
        )
