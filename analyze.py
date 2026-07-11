"""
Sports Broadcast Brand Exposure & Fan Sentiment Analysis
Analyzes brand exposure time, camera-angle drivers, audience value,
and fan sentiment trends across simulated sports broadcasts.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
NAVY = "#1F3864"
GOLD = "#B7952C"
PALETTE = sns.color_palette([NAVY, GOLD, "#6E9CC4", "#D9A441", "#3B6E8F", "#8C6E1F", "#4F7CAC", "#C99A2E"])

df = pd.read_csv("/home/claude/project/sports_brand_exposure_data.csv")
df["match_date"] = pd.to_datetime(df["match_date"])

# ---------------------------------------------------------
# 1. Brand exposure leaderboard (total seconds across all matches)
# ---------------------------------------------------------
brand_exposure = (
    df.groupby("brand")["exposure_seconds"].sum().sort_values(ascending=False)
)

plt.figure(figsize=(9, 5.5))
sns.barplot(x=brand_exposure.values, y=brand_exposure.index, palette=PALETTE.as_hex())
plt.title("Total Broadcast Exposure Time by Brand", fontsize=14, weight="bold", color=NAVY)
plt.xlabel("Total Exposure (seconds)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("/home/claude/project/chart_1_brand_exposure_leaderboard.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 2. Camera angle impact on exposure duration
# ---------------------------------------------------------
angle_avg = (
    df.groupby("camera_angle")["exposure_seconds"].mean().sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))
sns.barplot(x=angle_avg.index, y=angle_avg.values, palette=PALETTE.as_hex())
plt.title("Average Exposure Duration by Camera Angle", fontsize=14, weight="bold", color=NAVY)
plt.ylabel("Avg Exposure (seconds)")
plt.xlabel("")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("/home/claude/project/chart_2_camera_angle_impact.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 3. Exposure trend over time (weekly)
# ---------------------------------------------------------
weekly = (
    df.set_index("match_date")
    .resample("W")["exposure_seconds"]
    .sum()
)

plt.figure(figsize=(10, 5))
plt.plot(weekly.index, weekly.values, marker="o", color=NAVY, linewidth=2)
plt.fill_between(weekly.index, weekly.values, color=GOLD, alpha=0.15)
plt.title("Weekly Total Brand Exposure Across All Broadcasts", fontsize=14, weight="bold", color=NAVY)
plt.ylabel("Exposure (seconds)")
plt.xlabel("Week")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("/home/claude/project/chart_3_exposure_trend.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 4. Audience size vs exposure value (scatter, by league)
# ---------------------------------------------------------
match_level = df.groupby(["match_id", "league", "audience_millions"])["exposure_seconds"].sum().reset_index()

plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=match_level, x="audience_millions", y="exposure_seconds",
    hue="league", palette=PALETTE.as_hex()[:match_level["league"].nunique()], s=80
)
plt.title("Audience Size vs. Total Match Brand Exposure", fontsize=14, weight="bold", color=NAVY)
plt.xlabel("Audience (millions)")
plt.ylabel("Total Exposure (seconds)")
plt.legend(title="League", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("/home/claude/project/chart_4_audience_vs_exposure.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 5. Fan sentiment by brand
# ---------------------------------------------------------
sentiment_avg = df.groupby("brand")["fan_sentiment_score"].mean().sort_values(ascending=False)

plt.figure(figsize=(9, 5.5))
sns.barplot(x=sentiment_avg.values, y=sentiment_avg.index, palette=PALETTE.as_hex())
plt.title("Average Fan Sentiment Score by Sponsor Brand", fontsize=14, weight="bold", color=NAVY)
plt.xlabel("Avg Sentiment Score (1-5)")
plt.ylabel("")
plt.xlim(0, 5)
plt.tight_layout()
plt.savefig("/home/claude/project/chart_5_fan_sentiment.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# Print key numeric findings for the report
# ---------------------------------------------------------
print("=== TOP BRAND EXPOSURE ===")
print(brand_exposure.head(3))
print("\n=== CAMERA ANGLE AVG EXPOSURE ===")
print(angle_avg)
print("\n=== SENTIMENT LEADERS ===")
print(sentiment_avg.head(3))
print("\n=== CORRELATION: audience vs exposure ===")
print(match_level[["audience_millions", "exposure_seconds"]].corr())
print("\n=== PLACEMENT TYPE AVG EXPOSURE ===")
print(df.groupby("placement_type")["exposure_seconds"].mean().sort_values(ascending=False))
