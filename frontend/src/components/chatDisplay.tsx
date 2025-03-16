import { Message } from "@/types/chat";

export default function ChatDisplay({ messages }: { messages: Message[] }) {
    return (
        <>
            {messages.map((msg, index) => (
                <div key={index}>
                    <strong>{msg.sender === "U" ? "You" : "Bot"}:</strong>{" "}
                    {msg.text}
                </div>
            ))}
        </>
    );
}
