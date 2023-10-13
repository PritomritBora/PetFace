import os
import base64
import json

DB_DIR = 'db'


def get_profile(idx):
    with open(os.path.join(DB_DIR, str(idx), 'profile.json')) as f:
        return json.load(f)


def create_profile(name, contact_email, b64_image, animal='Cat', lost=True):
    id = max_profile_idx() + 1
    profile = {
        'id': id,
        'name': name,
        'animal': animal,
        'lost': lost,
        'contact_email': contact_email,
        'image': b64_image
    }
    dir = os.join(DB_DIR, str(id))
    os.mkdir(dir)
    save_json(os.join(dir, 'profile.json'))
    return profile


def max_profile_idx():
    return max([int(d) for d in os.listdir(DB_DIR) if d != 'utils.py'])


def image_b64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def save_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def create_random_db():
    names = ['Rover', 'Lotto', 'Molly', 'Apollo', 'Stacy', 'Tracy', 'Pickles', 'Fido', 'Sgt Pepper', 'K9', 'Rufus', 'Pippin', 'Bilbo']
    # dir_idx = ['a','b','c','d','e','f','g','h','i','j','k','l','m']
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            # os.rename(dir, str(dir_idx.index(dir)))
            profile = {
                'id': int(dir),
                'name': names[int(dir)],
                'animal': 'Cat',
                'lost': True,
                'contact_email': 'lost_my_pet@gmail.com',
                'image': image_b64(os.path.join(dir, os.listdir(dir)[0]))
            }
            save_json(os.path.join(dir, 'profile.json'), profile)


if __name__ == "__main__":
    create_random_db()

