import cv2 as cv
import numpy as np

# # simple images read and open it

# img = cv.imread(r'C:\Users\lenovo\Desktop\VS_DATA\face_recog\imges\ronaldo.jpg')
# cv.imshow('ronaldo', img)
# cv.waitKey(0)


# # read videos 

# captur = cv.VideoCapture(r"C:\Users\lenovo\Desktop\VS_DATA\face_recog\videos\cat.mp4")
# while True:
#     isTrue, frame = captur.read()
#     cv.imshow('cat', frame)
    
#     if cv.waitKey(20) & 0xFF == ord('d'):
#         break
# captur.release()
# cv.destroyAllWindows()    


# # resizing 
# # imgage resize
# img = cv.imread(r'C:\Users\lenovo\Desktop\VS_DATA\face_recog\imges\ronaldo.jpg')
# cv.imshow('ronaldo', img)

# def rescaleFrame(frame, scale=0.75):
#     width = int(frame.shape[1]*scale)
#     height = int(frame.shape[0]*scale)
#     dimensions = (width, height)
#     return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# resized_image = rescaleFrame(img, scale=0.2)
# cv.imshow('images', resized_image)



# # video resize

# def changeRes(capture, width, height):
#     # only for video 
#     capture.set(3, width)
#     capture.set(4, height)

# def rescaleFrame(frame, scale=0.75):
#     width = int(frame.shape[1]*scale)
#     height = int(frame.shape[0]*scale)
#     dimensions = (width, height)
#     return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# captur = cv.VideoCapture(r"C:\Users\lenovo\Desktop\VS_DATA\face_recog\videos\cat.mp4")
# while True:
#     isTrue, frame = captur.read()
    
#     frame_resized = rescaleFrame(frame, scale=.2)
    
#     cv.imshow('cat', frame)
#     cv.imshow('video resized', frame_resized)
    
#     if cv.waitKey(20) & 0xFF == ord('d'):
#         break
# captur.release()
# cv.destroyAllWindows()    



blank = np.zeros((500, 500, 3),  dtype='uint8')
# cv.imshow('blank', blank)

# img = cv.imread(r"C:\Users\lenovo\Desktop\VS_DATA\face_recog\imges\messi.jpg")
# cv.imshow('messi', img)

# # point the image a certain color
# blank[200:300, 300:400]= 0,0,255
# cv.imshow('green', blank)


# # draw a rectangle with color 
# cv.rectangle(blank, (0, 0), (blank.shape[1]//2, blank.shape[0]//2), (0, 255, 0), thickness=-1)
# cv.imshow('rectangle', blank)


## draw a circle 
# cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2),40, (0,0,255), thickness=-1) 
# cv.imshow('Circle', blank)
 
# #draw a line
# cv.line(blank,(100,250),(blank.shape[1]//2, blank.shape[0]//2), (255,255,255),3)
# cv.imshow('line', blank)

# cv.line(blank,(100,250),(300, 400), (255,255,255),3)
# cv.imshow('line', blank)

# #  write text
# cv.putText(blank, 'hello', (255, 255), cv.FONT_HERSHEY_SIMPLEX , 1.0, (0, 255, 0), 2)
# cv.imshow('Text', blank)





cv.waitKey(0)