"use client";
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { sessionAPI } from "../lib/api";

interface ChatSession {
  id: string;
  title: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_message_at: string;
  message_count: number;
  last_message_preview: string;
}

interface SessionContextType {
  sessions: ChatSession[];
  currentSession: ChatSession | null;
  loading: boolean;
  createSession: (
    title?: string,
    description?: string
  ) => Promise<ChatSession | null>;
  selectSession: (session: ChatSession) => void;
  updateSession: (
    sessionId: string,
    title?: string,
    description?: string
  ) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  refreshSessions: () => Promise<void>;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({ children }: { children: ReactNode }) {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(
    null
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const sessionsData = await sessionAPI.getSessions();
      setSessions(sessionsData);

      // If no current session and sessions exist, select the first one
      if (!currentSession && sessionsData.length > 0) {
        setCurrentSession(sessionsData[0]);
      }
    } catch (error) {
      console.error("Failed to load sessions:", error);
    } finally {
      setLoading(false);
    }
  };

  const createSession = async (
    title = "New Chat",
    description?: string
  ): Promise<ChatSession | null> => {
    try {
      const newSession = await sessionAPI.createSession(title, description);
      setSessions((prev) => [newSession, ...prev]);
      setCurrentSession(newSession);
      return newSession;
    } catch (error) {
      console.error("Failed to create session:", error);
      return null;
    }
  };

  const selectSession = (session: ChatSession) => {
    setCurrentSession(session);
  };

  const updateSession = async (
    sessionId: string,
    title?: string,
    description?: string
  ) => {
    try {
      const updatedSession = await sessionAPI.updateSession(
        sessionId,
        title,
        description
      );
      setSessions((prev) =>
        prev.map((s) => (s.id === sessionId ? updatedSession : s))
      );
      if (currentSession?.id === sessionId) {
        setCurrentSession(updatedSession);
      }
    } catch (error) {
      console.error("Failed to update session:", error);
      throw error;
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      await sessionAPI.deleteSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));

      // If deleted session was current, select another
      if (currentSession?.id === sessionId) {
        const remainingSessions = sessions.filter((s) => s.id !== sessionId);
        setCurrentSession(
          remainingSessions.length > 0 ? remainingSessions[0] : null
        );
      }
    } catch (error) {
      console.error("Failed to delete session:", error);
      throw error;
    }
  };

  const refreshSessions = async () => {
    await loadSessions();
  };

  const value: SessionContextType = {
    sessions,
    currentSession,
    loading,
    createSession,
    selectSession,
    updateSession,
    deleteSession,
    refreshSessions,
  };

  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error("useSession must be used within a SessionProvider");
  }
  return context;
}
