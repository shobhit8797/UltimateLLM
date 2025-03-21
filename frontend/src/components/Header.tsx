import { SidebarTrigger } from "./ui/sidebar";
import { Menu } from "lucide-react";

function Header() {
    return (
        <header className="flex items-center h-16 px-4 border-b shrink-0 md:px-6">
            <SidebarTrigger>
                <Menu className="h-6 w-6" />
            </SidebarTrigger>
            <div className="ml-4 font-semibold">My Vite React App</div>
            {/* Other header content */}
        </header>
    );
}

export default Header;
