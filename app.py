import cv2
from PIL import Image
import imageio
import numpy
import time
    

def error():
        print("\nVerify your inputs.\n")
        exit()

def merge(image1, image2, op):
    background = Image.fromarray(image1).resize(size,Image.LANCZOS).convert("RGBA")
    foreground = Image.fromarray(image2).resize(size,Image.LANCZOS).convert("RGBA")
    # difference = cv2.subtract(image1, image2)
    # b, g, r = cv2.split(difference)
    # if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
    return numpy.array(Image.blend(background, foreground, op).convert(mode))

def createOps(mult):
    if mult <= 0:
        error()
    try:
        ops=[]
        pf=1/mult
        result=0
        while result <= 0.95:
            result+=pf
            ops.append(result)
        return ops
    except:
        error()


targetFile=input("Video Target: ")
fpsMultiply=input("FPS Multiply: ")

try:
    ops=createOps(int(fpsMultiply))
except:
    error()

frames=[]


vidcap = cv2.VideoCapture(targetFile)
fps=vidcap.get(cv2.CAP_PROP_FPS)*(len(ops)+1)
print(f"\nFPS Before: {str(fps/(len(ops)+1))}")
print(f"FPS After: {str(fps)}")
print("\nSpliting Frames..\n")
reader=imageio.get_reader(targetFile, mode="I")
for i, frame in enumerate(reader):
    frames.append(frame)

size=Image.fromarray(frames[0]).size
mode=Image.fromarray(frames[0]).mode

start=time.perf_counter()

with imageio.get_writer("output.mp4", mode="I", fps=int(fps)) as writer:
    print("\nTotal Frames Before:  "+str(len(frames)))
    print("Total Frames After:  "+str(len(frames)*(len(ops)+1))+"\n")
    print(f"\nMode: {mode}\n")
    print(f"\nSize: {str(size)}\n")
    print("\nCompiling the video..\n")
    for index in range(0, len(frames)):
        frame=frames[index]
        writer.append_data(numpy.array(Image.fromarray(frame).convert(mode)))
        for op in ops:
            try:
                writer.append_data(merge(frame, frames[index+1], op))
            except IndexError:
                pass
    writer.close()

end=time.perf_counter()

totalTime=end-start
unit="s"
if totalTime >= 60:
    unit="m"
    totalTime/=60

input(f"\nFinished in {int(totalTime)}{unit}\n")
