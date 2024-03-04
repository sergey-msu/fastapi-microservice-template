# InvestApp: Auth microservice

Auth microservice based on JWT with MongoDB as a backend DB.
Hidden from outside in prod environment.

Layered architecture:
- api endpoints layer
- services lauer
- data layer

Hierarchical configuration: config.[dev|prod|...].yaml is merged to common config.yaml
Secrets are taken from environment variables.

Dependency injection via dependency_injector lib.
