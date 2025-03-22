import MainLayout from "@/components/layouts/MainLayout";
import { ThemeProvider } from "@/components/Theme/theme-provider";
import { Suspense, lazy } from "react";
import {
    Navigate,
    Outlet,
    Route,
    BrowserRouter as Router,
    Routes,
} from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";

const LoginPage = lazy(() => import("@/components/pages/LoginPage"));
const SignupPage = lazy(() => import("@/components/pages/SignupPage"));
const ChatApp = lazy(() => import("@/components/pages/ChatApp"));
const NotFound = lazy(() => import("@/components/pages/NotFound"));

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
                            <Route element={<MainLayout />}>
                                <Route
                                    path="/chat/:conversation_id?"
                                    element={<ChatApp />}
                                />
                            </Route>
                        </Route>

                        {/* 404 Page */}
                        <Route path="*" element={<NotFound />} />
                    </Routes>
                </Suspense>
            </Router>
        </ThemeProvider>
    </AuthProvider>
);

export default App;
