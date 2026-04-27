# 📊 Financial Intelligence Dashboard

A high-performance financial analysis tool built with **Streamlit**. Transform your business spreadsheets into actionable visual intelligence with a sleek, dark-mode interface.

## 🟢 Quick Start Guide

### 1. Prepare Your Data
The dashboard needs specific "ingredients" to work. Ensure your spreadsheet has these exact column headers:
* **Date:** (YYYY-MM-DD)
* **Revenue:** (Your total income)
* **Expenses:** (Your total spending)
* **Category:** (The type of transaction, e.g., 'Marketing')

> **Pro-Tip:** Not sure how to format it? Use the **"Download Example Spreadsheet"** button inside the app to get a perfect template.

### 2. Upload & Analyze
1. Launch the app.
2. Drag and drop your **Excel (.xlsx)** or **CSV** file into the sidebar.
3. Use the **Filters** to drill down into specific spending categories.
4. Switch between the **Visual Analysis** and **Business Intelligence** tabs for deep-dive reports.

## 🛠️ Technical Setup (For Developers)

1. **Install Dependencies:**
   ```bash
   pip install streamlit pandas plotly openpyxl