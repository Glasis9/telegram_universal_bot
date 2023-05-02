import requests


def give_random_funny_dog():
    dog = requests.get("https://dog.ceo/api/breeds/image/random").json()
    return dog["message"]
