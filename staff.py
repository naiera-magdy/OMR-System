from commonfunctions import *
import cv2
import os
import operator
class Staff:
    def __init__(self,image):
        self.image = image
        self.thickness = 0
        self.space = 0
        self.positions = np.zeros(5, dtype=np.int16)
        self.lines = np.zeros(self.image.shape, dtype=np.uint8)
        self.notes = np.zeros(self.image.shape, dtype=np.uint8)
        self.__get_staff_lines()
        #self.__get_staff_notes()
        # self.__get_staff_thickness()
        self.__get_staff_positions()

    def __get_staff_lines(self):
        img = np.uint8(self.image)

        if np.max(img) == 255:
            img = img // 255
        
        img_inv = 1 - img

        horizontal = np.uint8(np.copy(img_inv))
        # # Specify size on horizontal axis
        # cols = horizontal.shape[1]
        # horizontal_size = int(cols/16)

        # # Create structure element for extracting horizontal lines through morphology operations
        # horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

        # # Apply morphology operations
        # horizontal = cv2.erode(horizontal, horizontalStructure)
        # # show_images([horizontal])
        # horizontal = cv2.dilate(horizontal, horizontalStructure)

        # self.lines = horizontal
        # show_images([self.lines])

        rle = list()
        rle_total = list()
        for y in range(horizontal.shape[1]):
            count = 1
            rle_in = list()
            for x in range(1, horizontal.shape[0]):
                if(horizontal[x][y] == horizontal[x-1][y]):
                    count+=1  
                else :
                    rle_in.append(count)
                    count = 1
            rle_in.append(count)
            if len(rle_in) > 9:
                rle.append(np.array(rle_in))
            rle_total.append(np.array(rle_in))

        rle = np.array(rle)
        rle_total = np.array(rle_total)

        height = 0
        space = 0
        
        for i, col in enumerate(rle):
            line_freq = dict()
            space_freq = dict()
            start = 0
            
            if horizontal[0][i] == 0:
                start = 1
            
            for x in range(start, len(col), 2):
                if col[x] not in line_freq.keys():
                    line_freq[col[x]] = 0
                line_freq[col[x]] += 1

            for x in range(1 - start, len(col),2):
                if col[x] not in space_freq.keys():
                    space_freq[col[x]] = 0
                space_freq[col[x]] += 1
            
            height += max(line_freq.items(), key=operator.itemgetter(1))[0]
            space += max(space_freq.items(), key=operator.itemgetter(1))[0]

        self.thickness = int(np.round(height / len(rle)))
        self.space = int(np.round(space / len(rle)))
        
        Tlen = min(2*self.thickness, self.thickness+self.space)
        # print("Tlen: ", Tlen)

        for i, col in enumerate(rle_total):
            start = 0
            if horizontal[0][i] == 0:
                start = 1
            for x in range(start, len(col), 2):
                if col[x] >= Tlen:
                    horizontal[sum(col[:x]):sum(col[:x+1]), i] = 0

        self.lines = horizontal
        self.notes = img_inv - self.lines
        self.notes *= 255

        # sizey = self.space // 2
        # verticalStructure2 = cv2.getStructuringElement(cv2.MORPH_RECT, (sizey, sizey))

        # self.notes = cv2.erode(self.notes, verticalStructure2)
        # self.notes = cv2.dilate(self.notes, verticalStructure2)
        # show_images([self.lines, self.notes])




    def __get_staff_notes(self):
        img = np.uint8(self.image)

        if np.max(img) == 255:
            img = img // 255
        
        img_inv = 1 - img

        vertical = np.uint8((img_inv - self.lines)*255) 


        # Specify size on vertical axis
        rows = vertical.shape[0]
        # print(rows)
        verticalsize = 3

        # Create structure element for extracting vertical lines through morphology operations
        verticalStructure1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

        # Apply morphology operations
        vertical = cv2.erode(vertical, verticalStructure1)
        vertical = cv2.dilate(vertical, verticalStructure1)

        verticalStructure2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))

        vertical = cv2.dilate(vertical, verticalStructure2)
        vertical = cv2.erode(vertical, verticalStructure2)

        # show_images([vertical , img_inv , self.lines],["vertical", "Image","Lines"])
        self.notes = vertical


    # def __get_staff_thickness(self):
        
    #     ver_histo = self.lines.sum(axis=0)
    #     non_zero_histo = ver_histo[ver_histo !=0]
    
    #     self.thickness = int(round(sum(non_zero_histo) / (5*len(non_zero_histo))))
    
    def __get_staff_positions(self):
        # rle = list()
        # for y in range(self.lines.shape[1]):
        #     count = 1
        #     n = 0
        #     rle_in = list()
        #     for x in range(1,self.lines.shape[0]):
        #         if(self.lines[x][y] == self.lines[x-1][y]):
        #             count+=1
        #         else :
        #             rle_in.append(count)
        #             count = 1
        #     rle_in.append(count)
        #     if len(rle_in) > 9:
        #         print(np.array(rle_in))
        #         rle.append(np.array(rle_in))
        # rle = np.array(rle)

        # # print(rle)
        # rle_avg = np.int32(np.round(rle.sum(axis = 0) / rle.shape[0]))
        # positions = np.cumsum(rle_avg)
        # self.positions = positions[1:-1:2] - (self.thickness // 2 ) - 1
        lineVotes = np.zeros(self.lines.shape[0])
        for x in range(self.lines.shape[0]):
            if sum(self.lines[x]) > (self.lines.shape[1] // 4):
                lineVotes[x] = 1

        # self.thickness = int(sum(lineVotes) // 5)

        # start = 0
        # end = 0
        # for x in range(1, len(lineVotes)):
        #     if(lineVotes[x] == 1):
        #         start = x
        #         break
        # for x in range(len(lineVotes)-1,1,-1):
        #     if(lineVotes[x] == 1):
        #         end = x+1
        #         break
        
        # croppedLine = lineVotes[start:end]

        # self.space = int((len(croppedLine) - sum(croppedLine)) // 4)

        i = 0
        x = 0
        print(self.thickness, self.space)

        while x  < len(lineVotes):
            if(lineVotes[x] == 1 and i < 5):
                self.positions[i] = x + (self.thickness // 2)
                i+=1
                x += (self.thickness // 2) + (self.space // 2)
            x += 1
        print(self.positions)
        
        # print(self.positions)
        # print(self.lines[self.positions,100:130])
        # self.lines[self.positions,:] = 0
        # show_images([self.lines])
        
        # Space between staff lines
        # cropped_rle = rle[:,2:-2:2]
        # spaces = cropped_rle.sum(axis=0) // cropped_rle.shape[0]
        # self.space = int(round(cropped_rle.sum() / (cropped_rle.shape[0]*4)))

