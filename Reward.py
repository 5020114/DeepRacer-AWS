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
    marker_3=0.3*track_width
    marker_4=0.4*track_width 
    marker_5=0.5*track_width

    if distance_from_center<=marker_1:
        reward_dist_cent *= 1.5
    elif distance_from_center<=marker_2:
        reward_dist_cent *= 0.95
    elif distance_from_center<=marker_3:
        reward_dist_cent *= 0.85
    elif distance_from_center<=marker_4:
        reward_dist_cent *= 0.75
    elif distance_from_center<=marker_5:
        reward_dist_cent *= 0.2
    else:
        reward_dist_cent=1e-3

    #
    #all wheels on track
    #
    reward_on_track=1

    all_wheels_on_track=params['all_wheels_on_track']

    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward_on_track =1
    else:
        reward_on_track= 0.7
    #
    # direction  w.r.t. 2nd next next closest waypoint, and thus the track direction
    #
    reward_direc=1

    waypoints = params['waypoints']
    closest_waypoints=params['closest_waypoints']
    heading = params['heading']

    next_2nd_point = waypoints[closest_waypoints[1]+1]
    prev_2nd_point = waypoints[closest_waypoints[0]-1]

    track_direction = math.atan2(next_2nd_point[1] - prev_2nd_point[1], next_2nd_point[0]- prev_2nd_point[0])

    track_direction=math.degrees(track_direction)

    direction_diff_abs = abs(track_direction - heading)

    if direction_diff_abs >180 :
        direction_diff_abs=360-180
    
    DIRECTION_THRESHOLD=10.0

    if direction_diff_abs < DIRECTION_THRESHOLD:
        reward_direc = 0.9
    elif direction_diff_abs > DIRECTION_THRESHOLD:
        reward_direc = 0.7





    #
    # steering_angle
    #
    reward_str_a=1

    steering_angle=params['steering_angle']

    direction_diff=track_direction - heading

    if steering_angle == direction_diff:
        reward_str_a = 1
    elif steering_angle >= direction_diff*1.5:
        reward_str_a = 0.7
    elif steering_angle <= direction_diff*0.5:
        reward_str_a = 0.7
    else:
        reward_str_a = 1e-3

    #preventing zig-zag
    reward_zig_zag=1

    if abs(steering_angle)>15:
        reward_zig_zag = 0.8
        

    #
    #preventing collision
    #
    reward_pr_col=1

    objects_location = params['objects_location']
    agent_x = params['x']
    agent_y = params['y']
    next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']

    next_object_loc = objects_location[next_object_index]

    distance_closest_object = math.sqrt((agent_x - next_object_loc[0])**2 + (agent_y - next_object_loc[1])**2)

    # Decide if the agent and the next object is on the same lane
    is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center
    if is_same_lane:
        if 0.5 <= distance_closest_object < 0.8:
            reward_pr_col = 0.75
        elif 0.3 <= distance_closest_object < 0.5:
            reward_pr_col = 0.5
        elif distance_closest_object < 0.3:
            reward_pr_col = 1e-3  # Likely crashed
################################################################
    #
    #speed
    #
    reward_speed=1
    speed=params['speed']

    if direction_diff_abs >DIRECTION_THRESHOLD:
        if speed > prev_speed:
    ##define prev_speed
            reward_speed = 
################################################################
    
    
    reward = reward_dist_cent + reward_on_track + reward_direc + reward_str_a + reward_zig_zag + reward_pr_col + reward_speed
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


