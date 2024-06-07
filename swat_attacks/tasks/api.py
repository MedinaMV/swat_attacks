import threading
import time
from .models import Attack
from bson import ObjectId
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ProjectSerializer
from .tasks import generic_attack,bruteforce_attack,nuclei_attack
from celery.result import AsyncResult
from datetime import datetime
import pytz

def update_attack(instance_id, state, flag):
   attack = Attack.objects.get(_id=ObjectId(instance_id))
   attack.state = state
   if flag:
      attack.finished_time = datetime.now(pytz.timezone('UTC')).isoformat()
   attack.save()

def wait_for_tasks(threads):
    for thread in threads:
        thread.join()

def wait_for_task(task_id, instance_id, task_name, result_lock, completed_tasks, cont):
    result = AsyncResult(task_id)
    while not result.ready():
        time.sleep(60)  

    print(f'Task {task_name} with ID {task_id} finished. Result: {result.result}')

    with result_lock:
        completed_tasks.append(task_name)
        if len(completed_tasks) == cont:
            update_attack(instance_id,'COMPLETED',True)
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
         type = i.lower()
            
         if type == 'xss' or type == 'sqli':
            task = generic_attack.delay(data,instance_id,type)
         elif type == 'brf':
            task = bruteforce_attack.delay(data,instance_id)
         else:
            task = nuclei_attack.delay(data,instance_id)
            
         update_attack(instance_id,'EXECUTING',False)
         threads.append(threading.Thread(target=wait_for_task, args=(task.id, instance_id, type, result_lock, completed_tasks, cont)).start())

      threading.Thread(target=wait_for_tasks, args=(threads,)).start()
      return Response(status=status.HTTP_201_CREATED)
   
   