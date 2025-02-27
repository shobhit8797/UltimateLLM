import Categories from "@/components/categories";
import Navbar from "@/components/navbar";

const Home = () => {
    return (
        <main className="flex flex-col w-full">
            <Navbar />
            <div className="w-[80%] mx-auto">
                <Categories />
            </div>
        </main>
    );
};

export default Home;
