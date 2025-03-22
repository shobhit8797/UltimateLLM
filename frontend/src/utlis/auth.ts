export const setAuthToken = (token: string) => {
    localStorage.setItem("authToken", token);
};

export const getAuthToken = () => {
    return {
        Authorization: `Bearer ${localStorage.getItem("authToken") || null}`,
    };
};

export const removeAuthToken = () => {
    localStorage.removeItem("authToken");
};
