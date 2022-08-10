import math
def reward_function(params):
    #
    #Distance from center
    #
    reward_dist_cent=1.0

    track_width=params['track_width']
    distance_from_center=params['distance_from_center']

    marker_1=0.1*track_width
    marker_2=0.2*track_width
    marker_4=0.4*track_width 
    marker_5=0.5*track_width

    if distance_from_center<=marker_1:
        reward_dist_cent *= 1.5
    elif distance_from_center<=marker_2:
        reward_dist_cent *= 0.95
    elif distance_from_center<=marker_4:
        reward_dist_cent *= 0.8
    elif distance_from_center<=marker_5:
        reward_dist_cent *= 0.2
    else:
        reward_dist_cent=1e-3

    #
    # direction  w.r.t. 2nd next next closest waypoint, and thus the track direction
    #
    reward_direc=1

    waypoints = params['waypoints']
    closest_waypoints=params['closest_waypoints']
    heading = params['heading']

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]-1]

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0]- prev_point[0])

    track_direction=math.degrees(track_direction)

    direction_diff_abs = abs(track_direction - heading)

    if direction_diff_abs >180 :
        direction_diff_abs=360-180
    
    DIRECTION_THRESHOLD=10.0

    if direction_diff_abs < DIRECTION_THRESHOLD:
        reward_direc = 0.9
    elif direction_diff_abs > DIRECTION_THRESHOLD:
        reward_direc = 0.5
    
    reward= reward_dist_cent + reward_direc 

    #
    #Crash  , reverse , off-track
    #
    is_crashed=params['is_crashed']
    is_offtrack=params['is_offtrack']
    is_reversed=params['is_reversed']

    if (is_crashed ==True) or (is_offtrack==True):
        reward=1e-3
    elif is_reversed==True:
        reward=1e-3
    
    return float(reward)
