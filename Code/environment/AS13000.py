'''
Author: your name
Date: 2020-12-01 17:10:29
LastEditTime: 2020-12-17 16:43:13
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Code\environment\AS13000.py
'''
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

    def initialize(self):
        """ Initialize the environment when an episode starts
        Returns:
            state: np.array, current state
        """
        self.score = 0.0
        self.last_metrics = []
        self.steps = 0
        self.terminate = False

        flag = self._apply_knobs(self.default_knobs)
        i = 0
        while not flag:
            flag = self._apply_knobs(self.default_knobs)
            i += 1
            if i >= 5:
                print("Initialize: {} times ....".format(i))

        metrics = self.get_state()
        self.last_metrics = metrics
        self.default_metrics = metrics
        state = metrics
        knobs.save_knobs(
            self.default_knobs,
            metrics=metrics,
            knob_file='./tuner/knob_metric.txt'
        )
        return state, metrics

        
    def apply_knobs(self, knob):
        '''
        description: Apply the knobs to the AS13000
        param {*}   knob
        return {*}
        '''        
        f = open("/etc/icfs/icfs.conf", 'w')
        # f = open("./environment/icfs.conf", 'a')
        default_contents = "[global]\nfsid = 2596257f-e7d4-4f01-9e92-096064579b23\npublic_network = 188.188.40.0/24\ncluster_network = 192.168.40.0/24\nmon_initial_members = inspur01, inspur02, inspur03\nmon_host = 188.188.40.211,188.188.40.212,188.188.40.213\nauth_cluster_required = none\nauth_service_required = none\nauth_client_required = none\nosd_pg_cache_flag = 1\nnode_mem_pg_cache_target_gigabytes = 1\nosd_pg_cache_ssd_count = 1\nosd crush update on start = false\n"
        f.write(default_contents)
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
      
      
        delta_0_ReqstdOps_resp = float((metrics[1] - self.default_metrics[1]))/self.default_metrics[1]
        delta_t_ReqstdOps_resp = float((metrics[1] - self.last_metrics[1]))/self.last_metrics[1]
        ReqstdOpa_resp = self._calculate_reward(delta_0_ReqstdOps_resp, delta_t_ReqstdOps_resp)

        reward = 0.4 * ReqstdOpa_rate + 0.6 * ReqstdOpa_resp
        self.score += reward
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
        apply_time = utils.time_start()
        self.apply_knobs(knob)
        apply_time = utils.time_end(restart_time)
        self.state = self.get_state()
        metrics = self.state
        # print("state:{}".format(self.state))
        reward = self.get_reward(self.state)
        # print("reward::{}".format(reward))
        self.last_metrics = self.state
        terminate = self.terminate
        return reward, self.state, terminate, self.score, metrics, apply_time


        