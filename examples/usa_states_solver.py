from time import sleep
from PIL import Image
import pytesseract
import pyautogui
import shutil
import os

pytesseract.pytesseract.tesseract_cmd = r'X:\python\modules\pytes\tesseract.exe'

class SeterraSolver:

	def __init__(self, **kwargs):
		self.resolution = kwargs.get('resolution',"1920x1080")
		self.zoom = kwargs.get("zoom", 100)
		self.timeout = kwargs.get("timeout", 1)

		self.usa_states_dictionary = {}
		self.usa_states_list = []
		with open(f"../files/usa_states_{self.resolution}_{self.zoom}.txt", "r") as f:
			for i in f.readlines():
				split = i.strip().split(" ")
				self.usa_states_list.append(split[0])
				self.usa_states_dictionary[split[0]] = {"x": int(split[1]), "y": int(split[2])}
		
	def SolveUsaStates(self):
		dir = "../files/usa_states_temp"
		try:
			os.mkdir(dir)
		except:
			shutil.rmtree(dir)
			os.mkdir(dir)
		i = 0
		while 1:
			image_name = f"{dir}/_{i}.png"
			pyautogui.screenshot(image_name, region=(535, 220, 200, 35))
			image = Image.open(image_name)
			image_gray = image.convert('L')
			image_gray.save(image_name[:-4] + "_grayscale.jpg")
			text = pytesseract.image_to_string(image_gray, lang="eng")
			formatted_text = text.strip().replace(" ", "").lower()
			times = 0
			if formatted_text == "":
				break
			while formatted_text not in self.usa_states_list and times < 5:
				formatted_text = formatted_text[1:]
				if formatted_text == "lowa": formatted_text = "iowa"
				if formatted_text == "iltinois": formatted_text = "illinois"
				times += 1
			coords = self.usa_states_dictionary.get(formatted_text, None)
			if not coords:
				print("Name not found")
				continue
			pyautogui.click(x=coords["x"], y=coords["y"])
			sleep(self.timeout)
			i += 1
		shutil.rmtree(dir)

solver = SeterraSolver()

pyautogui.scroll(-240)
while 1:
	pyautogui.click(x=1241, y=1028) # Click the restart button
	solver.SolveUsaStates()
	sleep(1)
	pyautogui.click(x=814, y=635) # Click the OK button