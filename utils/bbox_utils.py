def get_center_of_bbox(bbox):
    """
    Get the center of a bounding box.

    Args:
        bbox (list): A list of four values representing the bounding box in the format [x1, y1, x2, y2].

    Returns:
        tuple: A tuple representing the center coordinates (x_center, y_center).
    """
    x1, y1, x2, y2 = bbox
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return int(x_center), int(y_center)

def get_bbox_width(bbox):
    return bbox[2] - bbox[0]

def measure_distance(p1,p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def measure_xy_distance(p1,p2):
    return p1[0]-p2[0],p1[1]-p2[1]