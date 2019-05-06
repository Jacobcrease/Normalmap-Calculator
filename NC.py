import numpy as np
import cv2
#from memory_profiler import profile


#@profile
def NC():
    input_name = "demo.jpg"

    pic = cv2.imread(input_name,1)
    gray = cv2.imread(input_name,0)
    _, th2 = cv2.threshold(gray,0,150,cv2.THRESH_BINARY)
    height, width, _ = pic.shape

    #for less extreme values set it lower
    # value should be between 0 and 1
    bmp_percent = 0.5
    nrm_percent = 0.7

    bump = gray
    bump = (np.ones((height,width),dtype = np.uint16)*200*(1-bmp_percent) + bump*bmp_percent)

    # bmp pic can be modified for bump or roughness
    cv2.imwrite(input_name[:len(input_name)-4]+"_notfinished_bmp.png",bump)

    #starting edge detection with sobel horizontal and vertical
    sobel_x = cv2.Sobel(bump, cv2.CV_16S,1,0, ksize =-1)
    sobel_y = cv2.Sobel(bump, cv2.CV_16S,0,1, ksize =-1)

    # Using absolute units if there is an (horizental or vertical) edge, and 0 if there is not
    abs_x = cv2.convertScaleAbs(sobel_x) - np.ones((height,width),dtype = np.uint8)*255
    abs_y = cv2.convertScaleAbs(sobel_y) - np.ones((height,width),dtype = np.uint8)*255

    #Converting into a value between -1 and 1 to be ready to convert into normalmap values
    pixel_x = (abs_x*(2/255)-1)
    pixel_y = (abs_y*(2/255)-1)

    #Array of ones (fastens the calculation)
    ones = np.ones((height,width),dtype = np.uint8)

    '''1 color for each pixel (3 dimensional array per pixel)
    x/y value is 1 z value is pixel_x/pixel_y
    this leads to a color change only if the is an horizontal/vertical edge'''

    dx = np.zeros((height,width,3),dtype = np.float64)
    dx[:,:,0] = ones
    dx[:,:,2] = pixel_x
    dy = np.zeros((height,width,3),dtype = np.float64)
    dy[:,:,1] = ones
    dy[:,:,2] = pixel_y

    #norm values are the lenght of each array(treated like vector's)
    dx_norm = np.sqrt(dx[:,:,0]**2+dx[:,:,1]**2+dx[:,:,2]**2)**-1
    dy_norm = np.sqrt(dy[:,:,0]**2+dy[:,:,1]**2+dy[:,:,2]**2)**-1

    #normalizing the arrays (treated like vector's)
    dx[:,:,0] = np.multiply(dx[:,:,0],dx_norm)
    dx[:,:,1] = np.multiply(dx[:,:,1],dx_norm)
    dx[:,:,2] = np.multiply(dx[:,:,2],dx_norm)

    dy[:,:,0] = np.multiply(dy[:,:,0],dy_norm)
    dy[:,:,1] = np.multiply(dy[:,:,1],dy_norm)
    dy[:,:,2] = np.multiply(dy[:,:,2],dy_norm)

    #cross product of x and y is the final normalmap(with extreme values)
    '''26.02.2019 better IDEA here
    Idea : if there are horizontal and vertical values,
    try to mark the shape and the top/bottom/side of the unevenness
    calculate a soft color flow (find out how it's treated in "real" normal's)
    (own hue or something like that)
    '''

    dcross = np.zeros((height,width,3),dtype = np.float)
    #mixed up course of cv2 bs
    dcross[:,:,2] = (np.multiply(dx[:,:,1],dy[:,:,2]) - np.multiply(dx[:,:,2],dy[:,:,1]) + ones)*(256/2)
    dcross[:,:,1] = (np.multiply(dx[:,:,2],dy[:,:,0]) - np.multiply(dx[:,:,0],dy[:,:,2]) + ones)*(256/2)
    dcross[:,:,0] = (np.multiply(dx[:,:,0],dy[:,:,1]) - np.multiply(dx[:,:,1],dy[:,:,0]) + ones)*(128/2) + ones * 128

    #calc normals to Normalmap
    # z is blue between 128 and 256
    # x is red between 0 and 256
    # y is green between 0 and 256
    blue = np.array([255,127,127])
    dcross = (dcross*nrm_percent + blue*(1-nrm_percent))
    color_matrix = dcross.astype(np.uint8)

    cv2.imwrite(input_name[:len(input_name)-4]+"_nrm.png",color_matrix)
    print ("ready")
    return ("ready")

if __name__ == '__main__':
    NC()
    end = input("end")