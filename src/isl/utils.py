import functools

import polars as pl


@functools.cache
def get_data(name: str) -> pl.DataFrame:
    """
    >>> get_data('Auto').columns[:4]
    ['mpg', 'cylinders', 'displacement', 'horsepower']
    """
    return pl.read_csv(f"https://raw.githubusercontent.com/intro-stat-learning/ISLP/refs/heads/main/ISLP/data/{name}.csv")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("All tests passed")
