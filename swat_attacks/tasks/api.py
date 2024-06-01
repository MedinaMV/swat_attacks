import threading
import time
from .models import Attack
from bson import ObjectId
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ProjectSerializer
from .tasks import xss, sqli
from celery.result import AsyncResult

def update_element(instance_id, state):
   attack = Attack.objects.get(_id=ObjectId(instance_id))
   attack.state = state
   attack.save()

def wait_for_task(task_id, instance_id, task_name):
   result = AsyncResult(task_id)
   while not result.ready():
      time.sleep(5) 

   print(f'Task {task_name} with ID {task_id} finished. Result: {result.result}')

def wait_for_tasks(threads):
    for thread in threads:
        thread.join()

def wait_for_task(task_id, instance_id, task_name, result_lock, completed_tasks, cont):
    result = AsyncResult(task_id)
    while not result.ready():
        time.sleep(1)  

    print(f'Task {task_name} with ID {task_id} finished. Result: {result.result}')

    with result_lock:
        completed_tasks.append(task_name)
        if len(completed_tasks) == cont:
            update_element(instance_id, 'COMPLETED')
            print(f'Updated attack {instance_id} state to completed')

class ProjectViewSet(viewsets.ModelViewSet):
   queryset = Attack.objects.all()
   permission_classes = [permissions.AllowAny]
   serializer_class = ProjectSerializer
   
   def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)

      instance_id = str(serializer.instance._id)
      data = request.data
      cont = len(data['attack_type'])
      threads = []
      result_lock = threading.Lock()
      completed_tasks = []
      for i in data['attack_type']:
         if i == 'XSS':
            task = xss.delay(data, instance_id)
            update_element(instance_id,'EXECUTING')
            threads.append(threading.Thread(target=wait_for_task, args=(task.id, instance_id, 'xss', result_lock, completed_tasks, cont)).start())

         if i == 'SQLI':
            task1 = sqli.delay(data, instance_id)
            update_element(instance_id,'EXECUTING')
            threads.append(threading.Thread(target=wait_for_task, args=(task1.id, instance_id, 'sqli', result_lock, completed_tasks, cont)).start())

      threading.Thread(target=wait_for_tasks, args=(threads,)).start()
      return Response(status=status.HTTP_201_CREATED)