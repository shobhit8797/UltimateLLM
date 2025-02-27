import CategoryCard from "@/components/category-card";
interface Category {
    aspect_ratio: number;
    image: string;
    image_title: string;
    deeplink: string;
    id: string;
};

const Categories = () => {
    const categoriesList: Category[] = [
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-12/paan-corner_web.png",
            image_title: "Paan Corner",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=229&l1_cat=1982",
            id: "9058276",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-2_10.png",
            image_title: "Dairy, Bread & Eggs",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=14&l1_cat=922",
            id: "9058277",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-3_9.png",
            image_title: "Fruits & Vegetables",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=1487&l1_cat=1489",
            id: "9058278",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-4_9.png",
            image_title: "Cold Drinks & Juices ",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=332&l1_cat=1102",
            id: "9058279",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-5_4.png",
            image_title: "Snacks & Munchies ",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=1237&l1_cat=940",
            id: "9058280",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-6_5.png",
            image_title: "Breakfast & Instant Food",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=15&l1_cat=954",
            id: "9058281",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-7_3.png",
            image_title: "Sweet Tooth",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=9&l1_cat=944",
            id: "9058282",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-8_4.png",
            image_title: "Bakery & Biscuits",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=888&l1_cat=28",
            id: "9058283",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-9_3.png",
            image_title: "Tea, Coffee & Health Drink ",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=12&l1_cat=957",
            id: "9058284",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-10.png",
            image_title: "Atta, Rice & Dal",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=16&l1_cat=1165",
            id: "9058285",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-11.png",
            image_title: "Masala, Oil & More ",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=1557&l1_cat=50",
            id: "9058286",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-12.png",
            image_title: "Sauces & Spreads",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=972&l1_cat=1131",
            id: "9058287",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-13.png",
            image_title: "Chicken, Meat & Fish ",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=4&l1_cat=1362",
            id: "9058288",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-14.png",
            image_title: "Organic & Healthy Living",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=175&l1_cat=801",
            id: "9058289",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-15.png",
            image_title: "Baby Care",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=7&l1_cat=1000",
            id: "9058290",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-16.png",
            image_title: "Pharma & Wellness",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=287&l1_cat=1826",
            id: "9058291",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-17.png",
            image_title: "Cleaning Essentials",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=18&l1_cat=986",
            id: "9058292",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-18.png",
            image_title: "Home & Office ",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=1379&l1_cat=1075",
            id: "9058293",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-19.png",
            image_title: "Personal Care",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=163&l1_cat=696",
            id: "9058294",
        },
        {
            aspect_ratio: 0.68,
            image: "https://cdn.grofers.com/layout-engine/2022-11/Slice-20.png",
            image_title: "Pet Care",
            deeplink: "lising?l0_cat=229&l1_cat=1982",
            // deeplink: "grofers://listing?l0_cat=5&l1_cat=133",
            id: "9058295",
        }
    ];

    return (
        <div>
            <ul className="grid grid-cols-8 md:grid-rows-6 gap-4 justify-center">
                {categoriesList.map((category) => (
                    <CategoryCard category={category} key={category.id} />
                ))}
            </ul>
        </div>
    );
};

export default Categories;
