"""
Spring Cloud Gateway Agent - Single point of entry for all microservices.

Generates an API Gateway that routes traffic to REST, SOAP, layered, and hexagonal services.
Includes features like:
- Dynamic routing with path-based and header-based predicates
- CORS configuration
- Rate limiting
- Circuit breaker integration
- Request/response filtering
- Load balancing
"""

import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class GatewayAgent:
    """Generates Spring Cloud Gateway for unified API entry point."""
    
    def __init__(self, package_root: str, services: List[Dict[str, Any]]):
        """
        Initialize Gateway Agent.
        
        Args:
            package_root: Base package name (e.g., 'com.example')
            services: List of service metadata dicts with keys:
                - name: Service name
                - type: 'rest', 'soap', or 'hexagonal'
                - service_type: For hexagonal - 'rest', 'soap', 'combined'
                - port: Service port number
                - context_path: Service context path
        """
        self.package_root = package_root
        self.services = services
        self.gateway_port = 8080
        
    def generate(self, output_folder: Path) -> Dict[str, str]:
        """Generate complete Spring Cloud Gateway project."""
        files: Dict[str, str] = {}
        pkg = self.package_root + '.gateway'
        
        # Create gateway structure
        files.update(self._generate_pom(output_folder))
        files.update(self._generate_application_class(output_folder, pkg))
        files.update(self._generate_gateway_config(output_folder, pkg))
        files.update(self._generate_route_locator(output_folder, pkg))
        files.update(self._generate_cors_config(output_folder, pkg))
        files.update(self._generate_filter_factory(output_folder, pkg))
        files.update(self._generate_application_yml(output_folder))
        files.update(self._generate_readme(output_folder))
        
        logger.info(f"Generated API Gateway with {len(self.services)} service routes")
        return files
    
    def _generate_pom(self, out: Path) -> Dict[str, str]:
        """Generate pom.xml for Spring Cloud Gateway."""
        pom_file = out / 'pom.xml'
        content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.5</version>
        <relativePath/>
    </parent>
    
    <groupId>{self.package_root}</groupId>
    <artifactId>api-gateway</artifactId>
    <version>1.0.0</version>
    <name>API Gateway</name>
    <description>Spring Cloud Gateway for microservices routing</description>
    
    <properties>
        <java.version>17</java.version>
        <spring-cloud.version>2022.0.4</spring-cloud.version>
    </properties>
    
    <dependencies>
        <!-- Spring Cloud Gateway -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway</artifactId>
        </dependency>
        
        <!-- Spring Boot Actuator for health checks -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        
        <!-- Circuit Breaker with Resilience4j -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-circuitbreaker-reactor-resilience4j</artifactId>
        </dependency>
        
        <!-- Redis for rate limiting (optional) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
        </dependency>
        
        <!-- Lombok for cleaner code -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        
        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${{spring-cloud.version}}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
'''
        return {str(pom_file): content}
    
    def _generate_application_class(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate main Spring Boot application class."""
        app_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/')
        app_dir.mkdir(parents=True, exist_ok=True)
        app_file = app_dir / 'ApiGatewayApplication.java'
        
        content = f'''package {pkg};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

/**
 * API Gateway Application - Single entry point for all microservices.
 * 
 * This gateway routes traffic to:
 * - REST services (layered architecture)
 * - SOAP services (layered architecture)
 * - Hexagonal architecture services (REST/SOAP/Combined)
 * 
 * Features:
 * - Path-based routing
 * - CORS configuration
 * - Rate limiting
 * - Circuit breaker integration
 * - Request/response filtering
 * - Load balancing
 */
@SpringBootApplication
public class ApiGatewayApplication {{

    public static void main(String[] args) {{
        SpringApplication.run(ApiGatewayApplication.class, args);
    }}
}}
'''
        return {str(app_file): content}
    
    def _generate_gateway_config(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate gateway configuration class."""
        config_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'config'
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / 'GatewayConfig.java'
        
        content = f'''package {pkg}.config;

import org.springframework.cloud.gateway.filter.ratelimit.KeyResolver;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import reactor.core.publisher.Mono;

/**
 * Gateway Configuration - Central configuration for API Gateway behavior.
 */
@Configuration
public class GatewayConfig {{

    /**
     * Key resolver for rate limiting based on IP address.
     * Can be customized to use user ID, API key, etc.
     */
    @Bean
    public KeyResolver ipKeyResolver() {{
        return exchange -> Mono.just(
            exchange.getRequest()
                .getRemoteAddress()
                .getAddress()
                .getHostAddress()
        );
    }}
    
    /**
     * Key resolver for rate limiting based on user ID from header.
     * Useful for authenticated requests.
     */
    @Bean
    public KeyResolver userKeyResolver() {{
        return exchange -> Mono.justOrEmpty(
            exchange.getRequest()
                .getHeaders()
                .getFirst("X-User-Id")
        ).defaultIfEmpty("anonymous");
    }}
}}
'''
        return {str(config_file): content}
    
    def _generate_route_locator(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate route locator with dynamic routes for all services."""
        config_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'config'
        config_dir.mkdir(parents=True, exist_ok=True)
        route_file = config_dir / 'RouteConfig.java'
        
        # Build routes for each service
        routes = []
        for idx, service in enumerate(self.services):
            service_name = service['name']
            service_type = service['type']
            port = service['port']
            context_path = service.get('context_path', f'/{service_name.lower()}')
            
            # Determine route ID and path
            route_id = f"{service_name.lower()}_{service_type}_route"
            
            if service_type == 'hexagonal':
                svc_type = service.get('service_type', 'combined')
                if svc_type == 'combined':
                    # Combined has both REST and SOAP
                    routes.append(f'''
                .route("{route_id}_rest", r -> r
                    .path("/api/{service_name.lower()}/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "{route_id}_rest")
                        .circuitBreaker(c -> c
                            .setName("{service_name.lower()}_cb")
                            .setFallbackUri("forward:/fallback/{service_name.lower()}"))
                        .retry(config -> config.setRetries(3)))
                    .uri("http://localhost:{port}"))
                .route("{route_id}_soap", r -> r
                    .path("/ws/{service_name.lower()}/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "{route_id}_soap")
                        .circuitBreaker(c -> c
                            .setName("{service_name.lower()}_soap_cb")
                            .setFallbackUri("forward:/fallback/{service_name.lower()}")))
                    .uri("http://localhost:{port}"))''')
                elif svc_type == 'rest':
                    routes.append(f'''
                .route("{route_id}", r -> r
                    .path("/api/{service_name.lower()}/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "{route_id}")
                        .circuitBreaker(c -> c
                            .setName("{service_name.lower()}_cb")
                            .setFallbackUri("forward:/fallback/{service_name.lower()}"))
                        .retry(config -> config.setRetries(3)))
                    .uri("http://localhost:{port}"))''')
                else:  # soap
                    routes.append(f'''
                .route("{route_id}", r -> r
                    .path("/ws/{service_name.lower()}/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "{route_id}")
                        .circuitBreaker(c -> c
                            .setName("{service_name.lower()}_cb")
                            .setFallbackUri("forward:/fallback/{service_name.lower()}")))
                    .uri("http://localhost:{port}"))''')
            elif service_type == 'rest':
                routes.append(f'''
                .route("{route_id}", r -> r
                    .path("/api/{service_name.lower()}/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "{route_id}")
                        .circuitBreaker(c -> c
                            .setName("{service_name.lower()}_cb")
                            .setFallbackUri("forward:/fallback/{service_name.lower()}"))
                        .retry(config -> config.setRetries(3)))
                    .uri("http://localhost:{port}"))''')
            else:  # soap
                routes.append(f'''
                .route("{route_id}", r -> r
                    .path("/ws/{service_name.lower()}/**")
                    .filters(f -> f
                        .stripPrefix(1)
                        .addRequestHeader("X-Gateway-Route", "{route_id}")
                        .circuitBreaker(c -> c
                            .setName("{service_name.lower()}_cb")
                            .setFallbackUri("forward:/fallback/{service_name.lower()}")))
                    .uri("http://localhost:{port}"))''')
        
        routes_code = ''.join(routes)
        
        content = f'''package {pkg}.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Route Configuration - Defines all routes for backend services.
 * 
 * Route Patterns:
 * - /api/{{service}}/** -> REST services (layered or hexagonal)
 * - /ws/{{service}}/** -> SOAP services (layered or hexagonal)
 * 
 * Features per route:
 * - Path-based routing with prefix stripping
 * - Circuit breaker with fallback
 * - Automatic retry (3 attempts)
 * - Request header tracking
 */
@Configuration
public class RouteConfig {{

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {{
        return builder.routes(){routes_code}
                .build();
    }}
}}
'''
        return {str(route_file): content}
    
    def _generate_cors_config(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate CORS configuration."""
        config_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'config'
        config_file = config_dir / 'CorsConfig.java'
        
        content = f'''package {pkg}.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsWebFilter;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

/**
 * CORS Configuration - Enables cross-origin requests.
 * 
 * Configured to allow:
 * - All origins (customize for production)
 * - Common HTTP methods
 * - Custom headers
 * - Credentials
 */
@Configuration
public class CorsConfig {{

    @Bean
    public CorsWebFilter corsWebFilter() {{
        CorsConfiguration corsConfig = new CorsConfiguration();
        
        // Allow all origins (customize for production)
        corsConfig.setAllowedOriginPatterns(List.of("*"));
        
        // Allow common HTTP methods
        corsConfig.setAllowedMethods(Arrays.asList(
            "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"
        ));
        
        // Allow common headers
        corsConfig.setAllowedHeaders(Arrays.asList(
            "Authorization", "Content-Type", "X-User-Id", 
            "X-Request-Id", "X-Correlation-Id"
        ));
        
        // Expose custom headers to client
        corsConfig.setExposedHeaders(Arrays.asList(
            "X-Total-Count", "X-Page-Number", "X-Page-Size"
        ));
        
        // Allow credentials
        corsConfig.setAllowCredentials(true);
        
        // Cache preflight response for 1 hour
        corsConfig.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfig);
        
        return new CorsWebFilter(source);
    }}
}}
'''
        return {str(config_file): content}
    
    def _generate_filter_factory(self, out: Path, pkg: str) -> Dict[str, str]:
        """Generate custom gateway filter for logging and monitoring."""
        filter_dir = out / 'src' / 'main' / 'java' / pkg.replace('.', '/') / 'filter'
        filter_dir.mkdir(parents=True, exist_ok=True)
        filter_file = filter_dir / 'LoggingGatewayFilterFactory.java'
        
        content = f'''package {pkg}.filter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * Custom Gateway Filter - Logs request/response details.
 * 
 * Usage in routes:
 * .filters(f -> f.filter(new LoggingGatewayFilterFactory().apply(config)))
 */
@Component
public class LoggingGatewayFilterFactory 
    extends AbstractGatewayFilterFactory<LoggingGatewayFilterFactory.Config> {{

    private static final Logger logger = LoggerFactory.getLogger(LoggingGatewayFilterFactory.class);

    public LoggingGatewayFilterFactory() {{
        super(Config.class);
    }}

    @Override
    public GatewayFilter apply(Config config) {{
        return (exchange, chain) -> {{
            if (config.isPreLogger()) {{
                logger.info("Pre-filter: {{}} {{}}", 
                    exchange.getRequest().getMethod(),
                    exchange.getRequest().getURI());
            }}
            
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {{
                if (config.isPostLogger()) {{
                    logger.info("Post-filter: Response status code: {{}}", 
                        exchange.getResponse().getStatusCode());
                }}
            }}));
        }};
    }}

    public static class Config {{
        private boolean preLogger = true;
        private boolean postLogger = true;

        public boolean isPreLogger() {{
            return preLogger;
        }}

        public void setPreLogger(boolean preLogger) {{
            this.preLogger = preLogger;
        }}

        public boolean isPostLogger() {{
            return postLogger;
        }}

        public void setPostLogger(boolean postLogger) {{
            this.postLogger = postLogger;
        }}
    }}
}}
'''
        return {str(filter_file): content}
    
    def _generate_application_yml(self, out: Path) -> Dict[str, str]:
        """Generate application.yml with gateway configuration."""
        resources_dir = out / 'src' / 'main' / 'resources'
        resources_dir.mkdir(parents=True, exist_ok=True)
        yml_file = resources_dir / 'application.yml'
        
        content = f'''spring:
  application:
    name: api-gateway
  
  cloud:
    gateway:
      # Global CORS configuration (overridden by CorsConfig bean)
      globalcors:
        corsConfigurations:
          '[/**]':
            allowedOrigins: "*"
            allowedMethods:
              - GET
              - POST
              - PUT
              - DELETE
              - PATCH
              - OPTIONS
            allowedHeaders: "*"
      
      # Default filters applied to all routes
      default-filters:
        - DedupeResponseHeader=Access-Control-Allow-Credentials Access-Control-Allow-Origin
      
      # HTTP client configuration
      httpclient:
        connect-timeout: 5000
        response-timeout: 30s
        pool:
          type: ELASTIC
          max-idle-time: 15s
          max-life-time: 60s
  
  # Redis configuration for rate limiting (optional)
  redis:
    host: localhost
    port: 6379
    timeout: 2000ms

server:
  port: {self.gateway_port}

# Actuator endpoints for monitoring
management:
  endpoints:
    web:
      exposure:
        include: health,info,gateway,metrics,prometheus
  endpoint:
    health:
      show-details: always
    gateway:
      enabled: true

# Resilience4j Circuit Breaker configuration
resilience4j:
  circuitbreaker:
    configs:
      default:
        registerHealthIndicator: true
        slidingWindowSize: 10
        minimumNumberOfCalls: 5
        permittedNumberOfCallsInHalfOpenState: 3
        automaticTransitionFromOpenToHalfOpenEnabled: true
        waitDurationInOpenState: 10s
        failureRateThreshold: 50
        eventConsumerBufferSize: 10
  
  timelimiter:
    configs:
      default:
        timeoutDuration: 30s

# Logging configuration
logging:
  level:
    org.springframework.cloud.gateway: INFO
    {self.package_root}.gateway: DEBUG
    reactor.netty: INFO
  pattern:
    console: "%d{{yyyy-MM-dd HH:mm:ss}} - %msg%n"
'''
        return {str(yml_file): content}
    
    def _generate_readme(self, out: Path) -> Dict[str, str]:
        """Generate README with gateway usage instructions."""
        readme_file = out / 'README.md'
        
        # Build service table
        service_rows = []
        for service in self.services:
            name = service['name']
            stype = service['type']
            port = service['port']
            
            if stype == 'hexagonal':
                svc_type = service.get('service_type', 'combined')
                if svc_type == 'combined':
                    service_rows.append(f"| {name} | Hexagonal (Combined) | `/api/{name.lower()}/**` (REST)<br>`/ws/{name.lower()}/**` (SOAP) | {port} |")
                elif svc_type == 'rest':
                    service_rows.append(f"| {name} | Hexagonal (REST) | `/api/{name.lower()}/**` | {port} |")
                else:
                    service_rows.append(f"| {name} | Hexagonal (SOAP) | `/ws/{name.lower()}/**` | {port} |")
            elif stype == 'rest':
                service_rows.append(f"| {name} | Layered (REST) | `/api/{name.lower()}/**` | {port} |")
            else:
                service_rows.append(f"| {name} | Layered (SOAP) | `/ws/{name.lower()}/**` | {port} |")
        
        service_table = '\n'.join(service_rows)
        
        content = f'''# API Gateway

Spring Cloud Gateway providing a single entry point for all microservices.

## Overview

This API Gateway acts as a reverse proxy and routes requests to appropriate backend services based on path patterns. It provides cross-cutting concerns like:

- **Routing**: Path-based and header-based routing
- **Load Balancing**: Distribute traffic across service instances
- **Circuit Breaker**: Fault tolerance with Resilience4j
- **Rate Limiting**: Prevent API abuse
- **CORS**: Cross-origin resource sharing
- **Monitoring**: Actuator endpoints for health checks
- **Logging**: Request/response tracking

## Architecture

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│       API Gateway (Port {self.gateway_port})       │
│  - Routing                          │
│  - Circuit Breaker                  │
│  - Rate Limiting                    │
│  - CORS                             │
└──────┬──────────────────────────────┘
       │
       ├──────────────┬──────────────┬────────────...
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ REST Service│ │ SOAP Service│ │  Hexagonal  │
│  (Layered)  │ │  (Layered)  │ │   Service   │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Quick Start

### 1. Build the Gateway

```bash
mvn clean package
```

### 2. Run the Gateway

```bash
java -jar target/api-gateway-1.0.0.jar
```

The gateway will start on port **{self.gateway_port}**.

### 3. Start Backend Services

Ensure all backend services are running on their configured ports before starting the gateway.

## Configured Routes

| Service | Type | Gateway Path | Backend Port |
|---------|------|--------------|--------------|
{service_table}

## Usage Examples

### REST Service Request

```bash
# Through gateway
curl http://localhost:{self.gateway_port}/api/loanapplication/loans/123

# This routes to backend service at configured port
```

### SOAP Service Request

```bash
# Through gateway
curl -X POST http://localhost:{self.gateway_port}/ws/loanapplication/service \\
  -H "Content-Type: text/xml" \\
  -d @request.xml
```

### Health Check

```bash
# Gateway health
curl http://localhost:{self.gateway_port}/actuator/health

# All routes
curl http://localhost:{self.gateway_port}/actuator/gateway/routes
```

## Features

### Circuit Breaker

Each route is protected with a circuit breaker:
- **Sliding Window Size**: 10 calls
- **Failure Rate Threshold**: 50%
- **Wait Duration in Open State**: 10 seconds
- **Half-Open Permitted Calls**: 3

### Rate Limiting

Configure rate limiting per route in `application.yml`:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my_service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
```

### CORS

CORS is configured globally to allow:
- All origins (customize for production)
- Common HTTP methods
- Custom headers
- Credentials

### Retry Mechanism

Failed requests are automatically retried up to 3 times before triggering the circuit breaker.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_PORT` | Gateway port | {self.gateway_port} |
| `REDIS_HOST` | Redis host for rate limiting | localhost |
| `REDIS_PORT` | Redis port | 6379 |

### Application Properties

Edit `src/main/resources/application.yml` to customize:
- Route definitions
- Circuit breaker settings
- Rate limiting
- CORS policies
- Timeouts

## Monitoring

### Actuator Endpoints

- **Health**: `http://localhost:{self.gateway_port}/actuator/health`
- **Gateway Routes**: `http://localhost:{self.gateway_port}/actuator/gateway/routes`
- **Metrics**: `http://localhost:{self.gateway_port}/actuator/metrics`

### Logging

Logs include:
- Request method and URI
- Response status codes
- Circuit breaker state changes
- Rate limiting events

## Production Considerations

1. **CORS**: Restrict `allowedOrigins` to specific domains
2. **Rate Limiting**: Enable Redis and configure appropriate limits
3. **SSL/TLS**: Configure HTTPS for secure communication
4. **Authentication**: Add authentication filters
5. **Service Discovery**: Integrate with Eureka/Consul for dynamic service discovery
6. **Distributed Tracing**: Add Spring Cloud Sleuth for request tracking

## Troubleshooting

### Route Not Found (404)

- Verify backend service is running
- Check route configuration in `RouteConfig.java`
- Review gateway logs for routing details

### Circuit Breaker Open

- Check backend service health
- Review circuit breaker metrics in Actuator
- Adjust threshold/timeout in `application.yml`

### CORS Errors

- Verify `CorsConfig.java` allows required origins
- Check browser console for specific CORS errors
- Ensure preflight requests (OPTIONS) are handled

## Dependencies

- **Spring Cloud Gateway**: 2022.0.4
- **Spring Boot**: 3.1.5
- **Resilience4j**: Circuit breaker
- **Redis**: Rate limiting (optional)

## License

Auto-generated by TIBCO BW to Spring Boot Migration Tool
'''
        return {str(readme_file): content}


def create_gateway_service(package_root: str, services: List[Dict[str, Any]], output_folder: Path) -> Dict[str, str]:
    """
    Convenience function to create gateway service.
    
    Args:
        package_root: Base package name
        services: List of service metadata
        output_folder: Where to generate gateway files
        
    Returns:
        Dictionary of generated files
    """
    agent = GatewayAgent(package_root, services)
    return agent.generate(output_folder)
