import { ThemeProvider } from "@/components/theme-provider";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";

import LoginPage from "@/pages/LoginPage";
import NotFound from "@/pages/NotFound";
import ChatApp from "./pages/ChatApp";
import SignupPage from "./pages/SignupPage";

const App = () => {
    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <Router>
                <Routes>
                    <Route path="/" element={<ChatApp />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/signup" element={<SignupPage />} />
                    {/* <Route path="/about" element={<About />} /> */}
                    <Route path="*" element={<NotFound />} />
                </Routes>
            </Router>
        </ThemeProvider>
    );
};

export default App;
