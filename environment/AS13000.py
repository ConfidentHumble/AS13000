# -*- coding: utf-8 -*-
import gym
import knobs
import os
import sys
import get_state

class AS13000(gym.Env):
    def __init__(self):
        self.score = 0.0
        self.steps = 0
        self.terminate = False
        self.state = []
        self.last_metrics = []
        self.default_metrics = []
        
    def apply_knobs(knob):
        '''
        description: Apply the knobs to the mysql
        param {*}   knob
        return {*}
        '''        
        f = open("/etc/icfs/icfs.conf", 'a')
        for i in range(len(KNOB)):
            name = KNOB[i]
            value = knob[name]
            f.write(name)
            f.write(' = ')
            f.write(value)
            f.write('\n')
        f.close()
        cmd = 'systemctl restart icfs.target'
        os.system(cmd)

    def get_state():
        '''
        description: run vdbench and get the state of system
        param {*}
        return {*} state
        '''
        run_vdbench()
        state = []
        state = read_file()
        return state


    def get_default_metrics():
        '''
        description: run vdbench and get the initial state of system
        param {*}
        return {*} state
        '''
        run_vdbench()
        self.default_metrics = read_file()
        self.last_metrics = self.default_metrics
    def _calculate_reward(delta_0, delta_t):
        '''
            description: calculate the reward
            param {*} delta_0 = S(t) - S(0), delta_t = S(t) - S(t-1)
            return {*} reward
        '''
        if delta_0 > 0:
            _reward = ((1+delta_0)**2-1) * math.fabs(1+delta_t)
        else:
            _reward = -((1-delta_0)**2-1) * math.fabs(1-delta_t)

        if _reward > 0 and delta_t < 0:
            _reward = 0
        return _reward

    def get_reward(self, metrics):
        # ReqstdOps_rate
        delta_0_ReqstdOps_rate = float((metrics[0] - self.default_metrics[0]))/self.default_metrics[0]
        delta_t_ReqstdOps_rate = float((metrics[0] - self.last_metrics[0]))/self.last_metrics[0]
        ReqstdOpa_rate = self._calculate_reward(delta_0_ReqstdOps_rate, delta_t_ReqstdOps)

    def step(self, knob):
        '''
        description: step function
        param {*} self knob
        return {*} reward, next_state, terminate, self.score
        '''        
        self.apply_knobs(knob)
        self.state = self.get_state()
        reward = self.get_reward(self.state)
        self.last_metrics = self.state
        terminate = self.terminate()
        return reward, self.state, terminate, self.score

    
    
   
        