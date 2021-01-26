This project was developed with [Python](https://www.python.org/) (python version 3.8.5) and with Vue to the UI interface.

## Introduction

The goal of this project is to simulate the logic behind building your own Blockchain for cryptocurrency traffic and how different nodes(servers) communicate to send transactions and always have the blockchain updated in the different nodes that are connected.

### How to run the project (Windows)

- The first step is install the tool [Anaconda Navigator](https://www.anaconda.com/products/individual) to create your own virtual enviroment (you can name the enviroment whatever you want) to run the project with the necessary libraries:

![anaconda](https://user-images.githubusercontent.com/11031069/105873108-6de3ae80-5ffb-11eb-82ef-c77d6770ca24.PNG)

- Once you have created your own virtual enviroment you need select in the top-center select input "Not Installed" and search for the following packages (and their dependencies):

- [x] 🔹 pycryptodome
- [x] 🔹 flask/flash-core
- [x] 🔹 requests

- The next step would be to press the play button of the new enviroment and open a new terminal (best option open two terminals to see the communication between nodes/servers )

- Go to the path where you have saved your project in both terminals and in the first terminal run the script `python node.py` and you can open in [http://localhost:5000](http://localhost:5000) to view it in the browser and in the second terminal run the script `python node.py -p=5001` and you can open in [http://localhost:5001](http://localhost:5001) (or the portal number you want )


### How to test the project

- Once the two servers are running and you open a browser to each one, the first step would be press the button 'Create new Wallet' in both interfaces to have a pair of keys (public-private). This will generate two text files, so you don't have to create a new wallet the next time and you only need to press the 'Load Wallet' button (remember create or load a wallet before start Mine Coins): 
![keys](https://user-images.githubusercontent.com/11031069/105875753-78ec0e00-5ffe-11eb-8c42-023628b37c7e.PNG)

- After this, you need go to the Network tab of the browser and add the node/server with which you want to communicate (and have the same blockchain):
![network](https://user-images.githubusercontent.com/11031069/105876001-c9fc0200-5ffe-11eb-9705-ad49acbaba8f.PNG)

**Note: Do the same in the browser of the other server**

- Now is all ready to make transactions and send money to any person(recipient), but first you need press the button 'Mine Coins' to have some funds (10 coins in this case):
![mine](https://user-images.githubusercontent.com/11031069/105876674-7b9b3300-5fff-11eb-9646-08f16beecf6d.PNG)

**Note: This action generate automatically a blockchain text file when storage the blockchain and all the open transactions(these are the transactions realized but they are not part of the blockchain until you press again the Mine Coins button)**

- Once you have funds, you can make a transaction to any person(recipient) that you want (be carefull to have enough funds) and automatically it´s subtracted from your funds:

![transaction](https://user-images.githubusercontent.com/11031069/105877423-43e0bb00-6000-11eb-8b3b-18fc0260b079.PNG)
![funds](https://user-images.githubusercontent.com/11031069/105877553-696dc480-6000-11eb-8325-01348bc94d65.PNG)

**Note: You can show the state of your blockchain and your open transactions at the bottom of the UI)**
![load](https://user-images.githubusercontent.com/11031069/105877836-b05bba00-6000-11eb-9ae8-b894b691bb61.PNG)

- Finally, you may try to make 'Mine Coins' but the length of the blockchain in the 2 servers is different or they have different blocks. In this case you can press the button 'Resolve Conflicts' to update the blockchain with the largest one and the one that it has been verified that no changes have been made fraudulently 

**Note: You will show an error message in the UI when this case occurs**


