
import math
class Reward:
    def __init__(self, verbose=False, track_time=False):
        self.prev_speed = 0.75
    def reward_function(self, params, direction_diff_abs):
        # Give a reward if our current speed is faster than our previous speed.
        if (direction_diff_abs < 3) and (params['speed'] >= self.prev_speed):
            return 1.0
        elif (direction_diff_abs > 3) and (params['speed'] < self.prev_speed):
            return 1.0
        return 0.0

reward_object = Reward()
    
def reward_function(params):

    #
    #Distance from center
    #

    track_width=params['track_width']
    distance_from_center=params['distance_from_center']

    marker_1=0.125*track_width
    # marker_2=0.250*track_width
    # marker_4=0.375*track_width 
    marker_5=0.5*track_width

    if distance_from_center<=marker_1:
        reward_dist_cent = 1
    # elif distance_from_center<=marker_2:
    #     reward_dist_cent = 0.75
    # elif distance_from_center<=marker_4:
    #     reward_dist_cent = 0.5
    elif distance_from_center<=marker_5:
        reward_dist_cent = 0.25
    else:
        reward_dist_cent=1e-3
#############################################################################################
    #
    # direction  w.r.t. 2nd next next closest waypoint, and thus the track direction
    #

    waypoints = params['waypoints']
    closest_waypoints=params['closest_waypoints']
    heading = params['heading']
    length=len(waypoints)
    temp1=closest_waypoints[1]
    temp2=closest_waypoints[0]
    two_points_ahead = waypoints[(temp1+2)%length]
    two_points_prev = waypoints[(temp2-2)%length]

    track_direction = math.atan2(two_points_ahead[1] - two_points_prev[1], two_points_ahead[0]- two_points_prev[0])

    track_direction=math.degrees(track_direction)

    direction_diff_abs = abs(track_direction - heading)

    if direction_diff_abs >180 :
        direction_diff_abs=360-180
    
    DIRECTION_THRESHOLD=8.0

    if direction_diff_abs < DIRECTION_THRESHOLD:
        reward_direc = 1
    elif direction_diff_abs >= DIRECTION_THRESHOLD:
        reward_direc = 0.5
    
###############################################################################################
    #
    # steering_angle
    #
    reward_str_a= 0.5

    steering_angle=params['steering_angle']

    direction_diff=track_direction - heading

    if steering_angle == direction_diff:
        reward_str_a = 1
    elif direction_diff>=0:
        if steering_angle >= direction_diff*1.2:
            reward_str_a = 1e-3
        elif steering_angle <= direction_diff*0.8:
            reward_str_a = 1e-3
    else:
        if steering_angle >= direction_diff*0.8:
            reward_str_a = 1e-3
        elif steering_angle <= direction_diff*1.2:
            reward_str_a = 1e-3

############################################################################################
    #preventing zig-zag
    reward_zig_zag=1

    if direction_diff_abs<steering_angle:
        reward_zig_zag = 1e-3
############################################################################################
    #
    #speed
    #
    reward_speed=reward_object.reward_function(params, direction_diff_abs)

#############################################################################################
    # same reward for going slow with greater steering angle then going fast straight ahead 
    speed=params['speed']
    reward_str2= math.sin(0.4949 * (0.475 * (speed - 1.5241) + 0.5111 * steering_angle ** 2))
       
#############################################################################################
    reward= 0.8*reward_dist_cent + reward_direc + reward_str_a + 0.8*reward_zig_zag + reward_speed +0.7*reward_str2
#############################################################################################
    #
    # progress
    #
    progress=params['progress']
    if progress==100:
        reward +=100
#############################################################################################
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

