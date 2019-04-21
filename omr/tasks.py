from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from celery import shared_task
from omr.models import Home, Excel
from omr.utils import pdf2bmp, generateExcel
import OpticalMarkRecognition_MATLAB_V2


@shared_task
def omr_process(answer_scheme_name, answer_scheme_type, answer_sheet_name, answer_sheet_type, total_questions, start_time, course_code_excel):
	fs = FileSystemStorage()
	omr = OpticalMarkRecognition_MATLAB_V2.initialize()
	collection_array = []

	if answer_scheme_type == 'application/pdf':
		answer_scheme_path = fs.path(answer_scheme_name)
		answer_scheme_bmp, answer_scheme_page_num = pdf2bmp(answer_scheme_path)	

	answer_scheme_bmp = omr.preprocess_register(answer_scheme_bmp)
	
	if (answer_scheme_bmp == "FAILED" or answer_scheme_page_num != 1):
		matric_number = course_code = answer_sheet_answers = result = "FAILED"

		collection_array.append([matric_number, course_code, answer_sheet_answers, result])
		excel_path = generateExcel(course_code_excel, collection_array)

	else:
		answer_scheme_answers = omr.answers(answer_scheme_bmp, total_questions)

		if answer_sheet_type == 'application/pdf':
			answer_sheet_path = fs.path(answer_sheet_name)
			answer_sheet_bmp, answer_sheet_page_num = pdf2bmp(answer_sheet_path)

		if (answer_sheet_page_num == 1):
			answer_sheet_bmp = omr.preprocess_register(answer_sheet_bmp)

			if (answer_sheet_bmp == "FAILED"):
				matric_number = course_code = answer_sheet_answers = result = "FAILED"

				collection_array.append([matric_number, course_code, answer_sheet_answers, result])
				excel_path = generateExcel(course_code_excel, collection_array)

			else:
				matric_number, course_code = omr.matric_course(answer_sheet_bmp, nargout = 2)
			
				if ((len(str(matric_number)) != 10) or (len(str(course_code)) != 7)):
					matric_number = course_code = answer_sheet_answers = result = "FAILED"

				else:
					answer_sheet_answers = omr.answers(answer_sheet_bmp, total_questions)
					result = omr.result(answer_scheme_answers, answer_sheet_answers, total_questions)
				
				collection_array.append([str(matric_number), str(course_code), str(answer_sheet_answers), result])
				excel_path = generateExcel(course_code_excel, collection_array)

		else:
			for i in range(answer_sheet_page_num):
				w = answer_sheet_bmp
				x = "(" + str(answer_sheet_page_num) + ").bmp"
				y = w.replace(x, "")
				z = y + "(" + str(i + 1) + ").bmp"
				z = omr.preprocess_register(z)	

				if (z == "FAILED"):
					matric_number = course_code = answer_sheet_answers = result = "FAILED"

					collection_array.append([matric_number, course_code, answer_sheet_answers, result])

				else:
					matric_number, course_code = omr.matric_course(z, nargout = 2)
					
					if ((len(str(matric_number)) != 10) or (len(str(course_code)) != 7)):
						matric_number = course_code = answer_sheet_answers = result = "FAILED"

					else:
						answer_sheet_answers = omr.answers(z, total_questions)
						result = omr.result(answer_scheme_answers, answer_sheet_answers, total_questions)	

					collection_array.append([str(matric_number), str(course_code), str(answer_sheet_answers), result])

			excel_path = generateExcel(course_code_excel, collection_array)

	omr.terminate()

	home = Home.objects.get(course_code = course_code_excel, date = start_time)
	data = Excel(path = excel_path, home_id = home.pk)
	data.save()
	Home.objects.filter(course_code = course_code_excel, date = start_time).filter(status = "PENDING").update(status = "COMPLETE")