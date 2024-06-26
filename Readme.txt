# Project Name

Hello and welcome to my project. This README provides instructions on how to set up and run the project.

## Quick Start

1. **Downloading and installing Docker:**
   - For Windows users, download [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/).
   - For Linux users, follow the [Linux installation guide](https://docs.docker.com/desktop/install/linux-install/).
   - For Mac OS users, use the [Mac installation guide](https://docs.docker.com/desktop/install/mac-install/).

2. **Configuring mail:**
   - For security reasons, the `mail_config.cfg` file is not included in the repository. 
   Create your own configuration file using the provided template in `web-files/website/mail_config.txt`.

     ```plaintext
     MAIL_SERVER='smtp.gmail.com'
     MAIL_USERNAME='yourmail@gmail.com'
     MAIL_PASSWORD='yourpassword'
     MAIL_PORT=587  # or 465 if you prefer using SSL instead of TLS
     MAIL_USE_SSL=False
     MAIL_USE_TLS=True
     ```

     - Input your mail configuration.
     - Rename `mail_config.txt` to `mail_config.cfg`.

3. **Launching the project:**
   - For Windows users, launch PowerShell as an administrator. For Linux and Mac users, use Terminal.
   - Ensure Docker Compose is set up correctly by running `docker compose version`.
   - Navigate to the project directory and run:

     ```bash
     docker compose up --build
     ```

     This command Builds and launches the project locally.

   * WARNING: 
     On first build, you might encounter an error right after -- MIGRATION -- , This is caused by database not initialising in given time,
     Keep in mind that this occures only when database is being created in first initialization,
     Hopefully there is an easy way to fix this issue, just wait for database to first initialize, ( for me its about 10 to 15 seconds ) to finish initialising, 
     then stop the process by pressing 'CTRL + c' hotkey and wait for it to fully stop, after that, just relaunch the project using 'docker compose up'
     

   -After First Build You dont have to rebuild it again, Unless you change Root directory files such as: Dockerfile, docker-compose.yml, entrypoint.sh
    
   -For regular docker compose startup run:
    
     ```bash
     docker compose up
     ```
   
4. **PGadmin**
   -For easy database management, there is an pgadmin4 included in the compose.
   *. After successfully launching the project, PGAdmin 4 should be accessible at http://localhost:5050 in your web browser.
    Use the following default login credentials for PGAdmin 4:

      Username: name@example.com
      Password: admin
  
   -For Detailed information on how to Connect PGadmin4 to projects database -
    ( https://docs.bitnami.com/aws/apps/discourse/administration/configure-pgadmin/ )

    credentials are as follows:
      maintanence database - postgres
      host name / address - postgres
      port - 5432
      user name - postgres
      password - postgres
      
    
## Things to Keep in Mind

### Docker Compose Daemon/Service Issues

Sometimes, the Docker Compose daemon or service may encounter issues and stop running. 
In most cases, restarting Docker Desktop can resolve the problem. However, if you prefer a manual approach, you can follow these steps:

1. **Restart Docker Desktop:**
   - Simply restarting Docker Desktop is often the quickest solution. Close the application and reopen it to restart the Docker daemon.

2. **Launch Docker Daemon Manually:**
   - If you prefer to start the Docker daemon manually, you can use the following command:

     ```bash
     docker compose up -d
     ```

     This command launches the Docker Compose services in detached mode.

3. **Check Docker Compose Logs:**
   - You can also check the logs for your Docker Compose services to identify any issues:

     ```bash
     docker compose logs
     ```

### Additional Notes

- Keep an eye on resource usage (CPU, memory) to ensure that your services are not exceeding system limits.

- If you encounter persistent issues with the Docker Compose setup, consider checking [Docker's official documentation](https://docs.docker.com/) or community forums for additional troubleshooting steps.
