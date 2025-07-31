/**
 * Calendar integration component for connecting/managing Google Calendar
 */

"use client";

import React, { useState, useEffect } from "react";
import { Calendar, CheckCircle, AlertCircle, ExternalLink } from "lucide-react";
import { calendarAPI } from "@/lib/api";
import toast from "react-hot-toast";

interface CalendarStatus {
  connected: boolean;
  provider: string | null;
  scopes: string[];
  connected_at: string | null;
}

export const CalendarIntegration: React.FC = () => {
  const [status, setStatus] = useState<CalendarStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(false);

  useEffect(() => {
    checkCalendarStatus();
  }, []);

  const checkCalendarStatus = async () => {
    try {
      const response = await calendarAPI.getStatus();
      setStatus(response);
    } catch (error) {
      console.error("Failed to check calendar status:", error);
      toast.error("Failed to check calendar status");
    } finally {
      setLoading(false);
    }
  };

  const connectCalendar = async () => {
    try {
      setConnecting(true);
      const response = await calendarAPI.connect();

      // Open Google OAuth in new window
      window.open(
        response.auth_url,
        "google-calendar-auth",
        "width=500,height=600"
      );

      // Listen for auth completion (simplified - in production, use postMessage)
      const checkConnection = setInterval(async () => {
        try {
          const newStatus = await calendarAPI.getStatus();
          if (newStatus.connected) {
            setStatus(newStatus);
            clearInterval(checkConnection);
            toast.success("Google Calendar connected successfully!");
            setConnecting(false);
          }
        } catch (error) {
          // Continue checking
        }
      }, 2000);

      // Stop checking after 2 minutes
      setTimeout(() => {
        clearInterval(checkConnection);
        setConnecting(false);
      }, 120000);
    } catch (error) {
      console.error("Failed to connect calendar:", error);
      toast.error("Failed to connect calendar");
      setConnecting(false);
    }
  };

  const disconnectCalendar = async () => {
    try {
      await calendarAPI.disconnect();
      setStatus({
        connected: false,
        provider: null,
        scopes: [],
        connected_at: null,
      });
      toast.success("Calendar disconnected");
    } catch (error) {
      console.error("Failed to disconnect calendar:", error);
      toast.error("Failed to disconnect calendar");
    }
  };

  if (loading) {
    return (
      <div className="bg-white shadow rounded-lg p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex items-center mb-4">
        <Calendar className="h-6 w-6 text-blue-500 mr-3" />
        <h3 className="text-lg font-medium text-gray-900">Google Calendar</h3>
      </div>

      {status?.connected ? (
        <div className="space-y-4">
          <div className="flex items-center text-green-600">
            <CheckCircle className="h-5 w-5 mr-2" />
            <span className="text-sm font-medium">Connected</span>
          </div>

          <div className="text-sm text-gray-600">
            <p>Provider: {status.provider}</p>
            <p>
              Connected: {new Date(status.connected_at!).toLocaleDateString()}
            </p>
            <p>Permissions: Event creation, Calendar access</p>
          </div>

          <div className="text-sm text-gray-500">
            <p>✅ You can now create calendar events by chatting!</p>
            <p>Try: "Schedule meeting tomorrow at 2pm"</p>
          </div>

          <button
            onClick={disconnectCalendar}
            className="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 border border-red-200 rounded-md hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Disconnect Calendar
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center text-yellow-600">
            <AlertCircle className="h-5 w-5 mr-2" />
            <span className="text-sm font-medium">Not Connected</span>
          </div>

          <p className="text-sm text-gray-600">
            Connect your Google Calendar to create events through chat commands.
          </p>

          <button
            onClick={connectCalendar}
            disabled={connecting}
            className="flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ExternalLink className="h-4 w-4 mr-2" />
            {connecting ? "Connecting..." : "Connect Google Calendar"}
          </button>

          <div className="text-xs text-gray-500">
            <p>This will open Google's authorization page</p>
            <p>Required permissions: Calendar event creation</p>
          </div>
        </div>
      )}
    </div>
  );
};
