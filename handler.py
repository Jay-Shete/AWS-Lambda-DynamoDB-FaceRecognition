import os
import face_recognition
import pickle
import numpy as np
import boto3
from boto3 import client as boto3_client
import pickle

input_bucket = "546proj2inputtrinity"
output_bucket = "546proj2outputtrinity"

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):
	print("Inside face_recognition_handler")
	DownloadFromS3AndStoreInTemp(event,context)
	#data = open_encoding('encoding.dat')
	recognizeImage(event['key'])
	print("Hello")

def recognizeImage(key):
	print("Inside recognizeImage")
	storage_path = "/tmp/"
	filename = storage_path + str(key)
	# Load face encodings
	with open('encoding.dat', 'rb') as f:
		all_face_encodings = pickle.load(f)
	print("Pickle File Loaded")
	face_names = list(all_face_encodings.keys())
	face_encodings = np.array(list(all_face_encodings.values()))

	unknown_image = face_recognition.load_image_file(filename)
	unknown_face = face_recognition.face_encodings(unknown_image)
	result = face_recognition.compare_faces(face_encodings, unknown_face)

	# Print the result as a list of names with True/False
	names_with_result = list(zip(face_names, result))
	print(names_with_result)

def DownloadFromS3AndStoreInTemp(event, context):
	print("Inside DownloadFromS3AndStoreInTemp")
	key = event['key']
	bucket = event['bucket']
	AWS_ACCESS_KEY = "AKIAY6MI7NBZ6EVPEWOD"
	AWS_SECRET_ACCESS_KEY = "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"
	AWS_REGION = "us-east-1"

	s3_client = boto3.client('s3', region_name=AWS_REGION)
	print("S3 Client Created")
	path = "/tmp/"
	video_file_path = path + key
	print("Video File Path"+video_file_path)

	response = s3_client.get_object(Bucket=bucket, Key=key)
	print("Got Response from s3 client")
	s3_client.download_file(bucket, key, video_file_path)
	print("Downloaded files ", os.listdir(path))
	os.system(
		"/opt/ffmpeglib/ffmpeg -i " + str(video_file_path) + " -frames:v 1 -s 160X160 " + str(path) + "image-%03d.png")
	print("Frames stored in"+os.listdir(path))

	return response

def FfmpegExtractImage():
	return 0
