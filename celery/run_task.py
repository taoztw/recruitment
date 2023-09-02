from tasks import hello

result = hello.delay(4, 4)

run_result = result.get(timeout=1)
print(f"task result {run_result}")
