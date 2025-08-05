/**
 * Protected chat page with session management
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useSession } from "@/contexts/SessionContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { chatAPI, sessionAPI } from "@/lib/api";
import {
  LogOut,
  User,
  Bot,
  Calendar,
  Cloud,
  Plus,
  MessageSquare,
  Trash2,
} from "lucide-react";
import toast from "react-hot-toast";
import { CalendarIntegration } from "@/components/calendar/CalendarIntegration";
import UpcomingMeetings from "@/components/calendar/UpcomingMeetings";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const { user, signout, loading } = useAuth();
  const {
    currentSession,
    sessions,
    createSession,
    selectSession,
    deleteSession,
  } = useSession();
  const router = useRouter();
  const [message, setMessage] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth/signin");
    }
  }, [user, loading, router]);

  // Load session messages when current session changes
  useEffect(() => {
    if (currentSession) {
      loadSessionMessages(currentSession.id);
    } else {
      setChatHistory([]);
    }
  }, [currentSession]);

  const loadSessionMessages = async (sessionId: string) => {
    try {
      const messages = await sessionAPI.getSessionMessages(sessionId);
      const formattedMessages: ChatMessage[] = messages.map(
        (msg: { role: string; content: string; created_at: string }) => ({
          role: msg.role as "user" | "assistant",
          content: msg.content,
          timestamp: new Date(msg.created_at),
        })
      );
      setChatHistory(formattedMessages);
    } catch (error) {
      console.error("Failed to load session messages:", error);
      toast.error("Failed to load conversation history");
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: message,
      timestamp: new Date(),
    };

    setChatHistory((prev) => [...prev, userMessage]);
    const currentMessage = message;
    setMessage("");

    try {
      setChatLoading(true);

      // Use current session or create new one
      let sessionId = currentSession?.id;
      if (!sessionId) {
        const newSession = await createSession(
          `Chat ${currentMessage.slice(0, 30)}...`
        );
        sessionId = newSession?.id;
      }

      const result = await chatAPI.sendMessage(currentMessage, sessionId);

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: result.response,
        timestamp: new Date(),
      };

      setChatHistory((prev) => [...prev, assistantMessage]);
    } catch (error) {
      toast.error("Failed to send message");
      console.error("Chat error:", error);
    } finally {
      setChatLoading(false);
    }
  };

  const handleSignout = () => {
    signout();
    router.push("/auth/signin");
  };

  const handleNewChat = async () => {
    try {
      await createSession();
      toast.success("New chat session created");
    } catch {
      toast.error("Failed to create new chat");
    }
  };

  const handleDeleteSession = async (sessionId: string) => {
    try {
      await deleteSession(sessionId);
      toast.success("Session deleted successfully");
    } catch {
      toast.error("Failed to delete session");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Session Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col max-h-screen">
        {/* Session management UI */}
        <div className="p-4 border-b border-gray-200 flex-shrink-0">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-medium text-gray-900">Chat Sessions</h2>
            <div className="flex items-center space-x-2">
              <User className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-600">
                {user?.username || "User"}
              </span>
            </div>
          </div>
          <button
            onClick={handleNewChat}
            className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Chat
          </button>
        </div>

        {/* Sessions list */}
        <div className="flex-1 overflow-y-auto min-h-0">
          {sessions.map((session) => (
            <div
              key={session.id}
              className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 ${
                currentSession?.id === session.id
                  ? "bg-blue-50 border-l-4 border-l-blue-600"
                  : ""
              }`}
            >
              <div
                className="flex items-center justify-between"
                onClick={() => selectSession(session)}
              >
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-gray-900 truncate">
                    {session.title}
                  </div>
                  <div className="text-sm text-gray-500 truncate mt-1">
                    {session.last_message_preview}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">
                    {session.message_count} messages
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteSession(session.id);
                  }}
                  className="ml-2 p-1 text-gray-400 hover:text-red-600 transition-colors"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Available Agents Section */}
        <div className="p-4 border-t border-gray-200 flex-shrink-0">
          <h3 className="text-sm font-medium text-gray-900 mb-3">
            Available Agents
          </h3>
          <div className="grid grid-cols-3 gap-2">
            <div className="flex flex-col items-center p-2 bg-blue-50 rounded-lg">
              <Cloud className="h-4 w-4 text-blue-500 mb-1" />
              <span className="text-xs text-gray-600">Weather</span>
            </div>
            <div className="flex flex-col items-center p-2 bg-green-50 rounded-lg">
              <MessageSquare className="h-4 w-4 text-green-500 mb-1" />
              <span className="text-xs text-gray-600">Slack</span>
            </div>
            <div className="flex flex-col items-center p-2 bg-purple-50 rounded-lg">
              <Calendar className="h-4 w-4 text-purple-500 mb-1" />
              <span className="text-xs text-gray-600">Calendar</span>
            </div>
          </div>
        </div>

        {/* Calendar Integration in Sidebar */}
        <div className="p-4 border-t border-gray-200 flex-shrink-0">
          <CalendarIntegration />
        </div>

        {/* Upcoming Meetings Widget - Made more compact */}
        <div className="p-4 border-t border-gray-200 flex-shrink-0 max-h-64 overflow-y-auto">
          <UpcomingMeetings query="today" autoRefresh={true} />
        </div>

        {/* Signout button */}
        <div className="p-4 border-t border-gray-200 flex-shrink-0">
          <button
            onClick={handleSignout}
            className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            <LogOut className="h-4 w-4 mr-2" />
            Sign Out
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <MessageSquare className="h-6 w-6 text-blue-600" />
              <h1 className="text-xl font-semibold text-gray-900">
                {currentSession?.title || "Select a chat session"}
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="grid grid-cols-3 gap-2">
                <div className="flex items-center space-x-1 text-xs text-gray-600">
                  <Cloud className="h-3 w-3 text-blue-500" />
                  <span>Weather</span>
                </div>
                <div className="flex items-center space-x-1 text-xs text-gray-600">
                  <MessageSquare className="h-3 w-3 text-green-500" />
                  <span>Slack</span>
                </div>
                <div className="flex items-center space-x-1 text-xs text-gray-600">
                  <Calendar className="h-3 w-3 text-purple-500" />
                  <span>Calendar</span>
                </div>
              </div>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Nexus AI v3.0
              </span>
            </div>
          </div>
        </div>

        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto p-6">
          {chatHistory.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <Bot className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              {currentSession ? (
                <>
                  <p>Start a conversation with your AI assistant!</p>
                  <p className="text-sm mt-2">
                    Try: &quot;What&apos;s the weather in Tokyo?&quot;,
                    &quot;Send a message to team&quot;, or &quot;Schedule
                    meeting tomorrow at 3pm&quot;
                  </p>
                </>
              ) : (
                <p>Select or create a chat session to start conversing!</p>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {chatHistory.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-3xl px-4 py-2 rounded-lg ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-white text-gray-900 shadow-sm border border-gray-200"
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                    <div
                      className={`text-xs mt-2 ${
                        msg.role === "user" ? "text-blue-100" : "text-gray-500"
                      }`}
                    >
                      {msg.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              ))}

              {chatLoading && (
                <div className="text-left mb-4">
                  <div className="inline-block bg-white text-gray-900 shadow-sm border border-gray-200 p-4 rounded-lg">
                    <div className="animate-pulse">AI is thinking...</div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Message input */}
        <div className="bg-white border-t border-gray-200 p-6">
          <form onSubmit={handleSendMessage} className="flex space-x-4">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={
                currentSession
                  ? "Type your message... (e.g., 'What's the weather in NYC?', 'Send hello to team', or 'Schedule meeting tomorrow at 2pm')"
                  : "Create or select a chat session first"
              }
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white placeholder-gray-500"
              disabled={chatLoading || !currentSession}
            />
            <button
              type="submit"
              disabled={chatLoading || !message.trim() || !currentSession}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {chatLoading ? "Sending..." : "Send"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
