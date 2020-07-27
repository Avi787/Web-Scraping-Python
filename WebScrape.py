import requests 
from bs4 import BeautifulSoup
from csv import writer
from random import choice
from colorama import init
from termcolor import colored, cprint
from pyfiglet import figlet_format
 
init()
 
root_url = "http://quotes.toscrape.com/"
 
def header():
	header = figlet_format("WEB SCRAPING PROJECT")
	header = colored(header, color="red", attrs=["bold"])
	print(header)
 
class Quote:
	def __init__(self, title, name, url):
		self.title = title
		self.name = name
		self.url = url
 
	def match(self, ans):
		if self.name.lower() == ans.lower():
			return True
 
	def hints(self, i):
		response = requests.get(root_url + self.url)
		soup = BeautifulSoup(response.text, "html.parser")
		birth_date = soup.find(class_="author-born-date").get_text()
		birth_location = soup.find(class_="author-born-location").get_text()
		arr = soup.find(class_="author-title").get_text().split(" ")
		initials = arr[0][0] + ". " + arr[1][0]
		firstnameletters = str(len(arr[0]))
		lastnameletters = str(len(arr[1]))
		hint_arr = [f"The person was born {birth_location} on {birth_date}",
				    f"The person's initials are {initials}",
				    f"The person's first name contains {firstnameletters} letters",
				    f"The person's last name contains {lastnameletters} letters"]
		return hint_arr[i]
 
def request():
	lst = []
	new_url = "page/1"
	while new_url:
		response = requests.get(root_url + new_url)
		soup = BeautifulSoup(response.text, "html.parser")
		quotes = soup.select(".quote")
		for quote in quotes:
			title = quote.find(class_="text").get_text()
			name = quote.find(class_="author").get_text()
			url = quote.find("a")["href"]
			lst.append(Quote(title, name, url))
		
		next_button = soup.find(class_="next")
		new_url = next_button.find("a")["href"] if next_button else None
	return lst
 
def play():
	lst = request()
	quote = choice(lst)
	max = 4
	print("Here's a quote: \n")
	print(f"{quote.title} \n")
	print(f"Who said this? Guesses remaining: {max}")
	i = 0
	for x in range(max):
		answer = input()
		if quote.match(answer):
			print(colored("You guessed correctly! Congratulations!", color="green", attrs=["bold"]))
			break
		else:
			if x == max - 1:
				print(colored(f"Sorry you out of guesses. The answer was {quote.name}", color="red", attrs=["bold"]))
			else:
				print(colored(f"Wrong, please try again. Guess remaining: {(max-1)-x}",color="red", attrs=["bold"]))
				print("Here's a hint: " + quote.hints(i))
				i += 1
 
def play_more():
	playing = True	
	while playing:
		play_again = input("Do you want to play again Y/N \n")
		if play_again.lower() == "y":
			play()
		else:
			playing = False
			print(colored(figlet_format("Goodbye!"), color="green", attrs=["bold"]))
	
 
header()
play()
play_more()
 