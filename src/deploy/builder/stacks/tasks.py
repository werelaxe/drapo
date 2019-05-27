from .models import Stack
from .celery import app


@app.task
def build_stack(stack_name):
    stack = Stack.objects.get(name=stack_name)
    print('building stack: {}, not implemented'.format(stack))
