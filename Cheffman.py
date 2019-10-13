import handy
import cv2
import time

from tkinter import *
from tkinter import ttk


a = []
apoint=0
delorder=False
class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.title("Order")
        self.minsize(640, 400)
        #self.configure(background = '#4D4D4D')

        self.initUI()
    
    def clickMe(self):

        a.append(self.name.get())
        
        self.label.configure(text = len(a))
        self.label.place(x = 100, y = 300)

        r = 100
        t = 0
        i = len(a) - 1
        while i>=0 and t<11:
            
            self.label = ttk.Label(self, text = a[i])
            self.label.place(x = 350, y = r)
            r += 20
            i = i - 1
            t = t + 1
    
    def initUI(self):

        self.name = StringVar()

        self.label = ttk.Label(self, text = "Enter your order")
        self.label.place(x = 50, y = 50)

        self.textbox = ttk.Entry(self, width = 20, textvariable = self.name)
        self.textbox.place(x = 50, y = 80)


        self.label = ttk.Label(self, text = "Total orders:")
        self.label.place(x = 50, y = 200)

        self.label = ttk.Label(self, text = len(a))
        self.label.place(x = 100, y = 300)


        self.button = ttk.Button(self, text = "Send order", command = self.clickMe)
        self.button.place(x = 50, y = 110)

        self.label1 = ttk.Label(self, text = "Recent orders")
        self.label1.place(x = 350, y = 50)


root = Root()
root.mainloop()

#VIDEO SETTINGS WEBCAM
cap = cv2.VideoCapture(0)

#FUNTIONS AND GLOBAL VARIABLES
x=[]
y=[]

cleft=(255,255,255)
dleft=False
cright=(255,255,255)
dright=True
corder=(255, 255, 255)
tinicio=time.time()
tfinal=False
def funciontype(x,longx,fallada,speed,direccion):
    size=len(x)
    if (size<2):
        return 0
    media=0.0
    i=size-1
    for i in range(i>0):
        media+=x[i]-x[i-1]
        i-=1
    direccion[0]=0
    ruido=x[size-1]-x[size-2]
    if ((media>0 and ruido>fallada)
        or (media<0 and -ruido>fallada)):
        return -1
    longitud=abs(x[size-1]-x[0])
    if (longitud<speed):
        x=[]
    elif (size>2):
        longitud=abs(x[size-1]-x[size-3])
        if (longitud>=longx):
            if (media<0): direccion[0]=1
            else: direccion[0]=-1
            return 2
    return 1

#STORE HAND
hist = handy.capture_histogram(source=0)

#SEARCH OF MOVEMENTS
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FACE BLOCK
    handy.detect_face(frame, block=True)

    # DETECT HAND
    f_frame = cv2.flip(frame, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    if(len(a)>0): 
        if(len(a)==1): dright=False
        cv2.putText(f_frame, a[apoint],(230, 35), font, 0.7, (corder), 2, cv2.LINE_AA)
    else:
        dright = False
        cv2.putText(f_frame, "No orders",(230, 35), font, 0.7, (corder), 2, cv2.LINE_AA)
    if (dleft): cv2.putText(f_frame, "<--",(20, 35), font, 0.7, cleft, 2, cv2.LINE_AA)
    if (dright): cv2.putText(f_frame, "-->",(565, 35), font, 0.7, cright, 2, cv2.LINE_AA)
    
    #cv2.rectangle(f_frame, (500, 100), (580, 180), (105, 105, 105), 2)

    hand = handy.detect_hand(f_frame, hist)

    # to get a quick outline of the hand
    quick_outline = hand.outline

    # to get the centre of mass of the hand
    com = hand.get_center_of_mass()
    #MOVEMENT CHECKS
    if com:
        cv2.circle(quick_outline, com, 10, (255, 0, 0), -1)
        x.append(com[0])
        y.append(com[1])
        xd=[0]
        yd=[0]
        xt=funciontype(x,150,60,20,xd)
        yt=funciontype(y,100,40,20,yd)
        if(yt+xt>=3):
            if (yt+xt==3 and not tfinal):
                tinicio=time.time()
                tfinal=True
                if (xt==2):
                    if (xd[0]==1): 
                        cright=(0,255,0)
                        if(apoint<len(a)-1): 
                            apoint+=1
                            dleft=True
                            if(apoint==len(a)-1): dright=False
                        else:
                            dright=False
                    else: 
                        cleft=(0,255,0)
                        if(apoint>0): 
                            apoint-=1
                            dright=True
                            if (apoint==0): dleft=False
                        else: dleft=False
                else:
                    if(len(a)>0):
                        if (yd[0]==1): 
                            corder = (0, 0, 255)
                        else:
                            corder = (0, 255, 0)
                        delorder=True
            x=[]
            y=[]
        if(yt==-1 or xt==-1):
            x=[]
            y=[]
    else:
        x=[]
        y=[]
    
    if (tfinal):
        tiempo=round(time.time()-tinicio,0)
        if (tiempo>=1.5):
            cleft=(255,255,255)
            cright=(255,255,255)
            corder=(255, 255, 255)
            if(delorder): 
                del a[apoint]
                if (apoint==len(a)): apoint=len(a)-1
                elif (apoint==len(a)-1): dright=False
                if (len(a)<=1): dleft=False
                delorder=False
            tfinal=False

    #DISPLAY
    cv2.imshow("Handy", quick_outline)
    #END, "q" for quit
    k = cv2.waitKey(5)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()