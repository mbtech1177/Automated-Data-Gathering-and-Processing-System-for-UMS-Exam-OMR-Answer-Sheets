import os, PythonMagick, PyPDF2, xlsxwriter
from PythonMagick import Image
from PyPDF2 import PdfFileWriter, PdfFileReader

def pdf2bmp(path):

	img = Image()
	f = open(path, "rb")
	opened_pdf = PdfFileReader(f)
	page_num = opened_pdf.getNumPages()

	if page_num == 1:
		img.read(path)				
		output_bmp = path.replace(".pdf", ".bmp")
		img.write(output_bmp)

	else:
		for i in range(page_num):
			pdfw = PdfFileWriter()
			pdfw.addPage(opened_pdf.getPage(i))

			output_path = os.path.splitext(path)[0]
			output_pdf = output_path + "_page(" + str(i + 1) + ").pdf"
			with open(output_pdf, "wb") as output:
				pdfw.write(output)

			img.read(output_pdf)
			output_bmp = output_pdf.replace(".pdf", ".bmp")
			img.write(output_bmp)

	f.close()

	return output_bmp, page_num

def generateExcel(course_code, data):

	excel_name = "media/" + course_code + ".xlsx"
	workbook = xlsxwriter.Workbook(excel_name)
	worksheet = workbook.add_worksheet()

	bold = workbook.add_format({'bold': True})
	worksheet.write('A1', 'Matric Number', bold)
	worksheet.write('B1', 'Course Code', bold)
	worksheet.write('C1', 'Answers', bold)
	worksheet.write('D1', 'Result', bold)

	row = 1
	col = 0

	for matric, course, answers, result in (data): 
		worksheet.write(row, col, matric)
		worksheet.write(row, col + 1, course)
		worksheet.write(row, col + 2, answers)
		worksheet.write(row, col + 3, result)
		row += 1

	workbook.close()

	return excel_name
