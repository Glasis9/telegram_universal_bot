import requests


def give_random_joke():
    joke = requests.get("http://rzhunemogu.ru/RandJSON.aspx?CType=11")
    return " ".join(joke.text.split("\"content\":")[1:]).lstrip().rstrip().strip("}\"")
