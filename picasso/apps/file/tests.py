import pytest
from django.urls import reverse
from rest_framework import status
from picasso.apps.file.models import File
from picasso.apps.file.tasks import process_file


@pytest.mark.django_db
def test_file_upload_view(client):
    file_data = {'file': open('README.md', 'rb')}
    response = client.post(reverse('file-upload'), data=file_data, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'task_id' in response.data


@pytest.mark.django_db
def test_file_list_view(client):
    File.objects.create(file='README.md')
    response = client.get(reverse('file-list'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == File.objects.count()


@pytest.mark.django_db
def test_check_task_status_view(client):
    task = process_file.apply_async(args=[1])
    response = client.get(reverse('check-task-status', kwargs={'task_id': task.id}))

    assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.django_db
def test_no_file_upload_view(client):
    response = client.post(reverse('file-upload'), format='multipart')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
