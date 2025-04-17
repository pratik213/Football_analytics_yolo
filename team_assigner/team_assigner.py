from sklearn.cluster import KMeans


class TeamAssigner:
    def __init__(self):
        pass


    def get_clustering_model(self,image):
        # Reshape image to 2d array
        image_2d=image.reshape(-1,3)

        # perform k-means clustering
        kmeans=KMeans(n_clusters=2,init="k-means++",n_init=1).fit(image_2d)

        return kmeans

    def get_player_color(self,frame,bbox):
        image=frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]
        top_half_image=image[0::int(image.shape[0]/2),:]

        # Get Clustering model
        kmeans=self.get_clustering_model(top_half_image)

        # Get the cluster labels for each pixel in the image
        labels=kmeans.labels_

        # Reshape the labels to the image
        clustered_image=labels.reshape(top_half_image.shape[0],top_half_image.shape[1])

        # Get the player cluster
        corner_cluster=[clustered_image[0,0],clustered_image[0,-1],clustered_image[-1,0],clustered_image[-1,-1]]
        non_player_cluster=max(set(corner_cluster),key=corner_cluster.count)
        player_cluster=1-non_player_cluster


    def assign_team_color(self,frame,player_detections):
        player_colot=[]
        for _,player_detection in player_detections.items():
            bbox=player_detections['bbox']
            player_color=self.get_player_color(frame,bbox)
            player_colot.append(player_color)