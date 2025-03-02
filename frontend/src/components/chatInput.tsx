import { cn } from "@/lib/utils";
import axios from "axios";
import { useState } from "react";

export default function ChatInput({
    className,
    ...props
}: React.ComponentPropsWithoutRef<"div">) {
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const API_BASE_URL = import.meta.env.VITE_BASE_URL;

    const handleSendMessage = async () => {
        try {
            if (!message.trim()) return;
            setIsLoading(true);

            const response = await fetch(
                `${API_BASE_URL}/api/chat/conversations/`,
                {
                    method: "POST",
                    body: JSON.stringify({
                        message: message,
                    }),
                    headers: {
                        Authorization: "Bearer hDDm5qJg2VSviWnziBZa8a8hDFXKBW",
                        "Content-Type": "application/json",
                    },
                }
            );

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            if (response.body) {
                const reader = response.body
                    .pipeThrough(new TextDecoderStream())
                    .getReader();

                try {
                    while (true) {
                        const { value, done } = await reader.read();
                        if (done) break;
                        console.log("Received: ", value);
                        const data = JSON.parse(value);
                        if ("conversation_id" in data) {
                            console.log(
                                "conversation_id:",
                                data.conversation_id
                            );
                        }
                    }
                } finally {
                    reader.releaseLock();
                }
            }

            // Clear the message input after successful send
            setMessage("");
        } catch (error) {
            console.error("Error in streaming response:", error);
            // Handle error (e.g., show error message to user)
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={cn("flex flex-col", className)} {...props}>
            <div className="relative">
                <textarea
                    value={message}
                    onChange={(e) => {
                        setMessage(e.target.value);
                    }}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            handleSendMessage();
                        }
                    }}
                    className="w-full min-h-[100px] p-4 pr-12 text-gray-800 dark:text-gray-200 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent  duration-200"
                    placeholder="Type your message here..."
                    rows={4}
                />
                <button
                    onClick={handleSendMessage}
                    className="absolute right-3 bottom-3 p-2 text-gray-500 hover:text-blue-500 dark:text-gray-400 dark:hover:text-blue-400 transition-colors duration-200"
                    aria-label="Send message"
                    disabled={isLoading || !message.trim()}
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
