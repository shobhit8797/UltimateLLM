import { FaSearch, FaUser } from "react-icons/fa"; // Assuming you use react-icons for icons
import { Button } from "@/components/ui/button";
import { ModeToggle } from "./mode-toggle";
import { Input } from "@/components/ui/input";
import Location from "@/components/location-component";

const Navbar = () => {
    return (
        <nav className="w-full flex justify-between items-center px-4 py-4  border-b">
            <div className="flex flex-col">
                <span className="text-2xl font-bold">SmartSaving</span>
            </div>
            <Location />
            <Input
                type="text"
                placeholder="Search"
                className="p-2 rounded-full "
            />
            {/* <FaSearch className="text-gray-500 mr-2" /> */}
            <div className="flex items-center">
                <FaUser className="text-gray-700 mr-2" />
                <span className="text-sm text-gray-700 mr-4">Login</span>
            </div>
            <ModeToggle />
            <Button variant="outline" className="boder">
                Cart
            </Button>
        </nav>
    );
};

export default Navbar;
