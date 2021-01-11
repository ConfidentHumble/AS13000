# -*- coding: utf-8 -*-
import os
import sys
import math
import utils
import knobs
import config 
import getMetrics
from knobs import KNOBS, KNOB_DETAILS

class AS13000(object):
    def __init__(self, wk_type='read', num_metric = 63, alpha = 1.0, beta1 = 0.5, beta2 = 0.5):
        self.score = 0.0
        self.steps = 0
        self.state = []
        self.last_metrics = None
        self.default_metrics = None
        
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.num_metric = num_metric
        self.default_knobs = knobs.get_init_knobs()

    def initialize(self):
        """ Initialize the environment when an episode starts
        Returns:
            state: np.array, current state
        """
        self.score = 0.0
        self.last_metrics = []
        self.steps = 0

        self.apply_knobs(self.default_knobs)

        metrics = self.get_metrics()
        self.last_metrics = metrics
        self.default_metrics = metrics
        # TODO：state need to be changed
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
        cmd = "icfs tell osd.* injectargs"
        for i in range(len(KNOBS)):
            name = KNOBS[i]
            value = knob[name]
            cmd_apply = cmd + "  " + "--" + str(name) + "  " + str(value)
            os.system(cmd_apply)


    def get_metrics(self):
        '''
        description: run vdbench and get the state of system
        param {*}
        return {*} state
        '''
        getMetrics.run_vdbench()
        metrics = getMetrics.read_file()
        return metrics


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
        if reward > 100 or reward < 100:
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

        # TODO: state need to change
        state = self.get_metrics()
        metrics = self.get_metrics()
        reward = self.get_reward(metrics)
        next_state = state
        terminate = self.terminate()
        return reward, next_state, terminate, self.score, metrics, apply_time


        