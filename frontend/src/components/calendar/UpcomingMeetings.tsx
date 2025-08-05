import React, { useState, useEffect, useCallback } from "react";
import { calendarAPI } from "../../lib/api";
import toast from "react-hot-toast";

interface UpcomingMeetingsProps {
  query?: string;
  autoRefresh?: boolean;
}

export default function UpcomingMeetings({
  query = "next 7 days",
  autoRefresh = false,
}: UpcomingMeetingsProps) {
  const [meetings, setMeetings] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [customQuery, setCustomQuery] = useState(query);

  const loadMeetings = useCallback(async () => {
    try {
      setLoading(true);
      const result = await calendarAPI.getUpcomingMeetings(query);
      setMeetings(result.meetings);
    } catch (error) {
      console.error("Failed to load meetings:", error);
      toast.error("Failed to load upcoming meetings");
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    loadMeetings();

    if (autoRefresh) {
      const interval = setInterval(loadMeetings, 5 * 60 * 1000); // Refresh every 5 minutes
      return () => clearInterval(interval);
    }
  }, [query, autoRefresh, loadMeetings]);

  const handleCustomQuery = async () => {
    try {
      setLoading(true);
      const result = await calendarAPI.getUpcomingMeetings(customQuery);
      setMeetings(result.meetings);
    } catch (error) {
      console.error("Failed to load meetings:", error);
      toast.error("Failed to load meetings");
    } finally {
      setLoading(false);
    }
  };

  const quickQueries = [
    { label: "Today", value: "today" },
    { label: "Tomorrow", value: "tomorrow" },
    { label: "This Week", value: "this week" },
    { label: "Next Week", value: "next week" },
    { label: "This Month", value: "this month" },
  ];

  const handleQuickQuery = async (queryValue: string) => {
    try {
      setCustomQuery(queryValue);
      setLoading(true);
      const result = await calendarAPI.getUpcomingMeetings(queryValue);
      setMeetings(result.meetings);
    } catch (error) {
      console.error("Failed to load meetings:", error);
      toast.error("Failed to load meetings");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-900">
          Upcoming Meetings
        </h3>
        <button
          onClick={loadMeetings}
          disabled={loading}
          className="text-blue-600 hover:text-blue-700 disabled:opacity-50 transition-colors"
          title="Refresh meetings"
        >
          {loading ? (
            <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-600"></div>
          ) : (
            <svg
              className="h-3 w-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          )}
        </button>
      </div>

      {/* Quick Query Buttons - Compact */}
      <div className="grid grid-cols-3 gap-1 mb-3">
        {quickQueries.slice(0, 3).map((q) => (
          <button
            key={q.value}
            onClick={() => handleQuickQuery(q.value)}
            disabled={loading}
            className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs hover:bg-blue-200 disabled:opacity-50 transition-colors"
          >
            {q.label}
          </button>
        ))}
      </div>

      {/* Custom Query Input - Compact */}
      <div className="flex gap-1 mb-3">
        <input
          type="text"
          value={customQuery}
          onChange={(e) => setCustomQuery(e.target.value)}
          placeholder="e.g., 'today', 'tomorrow'"
          className="flex-1 border border-gray-300 rounded px-2 py-1 text-xs focus:ring-1 focus:ring-blue-500 focus:border-transparent outline-none"
          onKeyPress={(e) => {
            if (e.key === "Enter") {
              handleCustomQuery();
            }
          }}
        />
        <button
          onClick={handleCustomQuery}
          disabled={loading}
          className="bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700 disabled:opacity-50 transition-colors text-xs"
        >
          {loading ? "..." : "Search"}
        </button>
      </div>

      {/* Meetings Display - Compact */}
      <div className="border border-gray-200 rounded p-2 bg-gray-50 min-h-[100px] max-h-[120px] overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center py-4">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-xs text-gray-600">Loading...</span>
          </div>
        ) : (
          <div className="whitespace-pre-wrap text-xs text-gray-800 font-mono">
            {meetings || "📅 You have no upcoming meetings today."}
          </div>
        )}
      </div>
    </div>
  );
}
