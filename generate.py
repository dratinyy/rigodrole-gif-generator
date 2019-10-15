from os import listdir, makedirs
from os.path import isfile, join, exists
from PIL import Image
import imageio

# Fonctionne en plusieurs étapes :
# 1. Découpe l'image animée de fond en frames
# 2. Ajoute des éléments tournoyants et la photo par dessus chaque frame
# 3. Compile à nouveau le gif

background_image_name   = "background/bg9.gif"
frame_count_multiplier  = 2
frame_duration          = 0.04
photo_name              = "Hugu.png"
item_names              = [ "items/bombe.png",
                            "items/canard.png",
                            "items/cochon.png",
                            "items/placard.png",
                            "items/tomate.png" ]

item_data               = [ { "item_index": 0,
                              "size": (110, 110),
                              "position": (530, 20),
                              "initial_angle": 0,
                              "rotation_speed": 1,
                              "rotation_direction": 1 },

                              { "item_index": 0,
                              "size": (110, 110),
                              "position": (270, 530),
                              "initial_angle": 75,
                              "rotation_speed": 3,
                              "rotation_direction": -1 },

                              { "item_index": 0,
                              "size": (110, 110),
                              "position": (10, 520),
                              "initial_angle": 210,
                              "rotation_speed": 4,
                              "rotation_direction": 1 },

                              { "item_index": 0,
                              "size": (110, 110),
                              "position": (10, 200),
                              "initial_angle": 260,
                              "rotation_speed": 7,
                              "rotation_direction": -1 },

                              { "item_index": 1,
                              "size": (150, 150),
                              "position": (490, 170),
                              "initial_angle": 30,
                              "rotation_speed": 3,
                              "rotation_direction": -1 },

                              { "item_index": 1,
                              "size": (150, 150),
                              "position": (310, 130),
                              "initial_angle": 270,
                              "rotation_speed": 4,
                              "rotation_direction": 1 },

                              { "item_index": 1,
                              "size": (150, 150),
                              "position": (200, 320),
                              "initial_angle": 120,
                              "rotation_speed": 6,
                              "rotation_direction": -1 },

                              { "item_index": 2,
                              "size": (160, 160),
                              "position": (100, 450),
                              "initial_angle": 210,
                              "rotation_speed": 4,
                              "rotation_direction": 1 },

                              { "item_index": 3,
                              "size": (250, 250),
                              "position": (110, 30),
                              "initial_angle": 210,
                              "rotation_speed": 1,
                              "rotation_direction": 1 },

                              { "item_index": 4,
                              "size": (80, 80),
                              "position": (50, 60),
                              "initial_angle": 310,
                              "rotation_speed": 8,
                              "rotation_direction": -1 },

                              { "item_index": 4,
                              "size": (80, 80),
                              "position": (60, 350),
                              "initial_angle": 220,
                              "rotation_speed": 3,
                              "rotation_direction": -1 },

                              { "item_index": 4,
                              "size": (80, 80),
                              "position": (380, 20),
                              "initial_angle": 70,
                              "rotation_speed": 4,
                              "rotation_direction": 1 } ]

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
