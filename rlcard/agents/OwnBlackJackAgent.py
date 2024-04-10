import rlcard
from rlcard.agents import DQNAgent
from rlcard.utils import (
    tournament,
    reorganize,
    Logger,
    plot_curve
)
import matplotlib.pyplot as plt

env = rlcard.make("blackjack")
print("Number of actions: ", env.num_actions)
print("Number of players: ", env.num_players)
print("State shape: ", env.state_shape)
print("Action shape: ", env.action_shape)

agent = DQNAgent(
    num_actions = env.num_actions,
    state_shape = env.state_shape[0],
    mlp_layers = [64, 64]
)

env.set_agents([agent])

with Logger("experiments/leduc_holdem_dqn_result/") as logger:
    for episode in range(1000):

        # Generate data from the environment
        trajectories, payoffs = env.run(is_training=True)

        # Reorganaize the data to be state, action, reward, next_state, done
        trajectories = reorganize(trajectories, payoffs)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate the performance.
        if episode % 50 == 0:
            logger.log_performance(
                env.timestep,
                tournament(
                    env,
                    10000,
                )[0]
            )

    # Get the paths
    csv_path, fig_path = logger.csv_path, logger.fig_path
    plt.plot(csv_path, fig_path)
    plt.show()


