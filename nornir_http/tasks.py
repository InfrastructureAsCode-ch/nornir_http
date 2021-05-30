import httpx
from typing import Optional, Any
from nornir.core.task import Task
from nornir_http.result import HTTPResult


def http_method(
    task: Optional[Task] = None,
    method: str = "get",
    url: str = "",
    raise_for_status: bool = False,
    is_error: bool = True,
    **kwargs: Any
) -> HTTPResult:
    """
    This is a helper task that uses `httpx <https://www.python-httpx.org/api/>`_ to
    interact with an HTTP server.
    Arguments:
        method: HTTP method to call
        url: URL to connect to
        raise_for_status: Whether to call `raise_for_status` method or not
        is_error: Whether to set Result.failed or not based on status code
        **kwargs: Keyword arguments will be passed to the request `httpx.request` method
    Returns:
        Result.result dict with the following keys set:
          * result (``str/dict``): Body of the response. Either text or a dict
                                   if the response was a json object
          * response (``httpx.Response``): Original `Response`
          * failed (``bool``): set to `response.is_failed` if is_error is true
    """
    response = httpx.request(method, url, **kwargs)

    if raise_for_status:
        response.raise_for_status()

    try:
        content_type = response.headers["Content-type"]
    except KeyError:
        content_type = "text"

    return HTTPResult(
        host=task.host if task else None,
        result=response.json() if "application/json" == content_type else response.text,
        response=response,
        failed=response.is_error if is_error else False,
    )
