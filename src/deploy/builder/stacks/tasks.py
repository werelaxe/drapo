from .celery import app
from .models import Stack
from .stack_processor import process_stack, StackProcessingError


@app.task
def process_stack_task(stack_name):
    stack = Stack.objects.get(name=stack_name)
    if stack.status != Stack.ENQUEUED_STATUS:
        return
    try:
        stack.status = Stack.PROCESSING_STATUS
        stack.save()
        process_stack(stack.context.file.name, stack_name)
        stack.status = Stack.PUSHED_STATUS
        stack.save()
    except StackProcessingError as e:
        stack.status = Stack.ERROR_STATUS
        stack.error_text = 'Processing stack error: ' + str(e)
        stack.save()