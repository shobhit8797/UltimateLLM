import ChatDisplay from "@/components/chatDisplay";
import ChatInput from "@/components/chatInput";
import { Message } from "@/types/chat";
import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function ChatApp() {
    const API_BASE_URL = import.meta.env.VITE_BASE_URL;
    const { conversation_id } = useParams();
    const navigate = useNavigate();

    const messagesEndRef = useRef<HTMLDivElement>(null);

    const [currentConversationId, setCurrentConversationId] = useState<
        string | undefined
    >(conversation_id);
    const [messages, setMessages] = useState<Message[]>([
        {
            id: "0d4aef41-b217-4880-b820-0b208a4f6873",
            conversation_id: "f97e9dbd-2a48-4031-b078-78fbbebdd885",
            text: "HI",
            sender: "U",
            timestamp: "2025-03-15T22:36:59Z",
        },
        {
            id: "0d4aef41-b217-4880-b820-0b208a4f6873",
            conversation_id: "f97e9dbd-2a48-4031-b078-78fbbebdd885",
            text: "Hello! How can I assist you today?",
            sender: "A",
            timestamp: "2025-03-15T22:36:59Z",
        },
    ]);
    const [isLoading, setIsLoading] = useState(false);

    // Update the local state when the URL parameter changes
    useEffect(() => {
        setCurrentConversationId(conversation_id);
    }, [conversation_id]);

    // Scroll to bottom when messages change
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const handleSubmit = async (message: string) => {
        try {
            setIsLoading(true);
            const response = await fetch(
                `${API_BASE_URL}/api/chat/conversations/`,
                {
                    method: "POST",
                    body: JSON.stringify({
                        message,
                        ...(currentConversationId && {
                            conversation_id: currentConversationId,
                        }),
                    }),
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem(
                            "token"
                        )}`,
                        "Content-Type": "application/json",
                    },
                }
            );

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            let assistantMessage = "";

            if (response.body) {
                const reader = response.body
                    .pipeThrough(new TextDecoderStream())
                    .getReader();

                let buffer = "";

                try {
                    while (true) {
                        const { value, done } = await reader.read();
                        if (done) break;

                        // Append the new chunk to our buffer
                        buffer += value;

                        // Try to extract complete JSON objects from the buffer
                        let startIndex = 0;
                        let endIndex;

                        // Process each complete JSON object in the buffer
                        while (
                            (endIndex = buffer.indexOf("}", startIndex)) !== -1
                        ) {
                            try {
                                const jsonStr = buffer.substring(
                                    startIndex,
                                    endIndex + 1
                                );
                                const data = JSON.parse(jsonStr);
                                console.log("Parsed data:", data);

                                if (data.text === "DONE") break;
                                else if (data.sender === "U") {
                                    setMessages((prev) => [
                                        ...prev,
                                        data,
                                        { ...data, text: "", sender: "A" },
                                    ]);

                                    // Update the local state and URL using the conversation field
                                    if (!currentConversationId) {
                                        const newConversationId =
                                            data.conversation ||
                                            data.conversation_id;
                                        setCurrentConversationId(
                                            newConversationId
                                        );
                                        navigate(`/chat/${newConversationId}`, {
                                            replace: true,
                                        });
                                    }
                                } else if (data.sender === "A") {
                                    assistantMessage += data.text;
                                    setMessages((prev) =>
                                        prev.map((msg, index) =>
                                            index === prev.length - 1
                                                ? {
                                                      ...msg,
                                                      text: assistantMessage,
                                                  }
                                                : msg
                                        )
                                    );
                                }

                                // Move to the next character after this JSON object
                                startIndex = endIndex + 1;

                                // Skip any whitespace
                                while (
                                    startIndex < buffer.length &&
                                    (buffer[startIndex] === " " ||
                                        buffer[startIndex] === "\n" ||
                                        buffer[startIndex] === "\r" ||
                                        buffer[startIndex] === "\t")
                                ) {
                                    startIndex++;
                                }
                            } catch (error) {
                                // If parsing fails, we might have an incomplete JSON object
                                // Let's try to find the next valid starting point
                                startIndex = buffer.indexOf(
                                    "{",
                                    startIndex + 1
                                );
                                if (startIndex === -1) break;
                            }
                        }

                        // Keep any remaining partial data in the buffer
                        buffer =
                            startIndex < buffer.length
                                ? buffer.substring(startIndex)
                                : "";
                    }
                } finally {
                    reader.releaseLock();
                }
            }
        } catch (error) {
            console.error("Error fetching LLM response:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
                <div className="flex flex-col w-full max-w-3xl mx-auto p-4">
                    <div className="flex-1 flex flex-col justify-center items-center text-center space-y-4">
                        {currentConversationId ? (
                            <ChatDisplay messages={messages} />
                        ) : (
                            <>
                                <h1 className="text-3xl md:text-4xl font-bold text-gray-800 dark:text-white">
                                    Welcome to Ultimate LLM
                                </h1>
                                <p className="text-lg text-gray-600 dark:text-gray-300 max-w-md">
                                    Hi there, How can I assist you today?
                                </p>
                            </>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                    <ChatInput onSubmit={handleSubmit} isLoading={isLoading} />
                </div>
            </div>
        </>
    );
}
