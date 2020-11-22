# -*- coding: utf-8 -*-
import os
import sys
import math
import utils
import knobs
import config 
import get_state
from knobs import KNOBS, KNOB_DETAILS

class AS13000(object):
    def __init__(self, wk_type='read', num_metric = 63, alpha = 1.0, beta1 = 0.5, beta2 = 0.5):
        self.score = 0.0
        self.steps = 0
        self.terminate = False
        self.state = []
        self.last_metrics = None
        self.default_metrics = None
        
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.num_metric = num_metric

        
    def apply_knobs(self, knob):
        '''
        description: Apply the knobs to the AS13000
        param {*}   knob
        return {*}
        '''        
        # f = open("/etc/icfs/icfs.conf", 'a')
        f = open("./environment/icfs.conf", 'a')
        for i in range(len(KNOBS)):
            name = KNOBS[i]
            value = knob[name]
            f.write(name)
            f.write(' = ')
            f.write(str(value))
            f.write('\n')
        f.close()
        cmd = 'systemctl restart icfs.target'
        os.system(cmd)

    def get_state(self):
        '''
        description: run vdbench and get the state of system
        param {*}
        return {*} state
        '''
        get_state.run_vdbench()
        state = []
        state = get_state.read_file()
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
    def _calculate_reward(self, delta_0, delta_t):
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
        # print("metrics[0]:{}, default_metrics[0]:{}, rate_0:{}, rate_t:{}, rate:{}".format(metrics[0], self.default_metrics[0], delta_0_ReqstdOps_rate,delta_t_ReqstdOps_rate, ReqstdOpa_rate))
        # ReqstdOps_resp
        delta_0_ReqstdOps_resp = float((metrics[1] - self.default_metrics[1]))/self.default_metrics[1]
        delta_t_ReqstdOps_resp = float((metrics[1] - self.last_metrics[1]))/self.last_metrics[1]
        ReqstdOpa_resp = self._calculate_reward(delta_0_ReqstdOps_resp, delta_t_ReqstdOps_resp)
        # Pct_read
        # delta_0_Pct_read = float((metrics[2] - self.default_metrics[2]))/self.default_metrics[2]
        # delta_t_Pct_read = float((metrics[2] - self.last_metrics[2]))/self.last_metrics[2]
        # Pct_read = self._calculate_reward(delta_0_Pct_read, delta_t_Pct_read)
        # # IOPS_read_rate
        # delta_0_IOPS_read_rate = float((metrics[3] - self.default_metrics[3]))/self.default_metrics[3]
        # delta_t_IOPS_read_rate = float((metrics[3] - self.last_metrics[3]))/self.last_metrics[3]
        # IOPS_read_rate = self._calculate_reward(delta_0_IOPS_read_rate, delta_t_IOPS_read_rate)
        # # IOPS_read_resp
        # delta_0_IOPS_read_resp = float((metrics[4] - self.default_metrics[4]))/self.default_metrics[4]
        # delta_t_IOPS_read_resp = float((metrics[4] - self.last_metrics[4]))/self.last_metrics[4]
        # IOPS_read_resp = self._calculate_reward(delta_0_IOPS_read_resp, delta_t_IOPS_read_resp)
        # # IOPS_write_rate
        # delta_0_IOPS_write_rate = float((metrics[5] - self.default_metrics[5]))/self.default_metrics[5]
        # delta_t_IOPS_write_rate = float((metrics[5] - self.last_metrics[5]))/self.last_metrics[5]
        # IOPS_write_rate = self._calculate_reward(delta_0_IOPS_write_rate, delta_t_IOPS_write_rate)
        # # IOPS_write_resp
        # delta_0_IOPS_write_resp = float((metrics[6] - self.default_metrics[6]))/self.default_metrics[6]
        # delta_t_IOPS_write_resp = float((metrics[6] - self.last_metrics[6]))/self.last_metrics[6]
        # IOPS_write_resp = self._calculate_reward(delta_0_IOPS_write_resp, delta_t_IOPS_write_resp)
        # # MbSec_read
        # delta_0_MbSec_read = float((metrics[7] - self.default_metrics[7]))/self.default_metrics[7]
        # delta_t_MbSec_read = float((metrics[7] - self.last_metrics[7]))/self.last_metrics[7]
        # MbSec_read = self._calculate_reward(delta_0_MbSec_read, delta_t_MbSec_read)
        # # MbSec_write
        # delta_0_MbSec_write = float((metrics[8] - self.default_metrics[8]))/self.default_metrics[8]
        # delta_t_MbSec_write = float((metrics[8] - self.last_metrics[8]))/self.last_metrics[8]
        # MbSec_write = self._calculate_reward(delta_0_MbSec_write, delta_t_MbSec_write)

        reward = 0.4 * ReqstdOpa_rate + 0.6 * ReqstdOpa_resp
        # print("reward:::{}".format(reward))
        # + IOPS_read_rate *
        # + IOPS_read_resp *
        # + IOPS_write_rate *
        # + IOPS_write_resp *
        return reward
        
    def terminate():
        if self.terminate:
            return True
        else:
            return False


    def step(self, knob):
        '''
        description: step function
        param {*} self knob
        return {*} reward, next_state, terminate, self.score
        '''
        restart_time = utils.time_start()
        self.apply_knobs(knob)
        restart_time = utils.time_end(restart_time)
        self.state = self.get_state()
        metrics = self.state
        # print("state:{}".format(self.state))
        reward = self.get_reward(self.state)
        # print("reward::{}".format(reward))
        self.last_metrics = self.state
        terminate = self.terminate
        return reward, self.state, terminate, self.score, metrics, restart_time


        