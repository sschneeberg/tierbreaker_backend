from random import randint
import datetime, uuid

def gen_alpha():
    ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alpha = []
    while len(alpha) < 6:
        ind = randint(0, len(ALPHA)-1)
        alpha.append(ALPHA[ind])
    return alpha

def gen_key():
    numeric = list(str(datetime.datetime.now()).split('.')[1])
    alpha = gen_alpha()
    key = []
    for i in range(len(numeric)):
        if i % 2 == 0: key.append(alpha[i])
        else: key.append(numeric[i])
        
    return "".join(key)


def test_collisions():
    collisions = []
    keys = {}
    for i in range(100000):
        key = gen_key()
        if key in keys: collisions.append(key)
        else: keys[key] = True
    return len(collisions)

def test_uuid():
    collisions = []
    keys = {}
    for i in range(1000000):
        key = uuid.uuid4().hex[:8]
        if key in keys: collisions.append(key)
        else: keys[key] = True
    return len(collisions)

# print(test_collisions()) # consistently returns 30-45 collisions in 
# print(test_uuid()) # at len 6 300+ collisions, at len 8, 0-4 collisions in 6 tests




