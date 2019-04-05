from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from celery import shared_task
from omr.models import Home
from omr.utils import pdf2bmp, generateExcel
import OpticalMarkRecognition_MATLAB


@shared_task
def omr_process(answer_scheme_name, answer_scheme_type, answer_sheet_name, answer_sheet_type, total_questions, template_bmp, start_time):
	fs = FileSystemStorage()
	omr = OpticalMarkRecognition_MATLAB.initialize()
	collection_array = []

	if answer_scheme_type == 'application/pdf':
		answer_scheme_path = fs.path(answer_scheme_name)
		answer_scheme_bmp, answer_scheme_page_num = pdf2bmp(answer_scheme_path)

	if answer_sheet_type == 'application/pdf':
		answer_sheet_path = fs.path(answer_sheet_name)
		answer_sheet_bmp, answer_sheet_page_num = pdf2bmp(answer_sheet_path)	

	answer_scheme_bmp = omr.preprocess_register(answer_scheme_bmp, template_bmp)
	answer_scheme_answers = omr.answers(answer_scheme_bmp, total_questions)

	if (answer_sheet_page_num == 1):
		answer_sheet_bmp = omr.preprocess_register(answer_sheet_bmp, template_bmp)
		matric_number, course_code = omr.matric_course(answer_sheet_bmp, nargout = 2)
		answer_sheet_answers = omr.answers(answer_sheet_bmp, total_questions)
		result = omr.result(answer_scheme_answers, answer_sheet_answers, total_questions)

		collection_array.append([str(matric_number), str(course_code), str(answer_sheet_answers), result])
		generateExcel(course_code, collection_array)

	else:
		for i in range(answer_sheet_page_num):
			w = answer_sheet_bmp
			x = "(" + str(answer_sheet_page_num) + ").bmp"
			y = w.replace(x, "")
			z = y + "(" + str(i + 1) + ").bmp"
			z = omr.preprocess_register(z, template_bmp)	

			matric_number, course_code = omr.matric_course(z, nargout = 2)
			answer_sheet_answers = omr.answers(z, total_questions)
			result = omr.result(answer_scheme_answers, answer_sheet_answers, total_questions)	

			collection_array.append([str(matric_number), str(course_code), str(answer_sheet_answers), result])

		generateExcel(course_code, collection_array)

	omr.terminate()
	Home.objects.filter(date = start_time).update(status = "COMPLETE")
