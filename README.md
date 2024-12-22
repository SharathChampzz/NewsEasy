# NewsEasy
**NewsEasy**  NewsEasy is a Django-based web application that simplifies news articles using AI. It fetches the latest news from various sources, simplifies the content for easy reading, and publishes it on a user-friendly platform.

Output:
![image](https://github.com/SharathChampzz/NewsEasy/assets/54370770/11fb4689-3328-4854-ba58-0d7d59e44c6c)

## API and UI Request Handling

In NewsEasy, the routing of requests is managed to ensure that API calls and UI requests are handled efficiently and securely.

### Request Routing

- **API Calls**: All requests to the `/api` endpoint are redirected to the backend application. This is where the core logic of fetching, processing, and simplifying news articles takes place.
- **UI Requests**: Requests that do not target the `/api` endpoint are served by the frontend application. This includes rendering the user interface and serving static assets.

### Middleware Configuration

To ensure secure and efficient handling of requests, several middlewares are configured in NewsEasy:

1. **Authentication Middleware**: This middleware ensures that only authenticated users can access certain endpoints. It verifies user credentials and manages user sessions.
2. **Logging Middleware**: This middleware logs all incoming requests and responses. It helps in monitoring the application, debugging issues, and maintaining an audit trail of user activities.
3. **Performance Middleware**: This middleware monitors the performance of the application by tracking the time taken to process requests. It helps in identifying bottlenecks and optimizing the application's performance.
4. **Security Middleware**: This middleware adds security headers to the responses to protect against common web vulnerabilities. It includes headers like `X-Frame-Options`, `X-Content-Type-Options`, and `Content-Security-Policy`.

By effectively routing requests and utilizing these middlewares, NewsEasy ensures a secure, efficient, and user-friendly experience for its users.

## Background Tasks with Celery

Celery is used in NewsEasy for handling background tasks such as fetching and simplifying news articles. Celery is a powerful, production-ready asynchronous job queue that allows you to run time-consuming Python functions in the background.

### Why Celery is Best for Django Projects

1. **Asynchronous Task Execution**: Celery allows you to execute tasks asynchronously, which means your web application can handle more requests without being blocked by long-running tasks.
2. **Scalability**: Celery can scale horizontally by adding more worker nodes, making it suitable for high-load applications.
3. **Reliability**: Celery supports task retries in case of failure, ensuring that tasks are eventually completed.
4. **Integration**: Celery integrates seamlessly with Django, making it easy to set up and use with Django projects.

By using Celery, NewsEasy can efficiently handle the background processing required to fetch and simplify news articles, providing a smooth and responsive user experience.
