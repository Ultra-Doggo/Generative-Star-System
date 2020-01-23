import cairo, argparse, math, random, datetime
from PIL import Image, ImageDraw

import gen_naming

star_colors_list = [
    #blues
    (123, 251, 253), (75, 179, 253), (87, 213, 255), (28, 198, 255), (103, 185, 234),
    #blue-whites
    (220, 237, 255), (191, 229, 249), (153, 240, 255), (186, 237, 250), (202, 234, 250),
    # white
    (255, 255, 255),
    # yellow-whites
    (255, 254, 209), (249, 224, 110), (255, 247, 131), (252, 242, 137), (255, 236, 153),
    # yellows
    (255, 231, 74), (255, 225, 106), (248, 219, 90), (255, 239, 97), (255, 225, 85),
    # oranges
    (242, 157, 56), (255, 195, 67), (255, 211, 97), (224, 103, 63), (237, 130, 59),
    # reds
    (255, 87, 69), (226, 75, 59), (204, 67, 47), (216, 82, 57), (173, 43, 29)
]

planet_colors_list = [
    # reds
    (163, 70, 74), (217, 76, 61), (192, 63, 48), (181, 101, 101), (255, 105, 105),
    # oranges
    (238, 107, 102), (227, 152, 86), (255, 146, 51), (242, 166, 0), (255, 182, 23),
    # yellows
    (224, 205, 81), (245, 214, 15), (255, 215, 0), (238, 232, 170), (255, 250, 205),
    # greens
    (144,238,144), (60,179,113), (114, 190, 171), (34,139,34), (50,205,50),
    # blues
    (125, 237, 249), (36, 72, 124), (174, 227, 249), (15, 158, 219), (82, 113, 191),
    # purples
    (176, 125, 183), (74, 36, 68), (167, 158, 219), (157, 115, 235), (116, 62, 150),
    # pinks
    (245, 108, 133), (227, 126, 176), (255, 186, 203), (219,112,147), (255, 140, 201),
    # browns
    (166, 111, 90), (160, 82, 45), (128, 0, 0), (165, 45, 45), (222, 184, 135),
    # wild cards
    (0, 226, 230), (238, 247, 166), (255, 99, 118), (0, 100, 122), (219, 67, 230)
]

background_colors_list = [
    (55, 56, 74), (33, 34, 44), (40, 42, 54), (25, 26, 23), (28, 30, 38), 
    (53, 56, 69), (30, 32, 34), (19, 28, 41), (74, 74, 74), (2, 19, 33)
]

def draw_orbit(cr, line_width, x, y, radius):
    cr.set_source_rgb(0.58, 0.58, 0.58)
    cr.set_line_width(line_width)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.stroke()

def draw_circle_fill(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.fill()

def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height)
    cr.fill()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", default = 3000, type = int)
    parser.add_argument("--height", default = 2000, type = int)
    parser.add_argument("--sunsize", default = random.randint(75, 140), type = int)
    parser.add_argument("--min_dist", default = 20, type = int)
    parser.add_argument("--max_dist", default = 60, type = int)
    args = parser.parse_args()

    # the range in how far planets can be from one another (in pixels)
    min_dist = args.min_dist
    max_dist = args.max_dist
    # in case max_dist isn't specified via command line
    if (max_dist < min_dist):
        max_dist = min_dist + 40

    # image dimensions
    width, height = args.width, args.height
    sun_size = args.sunsize

    # center the sun within the image
    sun_center_x = width / 2
    sun_center_y = height / 2

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    # choose background color
    bg_color = random.choice(background_colors_list)
    # convert rgb to 0 -> 1 float values
    back_r, back_g, back_b = bg_color[0]/255.0, bg_color[1]/255.0, bg_color[2]/255.0
    # first function call - create the background
    draw_background(cr, back_r, back_g, back_b, width, height)

    # choose sun's color
    sun_color = random.choice(star_colors_list)
    # convert rgb to 0 -> 1 float values
    sun_r, sun_g, sun_b = sun_color[0]/255.0, sun_color[1]/255.0, sun_color[2]/255.0
    # draw the sun
    draw_circle_fill(cr, sun_center_x, sun_center_y, sun_size, sun_r, sun_g, sun_b)


    prev_center_x = sun_center_x
    prev_center_y = sun_center_y
    prev_size = sun_size
    #print("prev_center_x:", prev_center_x)
    #print("prev_center_y:", prev_center_y)
    #print("prev_size:", prev_size)

    min_planet_size = sun_size // 14
    max_planet_size = sun_size // 4
    #print("min planet possible:", min_planet_size)
    #print("max planet possible:", max_planet_size)


    # drawing the planets, orbits, and disconnectors
    limit = random.randint(1, 9)
    #print(limit)
    for x in range(0, limit):

        #print()
        #print("PLANET ", x+1)
        #print("prev size = ", prev_size)
        
        # choose random color
        planet_color = random.choice(planet_colors_list)
        # convert to rgb of (0.0 to 1.0 scale)
        planet_r, planet_g, planet_b = planet_color[0]/255.0, planet_color[1]/255.0, planet_color[2]/255.0

        # randomly choose a distance the prev object and next object
        distance_between = random.randint(min_dist, max_dist)
        #print("distance between:", distance_between)

        # determine size of this planet
        next_size = random.randint(min_planet_size, max_planet_size)
        #print("next size:", next_size)


        # center point shorthand
        cx = width/2
        cy = height/2

        # temp center for planet, before rotating
        temp_center_x = prev_center_x + (prev_size) + distance_between
        temp_center_y = prev_center_y + (prev_size) + distance_between
        #print("temp center x = ", temp_center_x)
        #print("temp center y = ", temp_center_y)

        # shorthand
        tx = temp_center_x
        ty = temp_center_y

        # generate random angle for which planet will lie along
        rand_theta = random.randint(1, 360)
        #print("random theta = ", rand_theta)

        # calculate center of this planet
        ex = (cx + (tx-cx)*math.cos(rand_theta) + (cy-ty)*math.sin(rand_theta))
        ey = (cy + (ty-cy)*math.cos(rand_theta) + (tx-cx)*math.sin(rand_theta))
        #print("ex = ", ex)
        #print("ey = ", ey)

        # draw the orbit - use the distance formula
        orbit_radius = math.sqrt(pow((ex-cx), 2) + pow((ey-cy), 2))
        draw_orbit(cr, 3, width/2, height/2, orbit_radius)
        #print("orbit radius = ", orbit_radius)

        # draw the "disconnector"
        draw_circle_fill(cr, ex, ey, next_size*1.5, back_r, back_g, back_b)

        # draw the planet, at random place along revolution
        draw_circle_fill(cr, ex, ey, next_size, planet_r, planet_g, planet_b)

        # update control variables before looping to next planet
        prev_center_x = temp_center_x
        prev_center_y = temp_center_y
        prev_size = next_size


    # get current date & time
    currentDT = datetime.datetime.now()

    # generate name for the system
    system_name = gen_naming.system_name()
    #print(system_name)

    # saving the image as png
    #ims.write_to_png('output/' + system_name + ' @ ' + str(currentDT) + '.png')

    # simpler naming convention
    ims.write_to_png('output/' + system_name + '.png')


if __name__ == "__main__":
    main()