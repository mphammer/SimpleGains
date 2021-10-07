PROTEIN_CALORIES = 4.0 # per gram
CARBOHYDRATE_CALORIES = 4.0 # per gram
DIETARY_FAT_CALORIES = 9.0 # per gram

def calculate_BMR(weight_pounds, height_inches, age_years):
    '''
    Description:
    Returns float for the Base Metabolic Rate (BMR) based on the BiggerLeanerStronger
    formula.
    '''
    weight_kilograms = weight_pounds / 2.201
    height_centimeters = height_inches * 2.54

    return 10.0 * weight_kilograms + 6.25 * height_centimeters - 5.0 * age_years + 5.0

def get_average_weekly_TDEE(BMR, hours_of_weekly_exercise):
    '''
    Description:
    Returns the number of calories you should eat every day of the week 
    assuming you do 'hours_of_weekly_exercise' hours of exercise that week.
    
    BiggerLeanerStronger Notes:
    - 0 hours of exercise/sports has a BMR modifier of 1.15
    - 10 hours of exercise/sports has a BMR modifier of 1.8
    '''
    base_BMR_modifier = 1.15 
    base_hours_of_exercise = 0.0

    end_BMR_modifier = 1.8 
    end_hours_of_exercise = 10.0

    rate_of_modifier_increase_per_hour = (end_BMR_modifier - base_BMR_modifier) / (end_hours_of_exercise - base_hours_of_exercise)

    BMR_modifier_from_exercise = base_BMR_modifier + (rate_of_modifier_increase_per_hour * hours_of_weekly_exercise)

    TDEE = BMR * BMR_modifier_from_exercise

    return TDEE
