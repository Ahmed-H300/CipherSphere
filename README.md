# CipherSphere

The name of the chat app is CipherSphere.
it is chatting app by using socket programming (client and server architecture).
it works as two people want to talk in secure way.
so one of them act as server and establish the port to listen on it.
and the anoter one act as client and connect to it.
and start sending messages between each other encrypted by RSA Algorithm.

## How TO Use

1. You need to have Python installed on your computer. To install it, go to
<https://www.python.org/>
and download it, then follow the installation process.

2. Enter the environment called "cipherenv" that has the libraries needed for the app.
 To activate the environment, run this command while your current directory is the folder of CipherSphere:
```python .\cipherenv\Scripts\activate```
If you are on Linux or Mac, run this command instead:
`source .\cipherenv\Scripts\activate`
The environment is activated if you see "(cipherenv)" at the start of the command line.

3. Run the app by running
```python chat.py```.
The app will open.

Let's assume two users, Alice and Bob. If Alice is the one to create the connection, she will choose 1.
An IP and port will be shown. Bob should know this IP and port.
He will choose 2 and enter the IP, then enter the port of Alice. Both will be connected.

If anyone wants to send a message, they press Enter. `>>` will be shown.
They write the message then press Enter to send it. It will be sent to the other user.

If anyone wants to disconnect, they press Enter. `>>` will be shown.
They write "disconnect" then press Enter to send it. The connection will be terminated for both users.

Have fun using the app!
