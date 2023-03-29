'''
Creator: TLeonard
Copyright: Standard Mechanics, LLC 2023


To-Do List:

Add to ROI pop up to hit enter to continue (quality of life).
Make the edge highlight bolder (+/- 1 pix?) (quality of life).
Make the edge highlight work for target tracking (functionality).
Make the edge highlight work when edge goes out of image (functionality).
Likely only save the image to be used in the tool itself (optimization).
Remove the ability for user to analyze more lines than in image.

'''


from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from PIL import ImageTk, Image
import os
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
from customtkinter import *

set_appearance_mode("Dark")
set_default_color_theme("Theme.json")

##########################

#Extensometer_Functions.py

##########################

from bisect import bisect_left
from scipy.ndimage import uniform_filter1d

def PixPrint(image,line,pix):
    #This is just used for troubleshooting code.
    #print(f'Looking at line {line} pix {pix} value is {image[line][pix]}.')
    return()

def GetImage():
    file = filedialog.askopenfilename(filetypes = [("Images (.bmp)" , "*.bmp")])
    image = cv2.imread(file,0)
    return(image)

def GetQSImages(Image_Count):
    for i in range(Image_Count):
        images = GetImage()
        if i == 0:
            image = images
            continue
        image = np.vstack([image,images])
    return(image)

def GetForceData(ForceStrainFactor, file = ''):
    
    if file == '':
        file = filedialog.askopenfilename(filetypes = [("CSV" , "*.csv")])
    
    data = pd.read_csv(file)
    time = data['Time']
    trans_volt = data['Channel B']
    
    Force = []
    Time = []
    
    if trans_volt[0] == "(V)":
        unit = 'V'
        for data in range(len(trans_volt)-2):
            Force.append(float(trans_volt[data + 2]) * ForceStrainFactor)
            Time.append(float(time[data + 2]))

    elif trans_volt[0] == "(mV)":
        unit = 'mV'
        for data in range(len(trans_volt)-2):
            Force.append((float(trans_volt[data + 2])) / 1000  * ForceStrainFactor)
            Time.append(float(time[data + 2]))
    
    zero = bisect_left(Time,0)
    
    del Force[0:zero]
    del Time[0:zero]
    
    return(Force, Time, unit)

def GetQSStressData():
    file = filedialog.askopenfilename(filetypes = [("CSV" , "*.csv")])
    data = pd.read_csv(file)
    time = data['TEST_HEADER_START']
    stress = data['Start Timestamp']
    unit = 'MPa'
    
    Stress = []
    Time = []
    
    for data in range(len(stress)-4):
        Stress.append(float(stress[data + 2]))
        Time.append(float(time[data + 2]))

  
    zero = bisect_left(Time,0)
    
    del Stress[0:zero]
    del Time[0:zero]
    
    return(Stress, Time, unit)

def ForcetoStress(Force, Area, Time, TestType):
    Stress = [force / Area for force in Force]
    
    flag = 0

    if TestType == "Comp":
        peak = min(Stress)
        end_stress = int(peak * 0.1)

        for i in range(len(Stress)):
            if Stress[i] < end_stress - 50:
                flag = 1
            if flag == 1 and Stress[i] > end_stress:
                end_test = i + 5000
                break
        
    else:
        peak = max(Stress)
        end_stress = int(peak * 0.1)
    
        for i in range(len(Stress)):
            if Stress[i] > end_stress + 50:
                flag = 1
            if flag == 1 and Stress[i] < end_stress:
                end_test = i + 5000
                break

    del Stress[end_test:]
    del Time[end_test:]
    
    return(Stress,Time)

def ImageCutoff(image, time, Line_Rate):
    
    index = int( max(time) * Line_Rate + 100)
    
    image = image[:index]
    
    return(image)

def SetGage(image, black, white):

    scale = 3
    width = len(image[0])
    width_scaled = int(width / scale)
    
    first_line = image[0:10]
    first_line = cv2.resize(first_line, (width_scaled,400))

    roi = cv2.selectROI('Select Gage Section', first_line)
    cv2.destroyAllWindows()
    
    left = roi[0] * scale
    right = (roi[0] + roi[2]) * scale
    
    while image[0][left] < white:
        left -= 1
    
    while image[0][right] < white:
        right += 1
    
    #left += 50
    #right += 50
        
    return(left,right)  

def EdgeFinder(image, guess, blur_radius, black, white, threshold, line_limit):
    
    left_edge = []
    right_edge = []
    N = len(image[0]) - 1
    left_start = guess[0]
    right_start = guess[1]
    
    for line in range(min(len(image),line_limit)):

        left = 0
        right = 0
        flag = 0
        fit_R = 3 # Radius of points to fit a line to
    
        if min(image[line]) > black:
            print("Line " + str(line) + " has no black showing.")
            return(left_edge,right_edge)
        
        if max(image[line]) < white:
            print("Line " + str(line) + " has no white showing.")
            return(left_edge,right_edge)

        while flag == 0:  # Finding where black region begins
            for pix in range(left_start, N):
                if image[line][pix] < black:
                        flag = 1
                        left_start = pix
                        break
            if flag != 1: flag = -1

        while flag == 1:  # Finding white region boundary
            for pix in range(left_start):
                if image[line][left_start - pix] > white:
                    flag = 2
                    left_start = left_start - pix
                    break
            if flag!=2: flag = -1

        while flag == 2:  # Finding gray on left side
            for pix in range(left_start,N):
                if image[line][pix] < threshold:
                    flag = 3
                    left = pix
                    left_start = pix
                    break
       

        while flag == 3:  # Finding where black begins from right to left
            for pix in range(right_start):
                if image[line][right_start - pix] < black:
                    flag = 4
                    right_start = right_start - pix
                    break
            if flag!= 4: flag = -1

        while flag == 4:  # Finding white region right boundary
            for pix in range(right_start, N):
                if image[line][pix] > white:
                    flag = 5
                    right_start = pix
                    break
            if flag!= 5: flag = -1

        while flag == 5:  # Finding gray on right side
            for pix in range(right_start): 
                if image[line][right_start - pix] < threshold:
                    flag = 6
                    right = right_start - pix
                    right_start = right_start - pix
                    break


        if flag > 0:

            x_left = np.linspace(left-fit_R , left+fit_R , 2*fit_R)
            y_left = image[line][left-fit_R:left+fit_R]

            m_left,b_left = np.polyfit(x_left,y_left,1)
            left = (threshold-b_left)/m_left

            x_right = np.linspace(right-fit_R , right+fit_R , 2*fit_R)
            y_right = image[line][right-fit_R:right+fit_R]

            m_right,b_right = np.polyfit(x_right,y_right,1)
            right = (threshold-b_right)/m_right

            #Faster versions that lose some resolution
            #left = (left_high+left+left_low)/3
            #right = (right_high+right+right_low)/3
            #print(f'The pixel is {left} and the poly pixel is {left_poly}.')

            left_edge.append(left)
            right_edge.append(right)
            
            image[line][int(left)] = 0
            image[line][int(right)] = 255
        
        if line == line_limit or flag == -1:
            return(left_edge,right_edge)
        
    
    return(left_edge,right_edge)

def EdgetoStrain(left_edge, right_edge, Line_Rate):

    strain = []
    disp = []
    time = []
    
    for line in range(len(left_edge)):
        
        dist = right_edge[0]-left_edge[0]
        left = left_edge[line]
        right = right_edge[line]
        delta = (right - left) - dist

        strain.append(delta / dist)
        disp.append(delta)
        time.append(line/Line_Rate)
    
    return(strain,disp,time)

def EndTimeCut(Strain,StrainTime,StressTime):
    end_time = max(StressTime)
    end_index = bisect_left(StrainTime, end_time) + 1
    
    Strain = Strain[:end_index]
    StrainTime = StrainTime[:end_index]
    
    return(Strain,StrainTime)

def ImageShow(image):
    
    image_blur = cv2.resize(image,(1950,468))
    cv2.namedWindow("Marked Image")
    cv2.imshow("Marked Image", image_blur)
    
    return

def DataFilter(data, blur_radius):
    
    data = uniform_filter1d(data,blur_radius)
    
    return(data)

def StrainPlot(strain, time):

    plt.rcParams['font.size'] = '16'
    plt.rcParams['font.family'] = 'Arial'
    
    fig = plt.figure(figsize=(8,8))
    ax = plt.axes((0.15,0.15,0.7,0.7))
    
    plt.title("Engineering Strain vs Time", fontsize = 24, pad = 12)
    plt.xlabel("Time (ms)", fontsize = 20, labelpad = 10)
    plt.ylabel("Engineering Strain (mm/mm)", fontsize = 20, labelpad = 10)
    #plt.axis([0,len(strain),0,1])
    
    plt.plot(time, strain)
    plt.show()
    
    return

def StressPlot(stress, time):

    plt.rcParams['font.size'] = '16'
    plt.rcParams['font.family'] = 'Arial'
    
    fig = plt.figure(figsize=(8,8))
    ax = plt.axes((0.15,0.15,0.7,0.7))
    
    plt.title("Engineering Stress vs Time", fontsize = 24, pad = 12)
    plt.xlabel("Time (ms)", fontsize = 20, labelpad = 10)
    plt.ylabel("Engineering Stress (MPa)", fontsize = 20, labelpad = 10)
    #plt.axis([0,len(strain),0,1])
    
    plt.plot(time, stress)
    plt.show()
    
    return

def TimeAlignment(tx,x,ty,y): # x is strain, y is stress, t is their times

    j = 0                   # j is the counter for strain values.
    u = 0                   # u is the dummy variable for strains.
    X = []                  # X is the new strain values.
    T = []                  # T is the new times for the strains.
#    Y = []                  # Y is the new stress values if they need to be cut.
#    Yt = []                 # Yt is the new stress times if they need to be cut.
    
    #print("length of strain is " + str(len(x)))
    for i in range(len(y)):
        t = ty[i]           # t is the current stress time.
        T.append(t)         # Assign the new strain time as the current stress time.
        u = x[j] + (x[j+1]-x[j]) / (tx[j+1] - tx[j]) * (t - tx[j])
        X.append(u)
        if t >= tx[j+1]:    # If the time has reached a new strain data point
            j += 1          # Increase strain counter by 1

            #print(str(j))
#        print("Checking if " + str(j+1) + " is greater than or equal to " + str(len(x)))
#        if j+1 >= len(x):
#            print("IT IS! Cutting Stress time.")
#            Y = y[:i+1]
#            Yt = ty[:i+1]
#            break

    return(X,T)

def DataExport(strain, voltage, time):
    
    data_all = [time,strain,voltage]
    
    data_all = np.transpose(data_all)
    
    headings = ["Time (ms)", "Strain (mm/mm)", "Voltage (V)"]
    
    data_all = pd.DataFrame(data_all, columns=headings)
    
    name = filedialog.asksaveasfilename(filetypes = [("CSV (.csv)" , "*.csv")])
    
    print(name)

    data_all.to_csv(name + '.csv', index=False)
    
    return()

def QSDataExport(time, strain, stress):
    
    data_all = [time, strain, stress]
    
    data_all = np.transpose(data_all)
    
    headings = ["Time (s)", "Strain (mm/mm)", "Stress (MPa)"]
    
    data_all = pd.DataFrame(data_all, columns=headings)
    
    name = filedialog.asksaveasfilename(filetypes = [("CSV (.csv)" , "*.csv")])
    
    print(name)

    data_all.to_csv(name + '.csv', index=False)
    
    return()

def MakeVideo(image, fps, skip, frames):
    '''
    image is a cv2 image object
    fps is the rate desired for the output video
    skip is the number of lines to skip between saved lines in the video
    lines is the number of lines to export to video
    '''
    scale = 3
    width = len(image[0])
    width_scaled = int(width / scale)
    frame = (width_scaled,200)
    lines = []
    skip_save_count = skip

    video_name = filedialog.asksaveasfilename(filetypes = [("MP4 (.mp4)" , "*.mp4")]) +'.mp4'

    video = cv2.VideoWriter(video_name, 0, fps, frame)
    
    for line in range(len(image)):
        if skip_save_count != 0:
            skip_save_count -= 1
            continue
        if line > frames:
            break
        skip_save_count = skip
        temp = cv2.rotate(image[line], cv2.ROTATE_90_COUNTERCLOCKWISE)
        temp = cv2.resize(temp, frame)
        lines.append(temp)
        video.write(temp)
    
    #print("Saving Video as " + video_name)
    video.release()
    
    return()

def FindTarget(image, threshold, min_dPix):

    '''
    This function finds the nearest black white interface within the first line of an image then tracks the target down the image.
    
    The application for this is directly correlated to linescan camera outputs.

    This code was written for a 4k LS camera but the only edits would need to be changing the scale in the first line to see the whole image when selecting the target.

    threshold is the pixel value being looked for to be defined as the target.
    
    min_dPix is the minimum difference between black and white a target can lie within.

    '''
    
    # Showing the image and allowing the user to select the approximate location of the target

    scale = 3
    width = len(image[0])
    width_scaled = int(width / scale)
    
    first_line = image[0:10]
    first_line = cv2.resize(first_line, (width_scaled,400))

    roi = cv2.selectROI('Select Gage Section', first_line, fromCenter=TRUE)
    cv2.destroyAllWindows()

    target = int(roi[0]+(roi[2])/2) * scale
    #print(f'You selected target at pixel {target}.')

    dPix = 0 # This is a gradient checking if the target is black to white or white to black.
    i = 0 # i is a counting variable for the while loop.
    left = target
    right = target

    while abs(dPix) <= min_dPix:
        i += 1
        left -= 1
        right += 1        
        leftMag = image[0][left] # pulling the pixel value at the left side
        rightMag = image[0][right] # pulling the pixel value at the right side
        dPix = int(leftMag) - int(rightMag)
        #print(f'Finding the Gradient from {left} to {right} to be {leftMag} - {rightMag} = {dPix} at a radius of {i} from {target}.')

    direction = np.sign(dPix) # this specifies whether the target is white to black (1) or black to white (-1)
    left = target-i
    right = target+i

    #print(f'The range is from pixel {left} to {right}.')
    #print(f'The range goes from {leftMag} to {rightMag}.')

    if direction > 0:
        #print("The targeted range goes from white to black.")
        while image[0][target] < threshold: # moving the target to the left until it sees black.
            target -= 1
        while image[0][target] >= threshold: # moving the target back to the right until it sees white.
            target += 1
    else:
        #print("The targeted range goes from black to white.")
        while image[0][target] < threshold: # moving the target to the right until it sees white.
            target += 1
        while image[0][target] >= threshold: # moving the target back to the left until it sees black.
            target -= 1                

    return(image,target,direction)

def GetDisplacement(image, black, white, threshold, target, direction, rate, pixelRatio, limit=960):

    '''
    This function takes in a linescan image with line rate and pixel size defined with a target selected and defined by FindTarget
        and outputs displacement and velocity of that target wtih respect to time.
    '''

    #print(f'Evalutating {limit} lines.')
    start = target # starting location for the target tracker
    location = [] # initializing output variables
    disp = []
    time = []
    fit_R = 10 # Radius of points to fit a line to

    #Each line starts the tracker over by moving the start location towards the black region and then moving towards the white until the threshold is met.
    for line in range(min(len(image),limit)):
        
        if min(image[line]) > black:
            print("Line " + str(line) + " has no black showing.")
            location.append(location[-1])
            continue
        
        if max(image[line]) < white:
            print("Line " + str(line) + " has no white showing.")
            location.append(location[-1])
            continue
        

        #start = start + direction * 25 # the tracker moves 25 pixels away from the previous location to begin looking for the white.
        #print(f'Beginning search at {start}.')
        #print(str(image[line][start]))
        while image[line][start] < threshold:   # While the pixel is still black, move one pixel over and try again.
            start -= direction
            if start >= len(image[line]):
                break
        while image[line][start] > threshold:   # While the pixel is still black, move one pixel over and try again.
            start += direction
            if start >= len(image[line]):
                break


        #print(f'Target in line {line} is at pixel {start}.')
        
        #print(f'Original location = {start}.')
        x = np.linspace(start-fit_R , start+fit_R , 2*fit_R)
        y = image[line][start-fit_R:start+fit_R]
        #print(f'Length of x is {len(x)} and length of y is {len(y)}.')
        m,b = np.polyfit(x,y,1)
        start_fine = (threshold-b)/m        
        #print(f'Refined location = {start_fine}.')

        #location.append(start) # Once the threshold is found, the location is logged.
        location.append(start_fine) # Once the threshold is found, the location is logged.

    LenL = len(location)
    Movement = np.sign(location[-1]-location[0]) # movement defines the direction of movement of the target (left (-1) or right (1)) based on the initial and final locations.
    #print(f'There are {LenL} locations found, and movement went in the {Movement} direction.')

    u = location[0] # defining the inital location of the target.

    # Defining the location of the target vs time realtive to its starting position. Time is based off the rate of the LS camera.
    for i in range(len(location)):
        v = location[i]
        disp.append((v - u) * pixelRatio * Movement)
        time.append(i/rate *1000)

    # First velocity calculation uses the forward difference method.
    vel = [(disp[1]-disp[0])/(time[1]-time[0])]

    # All intermediary velocities use the central difference method.
    for d in range(len(disp)-2):
        vel.append((disp[d+2] - disp[d]) / (time[d+2] - time[d]))

    # Final veloicty caluclation uses the backward difference method.
    vel.append((disp[-1]-disp[-2])/(time[-1]-time[-2]))    

    # Optional section to output the total time, displacment, and velocity if desired.
    '''
    LenD = len(disp)
    LenT = len(time)
    LenV = len(vel)
    TotalD = max(disp)
    duration = max(time)
    MaxV = (max(vel))

    print(f'There are {LenD} displacements (total = {TotalD} mm), {LenT} times ({duration} ms), and {LenV} velocities (max = {MaxV}) m/s.')
    '''
    return(location,disp,vel,time)

def DispPlot(disp, time):

    plt.rcParams['font.size'] = '16'
    plt.rcParams['font.family'] = 'Arial'
    
    fig = plt.figure(figsize=(8,8))
    ax = plt.axes((0.15,0.15,0.7,0.7))
    
    plt.title("Displacement vs Time", fontsize = 24, pad = 12)
    plt.xlabel("Time (ms)", fontsize = 20, labelpad = 10)
    plt.ylabel("Displacement (mm)", fontsize = 20, labelpad = 10)

    plt.plot(time, disp)
    plt.show()
    return

def VelocityPlot(vel, time):

    plt.rcParams['font.size'] = '16'
    plt.rcParams['font.family'] = 'Arial'
    
    VvsTfig = plt.figure(figsize=(8,8))
    ax = plt.axes((0.15,0.15,0.7,0.7))
    
    plt.title("Velocity vs Time", fontsize = 24, pad = 12)
    plt.xlabel("Time (ms)", fontsize = 20, labelpad = 10)
    plt.ylabel("Velocity (m/s)", fontsize = 20, labelpad = 10)

    plt.plot(time, vel)
    plt.show()
    
    return

def DataExport_DispVel(time, disp, vel):
    
    data_all = [time,disp,vel]
    
    data_all = np.transpose(data_all)
    
    headings = ["Time (ms)", "Disp (mm)", "Vel (m/s)"]
    
    data_all = pd.DataFrame(data_all, columns=headings)
    
    name = filedialog.asksaveasfilename(filetypes = [("CSV (.csv)" , "*.csv")])
    
    print(name)

    data_all.to_csv(name + '.csv', index=False)
    
    return()



#########################

#Local Functions

#########################


def InsertLogo():

    im = Image.open('Standard_Mechanics_Stacked_Logo_Color_NoBackground_WhiteFont.png')
    
    tk_im = CTkImage(im,size=(250,60))

    imLabel = CTkLabel(root,image=tk_im,text='')
    imLabel.image = tk_im

    imLabel.place(relx=0.01,rely=0.8)


    return()

def GetImage():
    
    filetypes = [
    ("Image Files",".bmp")
    ]
    
    image_file = filedialog.askopenfilename(filetypes = filetypes)
    if image_file == '':
        return()
    #image_label.config(text=image_file,fg = 'black')

    temptextfile = open(r'C:\temp\LEAP_data/temp.txt',"w")
    
    temptextfile.writelines('Lines~' + image_file)

    temptextfile.close()
    
    if 'Image.bmp' in os.listdir(r'C:\temp\LEAP_data'):
        os.remove(r'C:\temp\LEAP_data/Image.bmp')
    
    ShowImage()

    return()

def FindImage():

    temptextfile = open(r'C:\temp\LEAP_data/temp.txt',"r")
        
    text = temptextfile.readlines()
    
    for line in text:
        if 'Lines' in line:
            line = line.split('~')
            line.remove('Lines')
            image_file = line[0]

    image = cv2.imread(image_file,0)
    return(image)

def ShowImage():

    if 'Image.bmp' in os.listdir(r'C:\temp\LEAP_data'):
        image_file = r'C:\temp\LEAP_data/Image.bmp'
    
    elif 'EdgedImage.jpg' in os.listdir(r'C:\temp\LEAP_data'):
        image_file = r'C:\temp\LEAP_data/EdgedImage.jpg'
    
    elif 'temp.txt' in os.listdir(r'C:\temp\LEAP_data'):
        temptextfile = open(r'C:\temp\LEAP_data/temp.txt',"r")
        
        text = temptextfile.readlines()
        
        for line in text:
            if 'Lines' in line:
                line = line.split('~')
                line.remove('Lines')
                image_file = line[0]
        
        temptextfile.close()
    
    else: image_file = 'Blank_Rectangle.jpg'

    image = Image.open(image_file)

    _,height = image.size
    line_limit.delete(0,END)
    line_limit.insert(0,str(height))

    image = image.resize((800,200))
    image = ImageTk.PhotoImage(image)

    #imageCTk = CTkImage(image)

    imageShowLabel = Label(root, image = image, text='')
    imageShowLabel.image = image

    


    imageShowLabel.grid(row = 1, column = 1, rowspan = 5, columnspan = 3)

    if 'Blank' not in image_file:
        calibrate_button.configure(state='normal')
        TT_button.configure(state='normal')
        Strain_button.configure(state='normal')
        Line_button.configure(state='normal')
        Reset_button.configure(state='normal')
        makeVideo_button.configure(state='normal')


    return()

def EdgeOverlay():

    image = FindImage()

    SData = pd.read_csv("LEAP_data/StrainTimeData.csv")
    time = SData['Time ms']
    left_edge = SData['Left Edge pix']
    right_edge = SData['Right Edge pix']

    imageColor = np.zeros((max(len(image),len(time)),len(image[0]), 4),np.uint8)
    overlay = np.zeros((max(len(image),len(time)),len(image[0]), 4),np.uint8)

    scale = 3

    for line in range(len(overlay)):
        overlay[line][int(left_edge[line])] = (0,255,0,255)
        overlay[line][int(right_edge[line])] = (0,0,255,255)
        for i in range(len(image[0])):
            pix = image[line][i]
            imageColor[line][i] = (pix,pix,pix,255)

    imageColorFull = imageColor
    cnd = overlay[:,:,3] > 0
    imageColorFull[cnd] = overlay[cnd]
    cv2.imwrite("LEAP_data/EdgedImageFull.jpg",imageColorFull)

    overlaySmall = np.zeros((int(len(overlay)/scale),int(len(overlay[0])/scale),4),np.uint8)

    for line in range(len(overlaySmall)):
        sum_L = 0
        sum_R = 0
        for i in range(scale):
            sum_L += left_edge[line*scale+i]
            sum_R += right_edge[line*scale+i]
        left = int(sum_L/scale/scale)
        right = int(sum_R/scale/scale)

        overlaySmall[line][left] = (0,255,0,255)
        overlaySmall[line][right] = (0,0,255,255)
        
    imageColor = cv2.resize(imageColor,(int(len(imageColor[0])/scale),int(len(imageColor)/scale)))

    cnd = overlaySmall[:,:,3] > 0
    imageColor[cnd] = overlaySmall[cnd]

    cv2.imwrite("LEAP_data/EdgedImage.jpg",imageColor)

    ShowImage()

    return()

def GetVoltage():

    filetypes = [
    ("CSV Files",".csv")
    ]
    
    voltage_file = filedialog.askopenfilename(filetypes = filetypes)
    if voltage_file == '':
        return()


    temptextfile = open(r'C:\temp\LEAP_data/temp.txt',"r")
    
    text = temptextfile.readlines()

    for line in text:
        if 'Voltages~' in line:
            text.remove(line)

    text.append('~\nVoltages~' + voltage_file)

    temptextfile.close()


    temptextfile = open(r'C:\temp\LEAP_data/temp.txt','w')

    temptextfile.writelines(text)
    
    temptextfile.close()

    WriteVoltData()

    return()

def WriteVoltData():
    
    if 'temp.txt' in os.listdir(r'C:\temp\LEAP_data'):
        temptextfile = open(r'C:\temp\LEAP_data/temp.txt',"r")
        
        text = temptextfile.readlines()
        
        for line in text:
            if 'Voltages~' in line:
                line = line.split('~')
                line.remove('Voltages')
                file = line[0]
        
        temptextfile.close()
    
    #else: image_file = 'Blank_Rectangle.jpg'

    data = pd.read_csv(file)
    time = data['Time']
    trans_volt = data['Channel B']
    
    Voltage = []
    Time = []
    units = [[],[]]
    
    if 'ms' in time[0]:
        units[0] = 'ms'
        time_scalar = 1
    else:
        units[0] = 's'
        time_scalar = 1000

    if 'mV' in trans_volt[0]:
        units[1] = 'mV'
        scalar = 0.001
    else:
        units[1] = 'V'
        scalar = 1

    data_out = []
    headings = ['Time ms', 'Voltage ' +units[1]]

    for data in range(len(trans_volt)-2):
        if float(time[data+2]) < 0:
            continue
        Voltage.append((float(trans_volt[data + 2])) * scalar)
        Time.append(float(time[data + 2]) * time_scalar)

        data_out.append([Time[-1],Voltage[-1]])

    data_out = pd.DataFrame(data_out, columns=headings) #Making the data_out variable into a DataFrame

    data_out.to_csv(r'C:\temp\LEAP_data/VoltageData.csv', index=False)              #Writing the data to the csv file

    #Checking if there exists a voltage data folder in LEAP_data directory
    if 'StrainTimeData.csv' in os.listdir(r'C:\temp\LEAP_data'):
        MergeStrainVoltage()

    return(Voltage, Time, units)

def MakeTempDataStorage():

    tempdirectory = r'C:\temp'
    if os.path.isdir(tempdirectory):
        tempdirectory = r'C:\temp'
    else:
        os.mkdir(tempdirectory)
        
    directory = r'C:\temp\LEAP_data'
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            os.remove(os.path.join(directory,file))
    else: os.mkdir(directory)                          

    return()

def Pix2DistCal():
    
    image = FindImage()

    messagebox.showinfo(title = 'Setting Distance', message = 'Select a known distance in the first line to calibrate distance.')

    scale = 3
    width = len(image[0])
    width_scaled = int(width / scale)
    
    first_line = image[0:10]
    first_line = cv2.resize(first_line, (width_scaled,400))

    roi = cv2.selectROI('Select Gage Section', first_line)
    cv2.destroyAllWindows()
    
    left = roi[0] * scale
    right = (roi[0] + roi[2]) * scale

    distance = simpledialog.askfloat(title="Distance", prompt="What is the distance between markers in mm?")   #This is awesome!!!
    scale = round(distance / (right - left) * 1000,2)

    pix2dist.delete(0,END)
    pix2dist.insert(0,str(scale))

    return()

def TargetTrack():
    
    if pix2dist.get() =='':
        Pix2DistCal()
    
    scale = float(pix2dist.get())/1000
    
    image = FindImage()
    black = int(black_level.get())
    white = int(white_level.get())
    gray = int(threshold.get())
    blur = int(blur_radius.get())
    rate = line_rate.get()
    limit = int(line_limit.get())
    
    while rate == '' or not rate.isnumeric():
        rate = str(simpledialog.askinteger(title="Line Rate", prompt="What is the line rate? (lines/s)"))
        line_rate.delete(0,END)
        line_rate.insert(0,str(rate))
    rate = int(line_rate.get())

    messagebox.showinfo(title = 'Selecting Target', message = 'Select a black-white or white-black target to track.')

    image, target, direction = FindTarget(image,gray,100)

    image = uniform_filter1d(image,blur)

    location, displacement, velocity, time = GetDisplacement(image, black, white, gray, target, direction, rate, scale, limit=limit)

    headings = ['Time (ms)', 'Location (pix)', 'Displacement (mm)', 'Velocity (m/s)']
    data_all = []
    
    for i in range(len(time)):
        data_all.append([time[i],location[i],displacement[i],velocity[i]])

    data_all = pd.DataFrame(data_all, columns=headings)
    data_all.to_csv(r'C:\temp\LEAP_data/TargetTracking.csv',index=FALSE)

    dispPlot_button.configure(state='normal')

    dispExport_button.configure(state='normal')

    return()

def PlotDispData():

    sample_data = pd.read_csv(r'C:\temp\LEAP_data/TargetTracking.csv')   #Extracting the data
    time = sample_data.iloc[:,0]
    location = sample_data.iloc[:,1]
    displacement = sample_data.iloc[:,2]
    velocity = sample_data.iloc[:,3]
    
    fig,ax = plt.subplots()
    ax.plot(time, displacement, color = 'orange')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Displacement (mm)')
    ax2 = ax.twinx()
    ax2.plot(time, velocity)
    ax2.set_ylabel('Velocity (m/s)')
    
    plt.show()


    return()

def ExportDispData():

    sample_data = pd.read_csv(r'C:\temp\LEAP_data/TargetTracking.csv')   #Extracting the data
    time = sample_data.iloc[:,0]
    location = sample_data.iloc[:,1]
    displacement = sample_data.iloc[:,2]
    velocity = sample_data.iloc[:,3]

    headings = ['Time (ms)', 'Location (pix)', 'Displacement (mm)', 'Velocity (m/s)']
    data_all = [time,location,displacement,velocity]
    data_all = np.transpose(data_all)
    data_all = pd.DataFrame(data_all, columns=headings)
    
    file_name = filedialog.asksaveasfilename(filetypes = [("CSV (.csv)" , "*.csv")])
    if file_name == '':
        return()
    data_all.to_csv(file_name + '.csv', index=False)

    return()

def FindStrains():

    #Importing image as cv2 image object
    image = FindImage()    

    #Taking in user inputs from GUI
    white = int(white_level.get())  
    black = int(black_level.get())
    gray = int(threshold.get())
    blur = int(blur_radius.get())
    rate = line_rate.get()
    limit = int(line_limit.get())
    
    while rate == '' or not rate.isnumeric():
        rate = str(simpledialog.askinteger(title="Line Rate", prompt="What is the line rate? (lines/s)"))
        line_rate.delete(0,END)
        line_rate.insert(0,str(rate))
    rate = int(line_rate.get())

    ########## EDIT HERE
    #direc = int(direction.get())

    #if direc == 0:
    #    messagebox.showinfo(title = 'Test Direction', message = 'Select either tension or compression.')
    #    return()

    #############

    messagebox.showinfo(title = 'Gage Length Selection', message = 'Select the gage of the sample to compute its strains.')

    #Finding the left and right edge in first line of image.
    left,right = SetGage(image,black,white)
    if left == 50 and right == 50:
        messagebox.showinfo(title = 'Gage Length Selection', message = 'No gage length selected.')
        return()  

    # Blurring lines to ensure more accurate edge detection
    image = uniform_filter1d(image, blur)
    
    #Tracking the two edges throughout all lines.
    left_edge,right_edge = EdgeFinder(image, (left,right), blur, black, white, gray, limit)  

    #Computing strains from edge locations.
    strain,displacement,time = EdgetoStrain(left_edge, right_edge, rate) 

    #Light filtering of strain data (averaging with a radius of 3 pixels).
    strain = DataFilter(strain,3) 

    #Automatically finds direction of strain based on sign at 1.0% strain.
    for e in strain:
        if float(e)**2 > 0.0001:
            direc = np.sign(e)
            break

    #Correcting sign of strains via direction of testing.
    for i in range(len(strain)):
        strain[i] = direc * strain[i]

    #Defining the headings for the temp CSV data file.
    headings = ['Time ms', 'Left Edge pix', 'Right Edge pix', 'Displacement pix', 'Strain mm/mm']
    data_all = []
    
    #Combining the data into one variable and then saving it to temp CSV data file.
    for i in range(len(time)):
        data_all.append([time[i]*1000, left_edge[i], right_edge[i], displacement[i], strain[i]])

    data_all = pd.DataFrame(data_all, columns=headings)
    data_all.to_csv(r'C:\temp\LEAP_data/StrainTimeData.csv',index=FALSE)

    #Creating the button to show the strain vs time data.
    strainPlot_button.configure(state="normal")

    #Creating the button to export the strain vs time data.
    strainExport_button.configure(state="normal")    

    #Checking if there exists a voltage data folder in LEAP_data directory
    if 'VoltageData.csv' in os.listdir(r'C:\temp\LEAP_data'):
        MergeStrainVoltage()

    #EdgeOverlay()

    return()

def MergeStrainVoltage():

    #Importing the voltage data from the temp folder.
    voltage_data = pd.read_csv(r'C:\temp\LEAP_data/VoltageData.csv')
    volt_time = voltage_data.iloc[:,0]
    voltage = voltage_data.iloc[:,1]
    
    with open(r'C:\temp\LEAP_data/VoltageData.csv') as file:
        content = file.readlines()
        file.close()
    if 'mV' in content[0]:
        V_unit = 'mV'
    else: V_unit = 'V'

    #Truncating the voltage data to initial rise and fall.
    #Changed this algorithm to not use user input 2/21/23.
    for V in voltage:
        if V**2 > 0.01:
            direc = np.sign(V)
    #direc = int(direction.get())
    
    flag = 0
    V = []
    Vt = []

    if direc < 0:   #Routine for compression
        peak = min(voltage)
        end_volt = peak * 0.2

        for i in range(len(voltage)):
            V.append(voltage[i])
            Vt.append(volt_time[i])
            if flag == 2 and i == end_test:
                break
            elif flag == 1 and voltage[i] > end_volt:
                end_test = i + 10000
                flag = 2
            elif voltage[i] < end_volt:
                flag = 1
    
    if direc > 0:   #Routine for tension
        peak = max(voltage)
        end_volt = peak * 0.1

        for i in range(len(voltage)):
            V.append(voltage[i])
            Vt.append(volt_time[i])
            if flag == 2 and i == end_test:
                break
            elif flag == 1 and voltage[i] < end_volt:
                end_test = i + 10000
                flag = 2
            elif voltage[i] > end_volt:
                flag = 1
    
    data_out = []
    headings = ['Time ms', 'Voltage ' + V_unit]

    for i in range(len(V)):
        data_out.append([Vt[i],V[i]])

    data_out = pd.DataFrame(data_out, columns=headings) #Making the data_out variable into a DataFrame
    data_out.to_csv(r'C:\temp\LEAP_data/VoltageData.csv', index=False) #Writing the data to the csv file
    
    
    TruncateImageandStrain(Vt)

    #Importing the strain data from temp folder.
    strain_data = pd.read_csv(r'C:\temp\LEAP_data/StrainTimeData.csv')
    strain_time = strain_data.iloc[:,0]
    strain = strain_data.iloc[:,4]

    s = []  #Strain data 
    st = [] #Strain time data

    for i in range(len(strain_time)):
        s.append(strain[i])
        st.append(strain_time[i])

    s,st = TimeAlignment(st,s,Vt,V)

    data_out2 = []
    headings2 = ['Time ms', 'Strain mm/mm', 'Voltage ' + V_unit]

    for i in range(len(st)):
        data_out2.append([st[i], s[i], V[i]])
    
    data_out2 = pd.DataFrame(data_out2, columns = headings2)
    data_out2.to_csv(r'C:\temp\LEAP_data/StrainVoltageData.csv')

    return()

def TruncateImageandStrain(time):

    image = FindImage()
    rate = int(line_rate.get())

    index = int( max(time) / 1000 * rate + 100)
    image = image[:index]

    cv2.imwrite(r'C:\temp\LEAP_data/Image.bmp', image)

    ShowImage()

    s = []  #Strain values
    st = [] #Strain time values
    LE = [] #Left Edge
    RE = [] #Right Edge
    D = []  #Displacement

    #Importing the strain data from temp folder.
    strain_data = pd.read_csv(r'C:\temp\LEAP_data/StrainTimeData.csv')
    strain_time = strain_data.iloc[:,0]
    left_edge = strain_data.iloc[:,1]
    right_edge = strain_data.iloc[:,2]
    displacement = strain_data.iloc[:,3]
    strain = strain_data.iloc[:,4]

    #Defining the headings for the temp CSV data file.
    headings = ['Time ms', 'Left Edge pix', 'Right Edge pix', 'Displacement pix', 'Strain mm/mm']
    data_all = []
    
    for i in range(index):
        data_all.append([strain_time[i],left_edge[i],right_edge[i],displacement[i],strain[i]])
    
    data_all = pd.DataFrame(data_all, columns=headings)
    data_all.to_csv(r'C:\temp\LEAP_data/StrainTimeData.csv',index=FALSE)

    


    return()

def PlotStrainData():

    sample_data = pd.read_csv(r'C:\temp\LEAP_data/StrainTimeData.csv')   #Extracting the data
    time = sample_data.iloc[:,0]
    strain = sample_data.iloc[:,4]

    StrainPlot(strain,time)

    return()

def ExportStrainData():

    if 'StrainVoltageData.csv' in os.listdir(r'C:\temp\LEAP_data'):
        sample_data = pd.read_csv(r'C:\temp\LEAP_data/StrainVoltageData.csv')
        time = sample_data.iloc[:,1]
        strain = sample_data.iloc[:,2]
        voltage = sample_data.iloc[:,3]

        with open(r'C:\temp\LEAP_data/StrainVoltageData.csv') as file:
            content = file.readlines()
            file.close()
        if 'mV' in content[0]:
            V_unit = 'mV'
        else: V_unit = 'V'

        headings = ['Time (ms)', 'Strain (mm/mm)', 'Voltage '+ V_unit]
        data_all = [time, strain, voltage]
    
    else:
        sample_data = pd.read_csv(r'C:\temp\LEAP_data/StrainTimeData.csv')   #Extracting the data
        time = sample_data.iloc[:,0]
        strain = sample_data.iloc[:,4]

        headings = ['Time (ms)', 'Strain (mm/mm)']
        data_all = [time, strain]
    
    data_all = np.transpose(data_all)
    data_all = pd.DataFrame(data_all, columns = headings)

    file_name = filedialog.asksaveasfilename(filetypes = [("CSV (.csv)" , "*.csv")])
    if file_name == '':
        return()
    data_all.to_csv(file_name + '.csv', index=False)


    return()

def ShowLineValues():
    
    temptextfile = open(r'C:\temp\LEAP_data/temp.txt',"r")
    text = temptextfile.readlines()
    for line in text:
        if 'Lines' in line:
            line = line.split('~')
            line.remove('Lines')
            image_file = line[0]

    image = Image.open(image_file)
    
    width, height = image.size

    line = int(simpledialog.askinteger(title="Line of Interest", prompt="Which line do you want to see?"))
    while line >= height:
        messagebox.showerror(message = f'Line must be less than {height}.')
        line = int(simpledialog.askinteger(title="Line of Interest", prompt="Which line do you want to see?"))
    line_data = []
    pixel = []
    for i in range(width):
        pixel.append(i)
        line_data.append(image.getpixel((i,line)))

    plt.rcParams['font.size'] = '16'
    plt.rcParams['font.family'] = 'Arial'
    
    fig = plt.figure(figsize=(8,8))
    ax = plt.axes((0.15,0.15,0.7,0.7))
    
    plt.title("Pixel Brightness Along Line", fontsize = 24, pad = 12)
    plt.xlabel("Pixel (pix)", fontsize = 20, labelpad = 10)
    plt.ylabel("Brightness (8 bit)", fontsize = 20, labelpad = 10)

    plt.plot(pixel, line_data)
    plt.show()

    return()

def ResetTool():
    
    MakeTempDataStorage()
    ShowImage()

    line_rate.delete(0,END)
    
    black_level.delete(0,END)
    black_level.insert(0,'50')
    
    white_level.delete(0,END)
    white_level.insert(0,'200')
    
    threshold.delete(0,END)
    threshold.insert(0,'125')

    blur_radius.delete(0,END)
    blur_radius.insert(0,'5')

    pix2dist.delete(0,END)
    #pix2dist.insert(0,'Run Calibration')

    Reset_button.configure(state='disabled')
    calibrate_button.configure(state='disabled')
    TT_button.configure(state='disabled')
    Strain_button.configure(state='disabled')
    Line_button.configure(state='disabled')
    dispPlot_button.configure(state='disabled')
    dispExport_button.configure(state='disabled')
    strainPlot_button.configure(state='disabled')
    strainExport_button.configure(state='disabled')
    makeVideo_button.configure(state='disabled')

    return()

def SaveVideo():
    
    def SaveVideo():
        fps = int(frame_rate.get())
        skips = int(skip_save.get())
        lines = int(video_length.get())

        MakeVideo(image, fps, skips, lines)
        
        return()
    
    image = FindImage()

    vidWindow = CTkToplevel(root)
    vidWindow.title('Export Video')
    vidWindow.geometry("350x200")
    vidWindow.iconbitmap('LEAPlogo.ico')

    label = CTkLabel(vidWindow, text='Input the Video settings.', font=('Arial Black',14))
    label.grid(row=0, column=0, columnspan = 2, pady = 15)

    frameRate_label = CTkLabel(vidWindow, text='Desired Frame Rate: ', font=('Arial Black',14))
    frameRate_label.grid(row=1, column=0, padx=10)
    frame_rate = CTkEntry(vidWindow,width=50)
    frame_rate.insert(0,'30')
    frame_rate.grid(row=1,column=1)

    skipSave_label = CTkLabel(vidWindow, text='Skip save: ', font=('Arial Black',14))
    skipSave_label.grid(row=2,column=0,padx=10)
    skip_save = CTkEntry(vidWindow,width=50)
    skip_save.insert(0,'0')
    skip_save.grid(row=2,column=1)

    videoLength_label = CTkLabel(vidWindow, text = 'Lines to Save: ', font=('Arial Black',14))
    videoLength_label.grid(row=3,column=0,padx=10)
    video_length = CTkEntry(vidWindow,width = 50)
    video_length.insert(0,line_limit.get())
    video_length.grid(row=3,column=1)

    Save_Button = CTkButton(vidWindow, text='Save', command=SaveVideo)
    Save_Button.grid(row=4, column=0,pady=15)

    Cancel_Button = CTkButton(vidWindow, text='Cancel', command=vidWindow.destroy)
    Cancel_Button.grid(row=4, column=1,pady=15)

    vidWindow.destroy

    return()

def on_closing():
    
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        MakeTempDataStorage()
        os.rmdir(r'C:\temp\LEAP_data')
        root.destroy()
    return()


#########################

#Main Code

#########################

root = CTk()
root.title('Standard Mechanics LEAP Tool')
root.iconbitmap('LEAPlogo.ico')
root.geometry("1300x400")

title_label =CTkLabel(root, text = '', font=('Arial Black',14))
title_label.grid(row = 0, column = 0, pady = 10, padx = 10, columnspan = 6)


data_button = CTkButton(root, text="Select Image", command=GetImage, font=('Arial Black',14))
data_button.grid(row = 1, column = 0, padx = 10)

calibrate_button = CTkButton(root, text="Calibrate Dist", command=Pix2DistCal, state='disabled', font=('Arial Black',14))
calibrate_button.grid(row = 3, column = 0, padx = 10)

#voltage_button = Button(root, text="Import Voltage", command=GetVoltage)
#voltage_button.grid(row = 5, column = 0, padx = 10)


#Set of buttons to appear after certain events
Reset_button = CTkButton(root, text = 'Reset Tool', command=ResetTool, state='disabled', font=('Arial Black',14))
TT_button = CTkButton(root, text = 'Target Track', command=TargetTrack, state='disabled', font=('Arial Black',14))
Strain_button = CTkButton(root, text = 'Find Strain', command=FindStrains, state='disabled', font=('Arial Black',14))
Line_button = CTkButton(root, text = 'Line Values', command=ShowLineValues, state='disabled', font=('Arial Black',14))
dispPlot_button = CTkButton(root, text = 'Show Plot', command=PlotDispData, state='disabled', font=('Arial Black',14))
dispExport_button = CTkButton(root, text = 'Export', command=ExportDispData, state='disabled', font=('Arial Black',14))
strainPlot_button = CTkButton(root, text = 'Show Plot', command=PlotStrainData, state='disabled', font=('Arial Black',14))
strainExport_button = CTkButton(root, text = 'Export', command=ExportStrainData, state='disabled', font=('Arial Black',14))
makeVideo_button = CTkButton(root, text='MakeVideo', command=SaveVideo, state='disabled', font=('Arial Black',14))

Reset_button.grid(row = 2, column = 0, padx = 10)
TT_button.grid(row = 6, column = 3)
Strain_button.grid(row = 6, column = 2)
Line_button.grid(row = 6, column = 1)
dispPlot_button.grid(row = 7, column = 3)
dispExport_button.grid(row = 8, column = 3)
strainPlot_button.grid(row = 7, column = 2)
strainExport_button.grid(row = 8, column = 2)    
makeVideo_button.grid(row = 4, column = 0, padx = 10)


linerate_label = CTkLabel(root, text = "Line Rate (/s)", font=('Arial Black',14))
linerate_label.grid(row = 1, column = 5)
line_rate = CTkEntry(root, placeholder_text='Lines/s')
line_rate.grid(row = 1, column = 6)

black_label = CTkLabel(root, text = "Black Level", font=('Arial Black',14))
black_label.grid(row = 2, column = 5)
black_level = CTkEntry(root)
black_level.insert(0,'50')
black_level.grid(row = 2, column = 6)

white_label = CTkLabel(root, text = "White Level", font=('Arial Black',14))
white_label.grid(row = 3, column = 5)
white_level = CTkEntry(root)
white_level.insert(0,'200')
white_level.grid(row = 3, column = 6)

threshold_label = CTkLabel(root, text = "Threshold", font=('Arial Black',14), anchor='e')
threshold_label.grid(row = 4, column = 5)
threshold = CTkEntry(root)
threshold.insert(0,'125')
threshold.grid(row = 4, column = 6)

lineLimit_label = CTkLabel(root, text = "Line Limit", font=('Arial Black',14))
lineLimit_label.grid(row = 5, column = 5)
line_limit = CTkEntry(root)
line_limit.grid(row = 5, column = 6)

blurradius_label = CTkLabel(root, text = "Blur Radius (pix)", font=('Arial Black',14))
blurradius_label.grid(row = 6, column = 5, pady = 12)
blur_radius = CTkEntry(root)
blur_radius.insert(0,'5')
blur_radius.grid(row = 6, column = 6)

pix2dist_label = CTkLabel(root, text = "Distance/Pix (um)", font=('Arial Black',14))
pix2dist_label.grid(row = 7, column = 5, pady = 9, padx = 5)
pix2dist = CTkEntry(root, placeholder_text='Run Calibration')
pix2dist.grid(row = 7, column = 6)

#direction_label = CTkLabel(root,text = 'Direction of Test', font=('Arial Black',14))
#direction_label.grid(row = 8, column = 5, rowspan = 2)
#direction = IntVar()

#R1 = CTkRadioButton(root, text="Tension", variable=direction, value=1)
#R1.grid( row = 8, column = 6, sticky=W )
#R2 = CTkRadioButton(root, text="Compression", variable=direction, value=-1)
#R2.grid( row = 9, column = 6, sticky=W )


MakeTempDataStorage()
InsertLogo()
ShowImage()

root.protocol('WM_DELETE_WINDOW',on_closing)

root.mainloop()