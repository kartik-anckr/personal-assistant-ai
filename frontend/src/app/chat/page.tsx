/**
 * Professional AI Chat Interface with Dark Theme
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { chatAPI } from "@/lib/api";

export default function ChatPage() {
  const { user, signout, loading } = useAuth();
  const router = useRouter();
  const [message, setMessage] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth/signin");
    }
  }, [user, loading, router]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    try {
      setChatLoading(true);
      setError("");
      const result = await chatAPI.sendMessage(message);
      setResponse(result.response);
      setMessage("");
    } catch (error: unknown) {
      setError("Failed to send message. Please try again.");
    } finally {
      setChatLoading(false);
    }
  };

  const handleSignout = () => {
    signout();
    router.push("/auth/signin");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-16 w-16 bg-gradient-primary rounded-2xl flex items-center justify-center mb-4 shadow-lg animate-pulse">
            <span className="text-2xl font-bold text-white">N</span>
          </div>
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400 text-lg">Initializing Nexus AI...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <div className="h-10 w-10 bg-gradient-primary rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-lg font-bold text-white">N</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Nexus AI</h1>
                <p className="text-xs text-gray-400">
                  Intelligent Personal Assistant
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-3 glass rounded-lg px-4 py-2">
                <div className="h-8 w-8 bg-gradient-secondary rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-white">
                    {(user.first_name || user.username || "U")
                      .charAt(0)
                      .toUpperCase()}
                  </span>
                </div>
                <div>
                  <p className="text-sm font-medium text-white">
                    {user.first_name || user.username}
                  </p>
                  <p className="text-xs text-gray-400">{user.email}</p>
                </div>
              </div>

              <button
                onClick={handleSignout}
                className="flex items-center space-x-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 px-3 py-2 rounded-lg transition-all duration-200"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                  />
                </svg>
                <span className="text-sm font-medium">Sign out</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="space-y-6">
          {/* Welcome Card */}
          <div className="glass rounded-2xl p-6 shadow-xl fade-in">
            <div className="flex items-start space-x-4">
              <div className="h-12 w-12 bg-gradient-primary rounded-xl flex items-center justify-center shadow-lg">
                <svg
                  className="w-6 h-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-bold text-white mb-2">
                  Welcome to Nexus AI
                </h2>
                <p className="text-gray-300 text-sm leading-relaxed">
                  Your intelligent assistant is ready to help! Ask me about
                  weather, send Slack messages, or chat about anything. I can
                  handle weather forecasts, team communication, and much more.
                </p>
                <div className="flex flex-wrap gap-2 mt-4">
                  <span className="px-3 py-1 bg-blue-500/20 text-blue-300 rounded-full text-xs font-medium">
                    Weather Insights
                  </span>
                  <span className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-xs font-medium">
                    Slack Integration
                  </span>
                  <span className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-xs font-medium">
                    AI Chat
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-500/20 border border-red-500/30 rounded-xl p-4 backdrop-blur-sm slide-in-right">
              <div className="flex items-center space-x-3">
                <svg
                  className="w-5 h-5 text-red-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <p className="text-red-200 font-medium">{error}</p>
              </div>
            </div>
          )}

          {/* Chat Response */}
          {response && (
            <div className="glass rounded-2xl p-6 shadow-xl slide-in-right">
              <div className="flex items-start space-x-4">
                <div className="h-10 w-10 bg-gradient-secondary rounded-xl flex items-center justify-center shadow-lg">
                  <svg
                    className="w-5 h-5 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                    />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-semibold text-blue-300 mb-2">
                    Nexus AI Response:
                  </h3>
                  <div className="prose prose-invert text-gray-200 max-w-none">
                    <p className="leading-relaxed">{response}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Chat Form */}
          <div className="glass rounded-2xl p-6 shadow-xl">
            <form onSubmit={handleSendMessage} className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-200 mb-3">
                  Send a message to your AI assistant
                </label>
                <div className="flex space-x-3">
                  <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    className="flex-1 px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 input-glow"
                    placeholder="Ask about weather, send Slack messages, or chat with AI..."
                    disabled={chatLoading}
                  />
                  <button
                    type="submit"
                    disabled={chatLoading || !message.trim()}
                    className="px-6 py-3 bg-gradient-primary rounded-xl text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed btn-glow transform hover:scale-[1.02] flex items-center space-x-2"
                  >
                    {chatLoading ? (
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    ) : (
                      <>
                        <span>Send</span>
                        <svg
                          className="w-4 h-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                          />
                        </svg>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </form>

            {/* Quick Actions */}
            <div className="mt-6">
              <p className="text-xs font-medium text-gray-400 mb-3">
                Quick Actions:
              </p>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setMessage("What's the weather like today?")}
                  className="px-3 py-2 bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 rounded-lg text-xs font-medium transition-colors duration-200"
                >
                  ☀️ Check Weather
                </button>
                <button
                  onClick={() => setMessage("Send a message to the team")}
                  className="px-3 py-2 bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 rounded-lg text-xs font-medium transition-colors duration-200"
                >
                  💬 Slack Message
                </button>
                <button
                  onClick={() => setMessage("What can you help me with?")}
                  className="px-3 py-2 bg-green-500/20 hover:bg-green-500/30 text-green-300 rounded-lg text-xs font-medium transition-colors duration-200"
                >
                  🤖 AI Help
                </button>
              </div>
            </div>
          </div>

          {/* User Profile Card */}
          <div className="glass rounded-2xl p-6 shadow-xl">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center">
              <svg
                className="w-5 h-5 mr-2 text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
              Your Profile
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-gray-800/30 rounded-lg p-4">
                <p className="text-sm font-medium text-gray-400 mb-1">
                  Username
                </p>
                <p className="text-white font-medium">{user.username}</p>
              </div>
              <div className="bg-gray-800/30 rounded-lg p-4">
                <p className="text-sm font-medium text-gray-400 mb-1">Email</p>
                <p className="text-white font-medium">{user.email}</p>
              </div>
              <div className="bg-gray-800/30 rounded-lg p-4">
                <p className="text-sm font-medium text-gray-400 mb-1">
                  Member since
                </p>
                <p className="text-white font-medium">
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
