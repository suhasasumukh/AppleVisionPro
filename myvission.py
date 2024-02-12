import cv2
import numpy as np

class drawingCanvas():
    def __init__(self):
        self.penrange = np.load('penrange.npy')
        self.cap = cv2.VideoCapture(0)
        self.canvas = None

        self.x1,self.y1=0,0

        self.val=1
        self.draw()

    def draw(self):
        while True:
            _, self.frame = self.cap.read()
            self.frame = cv2.flip( self.frame, 1 )

            if self.canvas is None:
                self.canvas = np.zeros_like(self.frame)
            
            mask=self.CreateMask()
            contours=self.ContourDetect(mask)
            self.drawLine(contours)
            self.display()
            k = cv2.waitKey(1) & 0xFF
            self.takeAction(k)
            

            if k == 27:
                break        
    def CreateMask(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV) 
        lower_range = self.penrange[0]
        upper_range = self.penrange[1]
        mask = cv2.inRange(hsv, lower_range, upper_range)
        return mask
    
    def ContourDetect(self,mask):

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def drawLine(self,contours):

        if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > 100:                
            c = max(contours, key = cv2.contourArea)    
            x2,y2,w,h = cv2.boundingRect(c)
    
            if self.x1 == 0 and self.y1 == 0:
                self.x1,self.y1= x2,y2
            else:
                self.canvas = cv2.line(self.canvas, (self.x1,self.y1),(x2,y2), [255*self.val,0,0], 10)
            self.x1,self.y1= x2,y2
        else:
            self.x1,self.y1 =0,0        
    
    def display(self):
        self.frame = cv2.add(self.frame,self.canvas)    
        cv2.imshow('frame',self.frame)
        cv2.imshow('canvas',self.canvas)
    
    def takeAction(self,k):
        if k == ord('c'):
            self.canvas = None
        if k==ord('e'):
            self.val= int(not self.val)
                   
if __name__ == '__main__':
    drawingCanvas()
    
cv2.destroyAllWindows()