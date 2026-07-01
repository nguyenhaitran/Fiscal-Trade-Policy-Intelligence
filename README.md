# U.S. Treasury Auction & Economic Policy Analytic Dashboard

An ultimate dashboard analysing U.S. Treasury auction data and its correlation with changes from economic policies (fiscal and trade) derived from news articles.

> 💡 **Data Refresh Schedule:** The U.S. Auction data pipeline automates updates daily, which can be seen on the `U.S. Auction` Page. Viewers are highly recommended to check the dashboard after **1:00 PM Perth Time (AWST)** to ensure the most recent auction results have fully populated.

**Tech Stack: Python, Power BI, Google Service**

## 📄 Project Documentation & Full Report
For the deep-dive project documentation, including our full article classification methodology, please refer to the official report:

👉 **[US Treasury Auction & Economic Policy Analytic Dashboard (Google Docs)](https://docs.google.com/document/d/10gIIDJV6leTY9hmdGoSVN-39W1vZaO_2xpHmWOZmOIs/edit?usp=sharing)**

---

## A. Executive Summary
This project aims to establish an advanced analytics workspace to analyse the correlation between economic policies discussed in the news and how people invest in U.S. Treasury Auctions.

By leveraging a custom Python ETL and text-mining pipeline, thousands of unstructured past articles from the Wall Street Journal were programmatically processed to create volatility-adjusted Economic metrics: the Fiscal Policy Index and the Trade Policy Index. These index trackers are dynamically mapped alongside U.S. Treasury auction data within an optimised relational Star Schema inside Power BI.

Empirical modelling from 2015 to 2025 reveals critical market insights: while escalating political and geopolitical risk increases drive up borrowing costs via higher demanded interest rates, market demand remains highly inelastic, validating the U.S. Treasury’s structural status as a global risk-free asset. Ultimately, this dashboard acts as a source of truth for economic analysts or people interested in economics, transforming fragmented public data and qualitative news sources into quantifiable market intelligence.

## B. Project Objective
### 1. The Importance of The U.S. Treasury Auction
The US Treasury market is the biggest and most liquid financial market in the world, as it is the main source of funding for U.S. government activities. Treasury securities are regarded as the ultimate "risk-free" asset because they are backed by the United States' full faith and credit. As a result, they set the standard for global economic changes and have an impact on everything, from interest rate adjustments to international trade finance.

In combination with analysing the auction results, understanding the underlying drivers of auction demand, high and low yield differences, and bidding behaviour is also significant. One of the driving factors that affects the investing behaviours of investors and dealers is how the shifts in economic policies are communicated to them, and how those economy-change news affects the behaviors.

### 2. Economic Policy and Indices
Treasury auctions are highly sensitive to Economic Policy Indices. Changes in Trade and Fiscal policy create market sentiment that directly impacts investors' decisions.
- Fiscal Policy News shows how a government modifies their spending and tax rates to monitor and influence the national economy. They affect people's expectations around debt supply and long-term sustainability. The index derived from Fiscal Policy News is called the Fiscal Policy Index or the Fiscal Index. 
- Trade Policy News represents how a government exchanges goods and services between countries and the tax or duty imposed by that government on those imported or exported goods and services. This news can affect how much people are interested in the auctions (Bid-to-Cover Ratio) and how big the gap between the highest and lowest yields for the auctions (Auction High-Low Yield Difference). The index derived from Trade Policy News is called the Trade Policy Index or Trade Index.

### 3. Core problems and using the Dashboard as a solution
To analyse the U.S. Treasury Auctions and Economic Policy Shift, there are two primary problems:
- Data Decentralisation: U.S. Treasury Auctions are stored in a massive, unoptimised data spreadsheet with many missing values, large numbers, and an inconsistent format. making it difficult to find the underlying trends.
- Unstructured News Data: The economic news is in text format and includes various topics. The main problem lies in classifying the economic news and converting it into 2 type of economic indices to measure the shifts in the economy.
This dashboard resolves these issues by standardising the economic news into Trade and Fiscal Indices. By aligning them with the standardised US Treasury Auctions in the same timeline, the dashboard allows people to see exactly how specific the economic policy news translates into real-world auction performance.

To bridge this gap, this project was executed following the steps in the Methodology section.

## C. Methodology
### 1. Data Extraction and Ingestion
- To optimise operational costs and maintain data privacy, archival articles were downloaded from the Wall Street Journal via ProQuest. A custom ETL Python script was developed to perform character recognition and tokenisation on PDF sources. These tokens were then processed through a classification model to generate daily Trade and Fiscal Policy Indices.
- Developed a robust Python pipeline to ingest real-time data from the TreasuryDirect API. The script manages API pagination, historical filtering (post-1998), and credential-based authentication via Google Cloud Service Accounts to automate data fetching and pushing into a Google Sheets repository.
- During the extraction phase, the script partitioned the raw data into an optimised relational structure, including three core tables:`Auction`, `Security`, and `Bidder`. 

![Data Modelling](https://github.com/nguyenhaitran/Fiscal-Trade-Policy-Intelligence/blob/main/Dashboard/screenshots/Model.png) 

### 2. In-depth Articles Classification to Index Calculation 
> To maintain repository scannability with comprehensive documentation regarding the articles classification and index calculation, please check section **[2. In-depth Articles Classification to Index Calculation](https://docs.google.com/document/d/10gIIDJV6leTY9hmdGoSVN-39W1vZaO_2xpHmWOZmOIs/edit?pli=1&tab=t.0)** in the report.

### 3. Data Transformation (Power Query)
- Standardised, fragmented, reissued, and reopened debt data by utilising `Original Security Term`. This allowed the categorisation of complex securities into "Short," "Medium," and "Long-Term" maturities for consistent longitudinal analysis.
- To satisfy executive dashboard tracking requirements, wide bidder-type data columns (such as Direct Bidder, Indirect Bidder, Primary Dealer) were programmatically unpivoted into unified Bidder Type and Status dimensions. This step filters out the source data's pre-aggregated total rows, preventing double-counting anomalies and allowing individual participant categories to fill the column height correctly. Additionally, this transformation was critical for enabling dynamic cross-filtering, allowing the dashboard to dynamically update based on specific metric selections.
- Architected a Star Schema within Power BI, implementing a central DateTable as a temporal bridge. This bridge synchronises high-frequency economic indices with periodic auction events, enabling multi-dataset correlation.

### 4. Visualisation (Power BI)
#### i. US Auction Overview
> **Economic Indices Page Reminder:** This view reflects periodic batch processing of unstructured archival news articles. It is **not automatically refreshed in real-time**, as it requires scheduled ETL model runs to parse and tokenise new text data.

![Economic Indices](https://github.com/nguyenhaitran/Fiscal-Trade-Policy-Intelligence/blob/main/Dashboard/screenshots/US%20Auction%20Page.png)

- Display total number of Auctions, Average Bid-to-Cover Ratios, Interest Rates, and Auction Median Yields. These scorecards will be dynamically updated based on the selected timeframe, security types, and security terms provided by viewers.
- Incorporates time-series line charts with automated linear regression trend lines to track long-term average Bid-to-Cover Ratios, Interest Rates, Auction High-Low Yield Differences.

#### ii. Economic Policy Analysis
![US Treasury Auctions](https://github.com/nguyenhaitran/Fiscal-Trade-Policy-Intelligence/blob/main/Dashboard/screenshots/Economic%20Indices%20Page.png) 
- Display the Fiscal and Trade Policy Indices, both standardised to a baseline historical average of 100. An index score of 150 signifies that the article's discussion intensity is 50% higher than the average baseline. Additional constant time stamps also support analysing the Indices trends based on the events. 
- A categorical Treemap detailing the specific term discussions driving the active index peaks. The displayed terms are related to Fiscal and Trade Policy, not to what was discussed in the articles at that point in time.

#### iii. Accepted vs Tendered Comparison
![Accepted vs Tendered Comparison](https://github.com/nguyenhaitran/Fiscal-Trade-Policy-Intelligence/blob/main/Dashboard/screenshots/Accepted%20vs%20Tendered.png)
- With the Accepted and Tendered side-by-side Stacked Barchart, it creates an ease for the viewers to compare the auction amounts and ratios between the two. Additionally, with the bidder type filter, it is easy to analyse how much was invested by all bidder types or individually.

#### iv. Policy Index and Market Correlation
![Correlation](https://github.com/nguyenhaitran/Fiscal-Trade-Policy-Intelligence/blob/main/Dashboard/screenshots/Correlation.png)
- Created scatterplots to find the correlation between fiscal and trade policy indices with auction yield, high-low yield difference and average interest rate. Additionally, the page also supports deeper analysis of how different the correlations are based on selected timeframe, security types and security terms filters. 

## D. Insights
### 1. Economic Policy Sentiment (2015–2025)
- The Trade Policy Index during the Trump administration reached intensities 2–2.5 times higher than those recorded during the COVID-19 pandemic or before the end of 2016. This significantly high index is because President Trump made many changes when he was in administration, leading to a significant rise in the volume of Trade Policy articles. The Fiscal Policy Index also shared a similar trend as the Trade Policy Index, with around 20% to 40% increased within the Trump administration.
- A granular shift in policy narrative was observed between Trump's election cycles: 
    - The 2016–2020 period was characterised by targeted trade negotiations, specifically with China (U.S.-China trade war).
    - The 2024 election cycle has seen a pivot toward broader, global  frameworks, which is also a topic within trade policy discussion.

### 2. U.S. Treasury Auctions Dynamics (2010–Present)
- There was a long-term downward trend observed in the Bid-to-Cover Ratio. This signals deep shifts in institutional primary dealer absorption capacity over time. While demand remained above the historical baseline (which will be discussed in the Accepted vs Tendered Comparison page later), the recent trend indicates an overall change in how the market is willing to invest.
- The High-Low Yield Spread serves as a proxy for auction pricing disagreement, exhibiting massive post-pandemic widening between 2018 and 2022, followed by a sharp climb starting in the second half of 2024 to now. This points to acute market friction in accurately pricing the debts during Trump's administration and the COVID Pandemic.
- The metrics capture clear interest rate inversions in the two years following the 2016 election cycle and 2020 pandemic, highlighting acute short-term capital stress before returning to normalised, stabilising long-term yield bounds. Overall, the interest rates for all security terms are going up, indicating that bidders are expecting higher returns from their debts.

### 3. The Connection of Policy Indices & Auction Results (2015–2025)
The decade between 2015 and 2025 illustrates a profound connection between Trade and Fiscal Policies and the US Treasury market.
- 2017 – Beginning of 2020 Period (The Trade Shock): High Trade Index scores during the initiation of the U.S.-China trade conflict synchronised with a widened High-Low Yield Difference, a declined Bid-to-Cover Ratio below the benchmark, and an increased interest rate for short and medium security terms. These trends suggest that while the market is willing to fund the government, there was a high degree of disagreement among bidders on how to price the debt during the economic uncertainty period.
- 2020–2022 Period (The Crisis Support): During the pandemic, all the Economic Policy Indices were below the baseline, and the Interest Rate significantly dropped. Surprisingly, the Bid-to-Cover Ratio went up above the baseline during this time, which represented that the market was willing to support the government debt during the pandemic.
- 2022 - 2024 Period (Post Pandemic Adjustment): While all the Economic Indices remained low during this period, the Average Interest Rate and the Median Yield of short and medium security terms surpassed the long-term ones. This shows because after COVID-19, the market demand shifted its concentration in shorter term liquidities. 
- 2024 – 2025 (The Trade-Tariff Pivot): In the second time of the Trump Administration, the recent surge in the Trade Policy (driven by White House's tariff proposals for all countries) has coincided with another Auction High-Low Yield Difference spike, suggesting another disagreement between bidders on how to price during this second uncertainty. Different from the 2017-2020 period, the market is no longer absorbing news with high demand; instead, the rising Bid-to-Cover Ratio above baseline and the higher long-term security interest rate and yield suggest that investors are becoming more interested and price-conscious at the same time, as the policy volatility period becomes a normal thing.

### 4. Accepted vs Tendered Amount Comparison
- The total amount of capital tendered by investors has grown exponentially since 2010, aggressively scaling from roughly $24 Trillion to a peak of over $65 Trillion in 2025. Conversely, the actual volume accepted by the Treasury has grown at a much slower, controlled pace from $7 trillion to $24 Trillion. This wide gap demonstrates that despite shifting political and economic regimes, market liquidity and bidders' appetite for U.S. sovereign debt remain extremely large. 
- Looking at the internal stacked segments, Primary Dealers (dark green) and Competitive Bidders (light orange) systematically absorb the largest percentage share of the Tendered column during high-volume spikes, most notably between 2023 and 2025, where their bid volume crossed $20 and $30 Trillion, respectively. Additionally, the Accepted amounts  remained so small for Primary Dealers and Competitive Bidders, with the accepted amount around $3 Trillion and $11 Trillion, respectively. This highlights their structural role as the market’s primary backstop during aggressive debt expansion cycles and how competitive they are.

### 5. Policy Indices vs. Auction Metrics Correlation
- Both Trade and Fiscal policy uncertainty show a clear, positive correlation with rising interest rates. As political changes intensify in the media, investors demand a higher yield premium to hedge against policy risks.
- The Bid-to-Cover Ratio remains remarkably flat across all index spikes. This proves that while policy friction causes investors to adjust their pricing targets (yields), it does not diminish their fundamental intent to buy US Treasuries as a safe asset.
- While trade spikes cause minor variance in price dispersion, intense fiscal media spikes (like budget battles and debt ceiling standoffs) actually correlate with a narrower High-Low Yield Spread. This suggests that primary dealers tightly consolidate their bidding strategies around specific technical prices when domestic supply risks rise.

## E. Future Prediction
Until now, the articles' data for 2026 have not been processed to quantify the shifts in the economic indices. However, with numerous articles discussing the recent conflict between the U.S. and Iran, which dramatically disrupted the global supply chains, based on historical data, the Trade Policy Index would rise and reach a new peak. Additionally, as the market trend is no longer absorbing the policy news, the Bid-to-Cover Ratio would potentially still go up above the baseline, along with a higher interest rate demanded from the bidders to hedge against the inflation of the risk from the war. The Auction High-Low Yield Difference would still persist to be large, and the bidder may continue to favour long-term investment to avoid any changes in policy from Trump until a future presidential transition occurs.
