package com.loan.gateway.filter;

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
    extends AbstractGatewayFilterFactory<LoggingGatewayFilterFactory.Config> {

    private static final Logger logger = LoggerFactory.getLogger(LoggingGatewayFilterFactory.class);

    public LoggingGatewayFilterFactory() {
        super(Config.class);
    }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            if (config.isPreLogger()) {
                logger.info("Pre-filter: {} {}", 
                    exchange.getRequest().getMethod(),
                    exchange.getRequest().getURI());
            }
            
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                if (config.isPostLogger()) {
                    logger.info("Post-filter: Response status code: {}", 
                        exchange.getResponse().getStatusCode());
                }
            }));
        };
    }

    public static class Config {
        private boolean preLogger = true;
        private boolean postLogger = true;

        public boolean isPreLogger() {
            return preLogger;
        }

        public void setPreLogger(boolean preLogger) {
            this.preLogger = preLogger;
        }

        public boolean isPostLogger() {
            return postLogger;
        }

        public void setPostLogger(boolean postLogger) {
            this.postLogger = postLogger;
        }
    }
}
