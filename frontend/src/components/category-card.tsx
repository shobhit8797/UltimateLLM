interface CategoryCardProps {
    category: {
        image: string;
        image_title: string;
    };
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category }) => {
    return (
        <div className="w-fit">
            <img
                src={category.image}
                alt={category.image_title}
                className="h-48 w-96 object-scale-down"
            />
        </div>
    );
};

export default CategoryCard;
