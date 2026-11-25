def normalize_price(total_price, quantity, unit):
    """
    Converts given quantity to base unit (kg, L, piece, etc.) 
    and calculates the price per base unit.
    """
    unit = unit.lower().strip()
    
    # Weight conversions -> Base unit: kg
    if unit in ['g', 'gram', 'grams']:
        base_unit = 'kg'
        base_quantity = quantity / 1000
    elif unit in ['kg', 'kilogram', 'kilograms']:
        base_unit = 'kg'
        base_quantity = quantity
        
    # Volume conversions -> Base unit: L
    elif unit in ['ml', 'milliliter', 'milliliters']:
        base_unit = 'L'
        base_quantity = quantity / 1000
    elif unit in ['l', 'liter', 'litre', 'litres', 'liters']:
        base_unit = 'L'
        base_quantity = quantity
        
    # Other units (piece, pack, box) -> No conversion needed
    else:
        base_unit = unit
        base_quantity = quantity

    # Calculate normalized price
    try:
        normalized_unit_price = total_price / base_quantity
        return round(normalized_unit_price, 2), base_unit
    except ZeroDivisionError:
        return 0.0, base_unit

# Testing the logic (Idhi run chesi test cheyachu)
if __name__ == "__main__":
    # Test Case: ₹550 for 4 Litres -> Should be ₹137.5 / L
    price, base = normalize_price(550, 4, 'L')
    print(f"Test 1: ₹{price} per {base}") 
    
    # Test Case: ₹60 for 500 grams -> Should be ₹120 / kg
    price, base = normalize_price(60, 500, 'g')
    print(f"Test 2: ₹{price} per {base}")