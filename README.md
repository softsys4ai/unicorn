# CADET
![image](https://user-images.githubusercontent.com/1433964/95892741-f6905480-0d54-11eb-82cb-140254d844c5.png)

Modern computing platforms are highly-configurable with thousands of interacting configurations. However, configuring these systems is challenging. Erroneous configurations can cause unexpected non-functional faults. This paper proposes CADET (short for Causal Debugging Toolkit) that enables users to identify, explain, and fix the root cause of non-functional faults early and in a principled fashion. CADET builds a causal model by observing the performance of the system under different configurations. Then, it uses casual path extraction followed by counterfactual reasoning over the causal model to: (a) identify the root causes of non-functional faults, (b) estimate the effects of various configurable parameters on the performance objective(s), and (c) prescribe candidate repairs to the relevant configuration options to fix the non-functional fault. We evaluated CADET on 5 highly-configurable systems deployed on 3 NVIDIA Jetson systems-on-chip. We compare CADET with state-of-the-art configuration optimization and ML-based debugging approaches. The experimental results indicate that CADET can find effective repairs for faults in multiple non-functional properties with (at most) 17% more accuracy, 28% higher gain, and 40× speed-up than other ML-based performance debugging methods. Compared to multi-objective optimization approaches, CADET can find fixes (at most) 9× faster with comparable or better performance gain. Our case study of non-functional faults reported in NVIDIA's forum show that CADET can find 14× better repairs than the experts' advice in less than 30 minutes.

## Dependencies
* pandas    
* flask 
* Keras 
* PyTorch 
* Tensorflow
* numpy  
* json  
* causalgraphicalmodels 
* causalnex 
* graphviz 
* py-causal 
* causality  
* python 3.6
## Run Instructions
To run experiments on NVIDIA Jetson TX1 or TX2 Xavier devices please use the 
following command to launch a flask on localhost:
```python
command: python run_service.py softwaresystem
```
For example to initialize a flask app with image recogntion softwrae system please use:
```python
command: python run_service.py Image
```

Once the flask app is running and modelserver is ready then please use the following command
to collect performance measurments for different configurations: 
```python
command: python run_params.py softwaresystem
```

To run causal models for a single-objective bug please run the following:
```python
command: python cadet.py  -o objective1 -d datafile -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software 
system in TX1 with initial datafile irtx1.csv use the following for a latency (single objective) bug : 
```python
command: python cadet.py  -o inference_time -d irtx1.csv -s Image -k TX1
```

To run causal models for a multi-objective bug please run the following:
```python
command: python cadet.py  -o objective1 -o objective2 -d datafile -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software 
system in TX1 with initial datafile irtx1.csv use the following for a latency and energy consumption (multi-ojective) bug : 
```python
command: python cadet.py  -o inference_time -o total_energy_consumption -d irtx1.csv -s Image -k TX1
```
## Contacts
|Name|Email|     
|---------------|------------------|      
|Shahriar Iqbal|miqbal@email.sc.edu|      
|Rahul Krishna|i.m.ralk@gmail.com|


## 📘&nbsp; License
CADET is released under the under terms of the [MIT License](LICENSE).
