/**
 * Sign in page
 */

import { SigninForm } from "@/components/auth/SigninForm";

export default function SigninPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <h1 className="text-3xl font-extrabold text-gray-900">Nexus AI</h1>
          <p className="mt-2 text-sm text-gray-600">
            AI-powered multi-agent assistant
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <SigninForm />
      </div>
    </div>
  );
}
