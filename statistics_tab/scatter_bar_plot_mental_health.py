import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

nb_ratings = 6
space_between_rating = 1
space_between_gender = 2

def data_gender_rating(survey_df):
    """
    :param survey_df: the survey data. We need the columns gender and mental_health
    :return: a pandas data frame, with 2 indexes : first the gender ("Man", "Woman", "Other", then the mental health grading (from 0 to 5).
    One column "percentage" with the the percentage of people in each mental health category, by gender
    """
    percentage_cat = pd.DataFrame(
        (survey_df.groupby(["gender", "mental_health"])["age"].count() / survey_df.groupby(["gender"])["age"].count()))
    percentage_cat = percentage_cat.rename(columns={"age": "percentage"})
    percentage_cat["percentage"] = percentage_cat["percentage"].round(2) * 100
    return percentage_cat


def location_scatterplot(percentage_cat, num_by_col=5):
    """
    :param percentage_cat: the result of the function data_gender_rating
    :param num_by_col: The number of points by row in each column of mental health rating. Default value is 5
    :return: The location (x,y) for all the points in the graph
    """
    # Columns of our new data frame
    columns = ["gender", "mental_health", "order", "x", "y"]
    # The order of genders in the scatter plot
    order = {"Woman": 0, "Other": 1, "Man": 2}
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
                          point_location["order"] * ((num_by_col + space_between_rating) * nb_ratings + space_between_gender)
    return point_location


def draw_scatterbarplot(survey_df, num_by_col=5):
    """
    :param survey_df: the result of the function location_df
    :param num_by_col: The number of points by row in each column of mental health rating. Default value is 5
    :return: the scatterbarplot
    """
    prepared_data = data_gender_rating(survey_df)
    location_df = location_scatterplot(prepared_data, num_by_col)
    # Position of the grading of mental health
    start_position1 = np.median(range(num_by_col))
    start_position2 = (num_by_col + space_between_rating) * nb_ratings + space_between_gender + start_position1
    start_position3 = ((num_by_col + space_between_rating) * nb_ratings + space_between_gender)*2 + start_position1
    mental_health_position_x = [start_position1 + x * (num_by_col + space_between_rating) for x in range(nb_ratings)] + [start_position2 + x * (num_by_col + space_between_rating) for x in range(nb_ratings)] + [start_position3 + x * (num_by_col + space_between_rating) for x in range(nb_ratings)]
    mental_health_position_y = [-0.25] * 18
    mental_health_label = [int(x) for x in list(range(6)) * 3]

    # Position of the gender label
    gender_position_x = [(num_by_col + 1)*nb_ratings / 2 - 1,
                         (num_by_col + 1)*nb_ratings +space_between_gender + (num_by_col + 1)*nb_ratings / 2 - 1,
                         ((num_by_col + 1)*nb_ratings +space_between_gender)*2 + (num_by_col + 1)*nb_ratings / 2 - 1]
    gender_position_y = [-1] * 3
    gender_text_label = ["Woman", "Other", "Man"]

    # Position of the small lines between the gradings
    small_line_position = [start_position1 + x *(num_by_col + space_between_rating) for x in range(nb_ratings-1)] + [start_position2 + x * (num_by_col + space_between_rating) for x in range(nb_ratings-1)] + [start_position3 + x * (num_by_col + space_between_rating) for x in range(nb_ratings-1)]
    # Position of the big line between the genders
    big_line_position = [nb_ratings*(num_by_col + 1), nb_ratings*(num_by_col + 1)*2+space_between_gender]

    # Graph
    fig = px.scatter(location_df, x="x",
                     y="y", color="gender",
                     color_discrete_sequence=["black", "white", "pink"]) #has to be same order as index, so men, other, women

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
            x=[x + 3, x + 3],
            y=[0, -0.5],
            mode="lines", marker=dict(color="white"),
            hoverinfo="skip"
        ))
    # Big Line
    for x in big_line_position:
        fig.add_trace(go.Scatter(
            x=[x, x],
            y=[-0.5, 4],
            mode="lines",
            marker=dict(color="white"),
            hoverinfo="skip"
        ))

    fig.update_layout(showlegend=False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    fig.update_xaxes(showticklabels=False, visible=False)
    fig.update_yaxes(showticklabels=False, visible=False)
    return fig
