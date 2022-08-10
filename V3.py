
import math
class PARAMS:
    prev_speed = None
    prev_abs_steering = None
    prev_steps = None


def reward_function(params):
    ...
    PARAMS.prev_speed = params['speed']


    #
    #Distance from center
    #
    reward_dist_cent=1.0

    track_width=params['track_width']
    distance_from_center=params['distance_from_center']

    marker_1=0.125*track_width
    marker_2=0.250*track_width
    marker_4=0.375*track_width 
    marker_5=0.5*track_width

    if distance_from_center<=marker_1:
        reward_dist_cent = 1
    elif distance_from_center<=marker_2:
        reward_dist_cent = 0.75
    elif distance_from_center<=marker_4:
        reward_dist_cent = 0.5
    elif distance_from_center<=marker_5:
        reward_dist_cent = 0.25
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
    prev_point = waypoints[closest_waypoints[0]]

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0]- prev_point[0])

    track_direction=math.degrees(track_direction)

    direction_diff_abs = abs(track_direction - heading)

    if direction_diff_abs >180 :
        direction_diff_abs=360-180
    
    DIRECTION_THRESHOLD=10.0

    if direction_diff_abs < DIRECTION_THRESHOLD:
        reward_direc = 0.9
    elif direction_diff_abs > DIRECTION_THRESHOLD:
        reward_direc = 0.6
    

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
    #speed
    #
    reward_speed=0.6

    if direction_diff_abs<0.5 and params['speed']>PARAMS.prev_speed*1.2:
        reward_speed=1

    reward= 0.8*reward_dist_cent + reward_direc + reward_str_a + 0.5*reward_zig_zag + reward_speed
    #
    #Crash  , reverse , off-track
    #
    is_crashed=params['is_crashed']
    is_reversed=params['is_reversed']

    if (is_crashed ==True):
        reward=1e-3
    elif is_reversed==True:
        reward=1e-3
    
    return float(reward)

