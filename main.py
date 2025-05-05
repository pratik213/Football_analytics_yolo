from utils import read_video,save_video
from trackers import Tracker
import cv2
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer


def main():
    # Read Video
    video_frames=read_video('input_video/footballclip.mp4')

    
    

    # Initialize Tracker
    tracker = Tracker('models/best.pt')

    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                        stub_path='stubs/track_stubs.pkl')
    
    # Get object positions
    tracker.add_position_to_tracks(tracks)
    
    # cameraman estimator
    camera_movement_estimator=CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame=camera_movement_estimator.get_camera_movement(video_frames,read_from_stub=True,stub_path='stubs/camera_movement_stub.pkl')
    
    camera_movement_estimator.add_adjust_position_to_tracks(tracks,camera_movement_per_frame)

    # View Transformer
    view_transformer=ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)


    # Interpolate ball position

    tracks['ball']=tracker.interpolate_ball_position(tracks['ball'])
    
    # Assign player to teams
    team_assigner=TeamAssigner()
    team_assigner.assign_team_color(video_frames[0],tracks['players'][0])

    for frame_num,player_track in enumerate(tracks['players']):
        for player_id,track in player_track.items():
            team=team_assigner.get_player_team(video_frames[frame_num],track['bbox'],player_id)
            
            tracks['players'][frame_num][player_id]['team']=team
            tracks['players'][frame_num][player_id]['team_color']=team_assigner.team_colors[team]
    
    # save cropped image of player
    # for track_id,player in tracks['players'][0].items():
    #     bbox=player['bbox']
    #     frame=video_frames[0]

    #     # crop bbox from frame
    #     # bbox = [x1, y1, x2, y2]  rows    = y1 to y2  (height)
    #     # columns = x1 to x2  (width)

    #     cropped_image=frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]

    #     # save the cropped image
    #     cv2.imwrite(f'output_videos/cropped_img.jpg',cropped_image)
    #     break

    
    # Assign ball acquisition
    player_assigner=PlayerBallAssigner()
    for frame_num,player_track in enumerate(tracks['players']):
        ball_bbox=tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track,ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
        
            
    
    # Draw output video
    # Draw object tracks
    output_video_frames=tracker.draw_annotations(video_frames, tracks)

    # Draw camera movement
    output_video_frames=camera_movement_estimator.draw_camera_movement(output_video_frames,camera_movement_per_frame)


    # Save Video
    save_video(output_video_frames,'output_videos/output_video.avi')

if __name__=="__main__":
    main()