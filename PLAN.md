# Sprint Plan: 11.11 Sale Analytics

## User Stories
1. **Store Owner:** As a store owner, I want to view key metrics (total revenue, orders, cancellation rate, AOV) and an AI-written sales briefing so I can quickly evaluate business performance and plan for next year.
   - Acceptance Criteria 1: Dashboard displays key numbers at the top.
   - Acceptance Criteria 2: "Generate briefing" button produces a 5-sentence summary using Gemini.
2. **Marketing Team:** As a marketer, I want to see revenue by category and hourly order volume trends so I can optimize promotional timing and ad spend.
   - Acceptance Criteria 1: Bar chart shows revenue by product category.
   - Acceptance Criteria 2: Line chart tracks order volume by hour of the day.
3. **Delivery Partner:** As a delivery partner, I want to analyze regional order distribution and payment method cancellation rates so I can allocate logistics capacity efficiently.
   - Acceptance Criteria 1: Region filter dynamically updates the dashboard view.
   - Acceptance Criteria 2: Analysis highlights COD cancellation trends.

## Task Backlog
- [x] Part A: Sprint planning (`PLAN.md`)
- [x] Part B: Generate 1M simulated orders and record file sizes
- [x] Part C: Clean data using PySpark and log row counts
- [x] Part D: Analyze data at scale and export summaries to `results/`
- [x] Part E: Build Streamlit dashboard (`app.py`)
- [x] Part F: Integrate Gemini API with error handling and document prompt
- [x] Part G: Deploy app on Streamlit Community Cloud (`requirements.txt`)
- [x] Part H: Complete ethical reflection (`REFLECTION.md`)
