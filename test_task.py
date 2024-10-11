from celery_app import add
from celery.result import AsyncResult
import time

# Submit the task
result = add.delay(4, 6)
print("Task submitted, result will be available later.")

# Wait for the task to complete and get the result
while not result.ready():
    time.sleep(1)  # Sleep for a second before checking again

# Get the result
if result.successful():
    print(f"Task result: {result.get(timeout=30)}")  # Adjust timeout if needed
else:
    print(f"Task failed with status: {result.status}")
