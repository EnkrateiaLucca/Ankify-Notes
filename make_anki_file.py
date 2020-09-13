from zipfile import ZipFile
import glob
import os
import pathlib

from bs4 import BeautifulSoup as bs4
import requests
import re

class Ankify:
	def __init__(self):
		self.question_indexes = []
		self.md_file = None
		self.py_file = None


	def ankify(self, file):
		extensions = [".zip", ".md", ".py"]
		for ext in extensions:
			if file.endswith(ext)==True:
				print(f"Its a {ext} file!")
				break
			
		if ext==".md":
			markdown_file_name = input("Input a name for the output markdown file: ")
			anki.md_file = file
			anki.ankify_markdown(txt_file="anki_{}.txt".format(markdown_file_name.strip(".md")))
		elif ext==".zip":
			anki.unzip_file_get_markdwon(file)
			print("Your markdown file was created: \n {}".format(anki.md_file))
			anki.md_file = anki.md_file[0]
			markdown_file_name = input("Input a name for the output markdown file: ")
			anki.ankify_markdown(txt_file="anki_{}.txt".format(markdown_file_name.strip(".md")))
		elif ext==".py":
			anki.py_file = file
			py_file = pathlib.Path(anki.py_file)
			anki.ankify_python(txt_file="anki_{}.txt".format(py_file.stem))

		print("Your questions were ankified!")

		
	def unzip_file_get_markdwon(self,zip_file):
		dest_folder = pathlib.Path(zip_file).parent
		with ZipFile(zip_file, "r") as zip:
			zip.extractall(dest_folder)

		self.md_file = glob.glob(str(dest_folder) + "/*.md")
		
	def ankify_markdown(self, txt_file="anki_question.txt"):
		with open(self.md_file, "r") as page:
			notion_page = page.readlines()
			for i,line in enumerate(notion_page):
				if "Anki*" in line:
					question = line[line.index("*")+2:]
					q_start_index = i
				try:
					if line.strip(" ").split()[0] == "#" and "q_start_index" in locals():
						q_end_index = i
						self.question_indexes.append([q_start_index,q_end_index,question])
						print(self.question_indexes)
				except:
					continue
		
		with open(txt_file, "w+") as anki_q:
			for i,ix_q in enumerate(self.question_indexes):
				anki_q.write(ix_q[2].strip("\n") + ";")
				for answer_line in notion_page[ix_q[0]+1:ix_q[1]]:
					anki_q.write(answer_line.strip("\n"))
				anki_q.write("\n")

	def ankify_python(self, txt_file="anki_question.txt"):
		with open(self.py_file, "r") as page:
			py_script = page.readlines()
			for i,line in enumerate(py_script):
				if "Anki*" in line:
					question = line[line.index("*")+2:]
					q_start_index = i
				try:
					if line.strip(" ").split()[0] == "#" and "q_start_index" in locals() and (len(line.strip(" ").split())==1):
						q_end_index = i
						self.question_indexes.append([q_start_index,q_end_index,question])
						print(self.question_indexes)
				except:
					continue
		
		with open(txt_file, "w+") as anki_q:
			for i,ix_q in enumerate(self.question_indexes):
				anki_q.write(ix_q[2].strip("\n") + ";")
				for answer_line in py_script[ix_q[0]+1:ix_q[1]]:
					anki_q.write(answer_line.strip("\n"))
				anki_q.write("\n")

	def ankify_article(self):
		url = "https://towardsdatascience.com/over-100-data-scientist-interview-questions-and-answers-c5a66186769a"
		#url = "https://towardsdatascience.com/10-algorithms-to-solve-before-your-python-coding-interview-feb74fb9bc27"
		headers = {'user-agent': 'Mozilla/5.0'} # Letting the server know we are real?
		r = requests.get(url, headers=headers)
		# Making sure that the page exists
		#question_pattern = "[1-9].* {1-20}"
		question_pattern = "Q: {1-50}"
		if r.status_code == 200:
		        html = r.text
		        soup = bs4(html, "html.parser")
		        potential_questions = soup.find_all("h2")
		        print("Printing Questions")
		        for line in potential_questions:
		        	question = re.findall(question_pattern, line.text)
		        	print(question)
        
if __name__=="__main__":
	file = input("Input the file path: ")
	anki = Ankify()
	anki.ankify(file)
	
	



				



