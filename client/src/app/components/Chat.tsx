"use client";

// Ensure these packages are installed:
// npm install react-markdown remark-gfm lucide-react

import React, { useState, useRef, useEffect, Fragment } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Menu, Transition } from "@headlessui/react";
import {
  Settings,
  Send,
  LogOut,
  CircleUserRound,
  BotMessageSquare,
  CircleDollarSign,
  Landmark,
  Tractor,
  Sprout,
  Hospital,
  PillBottle,
  ScanBarcode,
  ShoppingCart,
} from "lucide-react";

interface Message {
  question?: string;
  answer?: string;
  tool?: string;
  loading?: boolean;
}

interface AgentSelectorProps {
  agentType: string;
  setAgentType: (t: string) => void;
}

interface EmptyStateIconProps {
  agentType: string;
}

const AgentSelectionBox: React.FC<AgentSelectorProps> = ({
  agentType,
  setAgentType,
}) => {
  const handleAgentChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const select = e.target;
    const value = select.options[select.selectedIndex].text;
    setAgentType(value);
  };
  return (
    <div className="flex flex-col gap-3">
      <p>
        Select the <strong>AI Agent</strong> you want to interact with:
      </p>
      {/* Your selection UI here */}
      <select
        id="agentSelector"
        className="w-full p-2 bg-gray-700 text-white rounded-xl hover:cursor-pointer"
        onChange={handleAgentChange}
      >
        <option value={"bnf"}>Banking & Finance</option>
        <option value={"frm"}>Farming</option>
        <option value={"hlc"}>Healthcare</option>
        <option value={"rtl"}>Retail</option>
      </select>
    </div>
  );
};

function DataVisualization() {
  return (
    <div className="p-4 bg-gray-800 rounded-xl h-full overflow-auto">
      {/* Your charting library component here */}
      <p className="mb-5">
        Here you will see <strong>Graphs/Plots Visualization</strong> based on
        an AI Agent capabilities.
      </p>
      <p className="text-gray-400 text-center text-sm">
        Stay Tight! I am coming soon!
      </p>
    </div>
  );
}

const EmptyStateIcon: React.FC<EmptyStateIconProps> = ({ agentType }) => {
  switch (agentType) {
    case "Banking & Finance":
      return (
        <div className="flex gap-1">
          <CircleDollarSign size={30} className="mb-2" />
          <Landmark size={30} className="mb-2" />
        </div>
      );
    case "Farming":
      return (
        <div className="flex gap-1">
          <Tractor size={30} className="mb-2" />
          <Sprout size={30} className="mb-2" />
        </div>
      );
    case "Healthcare":
      return (
        <div className="flex gap-1">
          <Hospital size={30} className="mb-2" />
          <PillBottle size={30} className="mb-2" />
        </div>
      );
    case "Retail":
      return (
        <div className="flex gap-1">
          <ShoppingCart size={30} className="mb-2" />
          <ScanBarcode size={30} className="mb-2" />
        </div>
      );
    default:
      return (
        <div className="flex gap-1">
          <CircleDollarSign size={30} className="mb-2" />
          <Landmark size={30} className="mb-2" />
        </div>
      );
  }
};

export default function Chat() {
  const [username, setUsername] = useState("");
  const [agentType, setAgentType] = useState("Banking & Finance");
  const [input, setInput] = useState("");
  const [history, setHistory] = useState<Message[]>([]);
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const formRef = useRef<HTMLFormElement>(null);

  // Auto-scroll on new messages
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [history]);

  useEffect(() => {
    const storedUser = localStorage.getItem("username");
    if (storedUser) setUsername(storedUser);
  }, []);

  useEffect(() => {
    // Whenever agentType changes, reset history
    setHistory([]);
  }, [agentType]);

  const handleSubmit = async (e: React.FormEvent) => {
    setSending(true);
    e.preventDefault();
    const question = input.trim();
    const agentSelect = document.getElementById(
      "agentSelector"
    ) as HTMLSelectElement;
    const agent = agentSelect?.value;
    if (!question) return;

    // 1️⃣ Show user message
    setHistory((prev) => [...prev, { question }]);
    setInput("");
    // 2️⃣ Add a loading placeholder
    setHistory((prev) => [...prev, { loading: true }]);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:5010/api/v0/multi-agent/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Bearer ${token}` : "",
        },
        body: JSON.stringify({ question, agent }),
      });

      // 3️⃣ Swap spinner for an empty answer slot
      setHistory((prev) => {
        const updated = [...prev];
        const idx = updated.findIndex((m) => m.loading);
        if (idx !== -1) updated[idx] = { answer: "" };
        return updated;
      });

      // 4️⃣ Stream the response body
      const reader = res.body!.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const textChunk = decoder.decode(value, { stream: true });
          // Append each chunk to the bot message
          setHistory((prev) => {
            const updated = [...prev];
            const lastIndex = updated.length - 1;
            updated[lastIndex] = {
              tool: updated[lastIndex].tool,
              answer: updated[lastIndex].answer + textChunk,
            };
            return updated;
          });
        }
      }
    } catch (err: any) {
      // Remove spinner and show error
      setHistory((prev) => prev.filter((m) => !m.loading));
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="mt-2 mx-auto flex flex-col h-[95vh] source-sans-3-regular">
      {/* Header */}
      <div className="mb-3 flex items-center justify-between px-4 border-b-1 border-gray-600 pb-1">
        <h1 className="text-4xl nunito-bold">
          M. A. C. E.{" "}
          <span className="text-xs">
            (Multi Agents Collaborative Environment)
          </span>
        </h1>
        <Menu as="div" className="relative">
          <Menu.Button className="focus:outline-none hover:cursor-pointer hover:bg-gray-600 rounded-xl p-1">
            <Settings size={24} className="text-gray-300" />
          </Menu.Button>

          <Transition
            as={Fragment}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
          >
            <Menu.Items className="absolute right-0 w-50 bg-gray-900 rounded-xl shadow-lg outline-none z-20">
              <Menu.Item>
                <span className="flex items-center p-3 text-sm text-gray-600">
                  <CircleUserRound size={16} className="mr-2" />
                  Hello!&nbsp;&nbsp;{" "}
                  <span className="bg-gray-700 px-2 text-white rounded-xl">
                    {username}
                  </span>
                </span>
              </Menu.Item>
              <Menu.Item>
                {({ active }) => (
                  <a
                    href="/"
                    className={`flex items-center px-3 pb-3 text-sm ${
                      active ? "text-white" : "text-gray-400"
                    }`}
                  >
                    <LogOut
                      size={16}
                      className={`mr-2 ${
                        active ? "text-white" : "text-gray-400"
                      }`}
                    />
                    Sign Out
                  </a>
                )}
              </Menu.Item>
            </Menu.Items>
          </Transition>
        </Menu>
      </div>
      <div className="grid grid-cols-12 gap-4 h-[85vh] px-4">
        <div className="col-span-2">
          <AgentSelectionBox
            agentType={agentType}
            setAgentType={setAgentType}
          />
        </div>
        <div className="col-span-7 flex flex-col">
          {/* Chat Display */}
          <div className="mb-2 flex items-center justify-between">
            <div className="text-4xl nunito-semibold">Chat</div>
            <div className="flex gap-1 p-2 rounded-3xl bg-gray-700 mr-[1rem]">
              <span className="text-xs px-3 bg-gray-900 py-1 rounded-2xl">
                {agentType}
              </span>
              <BotMessageSquare size={23} className="text-gray-300" />
            </div>
          </div>
          <div className="bg-gray-700 rounded-xl overflow-hidden">
            <div
              ref={scrollRef}
              className="flex-1 overflow-y-auto p-4 space-y-4 h-[70vh] relative"
            >
              {history.length === 0 && !error ? (
                <div className="flex flex-col items-center justify-center h-full text-gray-400">
                  <EmptyStateIcon agentType={agentType} />
                  <p className="text-center w-[30rem]">
                    Hey! I am an AI Agent mostly answering your queries related
                    to
                  </p>
                  <span className="underline">{agentType}</span>
                  Ask a question to get started!
                </div>
              ) : (
                <>
                  {history.map((msg, idx) => (
                    <div key={idx}>
                      {/* User bubble */}
                      {msg.question && (
                        <div className="flex justify-end">
                          <div className="bg-gray-500 text-white p-3 rounded-l-2xl rounded-tr-2xl max-w-[75%] break-words">
                            {msg.question}
                          </div>
                        </div>
                      )}

                      {/* Loading spinner for bot */}
                      {msg.loading && (
                        <div className="flex justify-start text-sm">
                          <div className="h-4 w-4 border-2 border-t-transparent border-gray-400 rounded-full animate-spin" />
                          &nbsp;&nbsp;&nbsp;Working with agent....
                        </div>
                      )}

                      {/* Bot bubble with markdown rendering */}
                      {msg.answer && (
                        <div className="flex flex-col justify-start">
                          {msg.tool && (
                            <span className="bg-gray-900 px-2 mb-2 text-sm">
                              {msg.tool}
                            </span>
                          )}
                          <div className="p-3 text-lg break-words">
                            <ReactMarkdown
                              remarkPlugins={[remarkGfm]}
                              // className="prose max-w-full"
                            >
                              {msg.answer}
                            </ReactMarkdown>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                  {error && (
                    <div className="text-red-600 font-mono bg-red-300 px-3 py-1 rounded-xl text-xs">
                      {error}
                    </div>
                  )}
                </>
              )}
            </div>
            {/* Chat Input (ChatGPT-style) */}
            <div className="max-w-4xl mx-[1rem] pb-4">
              <form ref={formRef} onSubmit={handleSubmit} className="mt-4">
                <div className="bg-gray-200 rounded-xl pl-4 py-2 pr-2 flex items-center space-x-2 shadow-lg">
                  <textarea
                    rows={1}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault(); // prevent newline
                        formRef.current?.requestSubmit(); // submit form
                      }
                    }}
                    className="flex-grow resize-none outline-none text-gray-900 placeholder-gray-500"
                    placeholder="Ask your query ...."
                  />
                  <button
                    type="submit"
                    className={`p-3 hover:cursor-pointer hover:text-white rounded-lg text-gray-700 shadow-md ${
                      sending
                        ? "bg-gray-400 cursor-not-allowed"
                        : "bg-gray-400 hover:bg-gray-700"
                    }`}
                    disabled={sending}
                  >
                    {sending ? (
                      <svg
                        className="h-5 w-5 animate-spin"
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
                    ) : (
                      <Send size={20} />
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        <div className="col-span-3">
          <DataVisualization />
        </div>
      </div>
    </div>
  );
}
