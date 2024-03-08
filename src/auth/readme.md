# ExampleApp: Auth microservice

Auth microservice based on JWT with MongoDB as a backend DB.
Hidden from outside in prod environment.

Layered architecture:
- **api/** - api endpoints layer
- **services/** - services (business) layer
- **data/** - data layer

Also:
- **domain/** - all domain core business logic

Hierarchical configuration: config.[dev|prod|...].yaml is merged to common config.yaml
Secrets are taken from environment variables.

Dependency injection via dependency_injector lib.
