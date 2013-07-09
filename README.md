picmerj
=======

a script that uses PIL to "merge" two pictures, creating a third

fairly rudimentary, but it can produce some interesting (to the author) images.
it does a pixel-by-pixel comparison of the images, and chooses one of the input pixels
to write to the output image, based on a commandline flag & maybe an r,g,b value

here is a code excerpt:

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
