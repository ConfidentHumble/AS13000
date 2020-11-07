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
        ReqstdOpa_rate = self._calculate_reward(delta_0_ReqstdOps_rate, delta_t_ReqstdOps_rate)

        delta_0_ReqstdOps_resp = float((metrics[1] - self.default_metrics[1]))/self.default_metrics[1]
        delta_t_ReqstdOps_resp = float((metrics[1] - self.last_metrics[1]))/self.last_metrics[1]
        ReqstdOpa_resp = self._calculate_reward(delta_0_ReqstdOps_resp, delta_t_ReqstdOps_resp)

        delta_0_Pct_read = float((metrics[2] - self.default_metrics[2]))/self.default_metrics[2]
        delta_t_Pct_read = float((metrics[2] - self.last_metrics[2]))/self.last_metrics[2]
        Pct_read = self._calculate_reward(delta_0_Pct_read, delta_t_Pct_read)

        delta_0_IOPS_read_rate = float((metrics[3] - self.default_metrics[3]))/self.default_metrics[3]
        delta_t_IOPS_read_rate = float((metrics[3] - self.last_metrics[3]))/self.last_metrics[3]
        IOPS_read_rate = self._calculate_reward(delta_0_IOPS_read_rate, delta_t_IOPS_read_rate)

        delta_0_IOPS_read_resp = float((metrics[4] - self.default_metrics[4]))/self.default_metrics[4]
        delta_t_IOPS_read_resp = float((metrics[4] - self.last_metrics[4]))/self.last_metrics[4]
        IOPS_read_resp = self._calculate_reward(delta_0_IOPS_read_resp, delta_t_IOPS_read_resp)

        delta_0_IOPS_write_rate = float((metrics[5] - self.default_metrics[5]))/self.default_metrics[5]
        delta_t_IOPS_write_rate = float((metrics[5] - self.last_metrics[5]))/self.last_metrics[5]
        IOPS_write_rate = self._calculate_reward(delta_0_IOPS_write_rate, delta_t_IOPS_write_rate)

        delta_0_IOPS_write_resp = float((metrics[6] - self.default_metrics[6]))/self.default_metrics[6]
        delta_t_IOPS_write_resp = float((metrics[6] - self.last_metrics[6]))/self.last_metrics[6]
        IOPS_write_resp = self._calculate_reward(delta_0_IOPS_write_resp, delta_t_IOPS_write_resp)

        delta_0_MbSec_read = float((metrics[7] - self.default_metrics[7]))/self.default_metrics[7]
        delta_t_MbSec_read = float((metrics[7] - self.last_metrics[7]))/self.last_metrics[7]
        MbSec_read = self._calculate_reward(delta_0_MbSec_read, delta_t_MbSec_read)

        delta_0_MbSec_write = float((metrics[8] - self.default_metrics[8]))/self.default_metrics[8]
        delta_t_MbSec_write = float((metrics[8] - self.last_metrics[8]))/self.last_metrics[8]
        MbSec_write = self._calculate_reward(delta_0_MbSec_write, delta_t_MbSec_write)

        delta_0_MbSec_total = float((metrics[9] - self.default_metrics[9]))/self.default_metrics[9]
        delta_t_MbSec_total = float((metrics[9] - self.last_metrics[9]))/self.last_metrics[9]
        MbSec_total = self._calculate_reward(delta_0_MbSec_total, delta_t_MbSec_total)

        reward = ReqstdOps_rate * 
        + ReqstdOps_resp *
        + Pct_read *
        + IOPS_read_rate *
        + IOPS_read_resp *
        + IOPS_write_rate *
        + IOPS_write_resp *
        + MbSec_read *
        + MbSec_write *
        + MbSec_total *

    def terminate():
        return self.terminate


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

    
    
   
        