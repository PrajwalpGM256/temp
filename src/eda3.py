# eda.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

sns.set()

# Ensure 'figs' directory exists
output_dir = "/home/paztino/idmdp/finalproject2/maine-testimony/src/figs"
os.makedirs(output_dir, exist_ok=True)

# Load data from the functions in bills.py
from bills import list_bills, list_testimony

# Retrieve and display bills data
df_bills = list_bills()
print("Bills Data Overview:")
print(df_bills.info())
print(df_bills.head())

# Retrieve and display testimony data
df_testimony = list_testimony()
print("Testimony Data Overview:")
print(df_testimony.info())
print(df_testimony.head())

# Amendment Distribution
df_bills['has_amendment'] = df_bills['amendment'].notna()
amendment_counts = df_bills['has_amendment'].value_counts()
plt.figure(figsize=(6, 4))
sns.barplot(x=amendment_counts.index, y=amendment_counts.values, palette="viridis")
plt.title("Bills with and without Amendments")
plt.xticks(ticks=[0, 1], labels=["No Amendment", "Has Amendment"])
plt.xlabel("Amendment Status")
plt.ylabel("Number of Bills")
plt.savefig(f"{output_dir}/amendment_counts.png")
plt.show()

# Top Amendments
top_amendments = df_bills['amendment'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_amendments.values, y=top_amendments.index, palette="coolwarm")
plt.title("Top 10 Amendments by Frequency")
plt.xlabel("Frequency")
plt.ylabel("Amendment Code")
plt.savefig(f"{output_dir}/top_10_amendments.png")
plt.show()

# Bill Text Analysis (Word Cloud)
bill_texts = " ".join(df_bills['text'].dropna().apply(lambda x: " ".join(x)))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(bill_texts)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Common Words in Bill Texts")
plt.savefig(f"{output_dir}/bill_text_wordcloud.png")
plt.show()

# Bill Length Distribution
df_bills['text_length'] = df_bills['text'].apply(lambda x: len(" ".join(x)) if isinstance(x, list) else 0)
plt.figure(figsize=(10, 6))
sns.histplot(df_bills['text_length'], kde=True, bins=30, color="skyblue")
plt.title("Distribution of Bill Text Lengths")
plt.xlabel("Text Length (characters)")
plt.ylabel("Frequency")
plt.savefig(f"{output_dir}/bill_text_length_distribution.png")
plt.show()

# Common Terms in Titles (Word Cloud) if titles exist
if 'title' in df_bills.columns:
    titles_combined = " ".join(df_bills['title'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles_combined)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Common Words in Bill Titles")
    plt.savefig(f"{output_dir}/bill_title_wordcloud.png")
    plt.show()

# Top Organizations in Testimonies
if 'organization' in df_testimony.columns:
    top_organizations = df_testimony['organization'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_organizations.values, y=top_organizations.index, palette="plasma")
    plt.title("Top 10 Organizations by Testimony Count")
    plt.xlabel("Number of Testimonies")
    plt.ylabel("Organization")
    plt.savefig(f"{output_dir}/top_organizations_testimony.png")
    plt.show()

# Top Individuals in Testimonies
if 'name' in df_testimony.columns:
    top_individuals = df_testimony['name'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_individuals.values, y=top_individuals.index, palette="inferno")
    plt.title("Top 10 Individuals by Testimony Count")
    plt.xlabel("Number of Testimonies")
    plt.ylabel("Individual")
    plt.savefig(f"{output_dir}/top_individuals_testimony.png")
    plt.show()

# Testimonies by Town
if 'town' in df_testimony.columns:
    town_counts = df_testimony['town'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=town_counts.values, y=town_counts.index, palette="viridis")
    plt.title("Top 10 Towns by Testimony Count")
    plt.xlabel("Number of Testimonies")
    plt.ylabel("Town")
    plt.savefig(f"{output_dir}/top_towns_testimony.png")
    plt.show()

# Most Referenced Bills in Testimonies
if 'ld' in df_testimony.columns:
    top_bills_testimony = df_testimony['ld'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_bills_testimony.values, y=top_bills_testimony.index, palette="cool")
    plt.title("Top 10 Bills Referenced in Testimonies")
    plt.xlabel("Number of Testimonies")
    plt.ylabel("Bill ID (LD)")
    plt.savefig(f"{output_dir}/top_bills_testimony.png")
    plt.show()

# Testimony Text Length Distribution
df_testimony['text_length'] = df_testimony['text'].apply(lambda x: len(" ".join(x)) if isinstance(x, list) else 0)
plt.figure(figsize=(10, 6))
sns.histplot(df_testimony['text_length'], kde=True, bins=30, color="salmon")
plt.title("Distribution of Testimony Text Lengths")
plt.xlabel("Text Length (characters)")
plt.ylabel("Frequency")
plt.savefig(f"{output_dir}/testimony_text_length_distribution.png")
plt.show()

print("EDA Completed.")
