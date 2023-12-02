Hello and welcome to my project.

Short on how to start this project, Extended version will be Provided as well in Documentation.

please don't copy it whole and don't claim as your own.

1. Downloading and installing Docker.
 *.For Windows users it is recommended that you download Docker Desktop - https://docs.docker.com/desktop/install/windows-install/
 *.For Linux Users - https://docs.docker.com/desktop/install/linux-install/
 *.For Mac OS Users - https://docs.docker.com/desktop/install/mac-install/


2. Configuring mail.
 For security purposes i cant upload my mail_config.cfg file on github,
 but you can create your own, This is Google Smtp server example:
    MAIL_SERVER='smtp.gmail.com'
    MAIL_USERNAME='yourmail@gmail.com'
    MAIL_PASSWORD='yourpassword'
    MAIL_PORT=587 / or 465 if you prefer using SSL instead of TLS
    MAIL_USE_SSL=False
    MAIL_USE_TLS=True
 this is basic templating for mail_config.cfg file, it should be located in web-files/website directory, also i created a txt version of it
 for easy steps: 
    step 1: Input Your mail configuration
    step 2: Rename mail_config.txt to mail_config.cfg


3. Launching the project.
 *.For Windows users: Launch Powershell (Recommended launching it as administrator), For Linux and mac users use Terminal
  
   checking if docker compose is set up correctly is essential,
   try running 'docker-compose -v', if output looks something like this -- (docker-compose version x.x.x), docker compose is set up,
   after that you can just navigate to the project directory and run: 'docker compose up --build' command, which will launch the project locally

