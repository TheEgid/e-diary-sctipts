#from .datacenter.models import Schoolkid, Mark, Chastisement
import random

def read_file(filename):
    with open(filename, encoding='utf-8') as file_:
        return file_.readlines()

def get_random_compliment(filename='compliments.txt'):
    compliments = read_file(filename)
    compliments_list = [compliment.strip() for compliment in compliments]
    return random.sample(compliments_list, k=1)[0]




if __name__ == '__main__':
    print(get_random_compliment('compliments.txt'))
