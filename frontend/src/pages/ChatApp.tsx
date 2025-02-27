import React, { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

const API_BASE_URL = "http://localhost:8000/";
// const TOKEN = "your-auth-token-here"; // Replace with actual token

// axios.defaults.headers.common["Authorization"] = `Token ${TOKEN}`;

function ChatApp() {
    const [conversations, setConversations] = useState([]);
    const [selectedConversation, setSelectedConversation] = useState(null);

    useEffect(() => {
        fetchConversations();
    }, []);

    const fetchConversations = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}conversations/`);
            setConversations(response.data);
        } catch (error) {
            console.error("Error fetching conversations:", error);
        }
    };

    const createConversation = async () => {
        try {
            const response = await axios.post(`${API_BASE_URL}conversations/`, {
                title: "New Chat",
            });
            setConversations([...conversations, response.data]);
            setSelectedConversation(response.data.id);
        } catch (error) {
            console.error("Error creating conversation:", error);
        }
    };

    return (
        <div className="flex h-screen bg-gray-900 text-gray-100">
            <Sidebar
                conversations={conversations}
                onSelectConversation={setSelectedConversation}
                onNewConversation={createConversation}
            />
            <ChatWindow conversationId={selectedConversation} />
        </div>
    );
}

export default ChatApp;
