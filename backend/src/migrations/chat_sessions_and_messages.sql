-- Chat Session Management Database Schema
-- Add this migration after the existing database_schema.sql

-- Chat sessions for organizing conversations
CREATE TABLE chat_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL DEFAULT 'New Chat',
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_message_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_sessions_active ON chat_sessions(is_active);
CREATE INDEX idx_sessions_last_message ON chat_sessions(last_message_at DESC);
CREATE INDEX idx_sessions_updated_at ON chat_sessions(updated_at DESC);

-- RLS policies
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own sessions" ON chat_sessions FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users can create own sessions" ON chat_sessions FOR INSERT WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users can update own sessions" ON chat_sessions FOR UPDATE USING (user_id = auth.uid());
CREATE POLICY "Users can delete own sessions" ON chat_sessions FOR DELETE USING (user_id = auth.uid());

-- Individual messages within chat sessions
CREATE TABLE chat_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}', -- For storing tool calls, agent info, etc.
    message_order INTEGER NOT NULL, -- Sequence within session
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_messages_role ON chat_messages(role);
CREATE INDEX idx_messages_order ON chat_messages(session_id, message_order);
CREATE INDEX idx_messages_created_at ON chat_messages(created_at);

-- Ensure message order uniqueness within session
CREATE UNIQUE INDEX idx_messages_session_order ON chat_messages(session_id, message_order);

-- RLS policies
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own messages" ON chat_messages FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users can create own messages" ON chat_messages FOR INSERT WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users can update own messages" ON chat_messages FOR UPDATE USING (user_id = auth.uid());

-- View for session statistics and latest message preview
CREATE VIEW session_stats AS
SELECT
    s.id,
    s.user_id,
    s.title,
    s.description,
    s.is_active,
    s.created_at,
    s.updated_at,
    s.last_message_at,
    COUNT(m.id) as message_count,
    COALESCE(
        (SELECT content FROM chat_messages WHERE session_id = s.id ORDER BY message_order DESC LIMIT 1),
        'No messages yet'
    ) as last_message_preview
FROM chat_sessions s
LEFT JOIN chat_messages m ON s.id = m.session_id
GROUP BY s.id, s.user_id, s.title, s.description, s.is_active, s.created_at, s.updated_at, s.last_message_at; 