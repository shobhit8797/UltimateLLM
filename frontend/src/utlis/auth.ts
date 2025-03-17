export const setAuthToken = (token: string) => {
    localStorage.setItem("authToken", token);
};

export const getAuthToken = () => {
    return localStorage.getItem("authToken") || null;
};

export const removeAuthToken = () => {
    localStorage.removeItem("authToken");
};
