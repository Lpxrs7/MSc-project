#!/usr/bin/env python2
# -*- coding: utf-8 -*-
''' Face Feature Traveling Wave v.0

This script shows different facial feature in a cyclical fashion in order to 
attempt to elicit a traveling wave in Ventral temporal and Lateral Occipital 
areas of the cortex. If I remember correctly the order of stimuli should be
forhead to chin, and vice-versa.

v.0 16/02/2019 - Demo example for Rohan, to get things going.
To do:
1) Make sure that the categories I have created are the correct ones. 
2) N-back task.Detect and store button presses for responses from inside the scanner
2a) instead of N back task, do change in fixation mark... timings should be independant 
3) Instructions of participants
4) Add more images. Only one image per categories, maybe more are needed to achieve larger SNR.
5) Decide on precise timings.
6) Consider whether within feature (if more than1 is presented) stimuli are to be random with or without replacement.
7) Store experiment information. Responses, volumes onset, volume number, filename, order, session, etc...
8) Consider if we contrast modulation like in Rossion FPVS and size/position invariance to account possible differences in aspect ratios. 

Further notes to consider: Image & screen size

'''
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui, info
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle , choice
import os  # handy system and path functions
import random as r
import glob

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

#Checks for data directory, if not, creates it. 
directory = 'data'
if not os.path.exists(directory):
    os.makedirs(directory)

# Store info about the experiment session
expName = 'FaceTW'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'', 'Order':'f/r'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])
dataFile =  open(filename+'.csv', 'w')
dataFile.write('{},{},{}\n'.format('VolOnset', 'Volno', 'filename')) 
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Setup the Window
# win = visual.Window(size=(1024, 758), fullscr=True, screen=0, allowGUI=True, allowStencil=True,
#    monitor='testMonitor', color=[165,165,165], colorSpace='rgb255',blendMode='avg')#, useFBO=True )
win = visual.Window(size=(1440, 900), fullscr=True, screen=0, allowGUI=True, allowStencil=True,
    monitor='testMonitor', color=[165,165,165], colorSpace='rgb255',blendMode='avg')#, useFBO=True )
win.recordFrameIntervals = True
win.mouseVisible = False
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess
win.refreshThreshold = frameDur + 0.002

##----------------- End of Admin Stuff –––––––––––––––––––––––––––––

# --------- Set-up Stimuli ----------
categories = ['Eyes','Nose','Mouth']
catDict= {}
types = ('*.jpg', '*.png','*.bmp') # get file types used for the images

# put them all in a dictionary
for i,c in enumerate(categories):
    List = []
    for files in types:
        List.extend(glob.glob('Stimuli/%s/%s'%(c,files)))
    catDict[c] = List

instruction_text = visual.TextStim(win=win, ori=0, name='instruction_text',
    text='It is better to use an image for instructions than text'
    ' Press space to continue',
    font='Calibri', units='deg',
    pos=[0, 0.5], height=0.9, wrapWidth=20,
    color='white', colorSpace='rgb',
    depth=0.0)
    
wait_for_scanner = visual.TextStim(win=win, ori=0, name='instruction_text',
    text='Waiting for Scanner, please be still.'
    'Press 5 to emulate scanner start',
    font='Calibri', units='deg',
    pos=[0, 0.5], height=0.9, wrapWidth=20,
    color='white', colorSpace='rgb',
    depth=0.0)

# some stimuli place holders
myStim = visual.ImageStim(win, image='Stimuli/nithisDaisies.jpg', size = (4.4*4,4.4), units='deg') # change the file and image size here. Idea -> add equation that times by the relative size of each image file
fixation = visual.TextStim(win, text = '+', height = 1, color ='black', units = 'deg')
greyScreen = visual.TextStim(win, text = '<-->', height = 1, color ='white', units = 'cm')

# --------- Set-up experiment parameters ----------
# Clocks and timings
expClock = core.Clock()
stimClock = core.Clock()
cycleNumber = 4 # number of reps of the order
stimPerCycle = 3 # Was originally 5 --> for sake of pilot change to 3
stimDur = 2
expDuration = stimDur*stimPerCycle*cycleNumber

# Added by RS for loop
# stimNum = 15

##-------------- End of Set-up ----------------

# -------------- Start Experiment ----------------

#check for order and set-up conditions to loop over
condLoop = ['Eyes','Nose','Mouth']
if expInfo['Order'] == 'r': #r for reverse
    condLoop.reverse()

instruction_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

wait_for_scanner.draw()
win.flip()
event.waitKeys(keyList=['5'])
expClock.reset()

# start loop with the given parameters
for cycle in range(cycleNumber):
    for individual in [0, 1, 2, 3, 4]:
        for feature in condLoop:
         # if more images are to be shown start another loop here to iterate over the images. 
         # categories = directory we want to loop within
         # just testing
            print catDict[feature][individual]
            myStim.image=catDict[feature][individual]
            stimClock.reset()
            stimClock.add(stimDur)
            while stimClock.getTime() < 0: # This needs to be double-checked for non-slip timing, but I think we should be ok.
                myStim.draw()
                win.flip()
                keys = event.getKeys()
                if 'escape' in keys:
                    core.quit()
                    win.close()
        
print expClock.getTime()

