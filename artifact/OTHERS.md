## Unicorn usage on a different dataset
To run Unicorn on your a different dataset you will only need ```unicorn_debugging.py``` and ```unicorn_optimization.py```. In the online mode, to perform interventions using the recommended configuration you need to develop your own utilities (similar to ```run_params.py```). Additionally, you need to make some changes in the ```etc/config.yml``` to use the configuration options and their values accordingly. The necessary steps are the following:

**Step 1**: Update ```init_dir``` in ```config.yml``` with the directory where initial data is stored.

**Step 2**: Update ```bug_dir``` in ```config.yml``` with the directory where bug data is stored.

**Step 3**: Update ```output_dir``` variable in the ```config.yml``` file where you want to save the output data.

**Step 4**: Update ```hardware_columns``` in the ```config.yml``` with the hardware configuration options you want to use.

**Step 5**: Update ```kernel_columns``` in the ```config.yml``` with the kernel configuration options you want to use.

**Step 6**: Update ```perf_columns``` in the ```config.yml``` with the events you want to track using perf. If you use any other monitoring tool you need to update it accordingly.

**Step 7**: Update ```measurement_colums``` in the ```config.yml``` based on the performance objectives you want to use for bug resolve.

**Step 8**: Update ```is_intervenable``` variables in the ```config.yml``` with the configuration options you want to use and based on your application change their values to True or False. True indicates the configuration options can be intervened upon and vice-versa for False.

**Step 9**: Update the ```option_values``` variables in the ```config.yml``` based on the allowable values your option can take.

At this stage you can run ```unicorn_debugging.py``` and ```unicorn_optimization.py``` with your own specification. Please notice that you also need to update the directories according to your software and hardware name in data directory. If you change the name of the variables in the config file or use a new config fille you need to make changes accordingly from in ```unicorn_debugging.py``` and ```unicorn_optimization.py```.
