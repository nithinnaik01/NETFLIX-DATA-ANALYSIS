"""
==============================================
PROJECT 2: Netflix Content Strategy Analysis
By: PALTHIYA NITHIN NAIK
==============================================
"""

# ── STEP 0: Import Libraries ──────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  NETFLIX CONTENT STRATEGY ANALYSIS")
print("=" * 55)

# ── STEP 1: Load Data ─────────────────────────────────────────────
print("\n📂 STEP 1: Loading Netflix Dataset...")
df = pd.read_csv('netflix_data.csv')
print(f"   Total Titles: {len(df)}")
print(f"   Columns: {list(df.columns)}")
print(f"\n   First 3 rows preview:")
print(df.head(3).to_string())

# ── STEP 2: Data Cleaning ─────────────────────────────────────────
print("\n🧹 STEP 2: Data Cleaning...")
print(f"   Missing values before:\n{df.isnull().sum()}")
df.dropna(subset=['country', 'rating'], inplace=True)
df['date_added'] = pd.to_datetime(df['date_added'])
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
print(f"   After cleaning: {len(df)} records")

# ── STEP 3: SQL Analysis ──────────────────────────────────────────
print("\n🗄️  STEP 3: SQL-Based Analysis...")

# Load data into SQLite
conn = sqlite3.connect(':memory:')
df.to_sql('netflix', conn, index=False, if_exists='replace')

# SQL Query 1: Content by type
query1 = """
SELECT type, COUNT(*) as total_count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix), 2) as percentage
FROM netflix
GROUP BY type
ORDER BY total_count DESC
"""
result1 = pd.read_sql_query(query1, conn)
print("\n   📌 Content by Type:")
print(result1.to_string(index=False))

# SQL Query 2: Top genres
query2 = """
SELECT listed_in as Genre,
       COUNT(*) as total,
       ROUND(AVG(release_year), 1) as avg_release_year
FROM netflix
GROUP BY listed_in
ORDER BY total DESC
LIMIT 10
"""
result2 = pd.read_sql_query(query2, conn)
print("\n   📌 Top 10 Genres:")
print(result2.to_string(index=False))

# SQL Query 3: Top countries
query3 = """
SELECT country,
       COUNT(*) as total_titles,
       SUM(CASE WHEN type='Movie' THEN 1 ELSE 0 END) as movies,
       SUM(CASE WHEN type='TV Show' THEN 1 ELSE 0 END) as tv_shows
FROM netflix
GROUP BY country
ORDER BY total_titles DESC
LIMIT 10
"""
result3 = pd.read_sql_query(query3, conn)
print("\n   📌 Top 10 Countries by Content:")
print(result3.to_string(index=False))

# SQL Query 4: Rating distribution
query4 = """
SELECT rating,
       COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix), 2) as percentage
FROM netflix
GROUP BY rating
ORDER BY count DESC
"""
result4 = pd.read_sql_query(query4, conn)
print("\n   📌 Rating Distribution:")
print(result4.to_string(index=False))

# SQL Query 5: Content growth by year
query5 = """
SELECT year_added,
       COUNT(*) as titles_added,
       SUM(COUNT(*)) OVER (ORDER BY year_added) as cumulative_total
FROM netflix
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added
"""
result5 = pd.read_sql_query(query5, conn)
print("\n   📌 Content Growth by Year:")
print(result5.to_string(index=False))

conn.close()

# ── STEP 4: Visualizations ────────────────────────────────────────
print("\n📊 STEP 4: Creating Visualizations...")

fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle('Netflix Content Strategy Dashboard', fontsize=18,
             fontweight='bold', color='#E50914')

# Plot 1 - Content Type Pie
axes[0, 0].pie(result1['total_count'], labels=result1['type'],
               autopct='%1.1f%%', colors=['#E50914', '#221F1F'],
               startangle=90, textprops={'color': 'white', 'fontsize': 12})
axes[0, 0].set_title('Movies vs TV Shows', fontweight='bold', fontsize=13)
axes[0, 0].set_facecolor('#141414')
fig.patch.set_facecolor('#141414')
for ax in axes.flat:
    ax.set_facecolor('#1a1a1a')
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#444')

# Plot 2 - Top Genres
axes[0, 1].barh(result2['Genre'][::-1], result2['total'][::-1],
                color='#E50914', alpha=0.85)
axes[0, 1].set_title('Top 10 Genres', fontweight='bold', fontsize=13)
axes[0, 1].set_xlabel('Number of Titles')

# Plot 3 - Top Countries
axes[1, 0].bar(result3['country'], result3['total_titles'],
               color=['#E50914', '#ff6b6b', '#ff9999',
                      '#ffb3b3', '#ffd1d1', '#b30000',
                      '#cc0000', '#ff3333', '#ff8080', '#ffcccc'])
axes[1, 0].set_title('Top 10 Countries', fontweight='bold', fontsize=13)
axes[1, 0].set_ylabel('Number of Titles')
axes[1, 0].tick_params(axis='x', rotation=45)

# Plot 4 - Rating Distribution
axes[1, 1].bar(result4['rating'], result4['count'], color='#E50914', alpha=0.8)
axes[1, 1].set_title('Rating Distribution', fontweight='bold', fontsize=13)
axes[1, 1].set_ylabel('Count')
axes[1, 1].tick_params(axis='x', rotation=30)

# Plot 5 - Content Growth
axes[2, 0].fill_between(result5['year_added'], result5['titles_added'],
                         alpha=0.7, color='#E50914')
axes[2, 0].plot(result5['year_added'], result5['titles_added'],
                color='white', linewidth=2)
axes[2, 0].set_title('Titles Added Per Year', fontweight='bold', fontsize=13)
axes[2, 0].set_xlabel('Year')
axes[2, 0].set_ylabel('Titles Added')

# Plot 6 - Country breakdown (Movies vs Shows)
x = range(len(result3['country'][:6]))
w = 0.35
axes[2, 1].bar([i - w/2 for i in x], result3['movies'][:6], w,
               label='Movies', color='#E50914')
axes[2, 1].bar([i + w/2 for i in x], result3['tv_shows'][:6], w,
               label='TV Shows', color='#831010')
axes[2, 1].set_xticks(list(x))
axes[2, 1].set_xticklabels(result3['country'][:6], rotation=30, ha='right')
axes[2, 1].set_title('Movies vs TV Shows by Country', fontweight='bold', fontsize=13)
axes[2, 1].set_ylabel('Count')
legend = axes[2, 1].legend()
for text in legend.get_texts():
    text.set_color('white')

plt.tight_layout()
plt.savefig('netflix_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='#141414')
plt.show()
print("   ✅ Dashboard saved as: netflix_dashboard.png")

# ── STEP 5: Business Insights ─────────────────────────────────────
print("\n💡 STEP 5: Key Business Insights...")
print("""
   ┌──────────────────────────────────────────────┐
   │           KEY INSIGHTS SUMMARY               │
   ├──────────────────────────────────────────────┤
   │ 1. Movies dominate the Netflix library       │
   │ 2. Drama & Comedy are top genres             │
   │ 3. US produces most content by far           │
   │ 4. TV-MA rating is most common               │
   │ 5. Content additions grew after 2015         │
   └──────────────────────────────────────────────┘
""")

print("=" * 55)
print("  ✅ PROJECT 2 COMPLETE!")
print("  Files created: netflix_dashboard.png")
print("=" * 55)
