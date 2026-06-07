# 🚀 Deployment Guide

## Production Deployment

### Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (optional)
- Cloud provider account (AWS/GCP/Azure)
- Domain name and SSL certificate

### Environment Setup

1. **Clone the repository**
```bash
git clone https://github.com/Styljshioker/faceless-platform.git
cd faceless-platform
```

2. **Configure environment variables**
```bash
cp .env.production.example .env.production
# Edit .env.production with your settings
```

3. **Build the application**
```bash
docker-compose -f docker-compose.prod.yml build
```

### Docker Deployment

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Kubernetes Deployment

```bash
# Apply configurations
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n faceless-platform

# Get service URLs
kubectl get services -n faceless-platform
```

### Database Migration

```bash
# Run migrations
docker-compose exec api npm run migrate

# Seed initial data
docker-compose exec api npm run seed
```

### SSL Configuration

```bash
# Using Let's Encrypt with Certbot
certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

### Monitoring

- **Application**: Prometheus + Grafana
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Uptime**: Pingdom or StatusCake
- **Errors**: Sentry integration

### Performance Optimization

1. **CDN Configuration**
   - CloudFlare for static assets
   - AWS CloudFront for video content

2. **Caching Strategy**
   - Redis for session data
   - Memcached for query results
   - Browser caching headers

3. **Database Optimization**
   - Read replicas for analytics
   - Connection pooling
   - Query optimization

### Backup Strategy

```bash
# Database backup
docker-compose exec postgres pg_dump -U postgres faceless_platform > backup.sql

# File backup to S3
aws s3 sync /app/storage s3://faceless-platform-backups/$(date +%Y%m%d)/
```

### Security Checklist

- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] API rate limiting enabled
- [ ] CORS headers set
- [ ] Content Security Policy configured
- [ ] Regular security updates

### Health Checks

```bash
# Application health
curl https://api.yourdomain.com/health

# Database connection
curl https://api.yourdomain.com/health/database

# External services
curl https://api.yourdomain.com/health/services
```

### Scaling

**Horizontal Scaling:**
```bash
# Scale API servers
kubectl scale deployment api --replicas=5

# Scale workers
kubectl scale deployment workers --replicas=10
```

**Vertical Scaling:**
```yaml
# In k8s deployment
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

### Troubleshooting

**Common Issues:**

1. **Database connection timeout**
   ```bash
   # Check database status
   kubectl get pods -l app=postgres
   kubectl logs -l app=postgres
   ```

2. **High memory usage**
   ```bash
   # Check resource usage
   kubectl top pods
   kubectl top nodes
   ```

3. **Slow API responses**
   ```bash
   # Enable debug logging
   kubectl set env deployment/api DEBUG=true
   ```

### Maintenance

**Rolling Updates:**
```bash
# Update application
kubectl set image deployment/api api=faceless-platform:v1.1.0

# Check rollout status
kubectl rollout status deployment/api
```

**Backup Restoration:**
```bash
# Restore database
docker-compose exec postgres psql -U postgres -c "DROP DATABASE faceless_platform;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE faceless_platform;"
docker-compose exec postgres psql -U postgres faceless_platform < backup.sql
```

For more detailed deployment instructions, see our [Infrastructure Guide](https://docs.facelessplatform.com/infrastructure).