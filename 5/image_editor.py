#################################################################
# FILE : image_editor.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex3 2024
# DESCRIPTION: BATTLESHIPS
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################

from math import floor, ceil
from ex5_helper import *
from typing import Optional

WORST_POSSIBLE_MSE = 255 ** 2


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """seperates a matrix (rep. an image) to rgb factors"""
    layers = []
    for (color_index,_) in enumerate(image[0][0]):
        layers.append([])
        for (row_num,row) in enumerate(image):
            layers[color_index].append([])
            for (_,pixel) in enumerate(row):
                layers[color_index][row_num].append(pixel[color_index])
    return layers



def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """the reverse function  to seperat_channels"""
    colored = []
    for row in range(len(channels[0])):
        colored.append([])
        for col in range(len(channels[0][0])):
            colored[row].append([channels[x][row][col] for x in range(len(channels))])
    return colored


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """returns a greyscale image"""
    grey_scale = []
    for row_num, row in enumerate(colored_image):
        grey_scale.append([])
        for pixel in row:
            grey_scale[row_num].append(round(pixel[0]*0.299+pixel[1]*0.587+pixel[2]*0.114, 0))
    return grey_scale


def blur_kernel(size: int) -> Kernel:
    """returns a kernel of a given size"""
    if size%2==0 or size <= 0:
        return ValueError
    return [[1/(size*size)]*size]*size


def kernel_to_pixel(image, row_id, col_id, kernel):
    '''applies the kernel to a certain location'''
    total = 0
    for i in range(row_id - len(kernel)//2,row_id + len(kernel)//2+1):
        for j in range(col_id - len(kernel[0])//2, col_id + len(kernel[0])//2+1):
            kernel_gradient = kernel[i-(row_id - len(kernel)//2)][j-(col_id - len(kernel[0])//2)]
            if(0<=i<len(image) and 0<=j<len(image[0])):
                total += image[i][j]*kernel_gradient
            else:
                total += image[row_id][col_id]*kernel_gradient
    if 0 <= total <= 255:
        return round(total)
    if total > 255:
        return 255
    return 0


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """applies a kernel to blur images"""
    blured = []
    for row_loc,row in enumerate(image):
        blured.append([])
        for col,_ in enumerate(row):
            blured[row_loc].append(kernel_to_pixel(image,row_loc,col,kernel))
    return blured


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """preforms bilinear interpolation for pixels in an image""" ## לא נפתר
    delta_y, delta_x = y%1, x%1
    y, x= min(len(image)-1,y), min(len(image[0])-1,x)
    a = image[floor(y)][floor(x)] # unproblematic input
    b = image[floor(y)][ceil(x)]
    c = image[ceil(y)][floor(x)]
    d = image[ceil(y)][ceil(x)]
    return round(a * (1-delta_y) * (1-delta_x) +
                b * (1-delta_y) * delta_x +
                c * delta_y * (1-delta_x) +
                d * delta_x * delta_y)


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    """resizes an image to a desired size"""
    new_image = []
    y_ratio, x_ratio = ((len(image) - 1) / (new_height - 1),
                        (len(image[0]) - 1) / (new_width - 1))
    for i in range(new_height):
        new_image.append([])
        for j in range(new_width):
            if 0 < i < new_height - 1 or 0 < j < new_width -1:
                new_image[i].append(bilinear_interpolation(image,i*y_ratio,j*x_ratio))
            else:  # in this condition we will deal with corners
                if i == 0:
                    if j == 0:
                        new_image[i].append(image[0][0])
                    else:
                        new_image[i].append(image[0][-1])
                else:
                    if j == 0:
                        new_image[i].append(image[-1][0])
                    else:
                        new_image[i].append(image[-1][-1])
    return new_image


def rotate_90(image: Image, direction: str) -> Image:
    """rotates an image 90 degs to either direction"""
    rotated = []
    for i,_ in enumerate(image[0]):
        rotated.append([])
        if direction == "L":
            for j,_ in enumerate(image):
                rotated[i].append(image[j][-1-i])
        elif direction == "R":
            for j,_ in enumerate(image):
                rotated[i].append(image[-1-j][i])
        else:
            return ValueError
    return rotated


def mse(a_matrix: list[list[int]], b_matrix: list[list[int]]) -> float:
    """returns mean square error fo two matrices of the same size. it is permisible for 
    a_matrix to be wider than b_matrix, other than that they must have the same coordinates"""
    total = 0
    for i,row in enumerate(b_matrix):
        for j,pixel in enumerate(row):
            total += (a_matrix[i][j] - pixel) ** 2
    return total / (len(b_matrix) * len(b_matrix[0]))


def get_best_match(image: SingleChannelImage, patch: SingleChannelImage) -> tuple:
    """returns a tuple representing the location and degree of the best MSE"""
    best_match = ((0,0), WORST_POSSIBLE_MSE)
    for i in range(len(image)-len(patch)+1):
        for j in range(len(image[0])-len(patch[0])+1):
            new_mse = mse(
                focus_on_patch(image,i,j,len(patch),len(patch[0])),
                patch)
            if new_mse < best_match[1]:
                best_match = ((i,j), new_mse)
    return best_match


def find_patch_in_img(image: SingleChannelImage, patch: SingleChannelImage) -> dict:
    """allows you to find a patch i an image, effectively"""
    RESOLUTION = 3  # to define the resolution of the search (2^n)
    image_patch = [(image,patch)]
        # making a list containing pairs images in differing degrees of focus
    for _ in range(RESOLUTION):
        if len(image_patch[-1][1]) <= 2 or len(image_patch[-1][1][0]) <= 2:
            break
        image_patch.append((
            resize(image_patch[-1][0],len(image_patch[-1][0])//2,len(image_patch[-1][0][0])//2),
            resize(image_patch[-1][1],len(image_patch[-1][1])//2,len(image_patch[-1][1][0])//2)))
    loc_dict = {0:[],90:[],180:[],270:[]}
    for level in range(1,len(image_patch)+1):
        loc_dict = dic_for_level(loc_dict,image_patch[-level][0],image_patch[-level][1])
    return loc_dict


def dic_for_level(dictionary,image, patch):
    """updates a dictionary to include new values, in accordance with each level of the plan"""
    if dictionary[0] != []:
        for lst in dictionary.values():
            temp = imediate_neighbour(image,2*(lst[-1][0][0]),2*(lst[-1][0][1]),patch)
            best = get_best_match(temp[0],patch)
            lst.append(((best[0][0]+temp[1][0],best[0][1]+temp[1][1]),best[1]))
            patch = rotate_90(patch,"L")
    else:
        for lst in dictionary.values():
            lst.append(get_best_match(image,patch))
            patch = rotate_90(patch,"L")
    return dictionary


def imediate_neighbour(image: SingleChannelImage, y,x, patch):
    """returns a matrix that is only the imediate neighbours of a given location, while still 
    leaving room for a patch, and the (0,0) coordinates in the original"""
    neighbouring = []
    count = 0
    diff = None
    for row in enumerate(image):
        if y - 1 <= row[0] <= y + len(patch):
            neighbouring.append([])
            for pixel in enumerate(row[1]):
                if x-1 <= pixel[0] <= x + len(patch[0]):
                    if diff is None:
                        diff = (row[0],pixel[0])
                    neighbouring[count].append(pixel[1])
            count += 1
    return neighbouring, diff



def focus_on_patch(image: SingleChannelImage,
                  top_most: int, left_most: int,
                  height: int, width: int) -> SingleChannelImage:
    """makes a patch from a greyscale image. good for testing"""
    patch = []
    for i in range (height):
        patch.append([])
        for j in range(width):
            try:
                patch[i].append(image[i+top_most][j+left_most])
            except ValueError:
                if i+top_most > len(image) or j+left_most > len(image[0]):
                    print("desired patch too big")
                    patch = "RangeError"
                    break
                else:
                    patch = "StrangeError"
    return patch



if __name__ == '__main__':
    pass
