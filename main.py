from utils import read_video,save_video
from trackers import Tracker
import cv2

def main():
    # Read Video
    video_frames=read_video('input_video/footballclip.mp4')

    
    

    # Initialize Tracker
    tracker = Tracker('models/best.pt')

    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                        stub_path='stubs/track_stubs.pkl')
    
    # save cropped image of player
    for track_id,player in tracks['players'][0].items():
        bbox=player['bbox']
        frame=video_frames[0]

        # crop bbox from frame
        # bbox = [x1, y1, x2, y2]  rows    = y1 to y2  (height)
        # columns = x1 to x2  (width)

        cropped_image=frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]

        # save the cropped image
        cv2.imwrite(f'output_videos/cropped_img.jpg',cropped_image)
        break

    

    
    # Draw output video
    # Draw object tracks
    output_video_frames=tracker.draw_annotations(video_frames, tracks)

    



    # Save Video
    save_video(output_video_frames,'output_videos/output_video.avi')

if __name__=="__main__":
    main()