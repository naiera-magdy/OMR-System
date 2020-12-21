from commonfunctions import *
import cv2
import os

class Staff:
    def __init__(self,image):
        self.image = image
        self.thickness = 0
        self.space = 0
        self.positions = np.zeros(5)
        self.lines = np.zeros(self.image.shape)
        self.notes = np.zeros(self.image.shape)
        self.__get_staff_lines()
        self.__get_staff_notes()
        self.__get_staff_thickness()
        # self.__get_staff_positions()

    def __get_staff_lines(self):
        img = np.uint8(self.image)

        if np.max(img) == 255:
            img = img // 255
        
        img_inv = 1 - img

        horizontal = np.uint8(np.copy(img_inv))
        # Specify size on horizontal axis
        cols = horizontal.shape[1]
        horizontal_size = cols // 30

        # Create structure element for extracting horizontal lines through morphology operations
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

        # Apply morphology operations
        horizontal = cv2.erode(horizontal, horizontalStructure)
        # show_images([horizontal])
        horizontal = cv2.dilate(horizontal, horizontalStructure)

        self.lines = horizontal
        # show_images([self.lines])

    def __get_staff_notes(self):
        img = np.uint8(self.image)

        if np.max(img) == 255:
            img = img // 255
        
        img_inv = 1 - img

        vertical = np.uint8(np.copy(img_inv))
        
        # Specify size on vertical axis
        rows = vertical.shape[0]
        verticalsize = 4 # should be rows // 30

        # Create structure element for extracting vertical lines through morphology operations
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

        # Apply morphology operations
        vertical = cv2.erode(vertical, verticalStructure)
        vertical = cv2.dilate(vertical, verticalStructure)

        self.notes = vertical

    def __get_staff_thickness(self):
        
        ver_histo = self.lines.sum(axis=0)
        non_zero_histo = ver_histo[ver_histo !=0]
    
        self.thickness = int(round(sum(non_zero_histo) / (5*len(non_zero_histo))))
    
    def __get_staff_positions(self):
        rle = list()
        for y in range(self.lines.shape[1]):
            count = 1
            n = 0
            rle_in = list()
            for x in range(1,self.lines.shape[0]):
                if(self.lines[x][y] == self.lines[x-1][y]):
                    count+=1
                else :
                    rle_in.append(count)
                    count = 1
            rle_in.append(count)
            if len(rle_in) > 9:
                print(np.array(rle_in))
                rle.append(np.array(rle_in))
        rle = np.array(rle)

        # print(rle)
        rle_avg = np.int32(np.round(rle.sum(axis = 0) / rle.shape[0]))
        positions = np.cumsum(rle_avg)
        self.positions = positions[1:-1:2] - (self.thickness // 2 ) - 1
        
        # print(self.positions)
        # print(self.lines[self.positions,100:130])
        # self.lines[self.positions,:] = 0
        # show_images([self.lines])
        
        # Space between staff lines
        cropped_rle = rle[:,2:-2:2]
        # spaces = cropped_rle.sum(axis=0) // cropped_rle.shape[0]
        self.space = int(round(cropped_rle.sum() / (cropped_rle.shape[0]*4)))
