import { BASE_URL } from "@/env";
import axios from "axios";
import { getAuthToken } from "./auth";

export interface ApiRequestConfig {
    endpoint: string;
    method: "GET" | "POST" | "PATCH";
    payload?: Record<string, any> | string;
    queryParams?: string[];
}

const makeApiRequest = async (config: ApiRequestConfig) => {
    const { endpoint, method, payload, queryParams } = config;

    const queryString = queryParams?.length ? `?${queryParams.join("&")}` : "";
    const fullUrl = `${BASE_URL}/${endpoint}${queryString}`;

    try {
        const apiResponse = await axios({
            url: fullUrl,
            method,
            headers: {
                ...getAuthToken(),
                "Content-Type": "application/json",
            },
            data: method !== "GET" ? payload : undefined,
        });

        return apiResponse.data;
    } catch (error) {
        console.error("API request failed:", error);
        throw error;
    }
};

export default makeApiRequest;
