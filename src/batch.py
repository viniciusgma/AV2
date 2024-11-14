import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import csv
from mesa.batchrunner import batch_run
from src.model import ForestFire

"""Batch run a mesa model with a set of parameter values.

    Args:
        model_cls (Type[Model]): The model class to batch-run
        parameters (Mapping[str, Union[Any, Iterable[Any]]]): Dictionary with model parameters over which to run the model. You can either pass single values or iterables.
        number_processes (int, optional): Number of processes used, by default 1. Set this to None if you want to use all CPUs.
        iterations (int, optional): Number of iterations for each parameter combination, by default 1
        data_collection_period (int, optional): Number of steps after which data gets collected, by default -1 (end of episode)
        max_steps (int, optional): Maximum number of model steps after which the model halts, by default 1000
        display_progress (bool, optional): Display batch run process, by default True

    Returns:
        List[Dict[str, Any]]

    Notes:
        batch_run assumes the model has a `datacollector` attribute that has a DataCollector object initialized.

    To take advantage of parallel execution of experiments, `batch_run` uses
    multiprocessing if ``number_processes`` is larger than 1. It is strongly advised
    to only run in parallel using a normal python file (so don't try to do it in a
    jupyter notebook). Moreover, best practice when using multiprocessing is to
    put the code inside an ``if __name__ == '__main__':`` code black as shown below::

    from mesa.batchrunner import batch_run

    params = {"width": 10, "height": 10, "N": range(10, 500, 10)}

    if __name__ == '__main__':
        results = batch_run(
            MoneyModel,
            parameters=params,
            iterations=5,
            max_steps=100,
            number_processes=None,
            data_collection_period=1,
            display_progress=True,
        )

        
"""

params = {
    "height": 100,
    "width": 100,
    "tree_density": 0.9,
    "how_many_rivers": 2,
    "fire_focus": 3,
    "cloud_quantity": 3,
    "lightning_probability": 0.5,
    "rain_probability": 0.5,
    "fireman_life": 50,
    "fireman_spawn_interval": 10,
    "how_many_initial_fireman": 4,
    "new_fireman_rate": 1,
    "burn_rate": 0.1,
    "fire_propagation_rate": 0.1,
    "tree_life": 20,
}

if __name__ == "__main__":
    results = batch_run(
        ForestFire,
        parameters=params,
        iterations=1,
        max_steps=10,
        number_processes=None,
        data_collection_period=1,
        display_progress=True,
    )

    keys = results[0].keys() if results else []

    with open("data.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
