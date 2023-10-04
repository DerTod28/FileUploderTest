from .models import File

from picasso.celeryapp import app


@app.task(name='change_file_processed_status')
def process_file(file_id):
    file_instance = File.objects.get(id=file_id)
    file_instance.processed = True
    file_instance.save()
