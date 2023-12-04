# Project Name

Hello and welcome to my project. This README provides instructions on how to set up and run the project.

## Quick Start

1. **Downloading and installing Docker:**
   - For Windows users, download [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/).
   - For Linux users, follow the [Linux installation guide](https://docs.docker.com/desktop/install/linux-install/).
   - For Mac OS users, use the [Mac installation guide](https://docs.docker.com/desktop/install/mac-install/).

2. **Configuring mail:**
   - For security reasons, the `mail_config.cfg` file is not included in the repository. Create your own configuration file using the provided template in `web-files/website/mail_config.txt`.

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

     This command launches the project locally.

## Things to Keep in Mind

### Docker Compose Daemon/Service Issues

Sometimes, the Docker Compose daemon or service may encounter issues and stop running. In most cases, restarting Docker Desktop can resolve the problem. However, if you prefer a manual approach, you can follow these steps:

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
