from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db.models import F

from omr.forms import SignUpForm
from omr.models import Home, Excel
from omr.tasks import omr_process

from datetime import datetime
import os, openpyxl

# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST) 

		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
			user = authenticate(username = username, password = raw_password)
			login(request, user)
			return redirect('/omr/signup_complete')
	else:
		form = SignUpForm()

	return render(request, 'omr/signup.html', {'form': form})

def signup_complete(request):
	return render(request, 'omr/signup_complete.html')

def logged_out(request):
	return render(request, 'omr/logged_out.html')

def home(request):
	data = Home.objects.all()
	args = {'data': data}

	return render(request, 'omr/home.html', args)

def view_results(request, home_id):
	excel_path = Excel.objects.get(home_id = home_id).path
	task_number = Home.objects.get(pk = home_id).number
	wb = openpyxl.load_workbook(excel_path)
	worksheet = wb["Sheet1"]
	excel_data = list()
	args = {'excel_data': excel_data, 'home_id': home_id, 'task_number': task_number}

	for row in worksheet.iter_rows():
		row_data = list()
		
		for cell in row:
			row_data.append(str(cell.value))
		excel_data.append(row_data)

	return render(request, 'omr/view_results.html', args)

def download_excel(request, home_id):
	excel_path = Excel.objects.get(home_id = home_id).path
	generated_date = Home.objects.get(pk = home_id).date

	if os.path.exists(excel_path):
		with open(excel_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type = "application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename =' + '[' + str(generated_date.strftime("%x")) + ']' + '_' + '[' + str(generated_date.strftime("%X")) + ']' + '_' + os.path.basename(excel_path)
			return response

	raise Http404

def delete_tasks(request, task_number):
	task = Home.objects.get(number = task_number)
	task.delete()
	if Home.objects.filter(number__gt =  task_number).exists():
		Home.objects.filter(number__gt = task_number).update(number = F('number') - 1)

	return redirect('/omr/home')

def upload_files(request):
	start_time = datetime.now()

	if request.method == 'POST':
		fs = FileSystemStorage()

		course_code = request.POST.get('course_code')
		course_name = request.POST.get('course_name')
		total_questions = int(request.POST.get('total_ques'))
		if Home.objects.filter(number = 1).exists():
			number = Home.objects.values_list('number', flat = True).order_by("-id")[0] + 1
		else:
			number = 1

		data = Home(number = number, course_code = course_code, course_name = course_name, date = start_time, status = "PENDING")
		data.save()

		template_bmp = "template.bmp"

		answer_scheme = request.FILES['answer_scheme']
		answer_scheme_name = fs.save(answer_scheme.name, answer_scheme)
		answer_scheme_type = answer_scheme.content_type

		answer_sheet = request.FILES['answer_sheet']
		answer_sheet_name = fs.save(answer_sheet.name, answer_sheet)
		answer_sheet_type = answer_sheet.content_type
		omr_process.delay(answer_scheme_name, answer_scheme_type, answer_sheet_name, answer_sheet_type, total_questions, template_bmp, start_time, course_code)

		return redirect('/omr/home')

	return render(request, 'omr/upload_files.html')