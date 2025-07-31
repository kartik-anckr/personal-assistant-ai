-- Migration to make refresh_token nullable
-- Run this in your Supabase SQL editor

-- Make refresh_token nullable (since Google doesn't always provide it)
ALTER TABLE user_calendar_integrations 
ALTER COLUMN refresh_token DROP NOT NULL;

-- Verify the change
\d user_calendar_integrations; 