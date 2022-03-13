from time import sleep
from PIL import Image, ImageDraw
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

		self.africa_countries_dictionary = {}
		self.africa_countries_list = []
		with open(f"../files/africa_countries_{self.resolution}_{self.zoom}.txt", "r") as f:
			for i in f.readlines():
				split = i.strip().split(" ")
				self.africa_countries_list.append(split[0])
				self.africa_countries_dictionary[split[0]] = {"x": int(split[1]), "y": int(split[2])}

	def SolveAfricaCountries(self):
		dir = "../files/africa_countries_temp"
		try:
			os.mkdir(dir)
		except:
			shutil.rmtree(dir)
			os.mkdir(dir)
		i = 0
		while 1:
			image_name = f"{dir}/_{i}.png"
			seed = (108, 24)
			rep_value = (138, 181, 155)
			pyautogui.screenshot(image_name, region=(535, 200, 200, 35))
			image = Image.open(image_name).convert('RGB')
			ImageDraw.floodfill(image, seed, rep_value, thresh=50)
			image.save(image_name[:-4] + "_filled.png")
			text = pytesseract.image_to_string(image, lang="eng")
			formatted_text = text.strip().replace(" ", "").lower()
			times = 0
			if formatted_text == "":
				break
			while formatted_text not in self.africa_countries_list and times < 5:
				formatted_text = formatted_text[1:]
				if  "african" in formatted_text: formatted_text = "centralafricanrepublic"
				elif  "of" in formatted_text: formatted_text = "congo"
				elif  "prin" in formatted_text: formatted_text = "princip"
				elif  "verde" in formatted_text: formatted_text = "caboverde"
				elif  "bissau" in formatted_text: formatted_text = "guinea-bissau"
				elif  "cratic" in formatted_text: formatted_text = "democratic"
				elif  "dji" in formatted_text: formatted_text = "dijibouti"
				elif  "coast" in formatted_text: formatted_text = "ivorycoast"
				elif  "faso" in formatted_text: formatted_text = "burkinafaso"
				elif  "zambia" in formatted_text: formatted_text = "zambia"
				elif  "mauritic" in formatted_text: formatted_text = "mauritius"
				times += 1
			coords = self.africa_countries_dictionary.get(formatted_text, None)
			if not coords:
				print("Name not found")
				continue
			pyautogui.click(x=coords["x"], y=coords["y"])
			sleep(self.timeout)
			i += 1
		shutil.rmtree(dir)

solver = SeterraSolver(timeout=0)

pyautogui.scroll(-250)
while 1:
	pyautogui.click(x=1241, y=1028) # Click the restart button
	solver.SolveAfricaCountries()
	sleep(1)
	pyautogui.click(x=814, y=605) # Click the OK button