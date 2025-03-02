import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Button } from "./ui/Button";
import { Textarea } from "./ui/Textarea";

const API_BASE_URL = "http://localhost:8000/";
const TOKEN = "your-auth-token-here";

function ChatWindow({ conversationId }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);

    useEffect(() => {
        if (conversationId) {
            fetchMessages();
        } else {
            setMessages([]);
        }
    }, [conversationId]);

    const fetchMessages = async () => {
        try {
            const response = await axios.get(
                `${API_BASE_URL}api/chat/conversations/${conversationId}`,
                {
                    headers: {
                        Authorization: "Bearer hDDm5qJg2VSviWnziBZa8a8hDFXKBW",
                    },
                }
            );
            setMessages(response.data.messages);
        } catch (error) {
            console.error("Error fetching messages:", error);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || !conversationId) return;

        const messageText = input;
        setInput("");

        try {
            const response = await fetch(
                `${API_BASE_URL}api/chat/conversations/${conversationId}/send_message`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer hDDm5qJg2VSviWnziBZa8a8hDFXKBW",
                    },
                    body: JSON.stringify({ text: messageText }),
                }
            );

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let assistantResponse = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split("\n").filter(Boolean);

                for (const line of lines) {
                    const data = JSON.parse(line);
                    if (data.user_message) {
                        setMessages((prev) => [...prev, data.user_message]);
                    } else if (data.assistant_chunk) {
                        assistantResponse += data.assistant_chunk;
                        setMessages((prev) => {
                            const updated = [...prev.filter((m) => m.is_user)];
                            return [
                                ...updated,
                                {
                                    text: assistantResponse,
                                    is_user: false,
                                    created_at: new Date().toISOString(),
                                },
                            ];
                        });
                    } else if (data.done) {
                        // Stream completed
                    }
                }
            }
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex-1 flex flex-col bg-gray-900">
            <div className="flex-1 p-6 overflow-y-auto">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`max-w-[70%] p-4 mb-4 rounded-lg ${
                            msg.is_user
                                ? "ml-auto bg-blue-600 text-white"
                                : "mr-auto bg-gray-700 text-gray-100"
                        }`}
                    >
                        {msg.text}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            <div className="p-6 border-t border-gray-700 bg-gray-800">
                <div className="flex gap-4">
                    <Textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your message..."
                        className="flex-1"
                    />
                    <Button onClick={sendMessage}>Send</Button>
                </div>
            </div>
        </div>
    );
}

export default ChatWindow;
