import { MapPin } from "lucide-react";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "./ui/button";
import { useState } from "react";

export default function Location() {
    const [lat, setLat] = useState<number | null>(null);
    const [lon, setLon] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);

    const detectLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    console.log(position);
                    console.log(position.coords);
                    const { latitude, longitude } = position.coords;
                    setLat(latitude);
                    setLon(longitude);
                    setError(null);
                    console.log(
                        `Coordinates fetched: Latitude ${latitude}, Longitude ${longitude}`
                    );
                },
                (err) => {
                    setError(
                        "Unable to retrieve location. Please enable location services."
                    );
                    console.error("Geolocation error:", err);
                }
            );
        } else {
            setError("Geolocation is not supported by this browser.");
            console.error("Geolocation is not supported by this browser.");
        }
    };

    return (
        <>
            <Dialog>
                <DialogTrigger className="bg-gray-200 p-2 rounded-full">
                    <MapPin />
                </DialogTrigger>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>
                            <Button variant="outline" onClick={detectLocation}>
                                Detect Location
                            </Button>
                        </DialogTitle>
                        <DialogDescription>
                            {lat !== null && lon !== null ? (
                                <p>
                                    Latitude: {lat}, Longitude: {lon}
                                </p>
                            ) : error ? (
                                <p className="text-red-500">{error}</p>
                            ) : (
                                <p>
                                    Click "Detect Location" to get your current
                                    position.
                                </p>
                            )}
                        </DialogDescription>
                    </DialogHeader>
                </DialogContent>
            </Dialog>
        </>
    );
}
