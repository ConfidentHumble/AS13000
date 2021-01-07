KNOBS = [
    'internal_osd_journal_optimize',
    'osd_adjust_recovery_parameter_interval',
    'osd_admin_cluster_network_shards'
]
KNOB_DETAILS = { 
    'internal_osd_journal_optimize': ['OPT_BOOL', ['false', 'true', 1]],
    'osd_adjust_recovery_parameter_interval': ['OPT_FLOAT', [0.0, 5.0, 0.5]],
    'osd_admin_cluster_network_shards': ['OPT_INT', [1, 10, 3]],
}

def get_init_knobs():
    knobs = {}
    for name, value in KNOB_DETAILS.items():
        knob_value = value[1]
        knobs[name] = knob_value[-1]
    return knobs


def gen_continuous(action):
    knobs = {}
    for idx in range(len(KNOBS)):
        name = KNOBS[idx]
        value = KNOB_DETAILS[name]

        knob_type = value[0]
        knob_value = value[1]
        min_value = knob_value[0]

        if knob_type == 'OPT_INT' or knob_type == 'OPT_LONGLONG' or knob_type == 'OPT_U32' or knob_type == 'OPT_U64':
            max_val = knob_value[1]
            eval_value = int(max_val * action[idx])
            # eval_value is the bigger one between min_value and (max_val * action[idx])
            eval_value = max(eval_value, min_value)
        elif knob_type == 'OPT_FLOAT' or knob_type == 'OPT_DOUBLE':
            max_val = knob_value[1]
            eval_value = max_val * action[idx]
            # eval_value is the bigger one between min_value and (max_val * action[idx])
            eval_value = max(eval_value, min_value)
        elif knob_type == 'OPT_BOOL':
            if action[idx] <= 0.5:
                eval_value = True
            else:
                eval_value = False
        elif knob_type == 'OPT_STR':
            if action[idx] <= 0.5:
                eval_value = 'posix_acl'
            else:
                eval_value = 'none'
        knobs[name] = eval_value
    return knobs


def save_knobs(knob, metrics, knob_file):
    """ Save Knobs and their metrics to files
    Args:
        knob: dict, knob content
        metrics: list, tps and latency
        knob_file: str, file path
    """
    # format: tps, latency, knobstr: [#knobname=value#]
    knob_strs = []
    for kv in knob.items():
        knob_strs.append('{}:{}'.format(kv[0], kv[1]))
    result_str = '{},{},'.format(metrics[0], metrics[1])
    knob_str = "#".join(knob_strs)
    result_str += knob_str
    print("knob_file.{}".format(knob_file))
    with open(knob_file, 'a+') as f:
        f.write(result_str+'\n')

