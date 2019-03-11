# docker-flask-react

###1. Overview
###2. Structure
####2.1. Controller
####2.2. Model
####2.3. View
###3. Testing
###4. Production
###====Draft Area=====

Dev Configuration: development.env -> loaded into os.environ by docker-compose.yml -> retreived by config.py into Config class object -> loaded into flask.config by app.config.from_object(config.Config) -> can be accessed by current_app.config['ENV_NAME']  


 
