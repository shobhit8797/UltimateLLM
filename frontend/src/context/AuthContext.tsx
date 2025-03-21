import {
    createContext,
    useContext,
    useEffect,
    useState,
    ReactNode,
    useMemo,
} from "react";
import { getAuthToken, removeAuthToken, setAuthToken } from "../utlis/auth";

interface AuthContextType {
    isAuthenticated: boolean;
    login: (token: string) => void;
    logout: () => void;
}

// Create context with default undefined to enforce provider usage
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [token, setToken] = useState<string | null>(getAuthToken());

    useEffect(() => {
        setToken(getAuthToken());
    }, []);

    const isAuthenticated = !!token;

    const login = (newToken: string) => {
        setAuthToken(newToken);
        setToken(newToken);
    };

    const logout = () => {
        removeAuthToken();
        setToken(null);
    };

    // Memoize the context value to prevent unnecessary re-renders
    const authValue = useMemo(
        () => ({ isAuthenticated, login, logout }),
        [isAuthenticated]
    );

    return (
        <AuthContext.Provider value={authValue}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom hook for using authentication context
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
