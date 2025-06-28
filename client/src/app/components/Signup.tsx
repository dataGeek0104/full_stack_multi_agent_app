"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

interface SignupProps {
  onLoginLink: () => void;
}

export default function Signup({ onLoginLink }: SignupProps) {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:5010/api/v0/user/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        toast.error(data.error || "Signup failed");
        return;
      } else {
        toast.success("User created successfully!");
      }
      // After successful signup, redirect to login
      router.push("/");
    } catch {
      setError("An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-80">
      <h2 className="mb-4 text-4xl text-center pb-9 nunito-regular">Signup</h2>
      <label className="block mb-1 text-sm font-medium">Username</label>
      <input
        type="text"
        placeholder="Create your username ...."
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="w-full p-2 mb-4 border border-gray-400 rounded-xl"
        required
      />
      <label className="block mb-1 text-sm font-medium">Password</label>
      <input
        type="password"
        placeholder="Create password ...."
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full p-2 mb-4 border border-gray-400 rounded-xl"
        required
      />
      <div className="grid grid-cols-7">
        <button
          type="submit"
          className={`w-full p-2 font-semibold text-white rounded-lg col-start-3 col-end-6 hover:cursor-pointer ${
            loading
              ? "bg-green-500 cursor-not-allowed"
              : "bg-green-600 hover:bg-green-800"
          }`}
          disabled={loading}
        >
          {loading ? (
            <div className="flex items-center justify-center space-x-2">
              <svg
                className="h-5 w-5 animate-spin text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v8H4z"
                />
              </svg>
              <span>Creating ...</span>
            </div>
          ) : (
            "Create Account"
          )}
        </button>
      </div>
      <p className="mt-[3rem] text-center">
        Already have an account?&nbsp;&nbsp;&nbsp;{" "}
        <button
          type="button"
          onClick={onLoginLink}
          className="text-gray-300 underline hover:text-white hover:cursor-pointer"
        >
          Log in
        </button>
      </p>
    </form>
  );
}
