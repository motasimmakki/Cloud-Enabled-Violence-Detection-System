import time
import picamera
import boto3
import os
import datetime as dt
from botocore.exceptions import NoCredentialsError

def capture_image(file_path):
	with picamera.PiCamera() as camera:
		# Adjust the resolution as per need.
		camera.resolution = (1024, 768)
		
		CURRENT_DATE = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
		camera.annotate_text = CURRENT_DATE

		camera.capture(file_path)

def capture_video(file_path, duration = 3):
	with picamera.PiCamera() as camera:
		# Adjust the resolution as per need.
		camera.resolution = (1024, 768) 
		camera.start_recording(file_path)
		camera.wait_recording(duration)
		camera.stop_recording()

def upload_to_s3(file_path, bucket_name, object_name):
	aws_access_key_id = "AKIA6KGA7GO62DXDR5F6"
	aws_secret_access_key = "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"
	s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

	try:
		s3.upload_file(file_path, bucket_name, object_name)
		print(f"File uploaded to S3: s3://{bucket_name}/{object_name}")
	except FileNotFoundError:
		print("The file was not found.")
	except NoCredentialsError:		
		print("Credentials not available or incorrect.")

def main():
	# Change the path to your desktop path.
	data_path = '/home/pi/Desktop/captured_data/'
	# Replace with your bucket name.
	bucket_name = 'pibucket'

	IMAGE_NAME = dt.datetime.now().strftime('%m-%d-%Y_%H-%M-%S') 
	VIDEO_NAME = dt.datetime.now().strftime('%m-%d-%Y_%H-%M-%S') 

	# Capture image.
	image_file_path = data_path + IMAGE_NAME + ".jpg"
	capture_image(image_file_path)
	upload_to_s3(image_file_path, bucket_name, 'images/{}'.format(IMAGE_NAME + ".jpg"))

	# Capture video.
	video_file_path = data_path + VIDEO_NAME + ".h264"
	capture_video(video_file_path)
	upload_to_s3(video_file_path, bucket_name, 'videos/{}'.format(VIDEO_NAME + ".h264"))

	# Removing the captured data, from local directory, after uploading.
	# os.remove(data_path + IMAGE_NAME +'.jpg')
	# os.remove(data_path + VIDEO_NAME +'.h264')

if __name__ == "__main__":
	main()
