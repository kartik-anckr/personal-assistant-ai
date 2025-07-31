/**
 * Main landing page with authentication routing
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Bot, Users, Cloud, ArrowRight } from "lucide-react";

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (user) {
        router.push("/chat");
      }
    }
  }, [user, loading, router]);

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            <span className="text-blue-600">LangGraph</span> Assistant
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Your intelligent multi-agent AI assistant powered by LangGraph. Get
            weather updates, send Slack messages, and interact with multiple
            specialized AI agents through a single interface.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/auth/signup"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </a>
            <a
              href="/auth/signin"
              className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Sign In
            </a>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="flex justify-center mb-4">
              <Cloud className="h-12 w-12 text-blue-500" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              Weather Agent
            </h3>
            <p className="text-gray-600">
              Get real-time weather updates and forecasts for any location
              around the world with our specialized weather AI agent.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="flex justify-center mb-4">
              <Users className="h-12 w-12 text-green-500" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              Slack Integration
            </h3>
            <p className="text-gray-600">
              Send messages and interact with your team through Slack directly
              from the assistant interface with intelligent message routing.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="flex justify-center mb-4">
              <Bot className="h-12 w-12 text-purple-500" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              Smart Orchestration
            </h3>
            <p className="text-gray-600">
              Our AI orchestrator intelligently routes your requests to the
              right agent, ensuring optimal responses every time.
            </p>
          </div>
        </div>

        {/* How it works */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 font-bold text-xl">1</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Sign Up</h4>
              <p className="text-gray-600 text-sm">
                Create your account to get started
              </p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-green-600 font-bold text-xl">2</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Ask Questions
              </h4>
              <p className="text-gray-600 text-sm">
                Type your request in natural language
              </p>
            </div>

            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-purple-600 font-bold text-xl">3</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">AI Routes</h4>
              <p className="text-gray-600 text-sm">
                Our orchestrator selects the best agent
              </p>
            </div>

            <div className="text-center">
              <div className="bg-orange-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-orange-600 font-bold text-xl">4</span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Get Results</h4>
              <p className="text-gray-600 text-sm">
                Receive intelligent, contextual responses
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Experience the Future of AI Assistance?
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Join thousands of users who are already leveraging the power of
            multi-agent AI systems for their daily tasks.
          </p>
          <a
            href="/auth/signup"
            className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Start Your Journey
            <ArrowRight className="ml-2 h-6 w-6" />
          </a>
        </div>
      </div>
    </div>
  );
}
