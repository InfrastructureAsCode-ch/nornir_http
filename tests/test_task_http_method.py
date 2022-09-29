import pytest
import httpx
from pytest_httpx import HTTPXMock  # type: ignore
from nornir_http.tasks import http_method


def test_get_json(httpx_mock: HTTPXMock):
    data = {"test": True}
    # content-type header will be set to application/json
    httpx_mock.add_response(json=data)

    result = http_method(method="get", url="http://localhost/")
    assert result.result == data
    assert result.result["test"]


def test_get_text(httpx_mock: HTTPXMock):
    data = "this is a normal text"
    # content-type header will be set to application/json
    httpx_mock.add_response(text=data)

    result = http_method(method="get", url="http://localhost/")
    assert result.result == data


@pytest.mark.parametrize("status_code", [200, 201, 204, 301])
def test_failed_false(httpx_mock: HTTPXMock, status_code: int):
    httpx_mock.add_response(status_code=status_code)
    result = http_method(method="get", url="http://localhost/")
    assert not result.failed


@pytest.mark.parametrize("status_code", [404, 401, 500])
def test_is_error(httpx_mock: HTTPXMock, status_code: int):
    httpx_mock.add_response(status_code=status_code)
    result = http_method(method="get", url="http://localhost/")
    assert result.failed


@pytest.mark.parametrize("status_code", [404, 401, 500])
def test_disable_is_error(httpx_mock: HTTPXMock, status_code: int):
    httpx_mock.add_response(status_code=status_code)
    result = http_method(method="get", url="http://localhost/", is_error=False)
    assert not result.failed


@pytest.mark.parametrize("status_code", [404, 401, 500])
def test_enable_raise_for_status(httpx_mock: HTTPXMock, status_code: int):
    httpx_mock.add_response(status_code=status_code)
    with pytest.raises(httpx.HTTPStatusError):
        http_method(method="get", url="http://localhost/", raise_for_status=True)


@pytest.mark.parametrize("status_code", [404, 401, 500])
def test_disable_raise_for_status(httpx_mock: HTTPXMock, status_code: int):
    httpx_mock.add_response(status_code=status_code)
    result = http_method(method="get", url="http://localhost/", raise_for_status=False)
    assert result.response
    assert result.response.status_code == status_code


@pytest.mark.parametrize("method", ["get", "put", "patch", "post", "delete", "head"])
def test_method(httpx_mock: HTTPXMock, method: str):
    httpx_mock.add_response()
    result = http_method(method=method, url="http://localhost/", raise_for_status=False)
    assert result.response
    assert result.response.request.method.lower() == method
