import traceback

from .celery import app
from .models import Stack
from .stack_processor import process_stack, StackPostProcessingError, send_update


@app.task
def process_stack_task(stack_name):
    stack = Stack.objects.get(name=stack_name)
    if stack.status != Stack.ENQUEUED_STATUS:
        return
    try:
        stack.status = Stack.PROCESSING_STATUS
        stack.save()
        try:
            process_stack(stack.context.file.name, stack_name)
        except StackPostProcessingError as e:
            stack.error_text = f'Post processing error: {e}'
        stack.status = Stack.PUSHED_STATUS
        stack.save()
    except Exception:
        stack.status = Stack.ERROR_STATUS
        stack.error_text = 'Processing stack error: ' + traceback.format_exc()
        stack.save()
    try:
        send_update(stack_name)
    except Exception:
        stack.status = Stack.PUSHED_STATUS
        stack.error_text += 'Callback sending error: ' + traceback.format_exc()
        stack.save()
