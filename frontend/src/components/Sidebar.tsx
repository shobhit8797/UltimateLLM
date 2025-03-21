// // src/components/Sidebar.jsx
// import React from 'react';
// import { Sidebar, SidebarSection, SidebarNav, SidebarNavItem } from "./ui/sidebar";
// import { Home, Users, Settings } from "lucide-react";
// import { Link } from 'react-router-dom';

// function AppSidebar() {
//   return (
//     <Sidebar className="hidden md:flex h-screen border-r">
//       <SidebarSection>
//         <SidebarNav>
//           <SidebarNavItem asChild>
//             <Link to="/" className="flex items-center gap-2">
//               <Home className="h-4 w-4" />
//               Home
//             </Link>
//           </SidebarNavItem>
//           <SidebarNavItem asChild>
//             <Link to="/users" className="flex items-center gap-2">
//               <Users className="h-4 w-4" />
//               Users
//             </Link>
//           </SidebarNavItem>
//           <SidebarNavItem asChild>
//             <Link to="/settings" className="flex items-center gap-2">
//               <Settings className="h-4 w-4" />
//               Settings
//             </Link>
//           </SidebarNavItem>
//         </SidebarNav>
//       </SidebarSection>
//     </Sidebar>
//   );
// }

// export default AppSidebar;
// src/components/Sidebar.jsx
import { Home, Settings, Users } from "lucide-react";
import { Link } from "react-router-dom";
import {
    Sidebar,
    SidebarNav,
    SidebarNavItem,
    SidebarSection,
} from "./ui/sidebar";

function AppSidebar() {
    return (
        <Sidebar className="hidden md:flex h-screen border-r">
            <SidebarSection>
                <SidebarNav>
                    <SidebarNavItem asChild>
                        <Link to="/" className="flex items-center gap-2">
                            <Home className="h-4 w-4" />
                            Home
                        </Link>
                    </SidebarNavItem>
                    <SidebarNavItem asChild>
                        <Link to="/users" className="flex items-center gap-2">
                            <Users className="h-4 w-4" />
                            Users
                        </Link>
                    </SidebarNavItem>
                    <SidebarNavItem asChild>
                        <Link
                            to="/settings"
                            className="flex items-center gap-2"
                        >
                            <Settings className="h-4 w-4" />
                            Settings
                        </Link>
                    </SidebarNavItem>
                </SidebarNav>
            </SidebarSection>
        </Sidebar>
    );
}

export default AppSidebar;
