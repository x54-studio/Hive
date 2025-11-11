#!/usr/bin/env python3
"""
Script to seed the database with fake articles for testing.
Run from backend directory: python seed_articles.py

The script reads MONGO_URI from .env file or environment variables.
If running locally (outside Docker), ensure .env has:
  MONGO_URI=mongodb://admin:hivepass123@localhost:27027/
"""

from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

# Load .env file explicitly to ensure it's read
load_dotenv()

from app.config import Config
from utilities.logger import get_logger
from pymongo import MongoClient

logger = get_logger(__name__)

def get_mongo_uri():
    """
    Get MongoDB URI, automatically converting Docker hostname to localhost for local runs.
    """
    mongo_uri = Config.MONGO_URI
    
    # If URI contains Docker hostname and we're not in Docker, convert to localhost
    if "mongodb:" in mongo_uri and "localhost" not in mongo_uri and "127.0.0.1" not in mongo_uri:
        # Check if we're likely running locally (not in Docker)
        # Docker detection: check for Docker-specific files/env vars
        is_docker = (
            os.path.exists("/.dockerenv") or 
            os.path.exists("/proc/self/cgroup") or
            os.environ.get("DOCKER_CONTAINER") == "true"
        )
        
        if not is_docker:
            # Replace Docker hostname with localhost
            # Handle both "mongodb:" and "@mongodb:" patterns
            mongo_uri = mongo_uri.replace("@mongodb:", "@localhost:")
            mongo_uri = mongo_uri.replace("mongodb://mongodb:", "mongodb://localhost:")
            logger.info(f"Converted Docker hostname to localhost: {mongo_uri}")
    
    return mongo_uri

# Sample articles data
SAMPLE_ARTICLES = [
    {
        "title": "The Future of Web Development: Trends to Watch in 2025",
        "content": """Web development continues to evolve at a rapid pace, and 2025 promises to bring exciting new technologies and methodologies. From the rise of AI-powered development tools to the increasing adoption of serverless architectures, developers have much to look forward to.

One of the most significant trends is the integration of artificial intelligence into the development workflow. Tools like GitHub Copilot and ChatGPT are already changing how developers write code, offering intelligent suggestions and automating repetitive tasks.

Another key trend is the shift towards edge computing. As applications become more distributed, developers are leveraging edge networks to reduce latency and improve user experiences across the globe.

The JavaScript ecosystem also continues to mature, with frameworks like React, Vue, and Svelte pushing the boundaries of what's possible in the browser. TypeScript adoption is at an all-time high, bringing type safety to JavaScript projects of all sizes.

As we move forward, developers must stay adaptable and continuously learn new technologies. The landscape changes quickly, but those who embrace change will thrive in this dynamic field.""",
        "author": "Sarah Johnson"
    },
    {
        "title": "Understanding RESTful API Design Best Practices",
        "content": """RESTful APIs have become the standard for building web services, but designing them well requires careful consideration of several principles. A well-designed API is intuitive, consistent, and easy to use.

First and foremost, use proper HTTP methods. GET requests should only retrieve data, POST should create new resources, PUT should update entire resources, and DELETE should remove them. PATCH can be used for partial updates.

Resource naming is crucial. Use nouns, not verbs, and make them plural. For example, `/api/users` is better than `/api/getUser`. Keep URLs hierarchical and logical.

Status codes matter. Use 200 for successful GET requests, 201 for successful POST requests, 204 for successful DELETE requests. Use 400 for bad requests, 401 for unauthorized, 404 for not found, and 500 for server errors.

Version your APIs. Include version numbers in the URL path like `/api/v1/users` to allow for future changes without breaking existing clients.

Finally, provide clear error messages. When something goes wrong, return helpful error messages that guide developers toward fixing the issue. Include error codes and descriptions that make debugging easier.""",
        "author": "Michael Chen"
    },
    {
        "title": "Database Optimization Techniques for High-Traffic Applications",
        "content": """When building applications that need to handle thousands or millions of requests, database performance becomes critical. Poor database design can bring even the most well-architected application to its knees.

Indexing is your first line of defense. Create indexes on columns frequently used in WHERE clauses, JOIN conditions, and ORDER BY clauses. However, don't over-index, as each index adds overhead to write operations.

Query optimization is equally important. Use EXPLAIN or EXPLAIN ANALYZE to understand how your database executes queries. Look for full table scans and find ways to eliminate them.

Connection pooling helps manage database connections efficiently. Instead of creating a new connection for each request, maintain a pool of reusable connections that can be shared across requests.

Consider read replicas for read-heavy applications. By distributing read queries across multiple database servers, you can significantly improve performance and reduce load on your primary database.

Caching is another powerful tool. Use Redis or Memcached to cache frequently accessed data, reducing the number of database queries. Implement cache invalidation strategies to ensure data consistency.

Finally, consider database sharding for very large datasets. By partitioning data across multiple databases, you can scale horizontally and handle larger volumes of data and traffic.""",
        "author": "Emily Rodriguez"
    },
    {
        "title": "Introduction to Microservices Architecture",
        "content": """Microservices architecture has gained significant traction as organizations seek to build more scalable and maintainable systems. Unlike monolithic applications, microservices break applications into smaller, independent services.

Each microservice is responsible for a specific business capability and can be developed, deployed, and scaled independently. This approach offers several advantages, including improved fault isolation, technology diversity, and team autonomy.

However, microservices also introduce complexity. Service communication becomes more complex, requiring robust API design and potentially message queues. Distributed systems bring challenges like eventual consistency and distributed transactions.

Service discovery is crucial in microservices. Services need to find and communicate with each other, which can be handled through service registries or API gateways.

Monitoring and observability become more important than ever. With multiple services running, you need comprehensive logging, metrics, and tracing to understand system behavior and debug issues.

When considering microservices, start small. Not every application needs microservices, and the added complexity may not be worth it for smaller projects. Consider your team size, deployment capabilities, and actual scaling needs before making the leap.""",
        "author": "David Kim"
    },
    {
        "title": "Security Best Practices for Modern Web Applications",
        "content": """Security should be a top priority for every web application developer. With cyber threats becoming more sophisticated, implementing robust security measures is essential.

Authentication and authorization are fundamental. Use strong password hashing algorithms like bcrypt or Argon2. Implement multi-factor authentication for sensitive applications. Use JWT tokens securely, with appropriate expiration times and secure storage.

Input validation is critical. Never trust user input. Validate and sanitize all data on both client and server sides. Use parameterized queries to prevent SQL injection attacks.

Protect against Cross-Site Scripting (XSS) by properly escaping user-generated content. Use Content Security Policy headers to restrict which scripts can run on your pages.

Implement HTTPS everywhere. Encrypt data in transit using TLS/SSL certificates. Never transmit sensitive data over unencrypted connections.

Keep dependencies up to date. Regularly update your libraries and frameworks to patch known vulnerabilities. Use tools like npm audit or pip-audit to identify security issues.

Implement rate limiting to prevent abuse and DDoS attacks. Limit the number of requests a user can make within a certain time period.

Log security events and monitor for suspicious activity. Implement intrusion detection and set up alerts for unusual patterns. Regular security audits help identify vulnerabilities before attackers exploit them.""",
        "author": "Lisa Wang"
    },
    {
        "title": "Getting Started with Docker and Containerization",
        "content": """Docker has revolutionized how we build, ship, and run applications. Containerization provides a consistent environment across development, testing, and production, eliminating the "it works on my machine" problem.

A Docker container packages an application with all its dependencies into a single, portable unit. Unlike virtual machines, containers share the host operating system kernel, making them lightweight and fast.

Dockerfiles define how to build container images. They specify a base image, install dependencies, copy application files, and define how to run the application. Writing efficient Dockerfiles is key to creating fast, secure containers.

Docker Compose simplifies multi-container applications. Define all your services in a docker-compose.yml file, and Docker Compose handles networking, volumes, and service dependencies.

Container orchestration platforms like Kubernetes take containerization to the next level. They handle scaling, load balancing, service discovery, and self-healing for containerized applications.

Best practices include using multi-stage builds to reduce image size, running containers as non-root users for security, and using .dockerignore to exclude unnecessary files from builds.

Docker volumes persist data beyond container lifecycles, while bind mounts allow direct access to host filesystems. Choose the right approach based on your data persistence needs.

As you adopt Docker, remember that containers are ephemeral. Design your applications to be stateless when possible, storing state in external databases or storage systems.""",
        "author": "Robert Taylor"
    },
    {
        "title": "The Art of Code Review: Best Practices and Common Pitfalls",
        "content": """Code reviews are an essential part of maintaining code quality and sharing knowledge within a team. A good code review process catches bugs, improves code quality, and helps team members learn from each other.

When reviewing code, focus on the code, not the person. Provide constructive feedback that helps improve the codebase. Ask questions rather than making demands, and explain the reasoning behind your suggestions.

Look for bugs and potential issues. Check error handling, edge cases, and potential security vulnerabilities. Verify that the code meets the requirements and follows the project's coding standards.

Consider performance implications. Are there inefficient algorithms or database queries? Could the code be optimized without sacrificing readability?

Check for test coverage. Ensure that new code includes appropriate tests, and that existing tests still pass. Good test coverage helps prevent regressions.

Review for maintainability. Is the code readable and well-documented? Will future developers understand what the code does? Are there opportunities to reduce complexity or improve naming?

Be timely with reviews. Don't let pull requests sit for days. Quick feedback keeps the development flow moving and prevents context switching.

As a code author, be open to feedback. Don't take criticism personally. Respond to all comments, even if it's just to acknowledge them. Use reviews as learning opportunities to improve your skills.""",
        "author": "Jennifer Martinez"
    },
    {
        "title": "Building Scalable Frontend Applications with React",
        "content": """React has become the de facto standard for building modern user interfaces, but building scalable React applications requires careful architecture and best practices.

Component composition is key. Break down your UI into small, reusable components. Each component should have a single responsibility and be easy to test and maintain.

State management becomes crucial as applications grow. For simple state, React's built-in useState and useReducer hooks may suffice. For complex global state, consider Redux, Zustand, or React Query.

Performance optimization is essential for large applications. Use React.memo to prevent unnecessary re-renders, implement code splitting with React.lazy, and optimize images and assets. Use the React DevTools Profiler to identify performance bottlenecks.

Error boundaries catch JavaScript errors anywhere in the component tree and display fallback UI. Implement error boundaries strategically to provide better user experiences when things go wrong.

Testing is non-negotiable. Write unit tests for components, integration tests for user flows, and end-to-end tests for critical paths. Tools like Jest and React Testing Library make testing React applications straightforward.

Accessibility matters. Use semantic HTML, provide proper ARIA labels, ensure keyboard navigation works, and test with screen readers. Building accessible applications benefits all users.

Keep your bundle size manageable. Use dynamic imports, remove unused dependencies, and analyze your bundle regularly. Smaller bundles mean faster load times and better user experiences.""",
        "author": "Alex Thompson"
    },
    {
        "title": "CI/CD Pipelines: Automating Your Development Workflow",
        "content": """Continuous Integration and Continuous Deployment (CI/CD) pipelines automate the process of building, testing, and deploying applications. A well-designed pipeline catches issues early and enables rapid, reliable deployments.

Continuous Integration means automatically building and testing code whenever changes are pushed to the repository. This helps catch integration issues early, before they become bigger problems.

A typical CI pipeline includes steps like installing dependencies, running linters, executing tests, building the application, and potentially deploying to a staging environment.

Continuous Deployment takes CI a step further by automatically deploying code that passes all tests to production. This requires high confidence in your test coverage and deployment process.

Pipeline as Code allows you to version control your CI/CD configuration alongside your application code. Tools like GitHub Actions, GitLab CI, and Jenkins Pipeline support this approach.

Implement proper security scanning in your pipeline. Run dependency vulnerability scans, static code analysis, and container image scans as part of your build process.

Use feature flags to control feature rollouts. This allows you to deploy code to production while keeping features disabled until you're ready to enable them.

Monitor your deployments. Track metrics like deployment frequency, lead time, mean time to recovery, and change failure rate. These metrics help you understand and improve your development process.

Remember that CI/CD is a journey, not a destination. Start simple and gradually add more automation as your team and processes mature.""",
        "author": "Maria Garcia"
    },
    {
        "title": "Introduction to GraphQL: A Modern Alternative to REST",
        "content": """GraphQL has emerged as a powerful alternative to REST APIs, offering more flexibility and efficiency in how clients query data. Developed by Facebook, GraphQL provides a query language for APIs and a runtime for executing those queries.

Unlike REST, where clients receive fixed data structures, GraphQL allows clients to specify exactly what data they need. This reduces over-fetching and under-fetching of data, leading to more efficient network usage.

GraphQL uses a single endpoint for all queries, unlike REST which typically has multiple endpoints. Clients send queries to this endpoint, and the server returns exactly the requested data.

The schema is central to GraphQL. It defines the types available, their fields, and the relationships between them. This schema serves as a contract between client and server.

Resolvers handle the actual data fetching. Each field in a GraphQL query can have its own resolver function, allowing fine-grained control over how data is retrieved.

GraphQL supports mutations for modifying data and subscriptions for real-time updates. This makes it suitable for a wide range of application types.

However, GraphQL isn't always the right choice. REST may be simpler for straightforward CRUD operations, and GraphQL's flexibility can lead to complex queries that impact performance if not managed carefully.

When implementing GraphQL, consider query complexity, implement rate limiting, and use DataLoader to batch and cache database queries. Proper error handling and authentication are just as important as in REST APIs.""",
        "author": "James Wilson"
    },
    {
        "title": "The Importance of Monitoring and Observability in Production",
        "content": """Once your application is deployed to production, monitoring and observability become critical for maintaining reliability and performance. You can't fix what you can't see.

Logging is the foundation of observability. Implement structured logging with consistent formats. Include contextual information like request IDs, user IDs, and timestamps. Use appropriate log levels: DEBUG for development, INFO for normal operations, WARN for potential issues, and ERROR for actual problems.

Metrics provide quantitative data about your application's behavior. Track key metrics like request rate, error rate, latency, and resource utilization. Use tools like Prometheus to collect metrics and Grafana to visualize them.

Distributed tracing helps you understand request flows across multiple services. When a request spans multiple services, tracing shows you exactly where time is spent and where errors occur.

Set up alerting for critical issues. Define thresholds for key metrics and configure alerts that notify the right people at the right time. Avoid alert fatigue by setting appropriate thresholds and using alert grouping.

Dashboards provide at-a-glance views of your system's health. Create dashboards for different audiences: operations teams need technical metrics, while business stakeholders need business metrics.

Implement health checks and readiness probes. These endpoints allow load balancers and orchestration platforms to determine if your application is healthy and ready to receive traffic.

Remember that observability is an ongoing process. Regularly review your logs, metrics, and traces. Adjust your monitoring as your application evolves and new issues emerge. The goal is to have visibility into your system's behavior and the ability to quickly diagnose and resolve issues.""",
        "author": "Patricia Brown"
    },
    {
        "title": "Mastering Git: Essential Commands and Workflows for Developers",
        "content": """Git has become the standard version control system for software development, but many developers only scratch the surface of its capabilities. Mastering Git commands and workflows can significantly improve your productivity and collaboration.

Start with the basics: `git add` stages changes, `git commit` saves them to history, and `git push` uploads to a remote repository. Understanding the three states of files—modified, staged, and committed—is fundamental.

Branching is one of Git's most powerful features. Create feature branches for new work, use `git checkout` or `git switch` to move between branches, and merge when work is complete. The `git merge` and `git rebase` commands offer different approaches to integrating changes.

Stashing allows you to temporarily save uncommitted changes. Use `git stash` when you need to switch branches but aren't ready to commit, then `git stash pop` to restore your changes later.

Interactive rebasing with `git rebase -i` lets you clean up your commit history before sharing. You can squash commits, reorder them, or edit commit messages to create a cleaner history.

Understanding merge conflicts is crucial. When Git can't automatically merge changes, you'll need to manually resolve conflicts. Use `git status` to see conflicted files, edit them to resolve conflicts, then stage and commit the resolution.

Remote repositories enable collaboration. `git fetch` downloads changes without merging, while `git pull` fetches and merges in one step. `git remote` helps manage remote repository connections.

Advanced techniques like cherry-picking specific commits, using `git bisect` to find bugs, and leveraging hooks for automation can take your Git skills to the next level. Practice regularly and don't be afraid to experiment in a test repository.""",
        "author": "Daniel Lee"
    },
    {
        "title": "Building Responsive Web Designs: Mobile-First Approach",
        "content": """With mobile devices accounting for over half of web traffic, responsive design is no longer optional—it's essential. A mobile-first approach ensures your website works beautifully on all devices, from smartphones to large desktop monitors.

Mobile-first means designing for the smallest screen first, then progressively enhancing for larger screens. This approach forces you to prioritize content and functionality, resulting in cleaner, more focused designs.

CSS media queries are the foundation of responsive design. Use `@media` rules to apply different styles at different breakpoints. Common breakpoints include 480px (mobile), 768px (tablet), 1024px (desktop), and 1440px (large desktop).

Flexbox and CSS Grid are powerful tools for creating responsive layouts. Flexbox excels at one-dimensional layouts, while Grid handles complex two-dimensional layouts. Both adapt naturally to different screen sizes.

Relative units like `rem`, `em`, and percentages make your designs more flexible than fixed pixel values. `rem` units are particularly useful as they scale with the root font size, making your entire design more adaptable.

Images are often the largest assets on a page. Use responsive images with `srcset` and `sizes` attributes, or the `<picture>` element for art direction. Consider using modern formats like WebP or AVIF for better compression.

Touch targets should be at least 44x44 pixels for mobile devices. Ensure adequate spacing between interactive elements to prevent accidental taps. Test your designs on actual devices, not just browser developer tools.

Performance matters on mobile. Optimize images, minimize CSS and JavaScript, and consider lazy loading for below-the-fold content. A fast-loading site provides a better user experience and improves SEO rankings.""",
        "author": "Rachel Green"
    },
    {
        "title": "Understanding JavaScript Closures and Scope",
        "content": """Closures are one of JavaScript's most powerful and misunderstood features. Understanding closures and scope is essential for writing effective JavaScript code and avoiding common pitfalls.

Scope determines where variables are accessible. JavaScript has function scope (with `var`) and block scope (with `let` and `const`). Variables declared with `var` are function-scoped, while `let` and `const` are block-scoped.

A closure occurs when a function has access to variables from its outer (enclosing) scope even after the outer function has returned. This allows functions to "remember" their environment.

Closures are created every time a function is created. The inner function maintains a reference to the outer function's variables, preventing them from being garbage collected.

Common use cases for closures include data privacy, function factories, and event handlers. Closures enable the module pattern, allowing you to create private variables and methods.

Be careful with closures in loops. A common mistake is creating closures inside loops that reference the loop variable. By the time the closure executes, the loop may have completed, and all closures reference the final value.

To fix loop closure issues, use `let` instead of `var`, create an IIFE (Immediately Invoked Function Expression), or use `bind` to create a new function with the correct context.

Memory leaks can occur if closures hold references to large objects unnecessarily. Be mindful of what your closures capture and clean up references when they're no longer needed.

Understanding closures helps you write more efficient, maintainable code. They're fundamental to many JavaScript patterns and are used extensively in modern frameworks and libraries.""",
        "author": "Kevin Park"
    },
    {
        "title": "API Rate Limiting: Protecting Your Services from Abuse",
        "content": """Rate limiting is a crucial security and performance measure for APIs. It prevents abuse, ensures fair resource usage, and protects your services from being overwhelmed by too many requests.

Rate limiting controls how many requests a client can make within a specific time window. Common approaches include limiting requests per second, per minute, per hour, or per day.

The token bucket algorithm is a popular rate limiting strategy. Each client has a bucket of tokens that refills at a steady rate. Each request consumes a token, and requests are rejected when the bucket is empty.

The sliding window log tracks requests in a time window, providing more accurate rate limiting than fixed windows. However, it requires more memory to store request timestamps.

HTTP headers communicate rate limit information to clients. Include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers in responses so clients know their current limits.

Different endpoints may need different rate limits. Authentication endpoints might have stricter limits to prevent brute force attacks, while read-only endpoints might allow more requests.

Implement rate limiting at multiple layers. Application-level rate limiting provides fine-grained control, while infrastructure-level rate limiting (like load balancers) can handle DDoS protection.

Redis is commonly used for distributed rate limiting. It provides fast in-memory storage and supports atomic operations needed for accurate rate limiting across multiple servers.

Handle rate limit exceeded responses gracefully. Return HTTP 429 (Too Many Requests) with a `Retry-After` header indicating when the client can try again. Provide clear error messages explaining the limit.

Consider implementing different rate limits for different user tiers. Free users might have lower limits, while premium users get higher limits. This can be part of your monetization strategy.""",
        "author": "Amanda White"
    },
    {
        "title": "The Power of Test-Driven Development (TDD)",
        "content": """Test-Driven Development (TDD) is a software development approach where you write tests before writing the actual code. This methodology can improve code quality, reduce bugs, and make refactoring safer.

The TDD cycle follows three steps: Red, Green, Refactor. First, write a failing test (Red). Then write the minimum code to make it pass (Green). Finally, improve the code while keeping tests passing (Refactor).

Writing tests first forces you to think about the interface and behavior of your code before implementation. This leads to better design and clearer requirements.

TDD encourages writing smaller, more focused functions. When you write tests first, you naturally break down problems into smaller, testable units.

Test coverage improves with TDD because you write tests for every feature you implement. However, high coverage doesn't guarantee quality—meaningful tests matter more than coverage percentages.

Unit tests form the foundation of TDD. They test individual functions or methods in isolation. Integration tests verify that components work together correctly.

Mocking and stubbing help isolate units under test. Use mocks to replace dependencies and control their behavior, making tests faster and more reliable.

TDD can feel slow at first, especially when learning. However, the time invested in writing tests pays off through fewer bugs, easier refactoring, and better documentation of expected behavior.

Not all code needs TDD. Simple code, prototypes, or code that's hard to test might benefit from writing tests after implementation. Use your judgment and adapt the approach to your situation.

The key to successful TDD is starting small. Write a simple test, make it pass, then gradually add complexity. Don't try to test everything at once—build up your test suite incrementally.""",
        "author": "Thomas Anderson"
    },
    {
        "title": "Serverless Architecture: Building Applications Without Servers",
        "content": """Serverless computing has revolutionized how we build and deploy applications. Despite the name, serverless doesn't mean no servers—it means you don't manage them. Cloud providers handle server management, scaling, and maintenance.

Function as a Service (FaaS) is the core of serverless. You write functions that run in response to events, and the platform handles execution, scaling, and resource allocation automatically.

AWS Lambda, Azure Functions, and Google Cloud Functions are popular serverless platforms. They charge based on execution time and number of invocations, making them cost-effective for variable workloads.

Serverless excels at event-driven architectures. Functions can respond to HTTP requests, database changes, file uploads, scheduled events, or messages from queues.

Cold starts are a consideration in serverless. When a function hasn't been invoked recently, the first request may be slower as the platform initializes the runtime. Keep functions lightweight and consider provisioned concurrency for critical paths.

Statelessness is crucial in serverless. Functions shouldn't rely on local state between invocations. Use external storage like databases, object storage, or caching services for persistence.

API Gateway provides HTTP endpoints for serverless functions. It handles routing, authentication, rate limiting, and request/response transformation.

Serverless databases like DynamoDB, Cosmos DB, and Firestore complement serverless functions. They scale automatically and charge based on usage, matching the serverless model.

Monitoring serverless applications requires different approaches. Use cloud provider monitoring tools, distributed tracing, and structured logging to understand function performance and debug issues.

Cost optimization involves understanding pricing models, minimizing execution time, reducing memory allocation, and implementing efficient caching strategies. Monitor your usage and optimize accordingly.

Serverless isn't suitable for all applications. Long-running processes, applications requiring persistent connections, or workloads with consistent high traffic might be better served by traditional architectures.""",
        "author": "Sophie Martin"
    },
    {
        "title": "Effective Debugging Strategies for Modern Applications",
        "content": """Debugging is an essential skill for every developer. Effective debugging strategies can save hours of frustration and help you understand your code better.

Start by reproducing the bug consistently. If you can't reproduce it, you can't fix it. Document the steps that lead to the issue, including environment details, input data, and expected versus actual behavior.

Use logging strategically. Add log statements at key points in your code to trace execution flow. Use appropriate log levels—DEBUG for detailed information, INFO for general flow, WARN for potential issues, and ERROR for actual problems.

Breakpoints are powerful debugging tools. Use your IDE's debugger to pause execution, inspect variables, step through code line by line, and evaluate expressions. Learn your debugger's features—conditional breakpoints, watch expressions, and call stack navigation.

Read error messages carefully. They often contain clues about what went wrong. Stack traces show the execution path that led to the error, helping you trace back to the root cause.

Divide and conquer. If a bug is hard to isolate, systematically eliminate parts of your code to narrow down the problem. Use binary search techniques—comment out half your code, test, then focus on the problematic half.

Check your assumptions. Many bugs come from incorrect assumptions about how code works. Verify that variables have expected values, functions are called with correct parameters, and APIs behave as documented.

Use version control to your advantage. `git bisect` helps you find the commit that introduced a bug by binary searching through your commit history. This is especially useful for bugs that appeared recently.

Reproduce bugs in isolation. Create minimal test cases that demonstrate the issue. This helps you understand the problem better and verify the fix works.

Don't just fix symptoms—find root causes. A quick workaround might solve the immediate problem, but understanding why the bug occurred helps prevent similar issues and improves your code quality.

Take breaks when stuck. Sometimes stepping away from a problem helps you see it from a fresh perspective. Explain the problem to someone else, or write it down—the act of explaining often reveals insights.""",
        "author": "Christopher Moore"
    },
    {
        "title": "Working with Asynchronous JavaScript: Promises and Async/Await",
        "content": """Asynchronous programming is fundamental to JavaScript, especially for handling network requests, file operations, and user interactions. Understanding promises and async/await is crucial for writing modern JavaScript.

Callbacks were the original way to handle asynchronous operations in JavaScript, but they led to "callback hell" with deeply nested code that was hard to read and maintain.

Promises provide a cleaner alternative. A promise represents a value that may be available now, in the future, or never. Promises have three states: pending, fulfilled, or rejected.

The `.then()` method handles fulfilled promises, while `.catch()` handles rejections. You can chain promises to create sequences of asynchronous operations. `.finally()` runs regardless of the promise outcome.

`Promise.all()` runs multiple promises in parallel and waits for all to complete. If any promise rejects, the entire operation fails. `Promise.allSettled()` waits for all promises to settle regardless of outcome.

`Promise.race()` returns the first promise that settles, whether fulfilled or rejected. This is useful for timeouts or choosing the fastest response from multiple sources.

Async/await provides syntactic sugar over promises, making asynchronous code look more like synchronous code. Mark functions with `async` to use `await` inside them.

`await` pauses function execution until the promise resolves, then returns the resolved value. If the promise rejects, it throws an error that can be caught with try/catch.

Error handling with async/await uses standard try/catch blocks, which many developers find more intuitive than promise chains. However, remember that async functions always return promises.

Common mistakes include forgetting to await promises, not handling errors properly, and creating unnecessary sequential operations when parallel execution would be faster.

Use `Promise.all()` for independent operations that can run in parallel. Only await promises sequentially when one operation depends on another's result.

Understanding the event loop helps explain how asynchronous code executes. JavaScript is single-threaded, but the event loop manages asynchronous operations efficiently through callbacks, promises, and microtasks.""",
        "author": "Laura Davis"
    },
    {
        "title": "Design Patterns in Object-Oriented Programming",
        "content": """Design patterns are reusable solutions to common problems in software design. They provide a shared vocabulary and proven approaches to solving recurring design challenges.

The Singleton pattern ensures a class has only one instance and provides global access to it. Use it sparingly, as it can make testing difficult and create hidden dependencies.

The Factory pattern provides an interface for creating objects without specifying their exact classes. Factories encapsulate object creation logic, making code more flexible and maintainable.

The Observer pattern defines a one-to-many dependency between objects. When one object changes state, all dependent objects are notified automatically. This is the foundation of event-driven architectures.

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. This allows algorithms to vary independently from clients that use them.

The Decorator pattern attaches additional responsibilities to objects dynamically. It provides a flexible alternative to subclassing for extending functionality.

The Adapter pattern allows incompatible interfaces to work together. It acts as a bridge between two interfaces, converting one interface into another that clients expect.

The Facade pattern provides a simplified interface to a complex subsystem. It hides complexity behind a single, easy-to-use interface.

The Command pattern encapsulates requests as objects, allowing you to parameterize clients with different requests, queue operations, and support undo functionality.

Patterns are tools, not rules. Don't force patterns into your code—use them when they solve actual problems. Over-engineering with patterns can make code more complex than necessary.

Understand the problem before applying a pattern. Patterns solve specific problems, and using the wrong pattern can make things worse. Learn when patterns are appropriate and when simpler solutions suffice.

Modern languages and frameworks often incorporate patterns into their design. React uses the Observer pattern for state management, dependency injection frameworks implement the Factory pattern, and many frameworks use the Strategy pattern for plugins.

Remember that patterns are about communication. Using well-known patterns helps other developers understand your code quickly. However, don't sacrifice clarity for pattern adherence—readable code is more important than perfect pattern implementation.""",
        "author": "Ryan Johnson"
    },
    {
        "title": "Building Accessible Web Applications",
        "content": """Web accessibility ensures that websites and applications can be used by everyone, including people with disabilities. Building accessible applications isn't just the right thing to do—it's often legally required and improves usability for all users.

Semantic HTML is the foundation of accessibility. Use proper HTML elements like `<header>`, `<nav>`, `<main>`, `<article>`, and `<footer>` instead of generic `<div>` elements. Screen readers rely on semantic structure to navigate pages.

ARIA (Accessible Rich Internet Applications) attributes enhance accessibility when HTML semantics aren't sufficient. Use `aria-label` for descriptive labels, `aria-labelledby` to reference other elements, and `aria-describedby` for additional context.

Keyboard navigation is essential. Ensure all interactive elements are keyboard accessible. Users should be able to tab through your interface in a logical order. Use `tabindex` carefully—avoid positive values except when necessary.

Focus indicators are crucial for keyboard users. Ensure focus states are visible and clear. Don't remove focus outlines without providing custom, equally visible alternatives.

Color contrast matters. Text must meet WCAG contrast ratios: 4.5:1 for normal text, 3:1 for large text. Don't rely solely on color to convey information—use icons, labels, or patterns as well.

Alt text for images helps screen reader users understand visual content. Write descriptive alt text that conveys the image's purpose and content. Decorative images should have empty alt attributes.

Form accessibility includes proper labels, error messages, and validation feedback. Associate labels with inputs using the `for` attribute or by nesting inputs inside labels. Provide clear, specific error messages.

Dynamic content updates should be announced to screen readers. Use ARIA live regions (`aria-live`) to notify users of content changes without requiring them to navigate to that area.

Testing with screen readers is important. Tools like NVDA (Windows), VoiceOver (macOS/iOS), and JAWS help you understand how assistive technologies interact with your application.

Automated accessibility testing tools like axe, Lighthouse, and WAVE can catch many issues, but manual testing and user testing with people who have disabilities provide the most valuable insights.

Accessibility benefits everyone. Clear navigation, readable text, and intuitive interfaces improve the experience for all users, not just those with disabilities. Building accessible applications is an investment in better design.""",
        "author": "Nicole Taylor"
    },
    {
        "title": "Optimizing Frontend Performance: Techniques and Tools",
        "content": """Frontend performance directly impacts user experience, conversion rates, and SEO rankings. Fast-loading websites keep users engaged and reduce bounce rates. Optimizing performance requires understanding where time is spent and applying targeted improvements.

Bundle size significantly affects load time. Use code splitting to load only what's needed for each page. React.lazy() and dynamic imports enable route-based code splitting, reducing initial bundle size.

Image optimization is crucial. Compress images, use modern formats like WebP or AVIF, and implement responsive images with srcset. Consider lazy loading images below the fold to prioritize above-the-fold content.

Minification and compression reduce file sizes. Minify CSS and JavaScript, enable gzip or Brotli compression on your server, and remove unused code through tree shaking.

Caching strategies improve repeat visits. Set appropriate cache headers for static assets, use service workers for offline functionality, and implement browser caching for API responses when appropriate.

Critical CSS inlining improves perceived performance. Extract and inline CSS needed for above-the-fold content, then load the rest asynchronously to prevent render-blocking.

JavaScript execution can block rendering. Defer or async script loading, and consider using requestIdleCallback for non-critical JavaScript. Minimize main thread work to keep pages responsive.

Network optimization includes using CDNs for static assets, implementing HTTP/2 or HTTP/3, and reducing the number of HTTP requests through bundling and spriting.

Performance budgets help maintain performance over time. Set limits for bundle size, load time, and other metrics, and enforce them in your CI/CD pipeline.

Monitoring real user metrics (RUM) provides insights into actual performance. Tools like Web Vitals measure Core Web Vitals—Largest Contentful Paint (LCP), First Input Delay (FID), and Cumulative Layout Shift (CLS).

Profiling tools help identify bottlenecks. Chrome DevTools Performance tab, React DevTools Profiler, and Lighthouse provide detailed performance analysis. Use them regularly to find optimization opportunities.

Remember that performance is a feature. Fast websites provide better user experiences, improve SEO, and increase conversions. Make performance optimization part of your development workflow, not an afterthought.""",
        "author": "Brian Foster"
    },
    {
        "title": "Working with NoSQL Databases: MongoDB Best Practices",
        "content": """MongoDB is a popular NoSQL document database that offers flexibility and scalability. Understanding MongoDB best practices helps you build efficient, maintainable applications.

Schema design matters even in schemaless databases. While MongoDB doesn't enforce schemas, you should design consistent document structures. Use application-level validation or MongoDB's JSON Schema validation.

Embedding vs. referencing is a key design decision. Embed documents when data is accessed together and doesn't need to be queried independently. Reference documents when data is large, frequently updated, or accessed separately.

Indexes are crucial for query performance. Create indexes on fields used in queries, sorts, and filters. Compound indexes support queries that filter on multiple fields. Use explain() to analyze query plans.

The `_id` field is automatically indexed. Use it when possible, but be aware that ObjectIds are 12 bytes. Consider using shorter identifiers if storage is a concern.

Aggregation pipelines provide powerful data processing capabilities. Use `$match` early to filter documents, `$project` to select fields, and `$group` for aggregations. Pipeline stages execute in order, so optimize stage placement.

Connection pooling manages database connections efficiently. Configure appropriate pool sizes based on your application's concurrency needs. Too few connections cause queuing, while too many waste resources.

Write concerns control acknowledgment requirements. Use appropriate write concern levels based on your consistency and performance needs. `w: 1` acknowledges writes to the primary, while `w: majority` waits for replication.

Read preferences control which replica set members handle reads. Use `primary` for strong consistency, `secondary` to distribute read load, or `nearest` for low latency.

Transactions support multi-document operations. Use them when you need ACID guarantees across multiple documents. Be aware that transactions have performance overhead and aren't always necessary.

Regular maintenance includes monitoring, backups, and index optimization. Use MongoDB's built-in monitoring tools, implement regular backups, and review index usage to remove unused indexes.

Security best practices include authentication, authorization, encryption, and network security. Enable authentication, use role-based access control, encrypt data in transit and at rest, and restrict network access.

MongoDB's flexibility is powerful but requires discipline. Design your schemas thoughtfully, index appropriately, and monitor performance. Good practices in MongoDB lead to scalable, maintainable applications.""",
        "author": "Jessica Martinez"
    },
    {
        "title": "Container Orchestration with Kubernetes: Getting Started",
        "content": """Kubernetes has become the standard platform for container orchestration, enabling you to deploy, scale, and manage containerized applications efficiently. Understanding Kubernetes fundamentals is essential for modern DevOps practices.

Kubernetes clusters consist of control plane nodes and worker nodes. The control plane manages the cluster, while worker nodes run your applications. Pods are the smallest deployable units, typically containing one container.

Deployments manage pod replicas and provide rolling updates and rollbacks. They ensure a specified number of pod replicas are running and handle updates without downtime.

Services provide stable network endpoints for pods. Since pods are ephemeral, services abstract pod IP addresses and provide load balancing across pod replicas.

ConfigMaps and Secrets manage configuration data. ConfigMaps store non-sensitive configuration, while Secrets store sensitive data like passwords and API keys. Both can be mounted as files or environment variables.

Namespaces organize resources within a cluster. Use namespaces to separate environments, teams, or applications. Default namespace is fine for learning, but production should use dedicated namespaces.

Ingress controllers provide HTTP/HTTPS routing to services. They enable external access to services and can handle SSL termination, load balancing, and path-based routing.

PersistentVolumes and PersistentVolumeClaims manage storage. Applications request storage through PVCs, which are bound to PVs that provide actual storage resources.

Horizontal Pod Autoscaler (HPA) automatically scales pods based on CPU, memory, or custom metrics. This enables applications to handle varying loads efficiently.

Resource limits and requests control resource allocation. Set requests for guaranteed resources and limits to prevent pods from consuming too many resources.

Helm is a package manager for Kubernetes. It simplifies deploying complex applications by packaging Kubernetes manifests into charts. Use Helm for reusable application deployments.

kubectl is the command-line tool for interacting with Kubernetes clusters. Learn essential commands like `kubectl get`, `kubectl describe`, `kubectl logs`, and `kubectl exec` for debugging and management.

Start with local development using minikube or kind. These tools run Kubernetes clusters on your local machine, perfect for learning and testing. Once comfortable, move to managed Kubernetes services like EKS, GKE, or AKS.

Kubernetes has a steep learning curve, but understanding its core concepts unlocks powerful capabilities for deploying and managing applications at scale.""",
        "author": "Mark Thompson"
    }
]


def seed_articles():
    """Seed the database with sample articles."""
    try:
        # Use the adjusted MongoDB URI (converts Docker hostname to localhost if needed)
        mongo_uri = get_mongo_uri()
        
        # Create direct MongoDB connection (bypassing the singleton db.py)
        mongo_client = MongoClient(mongo_uri)
        db = mongo_client[Config.MONGO_DB_NAME]
        articles_collection = db.articles
        
        # Check if articles already exist
        existing_count = articles_collection.count_documents({})
        if existing_count > 0:
            print(f"Database already contains {existing_count} articles.")
            response = input("Do you want to add more articles? (y/n): ")
            if response.lower() != 'y':
                print("Seeding cancelled.")
                return
        
        # Create articles with timestamps spread over the past few weeks
        base_time = datetime.now(timezone.utc)
        created_articles = []
        
        for i, article_data in enumerate(SAMPLE_ARTICLES):
            # Spread articles over the past 4 weeks (28 days)
            days_ago = len(SAMPLE_ARTICLES) - i - 1
            created_at = base_time - timedelta(days=days_ago)
            
            article_doc = {
                "title": article_data["title"],
                "content": article_data["content"],
                "author": article_data["author"],
                "created_at": created_at,
                "updated_at": created_at
            }
            
            result = articles_collection.insert_one(article_doc)
            created_articles.append({
                "id": str(result.inserted_id),
                "title": article_data["title"]
            })
            print(f"Created article: {article_data['title']}")
        
        print(f"\nSuccessfully created {len(created_articles)} articles!")
        print(f"Total articles in database: {articles_collection.count_documents({})}")
        
        # Close the connection
        mongo_client.close()
        
    except Exception as e:
        logger.error(f"Error seeding articles: {str(e)}")
        print(f"Error seeding articles: {str(e)}")
        raise


if __name__ == "__main__":
    print("Starting article seeding...")
    print(f"Database: {Config.MONGO_DB_NAME}")
    
    # Get the adjusted URI (may convert Docker hostname to localhost)
    original_uri = Config.MONGO_URI
    adjusted_uri = get_mongo_uri()
    
    print(f"Original MongoDB URI: {original_uri}")
    if original_uri != adjusted_uri:
        print(f"Adjusted MongoDB URI: {adjusted_uri} (converted Docker hostname to localhost)")
    else:
        print(f"Using MongoDB URI: {adjusted_uri}")
    
    print("-" * 50)
    
    try:
        seed_articles()
        print("-" * 50)
        print("Seeding complete!")
    except Exception as e:
        print("-" * 50)
        print("Seeding failed!")
        if "getaddrinfo failed" in str(e) or "mongodb:" in str(e).lower():
            print("\n💡 TIP: If MongoDB is running locally, ensure your .env file has:")
            print("   MONGO_URI=mongodb://admin:hivepass123@localhost:27027/")
            print("\n   Or run MongoDB via Docker Compose and use the Docker hostname.")
        raise

