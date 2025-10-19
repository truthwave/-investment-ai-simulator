<h1 align="center">📊 Stock Price Simulation × Automated Investment Strategy App</h1>

<p align="center"><i>Trade weekly based solely on rules. Zero hesitation.</i></p>

<p align="center">
<img width="1536" height="1024" alt="投資" src="https://github.com/user-attachments/assets/55436c76-7d9c-497d-a484-172d33ef7889" />
</p>

---

## Experience (Three features are sufficient)

- **Automatically generates strategies**: Targets S&P 500 / Nikkei Average, **reconstructs** rules weekly for virtual trading
- **Operates via notifications**: Trading opportunities are **email notifications**. Weekly **profit/loss reports** are automatically sent
- **Constantly updates stocks**: Constituent stocks are **automatically retrieved monthly** (Execute with recent cash when failing)
> The goal is “consistency.” Leave judgment to rules, discard emotion.

---

## Before → After

- **Manual selection/recording**: 90 minutes/week → **10 minutes**
- **Hesitation in trade decisions**: “Probably” → **Rules**
- **Results review**: Spreadsheet → **Automatic report**
> ※ This tool is for learning and technical demonstration. It is not investment advice.

---

## Assumptions and Constraints (Only the important ones)

- **Data**: Uses yfinance closing prices, etc. (Possible delays/gaps)
- **Stock list**: Scraped monthly from Wikipedia. Falls back to recent cache if scraping fails
- **Strategy**: Weekly **hypothesis updates**. Past optimization does not guarantee future profits
- **Purpose: Learning/testing**. Actual trading requires independent judgment and responsibility

---

## What's Included (Key Points Only)

- **Simulator**: Weekly virtual trades / Aggregates P&L and win rate
- **Notifications**: Sends trade signals/weekly reports via smtplib
- **Updates**: Retrieves stocks with BeautifulSoup4 → Uses cache if fails
- **Visualization**: Plots performance with matplotlib
- **Learning**: Reconstructs features/rules using pandas / scikit-learn

---

## 📬 Email Notification Example

When a trading opportunity arises, you'll automatically receive an email notification:

<p align="center">
  <img src="https://github.com/user-attachments/assets/51277f69-2d4d-426f-a78e-ab2bcad8acfe" width="500" />
</p>

---

## License

MIT License

---

## 🧑‍💻 Author

**[Truth Wave ― 真理の波](https://github.com/truthwave)**  
We also share information about portfolios and AI tool development. Please take a look!

## Feel Free to Contact Me
[📩 Inquiries & Quotes](mailto:realmadrid71214591@gmail.com)

---

## 🏁 In Closing

> **Add, and you waver. Subtract, and you grow stronger.**
> Investing isn't about “how you feel,” but “how you repeat.”
