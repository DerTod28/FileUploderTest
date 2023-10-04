from celery.result import AsyncResult
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .tasks import process_file
from .models import File
from .serializers import FileSerializer
import filetype


class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():

            file_instance = serializer.save()
            filename = file_instance.file
            file_type = None

            if filetype.is_image(filename):
                file_type = 'image'
            elif filetype.is_video(filename):
                file_type = 'video'
            elif filetype.is_document(filename):
                file_type = 'text document'
            elif filetype.is_audio(filename):
                file_type = 'audio'

            task = process_file.apply_async(args=[file_instance.id])
            if task:
                response_data = {'task_id': task.id, 'file_type': file_type, **serializer.data}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to enqueue the task.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def file_list(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def check_task_status(request, task_id):
    result = AsyncResult(task_id)

    if result.ready():
        if result.successful():
            return Response({'status': 'Task succeeded'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Task failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status': 'Task is still running'}, status=status.HTTP_202_ACCEPTED)
