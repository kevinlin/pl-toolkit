import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define the keywords
kw_list = ["GlueStack", "React Native Paper", "Victory", "NativeBase"]

# Get Google Trends data
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
interest_over_time_df = pytrends.interest_over_time()

# Plot the trends
plt.figure(figsize=(14, 8))
for keyword in kw_list:
    plt.plot(interest_over_time_df[keyword], label=keyword)

plt.title('Google Search Trends Over the Past Year')
plt.xlabel('Date')
plt.ylabel('Interest')
plt.legend(title='Libraries')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig('google_trends.png')

# Show the plot
plt.show()

# Display the dataframe
print(interest_over_time_df.head())