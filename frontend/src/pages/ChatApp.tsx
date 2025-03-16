import ChatDisplay from "@/components/chatDisplay";
import ChatInput from "@/components/chatInput";
import { Message } from "@/types/chat";
import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";

export default function ChatApp() {
    const API_BASE_URL = import.meta.env.VITE_BASE_URL;
    const { conversation_id } = useParams();

    const messagesEndRef = useRef<HTMLDivElement>(null);

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

    console.log("messages::", messages);


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
                        ...(conversation_id && { conversation_id }),
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
                try {
                    while (true) {
                        const { value }: any = await reader.read();
                        console.log("value::", value);
                        const data: Message = JSON.parse(value);
                        console.log("data::", data);

                        if (data.text === "DONE") break;
                        else if (data.sender === "U") {
                            setMessages([
                                ...messages,
                                data,
                                { ...data, text: "", sender: "A" },
                            ]);
                            if (!conversation_id) {
                                window.history.pushState(
                                    {},
                                    "Chat",
                                    `/chat/${data.conversation_id}`
                                );
                            }
                        } else {
                            assistantMessage += data.text;
                            setMessages((prev) =>
                                prev.map((msg, index) =>
                                    index === prev.length - 1
                                        ? { ...msg, text: assistantMessage }
                                        : msg
                                )
                            );
                            // console.log("Setting Ai Message");
                        }
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
                        {conversation_id ? (
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
