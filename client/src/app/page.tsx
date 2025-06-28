"use client";

import { useState } from "react";
import Login from "./components/Login";
import Signup from "./components/Signup";

export default function Page() {
  const [view, setView] = useState<"login" | "signup">("login");
  return (
    <div className="flex items-center justify-center h-screen source-sans-3-regular">
      <div className="flex w-full max-w-7xl bg-gray-700 rounded-4xl shadow-xl overflow-hidden">
        <div className="w-[70rem] relative hidden md:block">
          <img
            src="images/login-bg.png"
            alt="Login Background"
            className="object-cover w-full h-full"
          />
          <div className="absolute inset-0 bg-black opacity-70" />
          <div className="absolute inset-0 flex flex-col items-center justify-center text-white px-[9rem]">
            <h2 className="text-6xl mb-2 nunito-bold">M. A. C. E.</h2>
            <p className="text-sm font-mono mb-4 bg-gray-700 px-3 py-1 rounded-xl">
              Multi Agents Collaborative Environment
            </p>
            <p className="text-lg mb-4 text-center">
              <span className="text-3xl">Hey!</span>&nbsp;&nbsp;&nbsp;Welcome
              to the platform where you can get access to multiple AI based
              Agentic flows associated with our most efficient and interactive{" "}
              <strong>Generative AI</strong> based&nbsp;{" "}
              <span className="bg-gray-300 text-gray-700 text-sm rounded-xl px-2 py-1 font-extrabold font-mono">
                🤖&nbsp;AI Agents
              </span>
            </p>
          </div>
        </div>
        <div className="md:w-[40rem] flex flex-col items-center justify-center">
          {view === "login" ? (
            <Login onSignupLink={() => setView("signup")} />
          ) : (
            <Signup onLoginLink={() => setView("login")} />
          )}
        </div>
      </div>
    </div>
  );
}
