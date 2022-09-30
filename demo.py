from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_http.tasks import http_method

nr = InitNornir(
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 100,
        },
    },
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "tests/demo_inventory/hosts.yaml",
            "group_file": "tests/demo_inventory/groups.yaml",
        },
    },
)


print(f"{'='*10} success {'='*10}")
results = nr.run(task=http_method, url="https://httpbin.org/status/200")
print(f"{results.failed=}")
print()


print(f"{'='*10} 404 not found {'='*10}")
results = nr.run(task=http_method, url="https://httpbin.org/status/404")
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].exception=}")
nr.data.reset_failed_hosts()
print()


print(f"{'='*10} 404 not found, raise for status {'='*10}")
results = nr.run(
    task=http_method, url="https://httpbin.org/status/404", raise_for_status=True
)
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].exception=}")
nr.data.reset_failed_hosts()
print()

print(f"{'='*10} 404 not found, no error{'='*10}")
results = nr.run(task=http_method, url="https://httpbin.org/status/404", is_error=False)
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].exception=}")
nr.data.reset_failed_hosts()
print()


print(f"{'='*10} Content-type 'application/json'{'='*10}")
results = nr.run(task=http_method, url="https://httpbin.org/json")
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].result=}")
nr.data.reset_failed_hosts()
print()


print(f"{'='*10} result {'='*10}")
results = nr.run(
    task=http_method, url="https://httpbin.org/base64/SFRUUEJJTiBpcyBhd2Vzb21l"
)
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].result=}")
nr.data.reset_failed_hosts()
print()


print(f"{'='*10} headers {'='*10}")
headers = {"Demo": "nornir_http demo", "Cache-Control": "no-cache"}
results = nr.run(task=http_method, url="https://httpbin.org/headers", headers=headers)
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].result=}")
nr.data.reset_failed_hosts()
print()


print(f"{'='*10} POST {'='*10}")
data = {"demo": "nornir_http demo"}
results = nr.run(
    task=http_method, url="https://httpbin.org/post", method="POST", json=data
)
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].result=}")
nr.data.reset_failed_hosts()
print()


print(f"{'='*10} subtask {'='*10}")


def subtask(task: Task) -> Result:
    http_result = task.run(
        http_method,
        method="PUT",
        url="https://httpbin.org/anything",
        json={"name": "nornir_http"},
    )
    return Result(
        host=task.host, result=http_result[0].result, failed=http_result.failed
    )


results = nr.run(task=subtask)
print(f"{results.failed=}")
print(f"{results['host1.cmh'][0].result=}")
nr.data.reset_failed_hosts()
print()
