
import rlcard
from rlcard.agents import (
    CFRAgent,
    RandomAgent,
)
from rlcard.utils import (
    tournament,
    Logger,
    plot_curve,
)

# Make environment
# steb back environment
env = rlcard.make(
    'leduc-holdem',
            config={
                'allow_step_back':True,
            }
)
# evaluation environment
eval_env = rlcard.make(
    'leduc-holdem',
)
# create agent and save it to the path once trained
agent = CFRAgent(env,
                 "experiments/leduc_holdem_cfr_result/cfr_model",
)

eval_env.set_agents([agent, RandomAgent(num_actions=eval_env.num_actions),
])

# training for 1000 games
with Logger("experiments/leduc_holdem_cfr_result/") as logger:
    for episode in range(1000):
        agent.train()
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

plot_curve(csv_path, fig_path, 'cfr')