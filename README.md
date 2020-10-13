# CADET
![image](https://user-images.githubusercontent.com/1433964/95892741-f6905480-0d54-11eb-82cb-140254d844c5.png)

Modern computing platforms are highly-configurable with thousands of interacting configurations. However, configuring these systems is challenging. Erroneous configurations can cause unexpected non-functional faults. This paper proposes CADET (short for Causal Debugging Toolkit) that enables users to identify, explain, and fix the root cause of non-functional faults early and in a principled fashion. CADET builds a causal model by observing the performance of the system under different configurations. Then, it uses casual path extraction followed by counterfactual reasoning over the causal model to: (a) identify the root causes of non-functional faults, (b) estimate the effects of various configurable parameters on the performance objective(s), and (c) prescribe candidate repairs to the relevant configuration options to fix the non-functional fault. We evaluated CADET on 5 highly-configurable systems deployed on 3 NVIDIA Jetson systems-on-chip. We compare CADET with state-of-the-art configuration optimization and ML-based debugging approaches. The experimental results indicate that CADET can find effective repairs for faults in multiple non-functional properties with (at most) 17% more accuracy, 28% higher gain, and 40× speed-up than other ML-based performance debugging methods. Compared to multi-objective optimization approaches, CADET can find fixes (at most) 9× faster with comparable or better performance gain. Our case study of non-functional faults reported in NVIDIA's forum show that CADET can find 14× better repairs than the experts' advice in less than 30 minutes.

## Contacts
|Name|Email|     
|---|---|      
|Shahriar Iqbal|miqbal@email.sc.edu|      
|Rahul Krishna|i.m.ralk@gmail.com|
|Pooyan Jamshidi|pjamshid@cse.sc.edu|

## License
CADET is released under the under terms of the [MIT License](LICENSE).

This paper proposes CAUPER(short for Causal Performance Debugging) that enables users toidentify, explain, and 
fix the root cause of non-functional faults early and in a principled fashion. CAUPER builds a causal model by 
observing the performance of the system under different configurations. Then, it uses casual path extraction 
followed by counterfactual reasoning over the causal model to:  (a) identify the root causes of non-functional faults, 
(b) estimate the effects of various configurable parameters on the performance objective(s), and (c) prescribe candidate 
repairs to the relevant configuration options to fix the non-functional fault. 
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

## Tutorial

### NVidia TK1, TX1, TX2 and Xavier AGX
**Un-boxing and Bringing up the Desktop GUI:**

Once you open the Jetson TX1/TX2 box please perform the following steps to load the GUI.  
1. Connect a monitor with Jetson TX1/TX2 using a HDMI cable.
2. Use the USB 3.0 ports on Jetson TX1/TX2 board to connect your keyboard/mouse/pointing devices.
3. Use an ethernet cable to connect Jetson TX1/TX2 to the network.
4. Power on the Jetson TX1/TX2 board using the supplied AC Adapter and press the Power button. 

This will bring up a command terminal and prompt for password.  
     Password for user nvidia: nvidia  
     Password for user ubuntu: ubuntu 

Then execute the following commands on you terminal.

1. cd NVIDIA-INSTALLER

2. sudo ./installer.sh
This will install some dependencies to load GUI and once finished will ask the system to reboot.
Use: 

3. sudo reboot   
Now you will have a desktop gui which will make your navigation easier. 

**Jetpack 3.3 Installation:**

Currently all the Jetson TX1/TX2 are using Jetpack 3.3. In order to configure Jetson TX1/TX2 you will need a host os and Jetson TX1/TX2. The installations are performed remotely from the host os because configuring own system dynamically cannot be performed on embedded architectures. 

Please make sure the host os is connected to the same network as the Jetson TX1/TX2.    

The instructions for flashing os and installing necessary software are listed below. 
1. Download Jetpack 3.3 Installer from https://developer.nvidia.com/embedded/downloads#?search=jetpack%203.3 (You might need to create your own nvidia developer account to download the binary)

2. Extract the installer and copy it to a new directory using
     
       mkdir TX1/TX2 (whichever you are using)   
       cp JetPack-L4T-3.3-linux-x64_b39.run ~/TX1 (or TX2)  

3. Change the permission to make it executable.  
     
       chmod +x JetPack-L4T-3.3-linux-x64_b39.run ~/TX1 (or TX2)  

4. Install ssh-askpass. This is very important as once the flashing is done the jetpack will ask you for remote system (Jetson TX1/TX2) ip, username and password. Without this step it will get stuck and will not get installed correctly.  
     
       sudo apt-get install ssh-askpass-gnome ssh-askpass  

5. Run the installer  
     
       ./JetPack-L4T-3.3-linux-x64_b39.run (Do not use sudo)  

This would start installing Jetpack on your host and will show the progress using a Nvidia Component Manager. 
In the component manager select Full (Flash OS and other necessary software e.g. cuda, cudnn, opencv, tensorRT etc.) installation and select to resolve all dependencies in the component manager gui. It will also prompt you to accept all the software license agreements and make sure you accept them (unless you have discovered patches to choose rebellion). 

Once the jetpack installation is completed on your host os it will show you some additional steps to perform as it requires the Jetson TX1/TX2 to run on force recovery mode. Please perform the following steps to do that. 

1. Disconnect the ac adapter from Jetson TX1/TX2.
2. Connect the developer cable between Jetson and Host machine.
3. Power on your Jetson TX1/TX2 using the power button after connecting the power cable.
4. Keep pressing the Force Recovery Button and while pressing it press and release the reset button.
5. Please wait for 2 seconds after releasing the reset button and then release the force recovery button.

In order to confirm that the jetson is ready to be flashed using the force recovery mode open a terminal in your host os and use  
     
     lsusb   

You should see a list of usbs and one of them should be NVIDIA-CORP which will indicate the Jetson is ready to be configured. Then press the enter button on the terminal from which the force recovery mode was initiated on your host os. 
This would start flashing os and install jetpack 3.3. It would create filesystems on your jetson tx1/tx2. 

Currently, there is an issue with Jetpack 3.3 which is it only flashes the os but does not install all the necessary software. In order to do so, you have to run the Jetpack run file again and this time make sure rather than selecting the full installation you select custom and right click on the target system ans select install. Before, doing so make sure you unplug the developer cable. This would ask you for the jetson tx1/tx2 ip, username and password. In order to get the ip from Jetson TX1/Tx2 use:  
     
     ifconfig   
Use the following command to make sure your Jetson TX1/TX2 is reachable from your host.   
     
     ping jetson_ip_address   
This time it will install all the necessary software. Once the softwares are installed now you may be interested in using tensorflow/caffe/pytorch etc.

Use the following  
     
     sudo apt-get install python-setuptools (for python 2.7)  
     sudo apt-get install python-pip    

**Tensorflow Installation:**

For Tensorflow:   
     
     sudo pip install     extra-index-url https://developer.download.nvidia.com/compute/redist/jp33 tensorflow-gpu

You should be able to open a python interpreter to ensure tensorflow is running. 

**Tensorflow & Keras install for jetson Xavier & Nano devices**

     sudo apt-get install python3-venv

     python3 -m venv your_env

     source your_env/bin/activate

     pip3 install Cython pandas

     sudo apt-get install libhdf5-serial-dev libhdf5-dev

     sudo apt-get install libblas3 liblapack3 liblapack-dev libblas-dev

     sudo apt-get install gfortran

     wget https://developer.download.nvidia.com/compute/redist/jp/v42/tensorflow-gpu/tensorflow_gpu-1.13.1+nv19.3-cp36-cp36m-linux_aarch64.whl

     pip3 install tensorflow_gpu-1.13.1+nv19.3-cp36-cp36m-linux_aarch64.whl

     pip3 install keras




## Run Instructions
To run experiments on NVIDIA Jetson TX1 or TX2 Xavier devices please use the 
following command to launch a flask on localhost:
```python
command: python src/utils/run_service.py softwaresystem
```
For example to initialize a flask app with image recogntion softwrae system please use:
```python
command: python src/utils/run_service.py Image
```

Once the flask app is running and modelserver is ready then please use the following command
to collect performance measurments for different configurations: 
```python
command: python src/utils/run_params.py softwaresystem
```

To run causal models for a single-objective bug please run the following:
```python
command: python Runcausal_model.py  -o objective1 -d datafile -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software 
system in TX1 with initial datafile irtx1.csv use the following for a latency (single objective) bug : 
```python
command: python Runcausal_model.py  -o inference_time -d irtx1.csv -s Image -k TX1
```

To run causal models for a multi-objective bug please run the following:
```python
command: python Runcausal_model.py  -o objective1 -o objective2 -d datafile -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software 
system in TX1 with initial datafile irtx1.csv use the following for a latency and energy consumption (multi-ojective) bug : 
```python
command: python Runcausal_model.py  -o inference_time -o total_energy_consumption -d irtx1.csv -s Image -k TX1
```
