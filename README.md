# Django Chatbot Project

This repository contains a Django web application that simulates a simple two‑chatgpt agents(A & B) “chatbot” conversation about food preferences.  The app stores the results in a SQL database and exposes an authenticated API endpoint that lists all simulated users who are vegetarian or vegan along with their top three favourite foods.

## Features

* **Django & Django REST Framework** – Provides a RESTful API over a SQL database (SQLite by default).
* **Smart Conversation Simulation** – A management command (`simulate_conversations`) runs 100 simulated conversations between two chatgpt agents A and B. Agent A asks “What are your top three favourite foods?”, and Agent B responds. If `OPENAI_API_KEY` is set, ChatGPT dynamically returns:
  - An array of three foods
  - A `vegetarian` flag (true if all three foods are meat-free)
  - A `vegan` flag (true if all three foods are free from all animal products)

  If the API is unavailable, the system falls back to a built-in keyword-based heuristic classifier.
* **Dietary Classification** – Every response is analyzed to determine whether the food set is vegetarian or vegan. If ChatGPT omits or incorrectly classifies them, the fallback logic supplements or corrects the result.
* **Authenticated API** – `/api/vegetarian_vegan/` returns only those conversations where the user’s top 3 foods are vegetarian or vegan. This endpoint is protected via HTTP Basic Authentication (`user` / `password`).
* **Dockerised** – A `Dockerfile` makes it easy to build and run the app in a container. The simulation runs automatically when the container starts.

## Running Locally

1. **Clone this repository** (replace with your own repository URL after pushing):

   ```bash
   git clone <your‑github‑repo-url
   cd django_chatbot_project
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t django-chatbot .
   ```

3. **Run the container:**

   ```bash
   docker run -p 8000:8000 -e OPENAI_API_KEY=your-api-key django-chatbot
   ```

4. **Access the API:**

   Visit `http://localhost:8000/api/vegetarian_vegan/` in your browser.  Use basic authentication with username `user` and password `password`.

The API will return a JSON list of conversations where the simulated user’s favourite foods are vegetarian or vegan.

## Deployment

This application is designed to run on Azure Web App Service or any comparable cloud platform that can host Docker containers.  To deploy:

## Deployment

This application can be deployed using **Azure Container Instances (ACI)** or any Docker-compatible cloud environment.

### Deploying to Azure Container Instances (ACI)

1. **Push the Docker image** to Azure Container Registry:
   ```bash
   az acr login --name yourRegistryName
   docker tag django-chatbot yourRegistryName.azurecr.io/django-chatbot:latest
   docker push yourRegistryName.azurecr.io/django-chatbot:latest
   ```

2. **Create a container instance**:
   ```bash
   az container create \
     --name django-chatbot-container \
     --resource-group YourResourceGroup \
     --image yourRegistryName.azurecr.io/django-chatbot:latest \
     --registry-login-server yourRegistryName.azurecr.io \
     --registry-username <ACR_USERNAME> \
     --registry-password <ACR_PASSWORD> \
     --dns-name-label django-chatbot-demo \
     --ports 8000 \
     --os-type Linux \
     --cpu 1 \
     --memory 1.5
   ```

3. **Test your deployment**:

Visit [http://django-chatbot-demo.eastus.azurecontainer.io:8000/api/vegetarian_vegan/](http://django-chatbot-demo.eastus.azurecontainer.io:8000/api/vegetarian_vegan/)  
   Use basic auth (`user` / `password`).

## Notes

- If `OPENAI_API_KEY` is not set in the container environment, the system will fallback to generating random food responses.
- To regenerate the simulated data, rebuild or restart the container.


Refer to the Azure documentation for detailed steps.  The provided Dockerfile uses only free resources and does not require any external services beyond the container itself.
