import { ThemeProvider } from "@/components/theme-provider";
import { Suspense, lazy } from "react";
import {
    Navigate,
    Outlet,
    Route,
    BrowserRouter as Router,
    Routes,
} from "react-router-dom";
import { SidebarProvider } from "./components/ui/sidebar";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ChatLayout from "./components/ChatLayout";

const LoginPage = lazy(() => import("@/pages/LoginPage"));
const SignupPage = lazy(() => import("@/pages/SignupPage"));
const ChatApp = lazy(() => import("@/pages/ChatApp"));
const NotFound = lazy(() => import("@/pages/NotFound"));

// Loading Fallback Component
const FallbackLoader = () => <div>Loading...</div>;

// Protected Route Wrapper
const ProtectedRoute = () => {
    const { isAuthenticated } = useAuth();
    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

const App = () => (
    <AuthProvider>
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <Router>
                <Suspense fallback={<FallbackLoader />}>
                    <Routes>
                        {/* Public Routes */}
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/signup" element={<SignupPage />} />

                        {/* Protected Routes */}
                        <Route element={<ProtectedRoute />}>
                            {/* <Route
                                element={
                                    <SidebarProvider>
                                        <ChatLayout />
                                    </SidebarProvider>
                                }
                            > */}
                            <Route
                                path="/chat/:conversation_id?"
                                element={<ChatApp />}
                            />
                        </Route>
                        {/* </Route> */}

                        {/* 404 Page */}
                        <Route path="*" element={<NotFound />} />
                    </Routes>
                </Suspense>
            </Router>
        </ThemeProvider>
    </AuthProvider>
);

export default App;
