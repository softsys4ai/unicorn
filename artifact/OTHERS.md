## Unicorn usage on a different dataset
To run Unicorn on a different dataset you will only need ```/tests/run_unicorn_debug.py``` and ```/tests/run_unicorn_optimization.py```. To perform interventions using the recommended configuration you need to develop your own utilities (similar to ```/services/run_params.py```). Additionally, you need to make some changes in the ```etc/config.yml``` to use the configuration options and their values accordingly. The necessary steps are the following:

### Steps
- Update ```init_dir``` in ```config.yml``` with the directory where initial data is stored.

- Update ```bug_dir``` in ```config.yml``` with the directory where bug data is stored.

- Update ```output_dir``` variable in the ```config.yml``` file where you want to save the output data.

- Update ```hardware_columns``` in the ```config.yml``` with the hardware configuration options you want to use.

- Update ```kernel_columns``` in the ```config.yml``` with the kernel configuration options you want to use.

- Update ```perf_columns``` in the ```config.yml``` with the events you want to track using perf. If you use any other monitoring tool you need to update it accordingly.

- Update ```measurement_colums``` in the ```config.yml``` based on the performance objectives you want to use for bug resolve.

- Update ```is_intervenable``` variables in the ```config.yml``` with the configuration options you want to use and based on your application change their values to True or False. True indicates the configuration options can be intervened upon and vice-versa for False.

- Update the ```option_values``` variables in the ```config.yml``` based on the allowable values your option can take.

- Now, you can run ```run_unicorn_debug.py``` and ```run_unicorn_optimization.py``` with your own specification. Please notice that you also need to update the directories according to your software and hardware name in data directory. If you change the name of the variables in the config file or use a new config file you need to make changes accordingly from in ```run_unicorn_debug.py``` and ```run_unicorn_optimization.py```.
