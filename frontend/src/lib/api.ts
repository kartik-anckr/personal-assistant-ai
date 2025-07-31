/**
 * API client for backend communication
 */

import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create axios instance
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem("access_token");
      localStorage.removeItem("user_data");
      if (typeof window !== "undefined") {
        window.location.href = "/auth/signin";
      }
    }
    return Promise.reject(error);
  }
);

// API Types
export interface User {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface SignupRequest {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface ChatMessage {
  message: string;
}

export interface ChatResponse {
  response: string;
  success: boolean;
  user_id: string;
}

// Auth API functions
export const authAPI = {
  signup: async (data: SignupRequest): Promise<AuthResponse> => {
    const response = await apiClient.post("/auth/signup", data);
    return response.data;
  },

  signin: async (data: SigninRequest): Promise<AuthResponse> => {
    const response = await apiClient.post("/auth/signin", data);
    return response.data;
  },

  getProfile: async (): Promise<User> => {
    const response = await apiClient.get("/auth/me");
    return response.data;
  },

  verifyToken: async (): Promise<{ valid: boolean; user_id: string }> => {
    const response = await apiClient.get("/auth/verify-token");
    return response.data;
  },
};

// Chat API
export const chatAPI = {
  sendMessage: async (message: string): Promise<ChatResponse> => {
    const response = await apiClient.post("/chat", { message });
    return response.data;
  },
};
