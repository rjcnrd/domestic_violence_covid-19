import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

nb_ratings = 6
space_between_rating = 1
space_between_gender = 2


def data_gender_rating(survey_df, include_other=True):
    """
    :param survey_df: the survey data. We need the columns gender and mental_health
    :return: a pandas data frame, with 2 indexes : first the gender ("Man", "Woman", "Other", then the mental health grading (from 0 to 5).
    One column "percentage" with the the percentage of people in each mental health category, by gender
    """
    percentage_cat = pd.DataFrame(
        (survey_df.groupby(["gender", "mental_health"])["age"].count() / survey_df.groupby(["gender"])["age"].count()))
    percentage_cat = percentage_cat.rename(columns={"age": "percentage"})
    percentage_cat["percentage"] = percentage_cat["percentage"].round(2) * 100
    if not include_other:
        percentage_cat = percentage_cat.drop("Other")
    return percentage_cat


def location_scatterplot(percentage_cat, num_by_col=5):
    """
    :param percentage_cat: the result of the function data_gender_rating
    :param num_by_col: The number of points by row in each column of mental health rating. Default value is 5
    :return: The location (x,y) for all the points in the graph
    """
    # Columns of our new data frame
    columns = ["gender", "mental_health", "order", "x", "y"]
    # Number of genders
    number_gender = len(percentage_cat.groupby(level=0))
    # The order of genders in the scatter plot
    if number_gender == 3:
        order = {"Woman": 0, "Other": 1, "Man": 2}
    else:
        order = {"Woman": 0, "Man": 1}
    # Create an empty dataframe
    point_location = pd.DataFrame(columns=columns)
    for index, percentage in percentage_cat.iterrows():
        for number in range(int(percentage.values)):
            y_location = number // num_by_col
            x_location = number % num_by_col
            point_location = point_location.append({"gender": index[0],
                                                    "mental_health": index[1],
                                                    "order": order[index[0]],
                                                    "x": x_location,
                                                    "y": y_location}, ignore_index=True)
    # The place in the mental health column + Adding a shift for the mental health + Adding a shift for the gender
    point_location["x"] = point_location["x"] + \
                          point_location["mental_health"] * (num_by_col + space_between_rating) + \
                          point_location["order"] * (
                                  (num_by_col + space_between_rating) * nb_ratings + space_between_gender)
    return point_location


def draw_scatterbarplot(survey_df, num_by_col=5, include_other=True):
    """
    :param survey_df: the result of the function location_df
    :param num_by_col: The number of points by row in each column of mental health rating. Default value is 5
    :return: the scatterbarplot
    """
    prepared_data = data_gender_rating(survey_df, include_other=include_other)
    location_df = location_scatterplot(prepared_data, num_by_col)
    number_gender = len(prepared_data.groupby(level=0))
    # Position of the grading of mental health
    start_position1 = np.median(range(num_by_col))
    start_position2 = (num_by_col + space_between_rating) * nb_ratings + space_between_gender + start_position1
    start_position3 = ((num_by_col + space_between_rating) * nb_ratings + space_between_gender) * 2 + start_position1
    mental_health_position_x = [start_position1 + x * (num_by_col + space_between_rating) for x in
                                range(nb_ratings)] + [start_position2 + x * (num_by_col + space_between_rating) for x in
                                                      range(nb_ratings)]
    if number_gender == 3:
        mental_health_position_x = mental_health_position_x + [start_position3 + x * (num_by_col + space_between_rating)
                                                               for x in range(nb_ratings)]
    mental_health_position_y = [-2] * number_gender * nb_ratings
    mental_health_label = [int(x) for x in list(range(nb_ratings)) * number_gender]

    # Position of the gender label
    gender_position_x = [(num_by_col + 1)*nb_ratings / 2 - 1,
                         (num_by_col + 1)*nb_ratings +space_between_gender + (num_by_col + 1)*nb_ratings / 2 - 1]

    if number_gender == 3:
        gender_position_x = gender_position_x + [((num_by_col + 1)*nb_ratings +space_between_gender)*2 + (num_by_col + 1)*nb_ratings / 2 - 1]
    gender_position_y = [-5] * 3
    if number_gender == 2:
        gender_text_label = ["Woman", "Man"]
    else :
        gender_text_label = ["Woman", "Other", "Man"]

    # Position of the small lines between the gradings
    small_line_position = [start_position1 + x *(num_by_col + space_between_rating) for x in range(nb_ratings-1)] + [start_position2 + x * (num_by_col + space_between_rating) for x in range(nb_ratings-1)]
    if number_gender == 3:
        small_line_position = small_line_position + [start_position3 + x * (num_by_col + space_between_rating) for x in range(nb_ratings-1)]
    # Position of the big line between the genders
    big_line_position = [nb_ratings*(num_by_col + 1)]
    if number_gender == 3:
        big_line_position=big_line_position+ [nb_ratings*(num_by_col + 1)*2+space_between_gender]

    #Color
    if number_gender == 3:
        color_sequence = ["black", "white", "pink"] # has to be same order as index, so men, other, women
    else :
        color_sequence = ["white", "pink"]

    # Graph
    fig = px.scatter(location_df, x="x",
                     y="y", color="gender",
                     color_discrete_sequence=color_sequence)

    fig.update_traces(hovertemplate=None, hoverinfo='skip')

    # Mental health grade
    fig.add_trace(go.Scatter(
        x=mental_health_position_x,
        y=mental_health_position_y,
        mode="text",
        text=mental_health_label,
        hoverinfo="skip",
        textfont=dict(color="white")
    ))
    # Gender text
    fig.add_trace(go.Scatter(
        x=gender_position_x,
        y=gender_position_y,
        mode="text",
        text=gender_text_label,
        hoverinfo="skip",
        textfont=dict(color="white")
    ))

    # Small line
    for x in small_line_position:
        fig.add_trace(go.Scatter(
            x=[x + np.median(range(num_by_col)) + space_between_rating,
               x + np.median(range(num_by_col)) + space_between_rating],
            y=[0, -3],
            mode="lines", marker=dict(color="white"),
            hoverinfo="skip"
        ))
    # Big Line
    for x in big_line_position:
        fig.add_trace(go.Scatter(
            x=[x, x],
            y=[-3, 4],
            mode="lines",
            marker=dict(color="white"),
            hoverinfo="skip"
        ))

    fig.update_layout(showlegend=False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    fig.update_xaxes(showticklabels=False, visible=False)
    fig.update_yaxes(showticklabels=False, visible=False, scaleanchor="x", scaleratio=1)
    return fig
