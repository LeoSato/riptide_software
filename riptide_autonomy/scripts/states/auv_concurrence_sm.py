#!/usr/bin/env python

import rospy
from smach import Concurrence
import smach_ros
from riptide_msgs import Constants
import master_switch_monitor_sm
import mission_control_sm
#import saftey_sm

#Child Termination Callback
#Preempt all other states (do NOT keep running), depending on the scenario (return True)
def child_term_cb(outcome_map):
    #If any cocnurrently running state machine exits, preempt all others
    return True

auv_concurrence = Concurrence(outcomes = ['exit'],
                 default_outcome = 'exit',
                 output_keys=[]
                 outcome_map = {})
auv_concurrence.userdata.master_switch_status = 0
auv_concurrence.userdata.mission_status = 0
auv_concurrence.userdata.safety_status = 0

with auv_concurrence:
    Concurrence.add(MASTER_SWITCH_MONITOR_SM', master_switch_monitor_sm,
                    remapping={'master_switch_status':'master_switch_status'})
    Concurrence.add('MISSION_CONTROL_SM', mission_control_sm,
                    remapping={'mission_status':'mission_status'})
    #Concurrence.add('SAFETY_SM', safety_sm,
    #                remapping={'safety_status':'safety_status'})


auv_concurrence.execute()