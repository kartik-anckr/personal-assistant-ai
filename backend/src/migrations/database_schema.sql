-- Supabase Users Table Schema
-- Run this SQL in your Supabase SQL Editor to create the users table

-- Users table for authentication and profile management
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_users_created_at ON users(created_at);

-- RLS (Row Level Security) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see and update their own data
CREATE POLICY "Users can view own profile" ON users FOR SELECT USING (id = auth.uid());
CREATE POLICY "Users can update own profile" ON users FOR UPDATE USING (id = auth.uid());

-- User calendar integrations table
CREATE TABLE user_calendar_integrations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL DEFAULT 'google',
    calendar_id VARCHAR(255),
    calendar_name VARCHAR(255),
    access_token TEXT NOT NULL, -- Encrypted
    refresh_token TEXT, -- Encrypted (can be NULL for subsequent OAuth flows)
    token_expires_at TIMESTAMP WITH TIME ZONE,
    scope VARCHAR(500), -- Granted permissions
    is_active BOOLEAN DEFAULT true,
    connected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, provider)
);

-- Indexes for performance
CREATE INDEX idx_calendar_user_id ON user_calendar_integrations(user_id);
CREATE INDEX idx_calendar_active ON user_calendar_integrations(is_active);
CREATE INDEX idx_calendar_provider ON user_calendar_integrations(provider);

-- RLS policies
ALTER TABLE user_calendar_integrations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own calendar integrations"
    ON user_calendar_integrations FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users can update own calendar integrations"
    ON user_calendar_integrations FOR UPDATE USING (user_id = auth.uid());

-- Log of created calendar events for tracking
CREATE TABLE calendar_events_log (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    integration_id UUID NOT NULL REFERENCES user_calendar_integrations(id),
    event_id VARCHAR(255) NOT NULL, -- Google event ID
    event_title VARCHAR(255),
    event_description TEXT,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    created_via_prompt TEXT, -- Original user prompt
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_events_user_id ON calendar_events_log(user_id);
CREATE INDEX idx_events_integration ON calendar_events_log(integration_id); 