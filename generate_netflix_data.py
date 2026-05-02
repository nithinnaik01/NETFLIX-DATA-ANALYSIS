import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 8000

genres = ['Drama', 'Comedy', 'Action', 'Thriller', 'Documentary',
          'Horror', 'Romance', 'Sci-Fi', 'Animation', 'Crime',
          'Biography', 'Fantasy', 'Mystery', 'Adventure', 'Family']

countries = ['United States', 'India', 'United Kingdom', 'Canada',
             'France', 'Germany', 'Japan', 'South Korea', 'Spain',
             'Australia', 'Brazil', 'Mexico', 'Italy', 'Turkey', 'Nigeria']

ratings = ['TV-MA', 'TV-14', 'TV-PG', 'R', 'PG-13', 'PG', 'G', 'TV-Y', 'TV-G', 'NR']
types = ['Movie', 'TV Show']

data = {
    'show_id': [f's{i}' for i in range(1, n + 1)],
    'type': np.random.choice(types, n, p=[0.7, 0.3]),
    'title': [f'Title_{i}' for i in range(1, n + 1)],
    'director': [f'Director_{random.randint(1, 500)}' for _ in range(n)],
    'country': np.random.choice(countries, n, p=[0.35, 0.15, 0.1, 0.05,
                                                   0.05, 0.04, 0.04, 0.04,
                                                   0.03, 0.03, 0.03, 0.03,
                                                   0.02, 0.02, 0.02]),
    'date_added': pd.date_range(start='2015-01-01', periods=n, freq='8h').strftime('%Y-%m-%d'),
    'release_year': np.random.choice(
        range(2000, 2023),
        n,
        p=(np.array([0.01] * 10 + [0.02] * 3 + [0.04, 0.05, 0.06, 0.07,
                   0.08, 0.09, 0.10, 0.10, 0.09, 0.09])
           / np.sum([0.01] * 10 + [0.02] * 3 + [0.04, 0.05, 0.06, 0.07,
                    0.08, 0.09, 0.10, 0.10, 0.09, 0.09]))),
    'rating': np.random.choice(ratings, n, p=[0.30, 0.25, 0.10, 0.12,
                                               0.08, 0.05, 0.03, 0.03,
                                               0.02, 0.02]),
    'listed_in': np.random.choice(genres, n),
    'duration': [f'{random.randint(60, 180)} min' if t == 'Movie'
                 else f'{random.randint(1, 8)} Season(s)'
                 for t in np.random.choice(types, n, p=[0.7, 0.3])],
    'description': [f'Description for title {i}.' for i in range(1, n + 1)]
}

df = pd.DataFrame(data)
df.to_csv('netflix_data.csv', index=False)
print(f"✅ Netflix dataset created: {len(df)} titles")
print(f"   Movies: {(df['type']=='Movie').sum()}")
print(f"   TV Shows: {(df['type']=='TV Show').sum()}")
print("   Saved as: netflix_data.csv")
