# Paddy Study #3

This repository shares all the python code used to analyze the data of the underlying study. The folder 'paddystudy3' thereby contains all the code used to analyze the date. In the subdirectory 'util' there are two modules that each contain one function. 
'import_vicon_lbi' is used to import and label the kinematic-marker data.
'calculate_wavespeed' processes the raw wave speed data from the two accelerometers and calculates the wave speed.

The 'main'-jupyter notebook utilizes these functions to analyze each individual trial. The results were exported to a spreadsheet which was then the basis for statistics, which were not done in python.

The data is split into kinematic data captured with an OptiTrack motion capture system and all the other data captured via the 1401 A/D acquisition interface. 
Trials are named as following:
- Maximum voluntary contractions: MVC_Angle_TrialNumber
- Fifty percent reference contractions: Fifty_Angle_TrialNumber
- Fixed-end contractions: H_length_TrialNumber (length: short - long - superlong)
- Stretch-hold contractions: SH_length_TrialNumber
- Leg flexion MVC: BF_MVC


The directory 'spike' contains the scripts used to acquire the data.# Bakenecker_et_al_2022
