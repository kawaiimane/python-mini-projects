import random
import string


def gen_rand_password(length):
    # character pool
    characters = string.ascii_letters + string.digits + string.punctuation

    # length
    password = "".join(random.choice(characters) for i in range(length))

    return password


print(gen_rand_password(12))
