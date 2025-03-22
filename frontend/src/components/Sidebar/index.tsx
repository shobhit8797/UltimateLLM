import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar";
import makeApiRequest from "@/utlis/request";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface Conversation {
    id: string;
    title: string;
    created_at: string;
}

export function AppSidebar() {
    const [conversationHistory, setConversationHistory] = useState<
        Conversation[]
    >([]);

    useEffect(() => {
        const fetchConversationHistory = async () => {
            try {
                const response = await makeApiRequest({
                    endpoint: "chat/conversations/",
                    method: "GET",
                });
                setConversationHistory(
                    response.results.length ? response.results : []
                );
                console.log("conversationHistory:", conversationHistory);
                console.log(
                    "response.results.length ?? response.resultsresponse.results.length ?? response.results:",
                    response.results.length ?? response.results
                );
            } catch (error) {
                console.error("Error fetching conversation history:", error);
            }
        };

        fetchConversationHistory();
    }, []);

    return (
        <Sidebar>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel>Application</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {conversationHistory.map((item) => (
                                <SidebarMenuItem key={item.id}>
                                    <SidebarMenuButton asChild>
                                        <Link to={`chat/${item.id}`}>
                                            <span>{item.id}</span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    );
}
