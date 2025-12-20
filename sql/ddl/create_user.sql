 CREATE USER 'claude'@'localhost' IDENTIFIED BY 'inv2025';
  GRANT ALL PRIVILEGES ON inventarium.* TO 'claude'@'localhost';
  FLUSH PRIVILEGES;

