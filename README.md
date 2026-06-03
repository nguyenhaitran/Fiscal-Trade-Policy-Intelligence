# US Treasury Auction & Economic Sentiment Analytic Dashboard

An ultimate dashboard analyzing U.S. Treasury auction data and its correlation with economic sentiment (fiscal, trade, and tariff) derived from news articles. 

![Dashboard Overview](Dashboard/screenshots/Indicies vs. Treasury Result.png)

Tech Stack: Python, PowerBI, Google Service

---

## A. Background
### 1. The Importance of The US Treasury
The US Treasury market is the biggest and most liquid financial market in the world as it is the main source of funding for US government activities. Treasury securities are regarded as the ultimate "risk-free" asset because they are backed by the United States's full faith and credit. As a result, they set the standard for interest rates globally and have an impact on everything from house mortgages to international trade finance.

### 2. Economic Policy and Indices
Treasury acutions are highly sensitive to Economical Policy Indices. The changes in Trade, Tariff and Fiscal policy create market sentiment that directly impact investors' decisions.
- Fiscal News shows how a governement modifies their spending, tax rates to monitor and influence national economy. They affect people expectation around debt supply and long-term sustainability. 
- Trade and Tariff News represent how a government exchanges goods and services between countries and the tax or duty imposed by that government on those imported or exported goods and services. These news can affect how much people are interested in the auctions (Bid-to-Cover Ratio) and how big the gap between highest and lowest yields for the auctions (Yield Tail or Yield Difference).

### 3. The way the Dashboard resolves the problem
To analysis the US Treasury Auctions and Economic Policy Shift, there are two primary problems:
- Data Decentralisation: US Treasury Auction are stored in a massive, unoptimised data spreadsheet and having many missing values, large numbers, and inconsistent format. making it difficult to find the underlying trends.
- Unstructured News Data: The economical news are in the text-format and includes various topics. The main problem lies in classifying the economical news and converted them into 3 type of economical indices to measure the shifts of the economic.

This dashboard resolves these issues by standardizing the economical news into Trade, Tariff and Fiscal Indices. By aligning them with the standardised US Treasury Auctions in the same timeline, the dashboard allows people to see exactly how specific the economic policy news translate into real-world auction performance.

## B. Methodology
### 1. Data Extraction
- Unstructured Data Processing: To optimize operational costs and maintain data privacy, archival articles were sourced from the Wall Street Journal via ProQuest. A custom ETL Python script was developed to perform character recognition and tokenization on PDF sources. These tokens were then processed through a classification model to generate daily Trade, Tariff, and Fiscal Sentiment Indices.
- API Integration & Automation: Developed a robust Python pipeline to ingest real-time data from the TreasuryDirect API. The script manages API pagination, historical filtering (post-1998), and credential-based authentication via Google Cloud Service Accounts to automate data fetching into a Google Sheets repository.
- Schema Design: During the extraction phase, the script programmatically partitioned the raw data into a relational structure including three core tables: Auction, Security, and Bidder. 


### 2. Data Transformation (Power Query)
- Maturity Normalization: Standardized fragmented reissued debt data by utilizing "originalSecurityTerm". This allowed for the categorization of complex securities into "Short," "Medium," and "Long-Term" maturities for consistent longitudinal analysis.

- Star Schema Modeling: Architected a Star Schema within Power BI, implementing a central DateTable as a temporal bridge. This bridge synchronizes high-frequency economic indices with periodic auction events, enabling multi-dataset correlation.

- Advanced Data Shaping: Performed complex Unpivot operations on Security, Bidder, and Index tables. This transformation was critical for enabling dynamic cross-filtering, allowing the dashboard to dynamically update based on specific metric selections.

### 3. Visualisation (PowerBI)
- Dynamic Trend Mapping: Developed time-series visualizations, in combination of using DAX (Data Analysis Expressions) to calculate advanced financial metrics, such as the Yield Tail (High vs. Low Yield spread).

- Statistical Correlation: Integrated scatter plots with Linear Regression trendlines to empirically test the relationship between economic policy sentiment scores and auction outcomes.

- Hierarchical Drill-Downs: Configured interactive hierarchies for both time-based,  security-based analysis. This allows stakeholders to check between high-level executive summaries and granular, auction-level details seamlessly.

## C. Insights
### 1. Economic Policy Sentiment (2015–2025)
- Geopolitical Volatility: The numbers of Trade and Tariff articles during the Trump administration reached intensities 2–3 times higher than those recorded during the COVID-19 pandemic or before the end of 2016. This significant rise in the volume of Trade and Tariff articles is directly reflected in the sustained peaks of the Trade and Tariff indices.

- Shifting Policy Focus: A granular shift in policy narrative was observed between Trump's election cycles: 
    - The 2016–2020 period was characterized by targeted trade negotiations, specifically with China (US-China trade war).
    - The 2024 election cycle has seen a pivot toward broader, global tariff frameworks.

### 2. US Treasury Auction Dynamics (2010–Present)
- Supply Focus: The Treasury continues to utilize Short-Term Bills as a primary liquidity, hosting significantly higher auction frequencies in this category compared to Medium or Long-Term Notes.

- Erosion of Demand Intensity: Even though the total tendered and total accepted amount increase overtime, there is a visible long-term decline in the Bid-to-Cover Ratio. While demand remained above the historical baseline prior to mid-2016 and during the 2020–2022 eras, the recent trend indicates changes in how the market willing to invest.

- Interest Rate and Median Yield Inversion & Spikes: Evidence of market stress is visible in the periodic "inversion" of interest rates and median yield; specifically, short and medium-term debt interest rate and median yield surpassed long-term ones in the two years after the 2016 election and the 2020 pandemic. This trend suggest that the situation at that time was unstable, while it would be more cooling-down in the future period.

- Widening Yield Difference: The Yield Difference represents a proxy for market uncertainty. The smaller the Yield Difference, the higher the confidence the market. If the difference getting larger, which means that they have to raise the interest rate to attract more buyers. There was a significant expansion between 2018–2022 and another aggressive climb starting in the second half of 2024 for all security terms, suggesting that the market was nervous and find it hards to price the debt accurately.

### 3. The Connection of Policy Indices & Auction Results (2015–2025)
The decade between 2015 and 2025 illustrates a profound connection between Washington and the Treasury market.

- 2017 – Beginning of 2020 Period (The Trade Shock): High Trade Index scores during the initiation of the US-China trade conflict synchronized with a widened Yield Difference, declined Bid-to-Cover Ratio, and increased interest rate for short and medium security terms. These trends suggest that while the market willing to fund the government, there was a high degree of disagreement among bidders on how to price the debt during the economic uncertainty period.

- 2020–2022 Period (The Crisis Support): During the pandemic, all the Economical Indices were below the baseline and the Interest Rate significantly dropped. Surprisingly, the Bid-to-Cover Ratio went up above the baseline during this time, repesented that the market was willing to support the governement debt during the pandemic.

- 2022 - 2024 Period (Post Pandemic Adjusment): While all the Economical Indices still remained low during this period, the Average Interest Rate and the Median Yield of short and medium security terms surpassed the long term ones. This shows because after COVID-19, the market demand shifted their concentration in shorter term liquidities. 

- 2024 – 2025 (The Tariff Pivot): In the second time of Trump Administation, the recent surge in the Tariff and Trade Indices (driven by White House's proposals for all countries) has coincided with another Yield Difference spike, suggesting another disagreement between bidders on how to price during this second uncertainty. Different to 2017-2020 period, the market is no longer absorbing news with high demand; instead, the rising Bid-to-Cover Ratio above baseline and the higher long-term security interest rate and yield suggest that investors are becoming more intersted and price-conscious at the same time within the policy volatility period becomes a normal thing.

### 4. Correlation: Policy Indices vs. Auction Metrics
- Pricing for Risk: A clear positive correlation exists between policy sentiment spikes and the cost of borrowing. As Fiscal, Trade, or Tariff indices escalate, market participants demand higher Interest Rates and Median Yields to compensate for perceived policy risk.

- Inelastic Demand: Despite price fluctuations, the Bid-to-Cover Ratio remains extremly stable across all index spikes. This validates the US Treasury's status as a safe asset; investors may adjust their price (Yield), but their fundamental intent to invest on the debts remains unchanged.

## D. Future Prediction
Until now, the articles data for 2026 has not been processed to quantify the shifts in the economical indices yet. However, with numorous amount of articles discussing about the recent conflict between US and Iran which dramatically disrupted the global supply chains, based on historical data, the Trade Index would rise and reach a new peak. Additionally, as the market trend is no longer absorbing the policy news, the Bid-to-Cover Ratio would potentially still go up above the baseline, along with higher interest rate demanded from the bidders to hedge against the inflation of the risk from the war. The Yield Difference would still persist to be large and the bidder may continue to favor long-term investment to avoid any changes in policy from Trump until a future presidential transition occurs.
