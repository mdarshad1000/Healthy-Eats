from typing import Any, List


dietlabels = {
    'balanced': 'Balanced',
    'high-fiber': 'High Fiber',
    'high-protein': 'High Protein',
    'low-carb': 'Low Carb',
    'low-fat': 'Low Fat',
    'low-sodium': 'Low Sodium'
}

healthlabels = {
    'alcohol-free': 'Alcohol-Free',
    'celery-free': 'Celery-Free',
    'dairy-free': 'Dairy-Free',
    'egg-free': 'Egg-Free',
    'fish-free': 'Fish-Free',
    'gluten-free': 'Gluten-Free',
    'keto-friendly': 'Keto-Friendly',
    'low-sugar': 'Low-Sugar',
    'No-oil-added': 'No oil added',
    'peanut-free': 'Peanut-Free',
    'pork-free': 'Pork-Free',
    'red-meat-free': 'Red-Meat-Free',
    'sesame-free': 'Sesame-Free',
    'soy-free': 'Soy-Free',
    'sugar-free': 'Sugar-Free',
    'vegan': 'Vegan',
    'vegetarian': 'Vegetarian',
}

cuisinetype = {
    'american': 'American',
    'asian': 'Asian',
    'british': 'British',
    'central europe': 'Central Europe',
    'chinese': 'Chinese',
    'french': 'French',
    'indian': 'Indian',
    'italian': 'Italian',
    'japanese': 'Japanese',
    'korean': 'Korean',
    'Mediterranean': 'Mediterranean',
    'mexican': 'Mexican',
    'middle eastern': 'Middle Eastern',
}

dishtype = {
    'starter': 'Starter',
    'main course': 'Main Course',
    'side dish': 'Side Dish',
    'drinks': 'Drinks',
    'desserts': 'Desserts'
}

def readable_list(seq: List[Any]) -> str:
    """
    Grammatically correct human readable string from list (with Oxford comma)
    https://stackoverflow.com/a/53981846/19845029
    """
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return ' and '.join(seq)
    return ', '.join(seq[:-1]) + ', and ' + seq[-1]
