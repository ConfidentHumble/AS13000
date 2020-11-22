import os
import sys
import utils
import knobs
import config 
import get_state
from AS13000 import AS13000

class Server(AS13000):
    """ Build an environment directly on Server
    """

    def __init__(self, wk_type, instance_name):
        AS13000.__init__(self, wk_type)
        self.wk_type = wk_type
        self.score = 0.0
        self.steps = 0
        self.terminate = False
        self.last_metrics = None
        self.instance_name = instance_name
        self.db_info = config.instance_config[instance_name]
        self.server_ip = self.db_info['host']
        self.alpha = 1.0
        # knobs.init_knobs(instance_name, num_more_knobs=0)
        self.default_knobs = knobs.get_init_knobs()

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

    def _apply_knobs(self, knob):
        '''
        description: Apply the knobs to the AS13000
        param {*}   knob
        return {*}
        '''        
        # f = open("/etc/icfs/icfs.conf", 'a')
        f = open("icfs.conf", 'a')
        for i in range(len(knobs.KNOBS)):
            name = knobs.KNOBS[i]
            value = knob[name]
            f.write(name)
            f.write(' = ')
            f.write(str(value))
            f.write('\n')
        f.close()
        cmd = 'systemctl restart icfs.target'
        os.system(cmd)
        ### TODO: design the approach for restart failure
        return True

   