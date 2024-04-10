''' An example of training a reinforcement learning agent on the uno environment in RLCard
'''
import os
import argparse
from datetime import datetime
import torch

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    reorganize,
    Logger,
    plot_curve,
)


def train(args):
    # Check whether gpu is available
    device = get_device()

    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlcard.make(
        args.env,
        config={
            'seed': args.seed,
        }
    )

    # Initialize the agent and use random agents as opponents
    if args.algorithm == 'dqn':
        from rlcard.agents import DQNAgent
        if args.load_checkpoint_path != "":
            agent = DQNAgent.from_checkpoint(checkpoint=torch.load(args.load_checkpoint_path))
        else:
            agent = DQNAgent(
                num_actions=env.num_actions,
                state_shape=env.state_shape[0],
                mlp_layers=[128, 128],
                device=device,
                save_path=args.log_dir,
                save_every=args.save_every
            )

    agents = [agent]
    for _ in range(1, env.num_players):
        agents.append(RandomAgent(num_actions=env.num_actions))
    env.set_agents(agents)

    # Start training
    with Logger(args.log_dir) as logger:
        for episode in range(args.num_episodes):

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            # Here, we assume that DQN always plays the first position
            # and the other players play randomly (if any)
            for ts in trajectories[0]:
                agent.feed(ts)

            # Evaluate the performance. Play with random agents.
            if episode % args.evaluate_every == 0:
                logger.log_performance(
                    episode,
                    tournament(
                        env,
                        args.num_eval_games,
                    )[0]
                )

        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, args.algorithm)

    # Save model
    save_path = os.path.join(args.log_dir, 'model.pth')
    torch.save(agent, save_path)
    print('Model saved in', save_path)


if __name__ == '__main__':

    # Define the base directory where logger data will be stored
    base_dir = 'experiments/no-limit-holdem-aggressive_dqn_results/'

    # Generate a timestamp to create a unique subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the full path including the timestamp
    log_dir = os.path.join(base_dir, timestamp)

    # Ensure the directory exists, create it if it doesn't
    os.makedirs(log_dir, exist_ok=True)

    parser = argparse.ArgumentParser("DQN example in RLCard for no-limit-holdem")
    parser.add_argument(
        '--env',
        type=str,
        default='no-limit-holdem-aggressive',
        choices=[
            'no-limit-holdem-aggressive',
        ],
    )
    parser.add_argument(
        '--algorithm',
        type=str,
        default='dqn',
        choices=[
            'dqn',
        ],
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
    )
    parser.add_argument(
        '--num_episodes',
        type=int,
        default=1000,
    )
    parser.add_argument(
        '--num_eval_games',
        type=int,
        default=100,
    )
    parser.add_argument(
        '--evaluate_every',
        type=int,
        default=10,
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default=log_dir,
    )

    parser.add_argument(
        "--load_checkpoint_path",
        type=str,
        default="",
    )

    parser.add_argument(
        "--save_every",
        type=int,
        default=-1)

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    train(args)