"""
Generate a synthetic but realistic sports broadcast sponsorship dataset.
Simulates what a company like Futures Sport & Entertainment would track:
brand exposure time during broadcasts, camera angles, placements, and
audience/fan sentiment data.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---- Reference data ----
leagues = ["AFL", "NRL", "A-League", "Super Rugby", "BBL"]
broadcasters = ["Channel 7", "Fox Sports", "Channel 9", "Kayo"]
brands = ["Adidas", "Toyota", "Telstra", "Qantas", "XXXX Gold", "Coca-Cola", "CommBank", "Optus"]
placements = ["Jersey Sponsor", "LED Perimeter Signage", "Stadium Signage", "Broadcast Graphics Overlay"]
camera_angles = ["Wide Shot", "Close-up", "Replay", "Aerial/Drone", "Player Cam"]
teams = {
    "AFL": ["Collingwood", "Richmond", "Carlton", "Essendon", "Geelong"],
    "NRL": ["Roosters", "Storm", "Panthers", "Broncos", "Rabbitohs"],
    "A-League": ["Sydney FC", "Melbourne Victory", "Western Sydney Wanderers", "Adelaide United"],
    "Super Rugby": ["Waratahs", "Brumbies", "Reds", "Force"],
    "BBL": ["Sixers", "Thunder", "Heat", "Stars", "Scorchers"],
}

n_matches = 60
records = []
match_id = 1000
start_date = datetime(2025, 8, 1)

for i in range(n_matches):
    league = np.random.choice(leagues)
    broadcaster = np.random.choice(broadcasters)
    match_date = start_date + timedelta(days=int(i * 3.2))
    home, away = np.random.choice(teams[league], size=2, replace=False)
    base_audience = {
        "AFL": 1.4, "NRL": 1.1, "A-League": 0.4, "Super Rugby": 0.5, "BBL": 0.9
    }[league]
    audience_millions = round(base_audience + np.random.normal(0, 0.15), 2)
    audience_millions = max(0.1, audience_millions)

    # Each match has multiple brand exposure events across the broadcast
    n_events = np.random.randint(15, 35)
    for _ in range(n_events):
        brand = np.random.choice(brands)
        placement = np.random.choice(placements)
        angle = np.random.choice(camera_angles, p=[0.30, 0.20, 0.15, 0.10, 0.25])

        # Exposure duration depends on placement + angle
        base_duration = {
            "Jersey Sponsor": 8, "LED Perimeter Signage": 5,
            "Stadium Signage": 4, "Broadcast Graphics Overlay": 12,
        }[placement]
        angle_multiplier = {
            "Wide Shot": 1.3, "Close-up": 1.8, "Replay": 0.7,
            "Aerial/Drone": 0.9, "Player Cam": 1.5,
        }[angle]
        exposure_seconds = max(1, round(np.random.exponential(base_duration * angle_multiplier)))

        # Fan sentiment score 1-5 (from post-match Futures fan surveys), brand-influenced
        sentiment_base = {
            "Adidas": 4.1, "Toyota": 3.8, "Telstra": 3.4, "Qantas": 3.9,
            "XXXX Gold": 3.6, "Coca-Cola": 3.7, "CommBank": 3.3, "Optus": 3.2,
        }[brand]
        sentiment_score = round(np.clip(np.random.normal(sentiment_base, 0.4), 1, 5), 1)

        records.append({
            "match_id": match_id,
            "match_date": match_date.strftime("%Y-%m-%d"),
            "league": league,
            "broadcaster": broadcaster,
            "home_team": home,
            "away_team": away,
            "audience_millions": audience_millions,
            "brand": brand,
            "placement_type": placement,
            "camera_angle": angle,
            "exposure_seconds": exposure_seconds,
            "fan_sentiment_score": sentiment_score,
        })
    match_id += 1

df = pd.DataFrame(records)
df.to_csv("/home/claude/project/sports_brand_exposure_data.csv", index=False)
print(df.shape)
print(df.head())
