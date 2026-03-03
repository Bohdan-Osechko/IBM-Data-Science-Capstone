import pandas as pd
import io
import urllib.request

def load_data():
    URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv'
    dataset_part_1_csv = io.BytesIO(urllib.request.urlopen(URL).read())
    return pd.read_csv(dataset_part_1_csv)

def main():
    df = load_data()
    df.head(10)

    # TASK 1: Count launches per site
    launches_per_site = df['LaunchSite'].value_counts()
    print(launches_per_site)

    # TASK 2: Calculate the number and occurrence of each orbit
    orbits = df[df['Orbit'] != 'GTO']['Orbit'].value_counts()
    print("\nOrbit counts (excluding GTO):")
    print(orbits)
    print("\nOrbit counts (including GTO):")
    print(df['Orbit'].value_counts())

    # TASK 3: Calculate the number and occurrence of mission outcome
    landing_outcomes = df['Outcome'].value_counts()
    print("\nLanding outcomes:")
    for i, outcome in enumerate(landing_outcomes.keys()):
        print(i, outcome)

    # TASK 4: Create landing outcome label
    bad_outcomes = set([list(landing_outcomes.keys())[i] for i in [1,3,5,6,7]])
    landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]
    df['Class'] = landing_class
    print("\nClass counts:")
    print(df['Class'].value_counts())
    print("\nLanding outcomes with class labels:")
    for i, outcome in enumerate(landing_outcomes.keys()):
        print(i, outcome, landing_outcomes[outcome], landing_class[i])





    print("\nSuccess rate:", df["Class"].mean())
    print(df.head(1))
    df.to_csv("dataset_part_2.csv", index=False)

main()