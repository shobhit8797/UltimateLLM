import { ThemeProvider } from "@/components/theme-provider";
import { Suspense, lazy, useEffect, useState } from "react";
import {
    Navigate,
    Outlet,
    Route,
    BrowserRouter as Router,
    Routes,
} from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";

const LoginPage = lazy(() => import("@/pages/LoginPage"));
const SignupPage = lazy(() => import("@/pages/SignupPage"));
const ChatApp = lazy(() => import("@/pages/ChatApp"));
// const Dashboard = lazy(() => import("@/pages/Dashboard"));
const NotFound = lazy(() => import("@/pages/NotFound"));

const ProtectedRoute = () => {
    const { isAuthenticated } = useAuth();
    const [isAuthChecked, setIsAuthChecked] = useState(false);

    useEffect(() => {
        setIsAuthChecked(true);
    }, [isAuthenticated]);

    if (!isAuthChecked) return <div>Loading...</div>;

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

const App = () => {
    return (
        <AuthProvider>
            <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
                <Router>
                    <Suspense fallback={<div>Loading...</div>}>
                        <Routes>
                            {/* Public Routes */}
                            <Route path="/login" element={<LoginPage />} />
                            <Route path="/signup" element={<SignupPage />} />

                            {/* Protected Routes */}
                            <Route element={<ProtectedRoute />}>
                                <Route
                                    path="/chat/:conversation_id?"
                                    element={<ChatApp />}
                                />
                                {/* <Route
                                    path="/dashboard"
                                    element={<Dashboard />}
                                /> */}
                            </Route>

                            {/* 404 Page */}
                            <Route path="*" element={<NotFound />} />
                        </Routes>
                    </Suspense>
                </Router>
            </ThemeProvider>
        </AuthProvider>
    );
};

export default App;
