# Django Chatbot Project

This repository contains a Django web application that simulates a simple two‑agent “chatbot” conversation about food preferences.  The app stores the results in a SQL database and exposes an authenticated API endpoint that lists all simulated users who are vegetarian or vegan along with their top three favourite foods.

## Features

* **Django & Django REST Framework** – Provides a RESTful API over a SQL database (SQLite by default).
* **Conversation Simulation** – A management command (`simulate_conversations`) runs 100 simulated conversations between two chat agents.  Agent A asks “What are your top three favourite foods?”, and Agent B responds.  By default the answers are three foods chosen at random from a predefined list, but if an environment variable `OPENAI_API_KEY` is set the command will instead call the OpenAI Chat Completion API to generate answers dynamically.
* **Vegetarian/Vegan Classification** – Foods are classified as meat, vegetarian, or vegan.  If a response contains only vegetarian foods it is labelled `vegetarian=true`; if all foods are vegan it is additionally marked `vegan=true`.
* **Authenticated API** – `/api/vegetarian_vegan/` returns the conversations where users are vegetarian or vegan.  Basic HTTP authentication protects this endpoint.  A default user (`user`/`password`) is created when the app first runs.
* **Dockerised** – A `Dockerfile` makes it easy to build and run the application inside a container.  When the container starts it runs the conversation simulation automatically.

## Running Locally

1. **Clone this repository** (replace with your own repository URL after pushing):

   ```bash
   git clone <your‑github‑repo-url>
   cd django_chatbot_project
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t django-chatbot .
   ```

3. **Run the container:**

   ```bash
   docker run -p 8000:8000 django-chatbot
   ```

4. **Access the API:**

   Visit `http://localhost:8000/api/vegetarian_vegan/` in your browser.  Use basic authentication with username `user` and password `password`.

The API will return a JSON list of conversations where the simulated user’s favourite foods are vegetarian or vegan.

## Deployment

This application is designed to run on Azure Web App Service or any comparable cloud platform that can host Docker containers.  To deploy:

1. Build and push the Docker image to a container registry (e.g. Docker Hub or Azure Container Registry).
2. Create a new Web App for Containers in Azure and configure it to use your container image.
3. Ensure the container exposes port 8000.

Refer to the Azure documentation for detailed steps.  The provided Dockerfile uses only free resources and does not require any external services beyond the container itself.
