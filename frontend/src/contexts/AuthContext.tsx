/**
 * Authentication context for managing user state
 */

"use client";

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { User, authAPI, AuthResponse } from "@/lib/api";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signin: (email: string, password: string) => Promise<void>;
  signup: (
    username: string,
    email: string,
    password: string,
    firstName?: string,
    lastName?: string
  ) => Promise<void>;
  signout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const userData = await authAPI.getProfile();
          setUser(userData);
        }
      } catch (error) {
        console.error("Auth check failed:", error);
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_data");
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const signin = async (email: string, password: string) => {
    try {
      setLoading(true);
      const response: AuthResponse = await authAPI.signin({ email, password });

      // Store token and user data
      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("user_data", JSON.stringify(response.user));

      setUser(response.user);
      console.log("Successfully signed in!");
    } catch (error: unknown) {
      const message =
        (error as { response?: { data?: { detail?: string } } }).response?.data
          ?.detail || "Sign in failed";
      console.error(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signup = async (
    username: string,
    email: string,
    password: string,
    firstName?: string,
    lastName?: string
  ) => {
    try {
      setLoading(true);
      const response: AuthResponse = await authAPI.signup({
        username,
        email,
        password,
        first_name: firstName,
        last_name: lastName,
      });

      // Store token and user data
      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("user_data", JSON.stringify(response.user));

      setUser(response.user);
      console.log("Account created successfully!");
    } catch (error: unknown) {
      const message =
        (error as { response?: { data?: { detail?: string } } }).response?.data
          ?.detail || "Sign up failed";
      console.error(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_data");
    setUser(null);
    console.log("Signed out successfully");
  };

  const value = {
    user,
    loading,
    signin,
    signup,
    signout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
