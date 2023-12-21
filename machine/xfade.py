from moviepy.editor import VideoFileClip
import subprocess
import time
import os

class Animation:
    def __init__(self,inputVid1, inputVid2):
        self.vid1 = inputVid1
        self.vid2 = inputVid2

    def GetTimeStamp(self, durationVid1, durationVid2):
        # Convert time stamps to seconds
        DurV1 = sum(int(x) * 60 ** i for i, x in enumerate(reversed(durationVid1.split(":"))))
        DurV2 = sum(int(x) * 60 ** i for i, x in enumerate(reversed(durationVid2.split(":"))))
        return DurV1, DurV2

    def GetDuration(self):
        # Get duration of video clips
        Vid1Dur = VideoFileClip(self.vid1).duration
        Vid2Dur = VideoFileClip(self.vid2).duration
        return Vid2Dur

    def GetAnimationList(self):
        # Return a list of available animation transitions
        transitions = [
            "circlecrop", "distance", "fade", "fadeblack", "fadewhite", "radial",
            "rectcrop", "slidedown", "slideleft", "slideright", "smoothup", "slideup",
            "wipedown", "wipeleft", "wiperight", "wipeup", "smoothleft", "smoothright",
            "smoothdown", "circleclose", "circleopen", "horzclose", "horzopen",
            "vertclose", "vertopen", "diagbl", "diagbr", "diagtl", "diagtr", "dissolve",
            "pixelize", "hlslice", "hrslice", "vdslice", "vuslice", "wipebl", "wipebr",
            "wipetl", "wipetr", "fadegrays", "hblur", "squezeh", "squeezev", "zoomin",
            "hlwind", "hrwind", "vuwind", "vdwind", "coverleft", "coverright", "coverup",
            "coverdown", "revealleft", "revealright", "revealup", "revealdown"
        ]
        return transitions

class AnimationActions:
    def __init__(self, output, vidInput1, vidInput2, animTrans, animDuration):
        self.outputs = output
        self.vidInput1 = vidInput1
        self.vidInput2 = vidInput2
        self.animfx = animTrans
        self.animDurations = animDuration
        self.Animations = Animation(vidInput1, vidInput2)

    def exceCommand(self, command):
        # Execute the given command using subprocess
        process = subprocess.Popen(command)
        process.wait()  # Wait for the process to finish
        time.sleep(1)  # Add a delay before terminating
        process.terminate()

    def GetResolution(self, video_path):
        # Get the resolution of the video
        vidpath = video_path.split("\\")[-1]
        resolution_command = f'ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0:s=x "{video_path}"'
        result = subprocess.run(resolution_command, capture_output=True, text=True, shell=True)
        print(result)
        width, height = result.stdout.strip().split('x')
        return int(width), int(height)

    def GetActions(self, tsVid1, tsVid2):
        # Get resolutions for both input videos
        stampVid1, stampVid2 = self.Animations.GetTimeStamp(tsVid1,tsVid2)
        
        width1, height1 = self.GetResolution(self.vidInput1)
        width2, height2 = self.GetResolution(self.vidInput2)
        print("width1: ", width1)
        print("width2: ", width2)
        
        outVideo = os.path.join("OutVid", f"{self.outputs}_{sum(os.path.isfile(os.path.join('OutVid', item)) for item in os.listdir('OutVid'))+1}.mp4")
        # Construct the ffmpeg command
        ffmpeg_command = [
            'ffmpeg',
            '-i', self.vidInput1,
            '-i', self.vidInput2,
            '-filter_complex', f'[0:v]trim=0:{stampVid1},fps=30,settb=1/12800,scale={width1}:{height1}[main_scaled];[1:v]trim={stampVid2}:{self.Animations.GetDuration()},fps=30,settb=1/12800,scale={width2}:{height2}[second_scaled];[main_scaled][second_scaled]xfade=transition={self.animfx}:duration=1:offset={stampVid1 - 1},format=yuv420p[v];[0:a]atrim=0:{stampVid1},afade=t=out:st={stampVid1 - 1}:d=1[a1];[1:a]atrim={stampVid2}:{self.Animations.GetDuration()},afade=t=in:st=0:d=1[a2];[a1][a2]acrossfade=d=1[aout]',
            '-map', '[v]',
            '-map', '[aout]',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-b:a', '192k',
            outVideo
        ]

        # Execute the ffmpeg command
        self.exceCommand(ffmpeg_command)

