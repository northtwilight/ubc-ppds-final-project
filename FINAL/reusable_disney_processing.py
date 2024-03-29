#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 18 Mar 2024 11.34am

@author: Massimo Savino
@email: north.twilight@gmail.com

Shebang, encoding declarations and this comment added manually.

reusable_disney_processing.py

"""
import pandas as pd 
import altair as alt 


def merge_with_movies(
    movie_df,
    right_df,
    movie_key_col,
    right_key_col,
    col_of_interest,
    col_revenue,
    shouldLimit=False,
    top_num=None,
):
    """
    Merges the movie_df with a right_hand_df

    Parameters
        movie_df - Object, Pandas Left-hand (LH) side dataframe
        right_df - Object, Pandas Right-hand (RH) side dataframe
        movie_key_col - String, LH primary key, needs to be matched against the next parameter below
        right_key_col - String, RH primary key
        col_of_interest - String, The column we're really interested in
        col_revenue - Float, total gross revenue, or adj for inflation
        shouldLimit - Optional bool, when true you should enter a number below
        top_n - Optional int, number to restrict output against

    Raises
        Exception as e
        ValueError via Exception as e

    Returns
        A merged DataFrame, which then can be plugged into Altair

    Examples
        directors_analysis = merge_with_movies(
            movies,
            directors,
            'movie_title',
            'name',
            'director',
            'total_gross'
        )
        directors_analysis <Pandas.DataFrame>
    """
    try:
        merge_df = pd.merge(
            movie_df,
            right_df,
            left_on=movie_key_col,
            right_on=right_key_col,
            how="inner",
        )

        merge_df

        # Group by col_of_interest and sum by units of col_revenue
        interest_group_df = (
            merge_df.groupby(col_of_interest)[col_revenue].sum().reset_index()
        )

        if shouldLimit:
            interest_group_sorted = interest_group_df.sort_values(
                by=col_revenue, ascending=True
            ).head(top_num)
        else:
            interest_group_sorted = interest_group_df.sort_values(
                by=col_revenue, ascending=True
            )

        return interest_group_sorted

    except Exception as e:
        print("Error: ", e)
        raise ValueError("Unable to merge desired dataframes") from e


def simple_plot_from(
    input_df,
    col_of_interest,
    class_letter,
    revenue_type,
    interest_title=None,
    revenue_title=None,
    plot_title=None,
    sort="y",
    top_n=None,
):
    """
    Constructs a simple Altair plot from defined inputs

    Parameters:
        input_df - input dataframe
        col_of_interest - String, what we're looking to investigate
        class_letter - String, classification
        revenue_type - gross or adj revenues
        interest_title=None - optional String
        revenue_title=None - optional String
        plot_title=None - optional String
        sort="y" - optional String
        top_n=None - optional Int

    Raises:
        Exception as e
        ValueError from within the exception

    Returns
        Simple ranked Altair bar chart graph

    Examples
        cinematographers_plotted = simple_plot_from(
            cinematographers_analysed,
            'cinematographer',
            'N',
            "total_gross",
            "Cinematographers",
            "Total gross revenue",
            "Top cinematographers by revenue")

        cinematographers_plotted <Altair chart>

    """
    try:
        simple_plot = (
            alt.Chart(input_df)
            .mark_bar()
            .encode(
                x=alt.X(
                    f"{col_of_interest}:{class_letter}",
                    title=interest_title if interest_title != None else "",
                    sort=sort,
                ),
                y=alt.Y(
                    f"{revenue_type}:Q",
                    title=revenue_title if revenue_title != None else "",
                ),
            )
            .properties(title=plot_title if plot_title != None else "")
        )
        return simple_plot

    except Exception as e:
        print("Error: ", e)
        raise ValueError("Unable to merge desired dataframes") from e


def analyze_by_genre(
    movie_df, 
    right_df, 
    movie_key_col, 
    right_key_col, 
    genre_col, 
    col_of_interest, 
    col_revenue):
    """
    Analyzes the profitability of people (ie directors) by movie genre.

    Parameters:
        movie_df - DataFrame containing movie data
        right_df - DataFrame containing data of the people (e.g., directors)
        movie_key_col - Column in movie_df to merge on (e.g., 'movie_title')
        right_key_col - Column in right_df to merge on (e.g., 'name')
        genre_col - Column in movie_df representing the genre
        col_of_interest - Column in right_df representing the person of interest (e.g., 'director')
        col_revenue - Column in movie_df representing the revenue (e.g., 'total_gross')
        
    Raises:
        ValueError via an Exception

    Returns:
        DataFrame with each genre and the total gross revenue for each person in that genre
    """
    try:
        # Merge the movie and right dataframes
        merged_df = pd.merge(
            movie_df,
            right_df,
            left_on=movie_key_col,
            right_on=right_key_col,
            how="inner"
        )

        # Group by genre and the column of interest, then sum the revenue
        result_df = merged_df.groupby([genre_col, col_of_interest])[col_revenue].sum().reset_index()

        # Sort the results by genre and then by total gross revenue in descending order
        result_df = result_df.sort_values(by=[genre_col, col_revenue], ascending=[True, False])

        return result_df
    except Exception as e:
        print("Error: ", e)
        raise ValueError("Unable to merge movies with intended DF") from e





def find_top_n_genre_people(
    movie_df,
    right_df,
    movie_key_col,
    right_key_col,
    genre_col,
    col_of_interest,
    col_revenue,
    genre_of_interest,
    top_n
):
    """
    Picks out the top_n [personnel] (your choice) by genre (also your choice)
    
    Parameters
        movie_df - DataFrame containing movie data
        right_df - DataFrame containing data of the people (e.g., directors)
        movie_key_col - Column in movie_df to merge on (e.g., 'movie_title')
        right_key_col - Column in right_df to merge on (e.g., 'name')
        genre_col - Column in movie_df representing the genre (NOT 'Adventure', but 'genre')
        col_of_interest - Column in right_df representing the person of interest (e.g., 'director')
        col_revenue - Column in movie_df representing the revenue (e.g., 'total_gross')
        genre_of_interest - The film category we want to explore
        top_n - Fill with the number of highest-performing people in this genre you want to see

    Results
        Returns a small number (n) of top performers by your chosen genre
    
    Raises
        Exception on error
        Raises ValueError from that Exception
        
    Examples
        adventure_directors_test = find_top_n_genre_people(
            movies,
            directors,
            'movie_title',
            'name',
            'genre',
            'director',
            'total_gross',
            'Adventure',
            7
        )
        <Returns a Pandas dataframe suitable for plotting in Altair.>
    """
    try:
        mashup = analyze_by_genre(
            movie_df,
            right_df,
            movie_key_col,
            right_key_col,
            genre_col,
            col_of_interest,
            col_revenue
        )
        top_n_from_mashup = mashup[mashup[genre_col] == genre_of_interest].head(top_n)

        return top_n_from_mashup

    except Exception as e:
        print('Error: ', e)
        raise ValueError('Unable to analyse top performers in your chosen genre') from e



def side_plot_for_genre_people(
    df_to_load,
    x_col,
    x_letter,
    x_title,
    y_col,
    y_letter,
    y_title,
    plot_title
):
    """
    Outputs an Altair horizontal plot of personnel by genre in dollar terms
    
    Parameters
        df_to_load - the dataframe we want to analyse (see find_top_n_genre_people)
        x_col - the horizontal axis to plot (this is the y-axis in our other plot method)
        x_letter - Ordinality, etc for units of measure along the x-axis
        x_title - The display title for the x-axis
        y_col - the vertical axis we want
        y_letter - Ordinality, etc for the x-axis
        y_title - The display title for the y-axis
        plot_title - Overall title for the plot at large
    
    Results
        Returns a horizontally-aligned plot for display
    
    Raises
        General exception is created on error
        ValueError is raised from this general exception
    
    Examples
        test_df # Created by find_top_n_genre_people, use its parameters here
        
        side_plot = side_plot_for_genre_people(
            test_df,
            x_col,
            x_letter,
            x_title,
            y_col,
            y_letter,
            y_title,
            plot_title
        )
    
    """
    try:
        # something
        chart = alt.Chart(df_to_load).mark_bar().encode(
            x=alt.X(
                f"{x_col}:{x_letter}",
                title=x_title
            ),
            y=alt.Y(
                f"{y_col}:{y_letter}",
                title=y_title,
                sort='-x'
            ),
        ).properties(title=plot_title)
        
        return chart

    except Exception as e:
        print("Error ", e)
        raise ValueError("Unable to plot personnel for your chosen genre")        