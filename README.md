# Encrypted Messenger
The messenger is a secure messaging platform designed to ensure the confidentiality and privacy of your conversations. Built with robust encryption protocols, this messenger prioritizes user privacy while providing a seamless messaging experience.

## Installation
```python
git clone https://github.com/eugenekravchuk/discrete-messenger/
cd frontend
npm install 
npm start
```

# App functionality
## Registration and login
If you have an account, you can login to the messenger<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/5df57f18-9aa0-45df-b57a-75568393c4cb)<br/>

If you don't, go to the register page<br/>
When you go to registration, all four key are generated<br/>
So you have to wait a little bit<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/92583678-0123-43ef-ab09-faf3dfdb2a3f)<br/>

When you filled all the data and pushed sign up button - all the keys appear on local host (You have to add avatar!)<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/a7c414a4-f201-49f6-a8f7-d8640e74ccac)<br/>

## Search
To start a conversation you have to find an account<br/>
For that use a search field:<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/dd7aa34a-0c60-4cb1-ad55-61ea9c05f7b9)<br/>

To begin a conversation, click on a search result and then click on a person<br/>
## Choosing Algorithm
Before writing a message and sending, you can choose an encoding algorithm<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/7b4ddfcc-75be-4a89-b861-b726d81bfa3a)<br/>

Also you can send a photos with text<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/0cadcfc5-87f1-4c85-bbca-e59220676dea)<br/>
## Sending a message
When you choose an algorithm, send a message:<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/2669f1aa-cf2e-4242-9932-17a4eccbb647)<br/>

Beneath every message there is a sign of verification by DSA algorithm and type of algorithm that encoded text:<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/d75cf5be-126a-4ba6-84b6-0616b9d5bddc)<br/>


## Server side
The data on server is entirely encrypted!<br/><br/>
![image](https://github.com/eugenekravchuk/discrete-messenger/assets/81439861/f4503828-5b6d-4cfc-9085-0ab1b966e8c2)<br/>


## Decryption
User decrypts every message individually using a private key in the local storage


# Responcibilities
[Eugene Kravhuk](https://github.com/eugenekravchuk) - Application development<br/>
Sofia Sampara - DSA and ECCDSA development and testing, creating graphs of comperison of algorithms<br/>
Iryna Denysova - implementation and testing of algorithm RSA, presentation<br/>
Ivan Shynkarenko - ElGamal and RCS development and testing<br/>

[Посилання на опис роботи алгоритмів](https://github.com/eugenekravchuk]
https://docs.google.com/document/d/1O1VqhuoDpnuu_mY0HOe9gzrCFR7H3yuTE3aHXMRhStM/edit?usp=sharing


 




