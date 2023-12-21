from machine import xfade
import os 

# Example usage

# File input paths
input_file1 = r"fxFade\InputVid\weldingshorts.mp4"
input_file2 = r"fxFade\InputVid\knifeMaster.mp4"

# Time inputs for cutting each video
time1 = "00:00:10"  # Cut for video 1
time2 = "00:00:15"  # Cut for video 2

# Animation settings
animation = "vuwind"
anim_duration = "1"  # Duration of transition

# Output file path
output = "exampleOutVideo"

tr = xfade.AnimationActions(output=output,vidInput1=input_file1,vidInput2=input_file2,animTrans="circlecrop",animDuration=1)
tr.GetActions(tsVid1=time1,tsVid2=time2)
