from typing import Any, Union
from httpx import Response
from nornir.core.task import Result
from nornir.core.inventory import Host


class HTTPResult(Result):
    """
    HTTPResult of running individual tasks.
    Inherited from (:obj:)`nornir.core.task.Result`

    Arguments:
        result (obj): Result of the task execution, see task's documentation for details
        response (:obj:`httpx.Response`): Response of the http request
        host (:obj:`nornir.core.inventory.Host`): Reference to the host
        failed (bool): Whether the execution failed or not

    Attributes:
        result (obj): Result of the task execution, see task's documentation for details
        response (:obj:`httpx.Response`): Response of the http request
        host (:obj:`nornir.core.inventory.Host`): Reference to the host
        failed (bool): Whether the execution failed or not
    """

    def __init__(
        self,
        host: Union["Host", None],
        response: Response,
        result: Any = None,
        failed: bool = False,
        **kwargs: Any
    ):

        super().__init__(host=host, result=result, failed=failed, **kwargs)
        self.response = response
