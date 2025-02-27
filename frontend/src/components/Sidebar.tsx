import React from "react";
import { Button } from "./ui/Button";

function Sidebar({ conversations, onSelectConversation, onNewConversation }) {
    return (
        <div className="w-64 bg-gray-800 p-4 border-r border-gray-700 overflow-y-auto">
            <Button onClick={onNewConversation} className="w-full mb-4">
                + New Chat
            </Button>
            <div className="space-y-2">
                {conversations.map((conv) => (
                    <div
                        key={conv.id}
                        onClick={() => onSelectConversation(conv.id)}
                        className="p-3 bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-600 transition-colors"
                    >
                        {conv.title || `Chat ${conv.id}`}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Sidebar;
