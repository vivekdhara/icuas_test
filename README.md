# icuas_test

1. GROUND TRUTH text files are obtained from FBM1.bag from ground_to_text.py

2. ORB txt file is saved from rosservice call rosservice call /orb_slam3/save_traj abbc.txt

3. Having 3(ground truth) + 1 (ORB) txt files. Run Graph.py - with transformations

4. Current txt files are for rgbd, launch, config file I used are in the folder launch
