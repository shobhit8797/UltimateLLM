import { AppSidebar } from "@/components/Sidebar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { LogOut, SquarePen } from "lucide-react";
import { Outlet, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { removeAuthToken } from "@/utlis/auth";

export default function Layout() {
    const navigate = useNavigate();
    return (
        <SidebarProvider>
            <AppSidebar />
            <main className="w-full relative">
                <div className="absolute top-5 left-5 z-10">
                    <div className="flex flex-col">
                        <SidebarTrigger />
                        <Button
                            variant="ghost"
                            size="icon"
                            className={cn("h-7 w-7 mt-2")}
                            onClick={() => {
                                navigate("/chat");
                            }}
                        >
                            <SquarePen />
                            <span className="sr-only">New Chat</span>
                        </Button>
                    </div>
                </div>

                <Outlet key={window.location.pathname} />

                <div className="absolute top-5 right-5 z-10">
                    <Button
                        variant="ghost"
                        size="icon"
                        className={cn("h-10 w-10 rounded-full")}
                        onClick={() => {
                            removeAuthToken();
                        }}
                    >
                        <LogOut />
                        <span className="sr-only">LogOut</span>
                    </Button>
                </div>
            </main>
        </SidebarProvider>
    );
}
