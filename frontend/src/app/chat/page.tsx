/**
 * Protected chat page
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { chatAPI } from "@/lib/api";
import {
  LogOut,
  User,
  Bot,
  Calendar,
  Cloud,
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
  const router = useRouter();
  const [message, setMessage] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth/signin");
    }
  }, [user, loading, router]);

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
      const result = await chatAPI.sendMessage(currentMessage);

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

  const handleClearChat = () => {
    setChatHistory([]);
    toast.success("Chat cleared");
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
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col max-h-screen">
        {/* User info */}
        <div className="p-4 border-b border-gray-200 flex-shrink-0">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-medium text-gray-900">Nexus AI</h2>
            <div className="flex items-center space-x-2">
              <User className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-600">
                {user?.username || "User"}
              </span>
            </div>
          </div>
          <button
            onClick={handleClearChat}
            className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center"
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Clear Chat
          </button>
        </div>

        {/* Available Agents */}
        <div className="flex-1 overflow-y-auto min-h-0">
          <div className="p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-3">
              Available Agents
            </h3>
            <div className="space-y-2">
              <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                <Cloud className="h-5 w-5 text-blue-500" />
                <div>
                  <div className="font-medium text-sm text-gray-900">
                    Weather Agent
                  </div>
                  <div className="text-xs text-gray-500">
                    Get weather forecasts
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                <MessageSquare className="h-5 w-5 text-green-500" />
                <div>
                  <div className="font-medium text-sm text-gray-900">
                    Slack Agent
                  </div>
                  <div className="text-xs text-gray-500">
                    Send team messages
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 bg-purple-50 rounded-lg">
                <Calendar className="h-5 w-5 text-purple-500" />
                <div>
                  <div className="font-medium text-sm text-gray-900">
                    Calendar Agent
                  </div>
                  <div className="text-xs text-gray-500">Schedule events</div>
                </div>
              </div>
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
                AI Assistant Chat
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
              <p>Start a conversation with your AI assistant!</p>
              <p className="text-sm mt-2">
                Try: &quot;What&apos;s the weather in Tokyo?&quot;, &quot;Send a
                message to team&quot;, or &quot;Schedule meeting tomorrow at
                3pm&quot;
              </p>
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
              placeholder="Type your message... (e.g., 'What's the weather in NYC?', 'Send hello to team', or 'Schedule meeting tomorrow at 2pm')"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white placeholder-gray-500"
              disabled={chatLoading}
            />
            <button
              type="submit"
              disabled={chatLoading || !message.trim()}
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
