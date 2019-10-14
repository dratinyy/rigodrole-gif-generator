from os import listdir, makedirs
from os.path import isfile, join, exists
from PIL import Image
import imageio

# Fonctionne en plusieurs étapes :
# 1. Découpe l'image animée de fond en frames
# 2. Ajoute des éléments tournoyants et la photo par dessus chaque frame
# 3. Compile à nouveau le gif

background_image_name   = "background/bg10.gif"
frame_count_multiplier  = 1
frame_duration          = 0.04
photo_name              = "josh.png"
item_names              = [ "items/brocoli.png",
                            "items/chaussure.png",
                            "items/singe.png",
                            "items/mouette.png" ]

item_data               = [ { "item_index": 0,
                              "size": (150, 150),
                              "position": (30, 230), 
                              "initial_angle": 120,
                              "rotation_speed": 1,
                              "rotation_direction": -1 },
                              { "item_index": 0,
                              "size": (150, 150),
                              "position": (470, 200), 
                              "initial_angle": 240,
                              "rotation_speed": 1,
                              "rotation_direction": 1 },
                              { "item_index": 0,
                              "size": (150, 150),
                              "position": (340, 480), 
                              "initial_angle": 0,
                              "rotation_speed": 1,
                              "rotation_direction": -1 },
                              { "item_index": 1,
                              "size": (140, 140),
                              "position": (320, 320), 
                              "initial_angle": 100,
                              "rotation_speed": 1,
                              "rotation_direction": 1 },
                              { "item_index": 1,
                              "size": (140, 140),
                              "position": (310, 30), 
                              "initial_angle": 300,
                              "rotation_speed": 1,
                              "rotation_direction": -1 },
                              { "item_index": 2,
                              "size": (130, 130),
                              "position": (40, 460), 
                              "initial_angle": 170,
                              "rotation_speed": 1,
                              "rotation_direction": 1 },
                              { "item_index": 2,
                              "size": (130, 130),
                              "position": (500, 20), 
                              "initial_angle": 230,
                              "rotation_speed": 1,
                              "rotation_direction": 1 },
                              { "item_index": 3,
                              "size": (200, 200),
                              "position": (180, 150), 
                              "initial_angle": 0,
                              "rotation_speed": 1,
                              "rotation_direction": 1 },
                              { "item_index": 3,
                              "size": (200, 200),
                              "position": (15, 10), 
                              "initial_angle": 130,
                              "rotation_speed": 1,
                              "rotation_direction": -1 },
                              { "item_index": 3,
                              "size": (200, 200),
                              "position": (450, 380), 
                              "initial_angle": 210,
                              "rotation_speed": 1,
                              "rotation_direction": -1 } ]

# Ouvre le gif de fond
bg_image_reader = imageio.get_reader(background_image_name)
frame_directory = "frames/"
if not exists(frame_directory):
    makedirs(frame_directory)

# Ouvre la photo
photo = Image.open(photo_name)
photo_size = photo.size

# Ouvre les éléments à faire tournoyer
items = [ Image.open(i) for i in item_names ]

# Augmente le nombre de frames pour ralentir la rotation des élements si nécessaire
bg_gif = list(bg_image_reader)
bg_gif = bg_gif * frame_count_multiplier

# On itère sur les frames
for i, frame in enumerate(bg_gif):
    # Chaque frame est enregistrée puis ouverte avec PIL.Image pour faciliter l'édition
    Image.fromarray(frame).save(f"{frame_directory}{i:04}.png")
    frame = Image.open(f"{frame_directory}{i:04}.png")
    frame = frame.resize(photo_size, Image.ANTIALIAS)

    # On itère sur les éléments à ajouter
    for item in item_data:
        # L'élément est ajuste à la bonne taille
        temp = items[item["item_index"]].resize(item["size"], Image.ANTIALIAS)
        # L'élément est tourné au besoin
        temp = temp.rotate(item["initial_angle"] + 360 
            * (i if item["rotation_direction"] == 1 else (len(bg_gif) - i)) 
            * item["rotation_speed"]
            / len(bg_gif))
        # L'élément est collé
        frame.paste(temp, item["position"], temp)
    
    # La photo est collée
    frame.paste(photo, (0, 0), photo)
    # La frame est enregistrée dans le dossier des frames
    frame.save(f"{frame_directory}{i:04}.png", "png")

# Les frames sont à nouveau compilée dans un gifs
frames = [f for f in listdir(frame_directory) if isfile(join(frame_directory, f))]
images = []
for f in frames:
    frame = imageio.imread(frame_directory + f)
    images.append(frame)
imageio.mimsave('output.gif', images, duration=frame_duration)
