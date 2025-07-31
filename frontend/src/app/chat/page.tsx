/**
 * Protected chat page
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { chatAPI } from "@/lib/api";
import { LogOut, Send, User, Bot, Calendar, Cloud } from "lucide-react";
import toast from "react-hot-toast";
import { CalendarIntegration } from "@/components/calendar/CalendarIntegration";

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

  const clearChat = () => {
    setChatHistory([]);
    toast.success("Chat history cleared");
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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Nexus AI</h1>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-gray-400" />
                <span className="text-sm text-gray-700">
                  {user.first_name || user.username}
                </span>
              </div>

              <button
                onClick={clearChat}
                className="text-gray-600 hover:text-gray-800 text-sm"
              >
                Clear Chat
              </button>

              <button
                onClick={handleSignout}
                className="flex items-center space-x-1 text-red-600 hover:text-red-800"
              >
                <LogOut className="h-5 w-5" />
                <span>Sign out</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="bg-white shadow rounded-lg mb-6">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">
              Welcome to Nexus AI
            </h2>
            <p className="text-sm text-gray-600">
              Your AI-powered multi-agent assistant is ready to help!
            </p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center space-x-3">
                <Cloud className="h-8 w-8 text-blue-500" />
                <div>
                  <h3 className="font-medium">Weather Agent</h3>
                  <p className="text-sm text-gray-600">Get weather forecasts</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Calendar className="h-8 w-8 text-green-500" />
                <div>
                  <h3 className="font-medium">Slack Agent</h3>
                  <p className="text-sm text-gray-600">Send team messages</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Calendar className="h-8 w-8 text-purple-500" />
                <div>
                  <h3 className="font-medium">Calendar Agent</h3>
                  <p className="text-sm text-gray-600">Schedule events</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Calendar Integration */}
        <CalendarIntegration />

        {/* Chat Interface */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">
              Chat with Your Assistant
            </h2>
          </div>

          {/* Chat History */}
          <div className="p-6 max-h-96 overflow-y-auto">
            {chatHistory.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                <Bot className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>Start a conversation with your AI assistant!</p>
                <p className="text-sm mt-2">
                  Try: &quot;What&apos;s the weather in Tokyo?&quot;, &quot;Send
                  a message to team&quot;, or &quot;Schedule meeting tomorrow at
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
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        msg.role === "user"
                          ? "bg-blue-600 text-white"
                          : "bg-gray-100 text-gray-900"
                      }`}
                    >
                      <p className="text-sm">{msg.content}</p>
                      <p
                        className={`text-xs mt-1 ${
                          msg.role === "user"
                            ? "text-blue-100"
                            : "text-gray-500"
                        }`}
                      >
                        {msg.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 px-4 py-2 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                        <span className="text-sm text-gray-600">
                          Assistant is thinking...
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Chat Input */}
          <div className="px-6 py-4 border-t border-gray-200">
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white placeholder-gray-500"
                placeholder="Type your message... (e.g., 'What's the weather in NYC?', 'Send hello to team', or 'Schedule meeting tomorrow at 2pm')"
                disabled={chatLoading}
              />
              <button
                type="submit"
                disabled={chatLoading || !message.trim()}
                className="flex items-center space-x-1 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="h-4 w-4" />
                <span>{chatLoading ? "Sending..." : "Send"}</span>
              </button>
            </form>
          </div>
        </div>

        {/* User Profile Section */}
        <div className="mt-6 bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Your Profile</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-700">Username</p>
                <p className="text-sm text-gray-900">{user.username}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Email</p>
                <p className="text-sm text-gray-900">{user.email}</p>
              </div>
              {user.first_name && (
                <div>
                  <p className="text-sm font-medium text-gray-700">
                    First Name
                  </p>
                  <p className="text-sm text-gray-900">{user.first_name}</p>
                </div>
              )}
              {user.last_name && (
                <div>
                  <p className="text-sm font-medium text-gray-700">Last Name</p>
                  <p className="text-sm text-gray-900">{user.last_name}</p>
                </div>
              )}
              <div>
                <p className="text-sm font-medium text-gray-700">
                  Member since
                </p>
                <p className="text-sm text-gray-900">
                  {new Date(user.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
