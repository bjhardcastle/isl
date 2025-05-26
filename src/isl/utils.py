import contextlib
import functools

import polars as pl


@functools.cache
def get_data(name: str) -> pl.DataFrame:
    """
    >>> get_data('Auto').columns[:4]
    ['mpg', 'cylinders', 'displacement', 'horsepower']
    """
    read_csv_kwargs = {}
    match name:
        case 'College':
            read_csv_kwargs['new_columns'] = ['Name']
        case 'Auto':
            read_csv_kwargs['infer_schema_length'] = 1000
    
    # some .csv files are on the website with extra columns, but some only live on github
    for source in (
        f"https://statlearning.com/s/{name}.csv",
        f"https://raw.githubusercontent.com/intro-stat-learning/ISLP/refs/heads/main/ISLP/data/{name}.csv"
    ):
        with contextlib.suppress(Exception):
            df = pl.read_csv(source, **read_csv_kwargs)
            break
    else:
        raise ValueError(f"Could not find data for {name!r} on ISLP website or GitHub repository")
    match name:
        case 'College':
            return df.with_columns(pl.col('Private').replace_strict({'Yes': True, 'No': False}, return_dtype=pl.Boolean))   
        case 'Auto':
            return (
                df
                .with_columns(
                    pl.col('horsepower').replace_strict({'?': None}, default=pl.col('horsepower'), return_dtype=pl.Int32),
                    pl.col('origin').replace_strict({1: 'USA', 2: 'Europe', 3: 'Japan'}, return_dtype=pl.String),
                )
            )
        case _:
            return df
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("All tests passed")
