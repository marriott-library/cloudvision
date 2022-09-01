import os
from django.conf import settings
from django.db import models
# Create your models here.


# Get Path of Input Images File, default set to os.path.join(settings.DATA_DIR, 'images')
def images_path():
    return os.path.join(settings.DATA_DIR, 'images')


# Get Path of OutPut JSON File, default set to os.path.join(settings.DATA_DIR, 'images')
def output_path():
    return os.path.join(settings.DATA_DIR, 'output')


class Log(models.Model):
    # user id that run the service
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # service name that was ran
    service_name = models.CharField(max_length=200)
    # service input file name in full path
    input_file = models.FilePathField(path=images_path)
    # ocr result file name in full path
    output_file = models.FilePathField(path=output_path)
    # ocr result in JSON format
    ocr_result = models.TextField()
    # log create time
    created = models.DateTimeField(auto_now_add=True)
    # service Run Start time
    run_start_time = models.DateTimeField()
    # service Run End time
    run_end_time = models.DateTimeField()
    # length of Process Time in million seconds
    run_time = models.IntegerField()

    # Return Log Id
    def __str__(self):
        return str(self.id)

    # Set Input and Output File Directory
    def set_file_dir(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        return self
