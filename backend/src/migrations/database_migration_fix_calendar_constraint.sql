-- Migration script to fix calendar integration constraint
-- Run this in your Supabase SQL editor if you've already created the original table

-- Drop the old constraint (if it exists)
ALTER TABLE user_calendar_integrations 
DROP CONSTRAINT IF EXISTS user_calendar_integrations_user_id_provider_calendar_id_key;

-- Add the new constraint (user_id, provider only)
ALTER TABLE user_calendar_integrations 
ADD CONSTRAINT user_calendar_integrations_user_id_provider_key 
UNIQUE (user_id, provider);

-- Verify the constraint was created
SELECT conname, contype, pg_get_constraintdef(oid) 
FROM pg_constraint 
WHERE conrelid = 'user_calendar_integrations'::regclass 
AND contype = 'u'; 