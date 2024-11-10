import os
import sys
import numpy as np
import cv2
from util import test_profile

if len(sys.argv) < 2:
    print("Usage: python test_profile.py <profile_name>")
    sys.exit(1)

profile_name = sys.argv[1]
profile = np.load('profiles/'+profile_name+'.npy')

positive = []
negative = []

labels = sorted(os.listdir('screenshots'))
for label in labels:
    images = sorted( os.listdir('screenshots/'+label))
    images = ['screenshots/'+label+'/'+image for image in images]
    if label == profile_name:
        positive += images
    else:
        negative += images

for i in range(len(positive)):
    sys.stdout.write('\r'+str(i+1)+' / '+str(len(positive)))
    sys.stdout.flush()
    path = positive[i]
    image = cv2.imread(path)
    result = test_profile(profile, image)
    if not result:
        print('\nFailed positive matching on: "{}"!'.format(path))
print()

for i in range(len(negative)):
    sys.stdout.write('\r'+str(i+1)+' / '+str(len(negative)))
    sys.stdout.flush()
    path = negative[i]
    image = cv2.imread(path)
    result = test_profile(profile, image)
    if result:
        print('\nFailed negative matching on: "{}"!'.format(path))
print()