export interface Message {
    id: string;
    conversation_id: string;
    sender: "A" | "S" | "U";
    text: string;
    timestamp: string;
}
