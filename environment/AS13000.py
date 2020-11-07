'''
Author: your name
Date: 2020-11-06 17:09:40
LastEditTime: 2020-11-06 21:21:16
LastEditors: your name
Description: In User Settings Edit
FilePath: \environment\AS13000.py
'''
# -*- coding: utf-8 -*-
import gym

class AS13000(gym.Env):
    def __init__(self):
        self.score = 0.0
        self.steps = 0
        self.terminate = False
        self.state = None
    def step(self, knob):
        '''
        description: step function
        param {*} knob
        return {*} reward, next_state, terminate, self.score
        '''        
        self.apply_knobs(knob)
        self.state = self.get_state()
        reward = self.get_reward(self.state)
        terminate = self.terminate()
        return reward, self.state, terminate, self.score

    
    def apply_knobs():
        '''
        description: Apply the knobs to the mysql
        param {*}
        return {*}
        '''        
        