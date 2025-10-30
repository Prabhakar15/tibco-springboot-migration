"""Spring Boot configuration templates"""

JMS_CONFIG = '''package {package}.config;

import jakarta.jms.ConnectionFactory;
import org.apache.activemq.spring.ActiveMQConnectionFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.jndi.JndiObjectFactoryBean;
import org.springframework.jndi.JndiTemplate;

import java.util.Properties;

@Configuration
public class JmsConfig {{
    @Value("${{jms.jndi.url}}")
    private String jndiUrl;
    
    @Value("${{jms.jndi.contextFactory}}")
    private String contextFactory;
    
    @Value("${{jms.jndiConnectionFactory}}")
    private String jndiConnectionFactory;

    @Bean
    public JndiTemplate jndiTemplate() {{
        Properties props = new Properties();
        props.setProperty("java.naming.factory.initial", contextFactory);
        props.setProperty("java.naming.provider.url", jndiUrl);
        return new JndiTemplate(props);
    }}

    @Bean 
    public JndiObjectFactoryBean jmsConnectionFactory() {{
        JndiObjectFactoryBean factory = new JndiObjectFactoryBean();
        factory.setJndiTemplate(jndiTemplate());
        factory.setJndiName(jndiConnectionFactory);
        return factory;
    }}

    @Bean
    public JmsTemplate jmsTemplate() {{
        return new JmsTemplate((ConnectionFactory) jmsConnectionFactory().getObject());
    }}
}}
'''

REST_CONFIG = '''package {package}.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class RestConfig {{
    @Value("${{creditscore.base-url}}")
    private String creditScoreBaseUrl;

    @Bean
    public WebClient webClient() {{
        return WebClient.builder()
            .baseUrl(creditScoreBaseUrl)
            .build();
    }}
}}
'''