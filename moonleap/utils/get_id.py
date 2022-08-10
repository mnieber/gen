import random
import uuid

# Use a fixed seed for the id generator
rd = random.Random()
rd.seed(0)


def get_id():
    return uuid.UUID(int=rd.getrandbits(128)).hex
