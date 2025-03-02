import React, { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import { Input } from "@/components/ui/input";
import ChatInput from "@/components/chatInput";

const API_BASE_URL = "http://localhost:8000/";
// const TOKEN = "your-auth-token-here"; // Replace with actual token

// axios.defaults.headers.common["Authorization"] = `Token ${TOKEN}`;

function ChatApp() {
    const [message, setMessage] = useState("");
    const [conversations, setConversations] = useState([]);
    const [selectedConversation, setSelectedConversation] = useState(null);

    useEffect(() => {
        fetchConversations();
    }, []);

    const fetchConversations = async () => {
        try {
            const response = await axios.get(
                `${API_BASE_URL}api/chat/conversations`,
                {
                    headers: {
                        Authorization: "Bearer hDDm5qJg2VSviWnziBZa8a8hDFXKBW",
                    },
                }
            );
            setConversations(response.data);
        } catch (error) {
            console.error("Error fetching conversations:", error);
        }
    };

    const createConversation = async () => {
        try {
            const response = await axios.post(
                `${API_BASE_URL}api/chat/conversations`,
                {
                    title: "New Chat",
                },
                {
                    headers: {
                        Authorization: "Bearer hDDm5qJg2VSviWnziBZa8a8hDFXKBW",
                    },
                }
            );
            setConversations([...conversations, response.data]);
            setSelectedConversation(response.data.id);
        } catch (error) {
            console.error("Error creating conversation:", error);
        }
    };

    return (
        <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
            <div className="flex flex-col w-full max-w-3xl mx-auto p-4">
                <div className="flex-1 flex flex-col justify-center items-center text-center space-y-4">
                    <h1 className="text-3xl md:text-4xl font-bold text-gray-800 dark:text-white">
                        Welcome to Ultimate LLM
                    </h1>
                    <p className="text-lg text-gray-600 dark:text-gray-300 max-w-md">
                        Hi there, How can I assist you today?
                    </p>
                </div>
                <ChatInput />
            </div>
        </div>
    );
}

export default ChatApp;
