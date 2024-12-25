## Changelog
Version 1.1.0
- Docker containers now use volumes to write logs to central location on host server
- Performance monitor now controlled by environment variable `ENABLE_MONITORING`
- Flask now is started via entrypoint scripts located in /app directory

Verion 1.0.0
- Flask now runs as a load-balanced service using Docker and Nginx
- Backwards compatability ensured with legacy routes supported

Version 0.9.0
- Added /commands route to support Simba GUI mode
- Created infrastructure for load-balancing Flask using Docker and Nginx

Version 0.8.0
- Migrated flask to a blueprints scheme for better code organization

## TODO
- [ ] Create read-only mode for automated testing
- [ ] Create automated tests
- [ ] Create CI/CD pipeline to test before release / upon new push
- [X] Create stress tests
- [X] Create post-stress test DB cleanup script
- [X] Ensure logs get written to filesystem and not inside containers
- [X] Migrate all legacy logic to new single/batch model