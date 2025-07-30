/**
 * Client wrapper for providers that need client-side rendering
 */

"use client";

import { AuthProvider } from "@/contexts/AuthContext";

interface ClientWrapperProps {
  children: React.ReactNode;
}

export function ClientWrapper({ children }: ClientWrapperProps) {
  return <AuthProvider>{children}</AuthProvider>;
}
