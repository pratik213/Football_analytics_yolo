from utils import read_video,save_video
from trackers import tracker

def main():
    # Read Video
    video_frames=read_video('input_video/footballclip.mp4')

    # Save Video
    save_video(video_frames,'output_videos/output_video.avi')

if __name__=="__main__":
    main()