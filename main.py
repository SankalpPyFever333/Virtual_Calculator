# We installed cvzone for this project
# we installed mediapipe

import cv2
from cvzone.HandTrackingModule import HandDetector
import winsound #for playing beep sound
import math

# Now we are going to create a class for button which we make objects everytime to create a number of buttons.

class Button():
      # for craeting a button we need position,width,color,value to be written on it. These can be taken as parameters and initialise them.
      def __init__(self,pos,width,height,value):
            self.pos=pos
            self.width=width
            self.height=height
            self.value=value
      # We create a separate method for craeting the button which we called each time from the while loop.
      def draw(self,img):
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),
                              (20, 22, 22), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),
                              (255, 0, 255),3)
                  
            cv2.putText(img, self.value, (self.pos[0]+30, self.pos[1]+60), cv2.FONT_HERSHEY_COMPLEX,  1, (255, 255, 255), 3)
      
      def CheckButtonClick(self,x,y):
            if self.pos[0]<x<self.pos[0]+self.width and self.pos[1]<y<self.pos[1]+self.height:
                  cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),(255, 255, 255), cv2.FILLED)
                  cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),(55, 55, 55), 3)

                  cv2.putText(img, self.value, (self.pos[0]+30, self.pos[1]+60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
                  return True
            else:
                  return False




# webcam
# our first webcam is 0 and if we have some more webcam, then we can give 1,2 or 3 like that.
cap = cv2.VideoCapture(0)
# we can there give the size of image but we keep it default i.e. 640x480
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
# creating buttons:
# we have to creaet now 16 buttons:
buttonListValues = [['7', '8', '9', '*', 'C'], ['4', '5', '6','+', 'X'], ['1', '2', '3', '-', '!'], ['0', '/', '.', '=', '%']]

buttonlist=[]
for x in range(5):
      for y in range(4):
            xpos= x*100+500 #defining position of buttons.
            ypos= y*100+50
            buttonlist.append(Button((xpos,ypos),100,100,buttonListValues[y][x]))
            


# variables
myEquation=""
delayCounter=0
checkPressEqual=False



while True:  # loop runs till we want to capture each frame.
      # set image from webcam:
      success, img = cap.read()
      # When we are on webcam, then our left is right and our right is left, so for that we have to flip horizontally the image:
      # It will flip img horizonatally, if you write 0 then flip the img vertically.
      img = cv2.flip(img, 1)

      # initialisation:

      detector = HandDetector(detectionCon=0.8, maxHands=1)
      # detectionCon is the confidence value, if it is 80% confidence then it will track it otherwise not, maxHands=1 means it will detect only single hand,if you change it to 2 or more then it will detect thta number of hands.

      # Detection of hand:
      # This is using the mediapipe package for finding hands.
      hands, img = detector.findHands(img)
      # It will sends all the list in this variable and detect hands in the image passed then it will be displayed using imshow(). It is telling the right hand to left hand bcoz we had flip our image.

      for button in buttonlist:
            button.draw(img)
      
      
      # creating entry box:
      cv2.rectangle(img, (500,-50), (500+500,50),
                  (220, 220, 220), cv2.FILLED)
      cv2.rectangle(img, (500, 50), (500+500, 50+100),(255, 80, 255), 3)


      # Check for hand and then click:
      if hands:
            # It gets true when hands list is not empty and then we are going to find the distance between fingers:
            lmlist=hands[0]["lmList"] #Inside the hands list, there is a dictionary called lmList(landmark list which have all the points of our fingers)
            x1,y1,z1= lmlist[8]
            x2,y2,z2= lmlist[12]
            lenght,_,img=detector.findDistance((x1,y1),(x2,y2),img)
            # print(lenght)
            # print(detector.findDistance(lmlist[8], lmlist[12]))
            # print("lmlist[8] is:",lmlist[8])
            # print("lmlist[12] is :",lmlist[12])

            # Now we have to find at which location those two fingers get close:
            # After it ,we have to check one by one whether the button has clicked or not.
            if lenght<50: #when you prinitng the length, you can see when two fingers are close then what is the distance between them.
                  for i,button in enumerate(buttonlist):
                        # i act as counter variable
                        if button.CheckButtonClick(x1,y1) and delayCounter==0: #it will return true if we close our finger at the right position and also when delayCounter is 0.
                              if checkPressEqual: #After pressing equal, it will make empty string which has to be put on screen.
                                    myEquation = ''
                                    checkPressEqual = False
                              cv2.rectangle(img, (500, -50), (500+500, 50),(40, 255,0), cv2.FILLED)


                              # print(buttonListValues[int(i%4)][int(i/4)]) by this we are accessing the values from that 2d list.
                              myValue = buttonListValues[int(i % 4)][int(i/4)]
                              # we are converting that value into int bcoz index value can't be float type.
                              if myValue=="C":
                                    myEquation="" 
                              if myValue=="X":
                                    mylist= list(myEquation)
                                    del mylist[-1]
                                    newEquation=""
                                    for l1 in mylist:
                                          newEquation=newEquation+l1
                                    myEquation= newEquation
                              if myValue=="=":
                                    myEquation=str(eval(myEquation)) #eval evaluate that expression and then return a int type which we have to convert it into string bcoz we have to put thta using putText().
                                    winsound.Beep(500,200) #playing sound,first parameter is frequency and second is time duration in milisecond.
                                    checkPressEqual=True
                              else:
                                    if myValue!="X" and myValue!="C" and myValue!="!": #add that value which is not X
                                          myEquation= myEquation+myValue
                                          winsound.Beep(650,200)
                              if myValue[-1]=="!":
                                    f= int(myValue[:len(myValue)-1])
                                    myEquation= math.factorial(f)
                                    winsound.Beep(500, 200)


                              delayCounter=1      
      # to avoid duplicates:
      # here we are waiting that after passing 10 frames then only we can click another button.
      if delayCounter!=0:
            delayCounter+=1
            if delayCounter>10:
                  delayCounter=0


      # display eqution or result:
      cv2.putText(img, myEquation, (510, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (55, 55, 55), 3)
      
      


      # Display img
      cv2.imshow("image", img)
      if cv2.waitKey(1)==ord('q'):
            break
