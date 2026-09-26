-- StockSense PostgreSQL Database Creation Script
SELECT 'CREATE DATABASE stocksense_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'stocksense_db')\gexec
