
# AigilityAI EDA Application

This README provides instructions on how to run the AigilityAI EDA application using Docker and directly from the source code.

## Running with Docker

You can easily run the application using the Docker image.

### Prerequisites

- Docker installed on your system

### Steps

1. Pull the Docker image:
   ```bash
   docker pull aigilityai_eda:latest
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 aigilityai_eda:latest
   ```

3. Access the application at `http://localhost:5000` in your web browser.

## Running without Docker

If you prefer not to use Docker, you can run the application directly.

### Prerequisites

- Python 3
- Git

### Steps

1. Clone the GitHub repository:
   ```bash
   git clone https://github.com/keshav787/aigilityai_eda.git
   ```

2. Navigate to the repository directory:
   ```bash
   cd aigilityai_eda
   ```

3. Install the required Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python3 app.py
   ```

5. Open `http://localhost:5000` in your web browser to access the application.

## Support

For any additional information or support, please contact the repository maintainers.
