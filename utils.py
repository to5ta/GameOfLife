import random 

def getUID(length=10) -> str:
    uid = ""
    pool = [*range(ord('0'), ord('9'))]
    pool += [*range(ord('a'), ord('z'))]
    pool += [*range(ord('A'), ord('Z'))]
    for _ in range(length):
        uid += chr(pool[random.randint(0,len(pool)-1)])
    return uid
