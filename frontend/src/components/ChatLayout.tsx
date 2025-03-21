// components/ChatLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";
import {
    Sidebar,
    SidebarSection,
    SidebarNav,
    SidebarNavItem,
    SidebarTrigger,
} from "./ui/sidebar";
import { MessageSquare, Users, Settings, Plus, LogOut } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
// import { ThemeToggle } from "./theme-toggle"; // Assuming you have this component

const ChatLayout: React.FC = () => {
    const { logout } = useAuth();

    return (
        <div className="flex min-h-screen flex-col">
            {/* Header */}
            <header className="flex items-center h-16 px-4 border-b shrink-0 md:px-6">
                <SidebarTrigger>
                    <MessageSquare className="h-6 w-6" />
                </SidebarTrigger>
                <div className="ml-4 font-semibold">Chat App</div>
                {/* <div className="ml-auto flex items-center gap-2">
                    <ThemeToggle />
                </div> */}
            </header>

            {/* Main content */}
            <div className="flex flex-1">
                {/* Sidebar */}
                <Sidebar className="w-64 transition-all duration-300">
                    <SidebarSection>
                        <div className="px-3 py-2">
                            <button className="w-full flex items-center justify-center gap-2 bg-primary text-primary-foreground rounded-md px-3 py-2 text-sm font-medium">
                                <Plus className="h-4 w-4" />
                                New Chat
                            </button>
                        </div>
                    </SidebarSection>

                    <SidebarSection>
                        <SidebarNav>
                            <SidebarNavItem asChild>
                                <a
                                    href="/chat"
                                    className="flex items-center gap-2"
                                >
                                    <MessageSquare className="h-4 w-4" />
                                    All Chats
                                </a>
                            </SidebarNavItem>
                            <SidebarNavItem asChild>
                                <a
                                    href="/contacts"
                                    className="flex items-center gap-2"
                                >
                                    <Users className="h-4 w-4" />
                                    Contacts
                                </a>
                            </SidebarNavItem>
                            <SidebarNavItem asChild>
                                <a
                                    href="/settings"
                                    className="flex items-center gap-2"
                                >
                                    <Settings className="h-4 w-4" />
                                    Settings
                                </a>
                            </SidebarNavItem>
                        </SidebarNav>
                    </SidebarSection>

                    <SidebarSection className="mt-auto">
                        <SidebarNav>
                            <SidebarNavItem
                                onClick={logout}
                                className="cursor-pointer"
                            >
                                <LogOut className="h-4 w-4 mr-2" />
                                Logout
                            </SidebarNavItem>
                        </SidebarNav>
                    </SidebarSection>
                </Sidebar>

                {/* Content */}
                <main className="flex-1 overflow-auto">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default ChatLayout;
