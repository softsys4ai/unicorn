## Debugging baselines
Unicorn supports four debugging baselines such as CBI, Delta Debugging, Encore and BugDoc. To run the baselines use the following commands:
```
python run_baseline_debug.py  -o objective -s softwaresystem -k hardwaresystem -m mode -b baseline
```
#### Example
To run single-objective ```latency``` debugging for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using CBI please use the following command:
```
python run_baseline_debug  -o inference_time -s Image -k TX2 -m offline -b c
```
To run single-objective ```latency``` debugging for ```Deespspeech``` in ```JETSON TX2``` in the ```offline``` mode using delta debugging please use the following command:
```
python run_baseline_debug  -o inference_time -s Speech -k TX2 -m offline -b dd
```
To run single-objective ```energy``` debugging for ```Deesptream``` in ```JETSON Xavier``` in the ```offline``` mode using encore please use the following command:
```
python run_baseline_debug  -o total_energy_consumption -s Deepstream -k Xavier -m offline -b encore
```
To run single-objective ```energy``` debugging for ```x264``` in ```JETSON Xavier``` in the ```offline``` mode using bugdoc please use the following command:
```
python run_baseline_debug  -o total_energy_consumption -s x264 -k Xavier -m offline -b bugdoc
```
## Optimization baselines
Unicorn supports two optimization baselines: SMAC and PESMO. SMAC is used for single-objective optimization while PESMO is used for multi-objective optimization. To run the baselines use the following commands:
```
python run_baseline_optimization.py  -o objective -s softwaresystem -k hardwaresystem -m mode -b baseline
```
#### Example
To run single-objective ```latency``` optimization for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using SMAC please use the following command:
```
python run_baseline_optimization  -o inference_time -s Image -k TX2 -m offline -b smac
```
To run multi-objective optimizaiton for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using PESMO please use the following command:
```
python run_baseline_optimization  -o inference_time -o total_energy_consumption -s Image -k TX2 -m offline -b pesmo
```



