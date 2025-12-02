-- Supply Chain Database Initialization
-- This script sets up the initial database structure

-- Create extensions for async operations
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types for supply chain domain
CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled');
CREATE TYPE priority_level AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE risk_level AS ENUM ('low', 'medium', 'high', 'critical');

-- Create audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create sample data for development
INSERT INTO audit_log (user_id, action, table_name, record_id, new_values) 
VALUES 
(uuid_generate_v4(), 'INIT', 'SYSTEM', uuid_generate_v4(), '{"message": "Database initialized successfully"}')
ON CONFLICT DO NOTHING;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO supply_chain_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO supply_chain_user;