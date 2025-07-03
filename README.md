# Django Project with Real-Time Notifications

This README provides a comprehensive guide to setting up and running this Django project on a Windows local environment. It particularly focuses on its real-time notification system, which is powered by Celery, Redis, and Django Channels.

-----

## 🚀 Overview

This project is a Django application set up to deliver real-time notifications to users upon login. It uses a combination of background tasks and WebSockets to create a seamless and instantaneous user experience. The backend is designed to be robust, leveraging Docker for its services like Redis and Celery, ensuring a consistent environment for development and production.

-----

## 🛠️ Tech Stack

The project is built with a modern and powerful set of technologies:

  * **Backend**: Django, Python 3.12+
  * **Asynchronous Tasks**: Celery
  * **Real-time Communication**: Django Channels, WebSockets
  * **Message Broker & Caching**: Redis
  * **Containerization**: Docker
  * **Frontend**: HTML, JavaScript
  * **Authentication**: django-allauth

-----

## 🏁 Getting Started

### Prerequisites

  * **Docker Desktop**: Ensure that Docker Desktop is installed and running on your Windows machine.
  * **Python**: Python 3.12 or higher.
  * **uv**: A fast Python package installer and resolver.

### Installation

1.  **Clone the Repository**:

    ```bash
    git clone <your-repository-url>
    cd django-project
    ```

2.  **Set up Virtual Environment and Install Dependencies with `uv`**:

    ```bash
    # Create a virtual environment
    uv venv

    # Activate the virtual environment
    .\.venv\Scripts\activate

    # Install dependencies
    uv pip install -r requirements.txt
    ```

3.  **Run Database Migrations**:

    ```bash
    python manage.py migrate
    ```

4.  **Create a Superuser**:

    ```bash
    python manage.py createsuperuser
    ```

-----

## ▶️ Running the Application

To run the application, you need to start three main services: **Redis**, the **Celery worker**, and the **Django development server**.

1.  **Start Redis and Celery with Docker**:
    Open a terminal and run the following command to start the Redis and Celery containers in detached mode:

    ```bash
    docker-compose up -d
    ```

    This command reads the `docker-compose.yml` file and starts the services defined within it.

2.  **Start the Django Development Server**:
    In a separate terminal (with the virtual environment activated), run:

    ```bash
    python manage.py runserver
    ```

    The Django development server will start, and you can access the application at `http://127.0.0.1:8000`.

-----

## 📢 Notification System Deep Dive

The real-time notification system is a core feature of this project. Here is a detailed, end-to-end breakdown of how it works:

### 1\. User Logs In

  * The process begins when a user successfully logs in. The `django-allauth` package emits a `user_logged_in` signal.

### 2\. Signal Handling

  * A signal receiver in `core/signals.py` listens for the `user_logged_in` signal.
  * When the signal is caught, the `user_logged_in_receiver` function is executed. This function then dispatches a Celery task, `send_login_notification`, to be executed in the background. This is done by calling `.delay()` on the task.

### 3\. Celery Task Execution

  * The Celery worker, running in its Docker container, picks up the `send_login_notification` task from the Redis message broker.
  * The task, defined in `core/tasks.py`, constructs a welcome message for the user.

### 4\. Sending the Notification via Channels

  * The Celery task uses `get_channel_layer()` to access the Django Channels layer, which is configured to use Redis as its backplane.
  * The task sends the notification message to a user-specific group. The group name is dynamically created using the user's ID (e.g., `notifications_1`).

### 5\. WebSocket Connection

  * When a user logs in, the `base.html` template establishes a WebSocket connection to the server at `ws/notifications/`.
  * The `core/routing.py` file routes this connection to the `NotificationConsumer`.

### 6\. The `NotificationConsumer`

  * The `NotificationConsumer` in `core/consumers.py` handles the WebSocket connection.
  * When a user connects, they are added to their own unique notification group based on their user ID. This ensures that users only receive their own notifications.

### 7\. Receiving the Notification in the Browser

  * The `send.notification` event, sent by the Celery task, is received by the `NotificationConsumer`.
  * The consumer's `send_notification` method forwards the message to the client over the WebSocket connection.
  * The JavaScript in the `base.html` template receives the message and logs it to the browser's console.