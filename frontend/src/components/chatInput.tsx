import { cn } from "@/lib/utils";
import { useState } from "react";

export default function ChatInput({
    className,
    onSubmit,
    isLoading,
    ...props
}: any) {
    const [input, setInput] = useState("");

    const handleSubmit = () => {
        if (input.trim() && onSubmit) {
            onSubmit(input);
            setInput("");
        }
    };

    return (
        <div className={cn("flex flex-col", className)} {...props}>
            <div className="relative">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit();
                        }
                    }}
                    className="w-full min-h-[100px] p-4 pr-12 text-gray-800 dark:text-gray-200 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent duration-200"
                    placeholder="Type your message here..."
                    rows={4}
                />
                <button
                    type="button"
                    onClick={handleSubmit}
                    className="absolute right-3 bottom-3 p-2 text-gray-500 hover:text-blue-500 dark:text-gray-400 dark:hover:text-blue-400 transition-colors duration-200"
                    aria-label="Send message"
                    disabled={isLoading}
                >
                    <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                        />
                    </svg>
                </button>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                AI may generate creative responses. Verify important
                information.
            </p>
        </div>
    );
}
