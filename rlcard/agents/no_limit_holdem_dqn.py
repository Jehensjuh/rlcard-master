import rlcard
from rlcard.agents import(
    DQNAgent as DQNAgent,
    RandomAgent as RandomAgent,
)
from rlcard.utils import (
    tournament,
    Logger,
    plot_curve, reorganize,
)

# Make environment
# step back environment for training
env = rlcard.make(
    'no-limit-holdem',
    config={
        'allow_step_back': True,
    }
)

# evaluation environment
eval_env = rlcard.make(
    'no-limit-holdem',
)

# create agent and save it to the path once trained
agent = DQNAgent(
    num_actions = env.num_actions,
    state_shape = env.state_shape[0],
    mlp_layers = [64, 64]
)

env.set_agents([agent, RandomAgent(num_actions=eval_env.num_actions)])
eval_env.set_agents([agent, RandomAgent(num_actions=eval_env.num_actions)])

# training for 1000 games
with Logger("experiments/no_limit_holdem_dqn_result/") as logger:
    for episode in range(1000):

        # Generate data from the environment
        trajectories, payoffs = env.run(is_training=True)

        # Reorganaize the data to be state, action, reward, next_state, done
        trajectories = reorganize(trajectories, payoffs)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % 50 == 0:
            logger.log_performance(
                env.timestep,
                tournament(
                    eval_env,
                    1000,
                )[0]
            )

# Get the paths
csv_path, fig_path = logger.csv_path, logger.fig_path

plot_curve(csv_path, fig_path, 'dqn')