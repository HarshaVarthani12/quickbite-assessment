# QuickBite Data Analyst Assessment

## Project Overview

This project involves cleaning, combining and analysing QuickBite food delivery data using Python. The objective is to identify business insights related to area performance, cuisine popularity and delivery efficiency.

## Tools and Technologies

- Python
- Pandas
- OpenPyXL
- Visual Studio Code

## Project Structure

```text
quickbite-assessment/
├── data/
│   └── QuickBite_Assessment.xlsx
├── scripts/
│   ├── cleaning.py
│   └── analysis.py
├── cleaned_data/
│   ├── Quick_Bite_Data_Cleaning.xlsx
│   └── Quick_Bite_Combined_Data.xlsx
├── analysis/
│   └── Quick_Bite_Analysis.xlsx
└── README.md
```

## Dataset

The original Excel dataset contains six sheets:

- Orders
- Customers
- Restaurants
- Areas
- Delivery Partners
- Feedback

## Task 1. Data Cleaning

The original dataset was cleaned using Pandas to improve data quality and consistency.

The following operations were performed:

- Removed duplicate records.
- Handled missing mandatory values.
- Removed unnecessary spaces.
- Standardised inconsistent text values.
- Corrected date and time formats.
- Converted order amounts and delivery durations into numerical values.
- Standardised phone numbers and email addresses.

The cleaned dataset was saved as Quick_Bite_Data_Cleaning.xlsx.

## Task 2. Data Combining

The six cleaned tables were combined using common ID columns through left joins.

Additional columns such as order date, order time, order day and late delivery status were created.

Delivered orders taking more than 45 minutes were classified as late deliveries.

The final combined dataset contains:

- Total orders: 1454
- Total columns: 19
- Duplicate order IDs: 0

The combined dataset was saved as Quick_Bite_Combined_Data.xlsx.

## Task 3. Data Analysis

Only delivered orders were considered for the business analysis.

Total delivered orders: 1350

### 1. Area Performance

Orders were grouped based on city and area to analyse revenue and delivery performance.

The areas were ranked based on total revenue.

Madhapur, Hyderabad generated the highest revenue of Rs. 71,813.42 with 171 delivered orders.

### 2. Top Cuisine by Day

Orders were grouped by day and cuisine to identify the most popular cuisine for each day of the week.

The percentage share was calculated using the cuisine order count and the total number of delivered orders on that day.

| Day | Top Cuisine | Orders | Percentage |
|---|---|---:|---:|
| Monday | South Indian | 49 | 27.53% |
| Tuesday | South Indian | 39 | 22.67% |
| Wednesday | Chinese | 55 | 26.83% |
| Thursday | South Indian | 41 | 21.81% |
| Friday | Biryani | 51 | 25.89% |
| Saturday | Pizza | 54 | 25.12% |
| Sunday | North Indian | 42 | 21.54% |

### 3. Vehicle Performance

Delivery vehicles were compared based on delivery count, average delivery time, on-time delivery performance and customer ratings.

Motorbike recorded the lowest average delivery time of 32.72 minutes and an on-time delivery rate of 90.66%.

Bicycle recorded the highest average delivery time of 45.52 minutes.

## Key Findings

- Madhapur, Hyderabad generated the highest revenue.
- South Indian cuisine was the most popular cuisine on three days of the week.
- Motorbike recorded the fastest average delivery time.
- Bicycle recorded the slowest average delivery time.

## Assumptions

- Only delivered orders were included in the business analysis.
- Delivery time above 45 minutes was considered late.
- Restaurant area was used for area performance analysis.
- The first record was retained when repeated IDs were found.
- Missing delivery durations were excluded from late delivery percentage calculations.

## Data Limitations

Out of 1350 delivered orders, 23 orders had missing vehicle information.

These orders were excluded from the vehicle performance comparison.

A total of 1327 orders were included in the vehicle analysis.

## Output Files

- Quick_Bite_Data_Cleaning.xlsx
- Quick_Bite_Combined_Data.xlsx
- Quick_Bite_Analysis.xlsx

The final analysis workbook contains three sheets covering area performance, top cuisine by day and vehicle performance.

## How to Run

Install the required Python libraries:

```bash
pip install pandas openpyxl
```

Run the data cleaning and combining script:

```bash
python scripts/cleaning.py
```

Run the data analysis script:

```bash
python scripts/analysis.py
```

## Conclusion

The project turns raw food delivery data into an organised set of records. The analysis provides insights that can help QuickBite understand customer preferences, identify high-performing areas and improve delivery efficiency.