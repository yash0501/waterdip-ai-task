import imp
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Task
from .serializers import TaskSerializer

# Create your views here.
@csrf_exempt
def task_api(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def task_detail_api(request, id):
    try:
        task = Task.objects.get(id=id)
    
    except Task.DoesNotExist:
        return JsonResponse({"error": "There is no task at that id"}, status=404)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data, status=200, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=data)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=204)

        return JsonResponse({ "error": "There is no task at that id" }, status=404)

    elif request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=204)

@csrf_exempt
def task_extra(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        bulk = data.get('tasks')

        tasks = []

        for task in bulk:
            title = task.get('title')
            is_completed = task.get('is_completed')
            Task.objects.create(title=title, is_completed=is_completed)
            tasks.append(Task.objects.get(title=title))

        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        bulk = data.get('tasks')

        for task in bulk:
            id = task.get('id')
            Task.objects.get(id=id).delete()

        return HttpResponse(status=204)