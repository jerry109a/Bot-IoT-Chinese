# Analysis and Classification of Attacks using Realistic Botnet Dataset in Internet of Things


## About the project
With IoT systems taking up a vital place in most of the sectors of IT Technology, it has become a conspicuous target for people with malicious intent. Taking into consideration such vulnerabilities and challenges in use of such systems, a need arises for development of effective protective measures such as intrusion detection systems, network forensic systems, etc. An efficient way to deal with such challenges is to use security systems based on Machine Learning. 

The project aims to analyse different types of attacks using the Bot-IoT dataset and also apply & compare different classification algorithms. In the project, machine learning algorithms are applied and tested using ten best features from the dataset. Based on the paper **“Towards the development of realistic botnet dataset in the Internet of Things for network forensic analytics: Bot-IoT dataset”** containing dataset description, the ten best features were extracted from the main data.

## Dataset
Bot IoT dataset was generated with the help of Ostinato Tool. Ostinato tool is used to generate realistic data with the help of a cloud server consisting of Virtual Machines and Kali machines. In the Kali machines, DNS, SSH, FTP, HTTP and various other services were deployed. Node red tool was used for the simulation of IoT devices and MQTT protocol was used for communication between IoT devices.

Five IoT scenarios were implemented in cloud server to collect the dataset:
  - A weather station
  - A smart fridge
  - Motion activated lights
  - A remotely activated garbage door
  - A smart thermostat

## 新增的一些說明
1. 資料集合請到[這裡]()去下載，並且專案創立一個Dataset Folder去放下載下的csv檔案，整體架構應該會像是:

``` 
project/
│
├── Dataset/
│   ├── XXX_1.csv
│   └── XXX_2.csv
├── Project Bot-IoT.py
├── prepare_top10_split.py
└── .gitignore
```

2. 接著先跑prepare_top10_split.py完成，架構會變成:

```
project/
│
├── Dataset/
│   ├── XXX_1.csv
│   └── XXX_2.csv
├── Dataset_for_train_and_test/
│   ├── train.csv
│   └── test.csv
├── Project Bot-IoT.py
├── prepare_top10_split.py
└── .gitignore
```

3. 再開始跑`Project Bot-IoT.py`