#!/usr/bin/env python
#
# picmerj.py 
#
# this snippet may have future use:
#    try :
#        filter_name = sys.argv[2]
#    except :
#        filter_name = "EEM"   # edge enhance more
           
#    if filter_name == "FE" :
#        filter = ImageFilter.FIND_EDGES
#    elif filter_name == "EE" :
#        filter = ImageFilter.EDGE_ENHANCE
#    elif filter_name == "EEM" :
#        filter = ImageFilter.EDGE_ENHANCE_MORE
#    elif filter_name == "MX" : 
#        filter = ImageFilter.MaxFilter
#    else :
#        filter = ImageFilter.FIND_EDGES

#    img2 = img.filter(filter)

import Image
import ImageFilter
import sys
import random

white = (255,255,255)
black = (0,0,0)
max_red = (255,0,0)
max_green = (0,255,0)
max_blue = (0,0,255)

def color(x,y) :
    red = (x*x+y*y)%255
    green = (y*y*2+2*x*x)%255
    blue = (y*y*3+3*x*x)%255
    return (red, green, blue)
    
def noise_or_color(col, noise) :
    """higher value for noise (a float in [0..1]) means more noise"""
    if random.random() < noise :
        red = (col[0] + random.randrange(-50,50)) % 256
        green = (col[1] + random.randrange(-50,50)) % 256
        blue = (col[2] + random.randrange(-50,50)) % 256
        return (red,green,blue)
    else :
        return col
        
def clamp(val,min,max) :
    if (val < min) : return min
    if (val > max) : return max
    return val
        
def noisy_color(col, noise, amount) :
    """higher value for noise (a float in [0..1]) means more noise"""
    if random.random() < noise :
        red = (col[0] + random.randrange(-amount,amount))
        green = (col[1] + random.randrange(-amount,amount))
        blue = (col[2] + random.randrange(-amount,amount))
        red = clamp(red,0,255)
        green = clamp(green,0,255)
        blue = clamp(blue,0,255)
        return (red,green,blue)
    else :
        return col
               
def average(px1, px2) :
    return ((px1[0] + px2[0])/2, (px1[1] + px2[1])/2, (px1[2] + px2[2])/2)

def keep2(px1, px2) :
    return px2
    
def random_source(px1, px2) :
    if (random.random() < 0.5) :
        return px1
    return px2
    
def sum_channels(pixel) :
    return pixel[0] + pixel[1] + pixel[2]
    
def red_channel(pixel) :
    return pixel[0]
    
def green_channel(pixel) :
    return pixel[1]
    
def blue_channel(pixel) :
    return pixel[2]
    
def euclidean_dist(px,px2) :
    return (px[0] - px2[0])**2 + (px[1] - px2[1])**2 + (px[2] - px2[2])**2
    
def dist_to_target(px) :
    return euclidean_dist(px, (target_red, target_green, target_blue))
    
def brighter(px1, px2) :
    if (sum_channels(px1) > sum_channels(px2)) :
        return px1
    return px2
    
def darker(px1, px2) :
    if (sum_channels(px1) < sum_channels(px2)) :
        return px1
    return px2
    
def redder(px1, px2) :
    if (red_channel(px1) > red_channel(px2)) :
        return px1
    return px2
    
def greener(px1, px2) :
    if (green_channel(px1) > green_channel(px2)) :
        return px1
    return px2
    
def bluer(px1, px2) :
    if (blue_channel(px1) > blue_channel(px2)) :
        return px1
    return px2
    
def less_red(px1, px2) :
    if (red_channel(px1) < red_channel(px2)) :
        return px1
    return px2    
    
def less_green(px1, px2) :
    if (green_channel(px1) < green_channel(px2)) :
        return px1
    return px2    
    
def less_blue(px1, px2) :
    if (blue_channel(px1) < blue_channel(px2)) :
        return px1
    return px2    
    
def redder2(px1, px2) :
    if (red_channel(px1) - (blue_channel(px1) + green_channel(px1)) > red_channel(px2) - (blue_channel(px2) + green_channel(px2))) :
        return px1
    return px2
    
def greener2(px1, px2) :
    if (green_channel(px1) - (red_channel(px1) + blue_channel(px1)) > green_channel(px2) - (red_channel(px2) + blue_channel(px2))) :
        return px1
    return px2

def bluer2(px1, px2) :
    if (blue_channel(px1) - (red_channel(px1) + green_channel(px1)) > blue_channel(px2) - (red_channel(px2) + green_channel(px2))) :
        return px1
    return px2
    
def closer(px1, px2) :
    if (dist_to_target(px1) < dist_to_target(px2)) :
        return px1
    return px2
    
def further(px1, px2) :
    if (dist_to_target(px1) > dist_to_target(px2)) :
        return px1
    return px2
    
def below(px1, px2) :
    if (red_channel(px1) < target_red and green_channel(px1) < target_green and blue_channel(px1) < target_blue) :
        return px2
    return px1
       
def bluer_than_threshold(px1, px2) :
    if (bluer(px2, (target_red, target_green, target_blue)) == px2) :
        return px2
    return px1
    
def make_comparator(condition) :
    def choose_pixel(px1, px2) :
        return (condition(px1, px2))
    return choose_pixel        
       
def combine(im1, im2, width, height, combination) :
    for i in range(width) :
        for j in range(height) :
            im1[i,j] = combination(im1[i,j], im2[i,j])
            
if __name__ == '__main__':

    try :
        print( 'trying to open ' + sys.argv[1] )
        img = Image.open(sys.argv[1])
        print( 'trying to open ' + sys.argv[2] )
        img2 = Image.open(sys.argv[2])
    except :
        print( 'failed!' )
        img_size = (1000, 1000)
        img = Image.new('RGB', img_size, white)
        img2 = Image.open('images/seven11.png')

    img_pix = img.load()
    (x_pixels, y_pixels) = img.size
    img2_pix = img2.load()
    (width, height) = img2.size
    # try to prevent out-of-range errors 
    # by using the smaller dimensions
    if (width > x_pixels) : width = x_pixels
    if (height > y_pixels) : height = y_pixels
    
    try :
        target_red = int(sys.argv[4])
        target_green = int(sys.argv[5])
        target_blue = int(sys.argv[6])
    except :
        target_red = 11
        target_green = 111
        target_blue = 255
    
    if (sys.argv[3] == 'd') :
        combiner = darker
    elif (sys.argv[3] == 'c') :
        combiner = closer
    elif (sys.argv[3] == 'f') :
        combiner = further
    elif (sys.argv[3] == 'a') :
        combiner = average
    elif (sys.argv[3] == 'r') :
        combiner = redder
    elif (sys.argv[3] == 'g') :
        combiner = greener
    elif (sys.argv[3] == 'b') :
        combiner = bluer
    elif (sys.argv[3] == 'lr') :
        combiner = less_red
    elif (sys.argv[3] == 'lg') :
        combiner = less_green
    elif (sys.argv[3] == 'lb') :
        combiner = less_blue
    elif (sys.argv[3] == 'r2') :
        combiner = redder2
    elif (sys.argv[3] == 'g2') :
        combiner = greener2
    elif (sys.argv[3] == 'b2') :
        combiner = bluer2
    elif (sys.argv[3] == 'bt') :
        combiner = bluer_than_threshold
    elif (sys.argv[3] == 'bt2') :
        combiner = make_comparator(bluer2)
    elif (sys.argv[3] == 'rb') :
        combiner = below
    else :
        combiner = brighter
        
    combine(img_pix, img2_pix, width, height, combiner)
    
    try :
        #print sys.argv[1]
        left_part = sys.argv[1].split('/')[-1]
        left_part = left_part[:-4]
        right_part = sys.argv[2].split('/')[-1]
        right_part = right_part[:-4]
        newfile = 'newimages/' + left_part + '-' + right_part + '-' + sys.argv[3] + '.jpg'
        print( 'writing to ' + newfile )
        img.save(newfile)
    except :
        print( 'writing to default.jpg' )
        img.save('default.jpg')
    