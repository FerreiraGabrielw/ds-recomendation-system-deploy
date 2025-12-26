# Hybrid Recommender System for E-commerce (End-to-End)

![Project Preview](quarto/capa.png)

### ➡️ Full and Detailed Documentation in My Portfolio  
[Access the complete project page here](https://ferreiragabrielw.github.io/portfolio-gabriel/projetos/DataScience/4RecomendationSystem/RecomendationSystemEN.html)

---

## About the Project

This project presents the design and implementation of a **Hybrid Recommender System for e-commerce**, developed end-to-end following real-world data science and production practices.

The system combines behavioral, semantic, and contextual signals to generate personalized product recommendations with the goal of increasing:

- Conversion rate  
- Average Order Value (AOV)  
- Recommendation relevance  
- Cross-sell opportunities  

The full pipeline covers database modeling, data ingestion, exploratory analysis, algorithm development, offline evaluation, artifact preparation, and cloud deployment using AWS serverless services.

---

## Recommender Architecture

The final solution integrates three complementary approaches:

- **Item-Item Collaborative Filtering**  
  Captures behavioral similarity from historical purchase patterns.

- **Content-Based Filtering (TF-IDF)**  
  Uses product metadata to handle cold-start scenarios and improve coverage.

- **Association Rules (Apriori)**  
  Identifies frequently co-purchased products for contextual cross-sell recommendations.

Scores from each component are normalized and combined through a weighted hybrid strategy.

---

## Technologies and Process

**Main Tools & Technologies**

- Python (Pandas, NumPy, Scikit-learn, MLxtend)
- SQL (MySQL)
- Quarto & Jupyter Notebook
- AWS (S3, Lambda, API Gateway)
- Matplotlib
- Pickle / Parquet (model artifacts)

**End-to-End Pipeline**

- Database design and SQL ingestion  
- SQL-based validation and exploratory analysis  
- Exploratory Data Analysis (EDA)  
- Feature engineering and interaction modeling  
- Collaborative Filtering, Content-Based Filtering, and Association Rules  
- Offline evaluation (Leave-Last-Out, Hit Rate@K)  
- Hybrid model tuning  
- Artifact generation for production  
- Serverless deployment on AWS  

---

## Repository Structure

```

.
├── aws/
│   └── Scripts and configuration files for AWS deployment
│
├── data/
│   └── CSV datasets (customers, products, transactions, product_views)
│
├── notebook/
│   └── ProductRecomentation.ipynb (full modeling and experimentation)
│
├── quarto/
│   ├── RecomendationSystemEN.qmd
│   └── Videos used for demonstrations in the report
│
├── sql/
│   ├── ER diagram
│   └── SQL scripts for schema creation and data loading
│
├── README.md
└── LICENSE

---

## How to Explore the Project

- **Online (Recommended)**  
  View the full interactive report with explanations, figures, and videos:  
  👉 [Project Page on Portfolio](https://ferreiragabrielw.github.io/portfolio-gabriel/projetos/DataScience/4RecomendationSystem/RecomendationSystemEN.html)

- **Jupyter Notebook**  
  Explore the full modeling process in `notebook/ProductRecomentation.ipynb`.

- **Locally (Quarto)**  
  1. Open `quarto/RecomendationSystemEN.qmd`  
  2. Install Quarto and Python dependencies  
  3. Render the document to HTML  

---

## Cloud Deployment

The recommender system is deployed using a **serverless architecture on AWS**:

- **Amazon S3** → Model artifact storage and versioning  
- **AWS Lambda** → On-demand inference execution  
- **Amazon API Gateway** → REST API exposure  

This setup enables low-latency recommendations and easy model updates by replacing artifacts without changing the API.

---

## License

This project is licensed under the [MIT License](LICENSE).