# -*- coding: utf-8 -*-
"""
Train the model
"""

import os
import sys
import utils
import pickle
import argparse
#sys.path.append('./')
#sys.path.append('./environment')
#sys.path.append('./models')
sys.path.append('./')		
print(sys.path)
import models
import numpy as np
import environment
# from environment.AS13000 import AS13000


def generate_knob(action):
    return environment.gen_continuous(action)
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--params', type=str, default='', help='Load existing parameters')
    parser.add_argument('--workload', type=str, default='read', help='Workload type [`read`, `write`, `readwrite`]')
    parser.add_argument('--memory', type=str, default='', help='add replay memory')
    parser.add_argument('--noisy', action='store_true', help='use noisy linear layer')
    parser.add_argument('--batch_size', type=int, default=16, help='Training Batch Size')
    parser.add_argument('--epoches', type=int, default=5000000, help='Training Epoches')
    parser.add_argument('--metric_num', type=int, default=2, help='metric nums')
    parser.add_argument('--default_knobs', type=int, default=187, help='default knobs')
    opt = parser.parse_args()

    # Create Environment
    env = environment.AS13000(wk_type=opt.workload)

    # Build models
    ddpg_opt = dict()
    ddpg_opt['tau'] = 0.00001
    ddpg_opt['alr'] = 0.00001
    ddpg_opt['clr'] = 0.00001
    ddpg_opt['model'] = opt.params
    ddpg_opt['gamma'] = 0.9
    ddpg_opt['batch_size'] = opt.batch_size
    ddpg_opt['memory_size'] = 100000

    n_states = opt.metric_num
    num_actions = opt.default_knobs
    model = models.DDPG(
        n_states=n_states,
        n_actions=num_actions,
        opt=ddpg_opt,
        mean_var_path='mean_var.pkl',
        ouprocess=not opt.noisy
    )

    # make new directory
    if not os.path.exists('log'):
        os.mkdir('log')
    if not os.path.exists('save_memory'):
        os.mkdir('save_memory')
    if not os.path.exists('save_knobs'):
        os.mkdir('save_knobs')
    if not os.path.exists('save_state_actions'):
        os.mkdir('save_state_actions')
    if not os.path.exists('model_params'):
        os.mkdir('model_params')

    # set the name of log file
    expr_name = 'train_{}_{}'.format("ddpg", str(utils.get_timestamp()))
    logger = utils.Logger(
        name="ddpg"
        log_file='log/{}.log'.format(expr_name)
    )
    # Replay memory
    if len(opt.memory) > 0:
        model.PrioritizedReplayMemory.load_memory(opt.memory)
        print("Load Memory: {}".format(len(model.PrioritizedReplayMemory)))
    
    # step counter
    step_counter = 0
    # times for train
    train_step = 0
    # time for every step
    step_times = []
    # time for training
    train_step_times = []
    # time for setup, restart, test
    env_step_times = []
    # apply time
    env_apply_times = []
    # choose_action_time
    action_step_times = []

    fine_state_actions = []


    current_knob = environment.get_init_knobs()
    # decay rate
    sigma_decay_rate = 0
   
    accumulate_loss = [0, 0]

    # start to train
    for episode in range(opt.epoches):
        # get the initial state and metrics of environment  record the initial metrics to log file
        current_state, initial_metrics = env.initialize()
        logger.info("\n[Env initialized][Metric rate: {} resp: {}]".format(
            initial_metrics[0], initial_metrics[1]))
        ### TODO How to set the initial sigma
        # model.reset(sigma)
        # t: step counter for current episode
        t = 0
        while True:
            step_time = utils.time_start()
            state = current_state
            if opt.noisy:
                model.sample_noise()
            # select action by models  calculate the time costed  record the value of action to log file
            action_step_time = utils.time_start()
            action = model.choose_action(state)
            action_step_time = utils.time_end(action_step_time)
            logger.info("[ddpg] Action: {}".format(action))
            # change action value to knob value
            current_knob = generate_knob(action)

            # apply knob value to environment  calculate the time costed and append to 'env_apply_time' list    record the infos of step to log file
            env_step_time = utils.time_start()
            reward, state_, done, score, metrics, apply_time = env.step(current_knob)
            env_step_time = utils.time_end(env_step_time)
            logger.info(
                "\n[{}][Episode: {}][Step: {}][Metric rate:{} resp:{}]Reward: {} Score: {} Done: {}".format(
                    "ddpg", episode, t, metrics[0], metrics[1], reward, score, done
                ))
            env_apply_times.append(apply_time)

            # use current step infos to update network and add them to replay_memory
            next_state = state_
            model.add_sample(state, action, reward, next_state, done)

            # record fine state and actions
            if reward > 10:
                fine_state_actions.append((state, action))

            current_state = next_state
            # Update the Actor and Critic with a batch data from replay memory
            train_step_time = 0.0
            if len(model.replay_memory) > opt.batch_size:
                losses = []
                train_step_time = utils.time_start()
                # update two times
                for i in range(2):
                    losses.append(model.update())
                    train_step += 1
                train_step_time = utils.time_end(train_step_time)/2.0

                # accumulate the loss of critic and actor
                accumulate_loss[0] += sum([x[0] for x in losses])
                accumulate_loss[1] += sum([x[1] for x in losses])
                logger.info('[{}][Episode: {}][Step: {}] Critic: {} Actor: {}'.format(
                    "ddpg", episode, t, accumulate_loss[0] / train_step, accumulate_loss[1] / train_step
                ))

            # to here, the total step process finish
            step_time = utils.time_end(step_time)

            # add all the time to the corresponding list
            action_step_times.append(action_step_time)
            env_step_times.append(env_step_time)
            train_step_times.append(train_step_time)
            step_times.append(step_time)

            # record all the time to log file
            logger.info("[{}][Episode: {}][Step: {}] step: {}s env step: {}s train step: {}s restart time: {}s "
                        "action time: {}s"
                        .format("ddpg", episode, t, step_time, env_step_time, train_step_time, apply_time,
                                action_step_time))
            # record all the average time to log file
            logger.info("[{}][Episode: {}][Step: {}][Average] step: {}s env step: {}s train step: {}s "
                        "restart time: {}s action time: {}s"
                        .format("ddpg", episode, t, np.mean(step_time), np.mean(env_step_time),
                                np.mean(train_step_time), np.mean(restart_time), np.mean(action_step_times)))
            # update the step counter of current episode and global episode
            t += 1
            step_counter += 1

            # save replay memory
            if step_counter % 10 == 0:
                model.replay_memory.save('save_memory/{}.pkl'.format(expr_name))
                utils.save_state_actions(fine_state_actions, 'save_state_actions/{}.pkl'.format(expr_name))
                # sigma = origin_sigma*(sigma_decay_rate ** (step_counter/10))

            # save network
            if step_counter % 5 == 0:
                model.save_model('model_params', title='{}_{}'.format(expr_name, step_counter))

            if done or step_counter > 10000:
                break







