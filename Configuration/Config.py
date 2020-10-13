sys_id_dict = { "33": "TX1",
                "24": "TX2",
                "67": "Xavier"}
sys_id_file = "/sys/module/tegra_fuse/parameters/tegra_chip_id"
systems = {"TX1":{
              "cpu":{
                  "cores":{
                      "core0":"cpu0",
                      "core1":"cpu1",
                      "core2":"cpu2",
                      "core3":"cpu3"},
                  "frequency":{
                      "available":"/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"}
              },
              "gpu":{
                  "frequency":{
                      "available":"/sys/kernel/debug/clock/gbus/possible_rates",
                      "current":"/sys/kernel/debug/clock/gbus/rate"},
                      "status":"/sys/kernel/debug/clock/gbus/state"
              },
              "emc":{
                  "frequency":{
                      "available":"/sys/kernel/debug/clock/emc/possible_rates",
                      "current":"/sys/kernel/debug/clock/emc/rate"},
                      "status":"/sys/kernel/debug/clock/emc/state"
              },
              "power_state":{},
              "temperature":{},
              "power":{
                  "total":"/sys/devices/platform/7000c400.i2c/i2c-1/1-0040/iio_device/in_power0_input",
                  "gpu":"/sys/devices/platform/7000c400.i2c/i2c-1/1-0040/iio_device/in_power1_input",
                  "cpu":"/sys/devices/platform/7000c400.i2c/i2c-1/1-0040/iio_device/in_power2_input"
              }
                         
          },
           "TX2":{
               "cpu":{
                   "cores":{
                       "core0":"cpu0",
                       "core1":"cpu3",
                       "core2":"cpu4",
                       "core3":"cpu5"},
                   "frequency":{
                       "available":"/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"}
                   },
                   "gpu":{
                       "frequency":{
                           "available":"/sys/devices/17000000.gp10b/devfreq/17000000.gp10b/available_frequencies",
                           "current":"/sys/devices/17000000.gp10b/devfreq/17000000.gp10b/cur_freq"},
                           "status":"/sys/kernel/debug/bpmp/debug/clk/gpu/state"
                   },
                   "emc":{
                       "frequency":{
                           "available":"/sys/kernel/debug/bpmp/debug/emc/possible_rates",
                           "current":"/sys/kernel/debug/clk/emc/clk_rate"},
                           "status":"/sys/kernel/debug/bpmp/debug/clk/emc/state"
                   },
                   "power_state":{},
                   "temperature":{
                       "total":"/sys/devices/virtual/thermal/thermal_zone5/temp",
                       "gpu":"/sys/devices/virtual/thermal/thermal_zone2/temp",
                       "cpu":"/sys/devices/virtual/thermal/thermal_zone1/temp"},
                   "power":{
                       "total":"/sys/bus/i2c/drivers/ina3221x/0-0041/iio:device1/in_power0_input",
                       "gpu":"/sys/bus/i2c/drivers/ina3221x/0-0040/iio:device0/in_power0_input",
                       "cpu":"/sys/bus/i2c/drivers/ina3221x/0-0041/iio:device1/in_power1_input",
                   },        
          },
           "Xavier":{
               "cpu":{
                   "cores":{
                       "core0":"cpu0",
                       "core1":"cpu3",
                       "core2":"cpu4",
                       "core3":"cpu5"},
                   "frequency":{
                       "available":"/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"}
                   },
                   "gpu":{
                       "frequency":{
                           "available":"/sys/devices/17000000.gp10b/devfreq/17000000.gp10b/available_frequencies",
                           "current":"/sys/devices/17000000.gp10b/devfreq/17000000.gp10b/cur_freq"},
                           "status":"/sys/kernel/debug/bpmp/debug/clk/gpu/state"
                   },
                   "emc":{
                       "frequency":{
                           "available":"/sys/kernel/debug/bpmp/debug/emc/possible_rates",
                           "current":"/sys/kernel/debug/clk/emc/clk_rate"},
                           "status":"/sys/kernel/debug/bpmp/debug/clk/emc/state"
                   },
                   "power_state":{},
                   "temperature":{
                       "total":"/sys/devices/virtual/thermal/thermal_zone5/temp",
                       "gpu":"/sys/devices/virtual/thermal/thermal_zone2/temp",
                       "cpu":"/sys/devices/virtual/thermal/thermal_zone1/temp"},
                   "power":{
                       "total":"/sys/bus/i2c/drivers/ina3221x/0-0041/iio:device1/in_power0_input",
                       "gpu":"/sys/bus/i2c/drivers/ina3221x/0-0040/iio:device0/in_power0_input",
                       "cpu":"/sys/bus/i2c/drivers/ina3221x/0-0041/iio:device1/in_power1_input",
                   },        
          }
}
hardware_columns = {"TX2": ["core0_status", "core1_status", "core2_status",
                            "core3_status", "core_freq", "gpu_freq", 
                            "emc_freq", "cache_pressure", "swappiness", 
                            "dirty_bg_ratio", "dirty_ratio", "drop_caches", 
                            "sched_child_runs_first", "sched_rt_runtime", "policy"],
                    "TX1": ["core0_status", "core1_status", "core2_status",
                            "core3_status", "core_freq", "gpu_freq", 
                            "emc_freq", "cache_pressure", "swappiness", 
                            "dirty_bg_ratio", "dirty_ratio", "drop_caches", 
                            "sched_child_runs_first", "sched_rt_runtime", "policy"],
                    "Xavier": ["core0_status", "core1_status", "core2_status",
                            "core3_status", "core_freq", "gpu_freq", 
                            "emc_freq", "cache_pressure", "swappiness", 
                            "dirty_bg_ratio", "dirty_ratio", "drop_caches", 
                            "sched_child_runs_first", "sched_rt_runtime", "policy"]}
software_columns = {"Image": ["memory_growth"],
                    "NLP": ["memory_growth"],
                    "Speech":["memory_growth"],
                    "x264":[],
                    "SQLite":[]}
measurement_columns = ["inference_time", "total_energy_consumption", "gpu_energy_consumption", 
                       "cpu_energy_consumption", "total_temp", "gpu_temp", 
                       "cpu_temp"]  
util_dir = "/Utils/"
output_dir = "/Data/Output/"
config_file = "Params.py"
init_dir = "/Data/Initial/"
bug_dir = "/Data/Bug/"

