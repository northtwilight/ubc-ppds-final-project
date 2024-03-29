#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 18 Mar 2024 11.28am

@author: Massimo Savino
@email: north.twilight@gmail.com

Shebang, encoding declarations and this comment added manually.

tests_reusable_disney_processing.py

"""
# Imports moved to within each method as needed
# as we may import just each function and not the whole file

# Test 1: Basic merge functionality testing
from reusable_disney_processing import *

def test_merge_with_movies_basic():
    import pandas as pd

    # Given: Setup test data with two dataframes to merge
    movie_df = pd.DataFrame(
        {
            "movie_title": ["Movie A", "Movie B", "Movie C"],
            "total_gross": [100, 200, 300],
        }
    )
    right_df = pd.DataFrame(
        {
            "name": ["Movie A", "Movie B", "Movie D"],
            "director": ["Director 1", "Director 2", "Director 3"],
        }
    )

    # When: Merging the dataframes using the merge_with_movies function
    result_df = merge_with_movies(
        movie_df, right_df, "movie_title", "name", "director", "total_gross"
    )

    # Then: The result should match the expected merged and summed dataframe
    expected_df = pd.DataFrame(
        {"director": ["Director 1", "Director 2"], "total_gross": [100, 200]}
    )
    assert result_df.equals(
        expected_df
    ), "The merge_with_movies function didn't produce the expected output."
    # If the above line hasn't fired, we passed, congratulations!
    print("Test 1: Basic merge functionality testing - PASSED")


# Run test 1
# test_merge_with_movies_basic()


# Test 2: Limiting results


def test_merge_with_movies_limit():
    import pandas as pd

    # Given: Setup test data with two dataframes and limiting parameters
    movie_df = pd.DataFrame(
        {
            "movie_title": ["Movie A", "Movie B", "Movie C"],
            "total_gross": [100, 200, 300],
        }
    )
    right_df = pd.DataFrame(
        {
            "name": ["Movie A", "Movie B", "Movie C"],
            "director": ["Director 1", "Director 2", "Director 3"],
        }
    )

    # When: Merging the dataframes using the merge_with_movies function with limits
    result_df = merge_with_movies(
        movie_df,
        right_df,
        "movie_title",
        "name",
        "director",
        "total_gross",
        shouldLimit=True,
        top_num=1,
    )

    # Then: The result should be limited to the top 1 entry as specified
    expected_df = pd.DataFrame({"director": ["Director 1"], "total_gross": [100]})
    assert result_df.equals(
        expected_df
    ), "The merge_with_movies function didn't limit the results correctly."
    # If the above line hasn't fired, we passed, congratulations!
    print("Test 2: Limiting results - PASSED")


# Run test 2
# test_merge_with_movies_limit()


# Test 3: Generating a basic plot


def test_simple_plot_from_basic():
    import pandas as pd
    import altair as alt

    # Given: Setup test data and basic parameters for plotting
    input_df = pd.DataFrame(
        {"genre": ["Action", "Comedy", "Drama"], "gross": [120, 150, 100]}
    )
    col_of_interest = "genre"
    class_letter = "N"
    revenue_type = "gross"

    # When: Generating a plot using the simple_plot_from function
    plot = simple_plot_from(input_df, col_of_interest, class_letter, revenue_type)

    # Then: The function should return an Altair Chart object
    assert isinstance(
        plot, alt.Chart
    ), "The simple_plot_from function should return an Altair Chart."

    # Only if the assertion isn't fired
    print("Test 3: Basic plotting is working - PASSED")


# Run test 3
# test_simple_plot_from_basic()


# Test 4: Custom sort and title


def test_simple_plot_from_sort_and_title():
    import pandas as pd
    import altair as alt

    # Given: Setup test data with sorting and title parameters
    input_df = pd.DataFrame(
        {
            "director": ["Director A", "Director B", "Director C"],
            "adj_gross": [300, 200, 400],
        }
    )
    col_of_interest = "director"
    class_letter = "O"
    revenue_type = "adj_gross"
    interest_title = "Director"
    revenue_title = "Adjusted Gross"
    plot_title = "Revenue by Director"

    # When: Generating a plot with customized sorting and titles
    plot = simple_plot_from(
        input_df,
        col_of_interest,
        class_letter,
        revenue_type,
        interest_title=interest_title,
        revenue_title=revenue_title,
        plot_title=plot_title,
        sort="x",
    )

    # Then: The plot should reflect the provided titles and sorting preference
    assert (
        plot.encoding.x.sort == "x" and plot.title == "Revenue by Director"
    ), "The simple_plot_from function should apply sorting and title customization correctly."

    # Printed only if the test passes/matches the above assertion
    print("Test 4: Custom sort and title - PASSED")


# Run test 4
# test_simple_plot_from_sort_and_title()
