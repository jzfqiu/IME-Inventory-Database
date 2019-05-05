# IME-Inventory-Database

## 0. Developer Notes:
Use Robo 3T to do shell operations. 27017 port in container mapped to 20717 in host, use authentication in env file. 



## 1. Overview
TO-DO
## 2. Testing Instruction
 
#### Step 1. Download Requirement
* [git (come with Xcode)](https://developer.apple.com/xcode/)
* [docker](https://www.docker.com/products/docker-desktop)


#### Step 2. Download repository
1. Change working directory to desired download location. (e.g. Mac user downloading into Document folder can run ```cd Documents/```)  
2. Run ```git clone https://github.com/jeff-zqiu/IME-Inventory-Database.git```. 

#### Step 3. Compose and run
1. Make sure docker is installed and running.  
2. Change working directory into the IME-Inventory-Database folder (Run ```cd IME-Inventory-Database/```) 
3. Run ```docker-compose up --build```.  
4. If you see something like this:  
```
web_1    |  * Serving Flask app "web" (lazy loading)
web_1    |  * Environment: development
web_1    |  * Debug mode: on
web_1    |  * Running on http://0.0.0.0:8008/ (Press CTRL+C to quit)
web_1    |  * Restarting with stat
mongo_1  | 2019-04-05T21:45:50.362+0000 I NETWORK  [listener] connection accepted from 172.18.0.3:43702 #150 (1 connection now open)
mongo_1  | 2019-04-05T21:45:50.363+0000 I NETWORK  [conn150] end connection 172.18.0.3:43702 (0 connections now open)
web_1    |  * Debugger is active!
web_1    |  * Debugger PIN: 660-294-431
```
You are good to go.

#### Step 4. Testing
1. Go to http://0.0.0.0:8008/ in your browser
....


## 3. Progress
Backend:
- [x] Add new entries, with any number of fields
- [x] Display existing documents
- [x] Display detailed documents
- [x] Simple, one keyword search
- [x] Edit existing entries
- [x] Delete existing entries
- [ ] Advanced search: partial matching, multiple keywords...
- [ ] Access management: only user with access code can make changes

Frontend:  
TO-DO
