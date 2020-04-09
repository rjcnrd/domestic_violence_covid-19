
def first_time_assault_count(survey_df):
    """
    :param survey_df: survey data. Using the "first time experience"
    :return: number of women who have experience first assault during lockdown
    """
    return sum(survey_df.first_time_experience == "yes")
