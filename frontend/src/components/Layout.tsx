// src/components/Layout.jsx
import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./Header";
import AppSidebar from "./Sidebar";

function Layout() {
    return (
        <div className="flex min-h-screen flex-col">
            <Header />
            <div className="flex flex-1">
                <AppSidebar />
                <main className="flex-1 p-4">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}

export default Layout;
