
def first_time_assault_count(survey_df):
    """
    :param survey_df: survey data. Using the "first time experience"
    :return: number of women who have experience first assault during lockdown
    """
    return sum(survey_df.first_time_experience == "yes")


def first_time_assault_percentage(survey_df):
    """
    :param survey_df: survey data. Using the "first time experience"
    :return: % of women who have experience first assault during lockdown
    """
    percentage = sum(survey_df.first_time_experience == "yes") / len(survey_df)
    return "{:.0%}".format(percentage)


def agressor(survey_df, name_agressor):
    """
    :param name_agressor: str with the name of the agressor. Can be "father", "partner", "brother"
    :param survey_df: survey data. Using the "agressor" column
    :return: number of women who have experience first assault during lockdown
    """
    return sum(survey_df.aggressor == name_agressor)
