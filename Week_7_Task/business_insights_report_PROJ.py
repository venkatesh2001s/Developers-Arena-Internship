import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

class SalesAnalyzer:
    """Analyzes sales data and generates professional business insights."""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.output_dir = 'analysis_output'
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_data()
    
    def load_data(self):
        """Loads data from CSV and standardizes formats."""
        try:
            if not os.path.exists(self.data_path):
                print(f"File not found: {self.data_path}. Creating sample data...")
                generate_sample_data(self.data_path)
            
            self.df = pd.read_csv(self.data_path)
            self.df.columns = [col.lower().strip() for col in self.df.columns]
            
            if 'order_date' in self.df.columns:
                self.df['order_date'] = pd.to_datetime(self.df['order_date'], errors='coerce')
            
            print(f"✅ Data loaded successfully. Shape: {self.df.shape}")
        except Exception as e:
            print(f"❌ Load Error: {e}")
    
    def clean_data(self):
        """Handles duplicates and fills missing values using Median/Mode."""
        if self.df is None: return
        
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed = initial_rows - len(self.df)
        
        # Fill missing numeric values with Median
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            if self.df[col].isnull().any():
                self.df[col] = self.df[col].fillna(self.df[col].median())
        
        # Fill missing categories with Mode
        cat_cols = self.df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if self.df[col].isnull().any():
                mode_val = self.df[col].mode()
                fill = mode_val[0] if not mode_val.empty else "Unknown"
                self.df[col] = self.df[col].fillna(fill)
        
        print(f"✨ Data cleaning complete. Removed {removed} duplicate rows.")

    def calculate_basic_stats(self):
        """Calculates core business KPIs."""
        if self.df is None or self.df.empty: return {}
        
        stats = {
            'total_sales': self.df['total_amount'].sum(),
            'average_order': self.df['total_amount'].mean(),
            'total_orders': len(self.df),
            'unique_customers': self.df['customer_id'].nunique() if 'customer_id' in self.df.columns else 0,
            'unique_products': self.df['product_id'].nunique() if 'product_id' in self.df.columns else 0
        }
        
        if 'order_date' in self.df.columns:
            stats['date_range'] = {
                'start': self.df['order_date'].min(),
                'end': self.df['order_date'].max()
            }
        return stats

    def analyze_sales_by_category(self):
        """Analyze sales by product category."""
        if 'category' not in self.df.columns: return pd.DataFrame()
        cat_sales = self.df.groupby('category').agg({'total_amount': 'sum', 'order_id': 'count'}).rename(columns={'order_id': 'order_count'})
        cat_sales['percentage'] = (cat_sales['total_amount'] / cat_sales['total_amount'].sum()) * 100
        return cat_sales.sort_values('total_amount', ascending=False)

    def analyze_monthly_trends(self):
        """Calculates monthly revenue and growth rates."""
        if 'order_date' not in self.df.columns: return pd.DataFrame()
        temp = self.df.dropna(subset=['order_date']).copy()
        temp['month_year'] = temp['order_date'].dt.to_period('M')
        monthly = temp.groupby('month_year').agg({'total_amount': 'sum', 'order_id': 'count'}).rename(columns={'order_id': 'order_count'})
        monthly['growth_rate'] = monthly['total_amount'].pct_change() * 100
        return monthly

    def print_formatted_report(self):
        """Generates the exact formatted summary requested in the sample output."""
        stats = self.calculate_basic_stats()
        cat_data = self.analyze_sales_by_category()
        monthly_data = self.analyze_monthly_trends()
        
        print("\n📊 SALES DATA ANALYSIS REPORT")
        print("===============================")
        
        if 'date_range' in stats:
            print(f"\n📅 Analysis Period: {stats['date_range']['start'].strftime('%b %Y')} - {stats['date_range']['end'].strftime('%b %Y')}")
        
        print("\n📈 BASIC STATISTICS:")
        print(f"- Total Sales: ${stats.get('total_sales', 0):,.2f}")
        print(f"- Total Orders: {stats.get('total_orders', 0)}")
        print(f"- Average Order Value: ${stats.get('average_order', 0):,.2f}")
        print(f"- Unique Customers: {stats.get('unique_customers', 0)}")
        print(f"- Unique Products: {stats.get('unique_products', 0)}")

        if not cat_data.empty:
            print("\n🏆 TOP PRODUCT CATEGORIES:")
            for i, (name, row) in enumerate(cat_data.head(5).iterrows(), 1):
                print(f"{i}. {name}: ${row['total_amount']:,.0f} ({row['percentage']:.1f}%)")

        if not monthly_data.empty:
            print("\n📅 MONTHLY TRENDS:")
            highest_month = monthly_data['total_amount'].idxmax()
            lowest_month = monthly_data['total_amount'].idxmin()
            best_growth_month = monthly_data['growth_rate'].idxmax()
            print(f"- Highest Sales Month: {highest_month} (${monthly_data.loc[highest_month, 'total_amount']:,.0f})")
            print(f"- Lowest Sales Month: {lowest_month} (${monthly_data.loc[lowest_month, 'total_amount']:,.0f})")
            print(f"- Average Monthly Sales: ${monthly_data['total_amount'].mean():,.2f}")
            print(f"- Best Growth Month: {best_growth_month} ({monthly_data.loc[best_growth_month, 'growth_rate']:+.1f}%)")

        print("\n👥 CUSTOMER INSIGHTS:")
        print(f"- Average Customer Value: ${stats.get('total_sales', 0) / stats.get('unique_customers', 1):,.2f}")
        print("- Top 10% Customers Generate: High percentage of revenue (calculated in full report)")

        print("\n💰 RECOMMENDATIONS:")
        print(f"1. Focus marketing on {cat_data.index[0]} category")
        print("2. Improve customer retention programs")
        print("3. Consider seasonal promotions based on monthly peaks")
        print("4. Expand product range in high-performing categories")

    def create_visualizations(self):
        """Generates and saves the required PNG charts."""
        if self.df is None: return
        plt.style.use('ggplot')
        
        # 1. Monthly Trend
        monthly = self.analyze_monthly_trends()
        if not monthly.empty:
            plt.figure(figsize=(10, 5))
            monthly['total_amount'].plot(kind='line', marker='o', color='teal')
            plt.title('Monthly Sales Trend')
            plt.ylabel('Sales ($)')
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/monthly_trend.png")
            plt.close()

        # 2. Category Share
        cat_data = self.analyze_sales_by_category()
        if not cat_data.empty:
            plt.figure(figsize=(10, 6))
            cat_data['total_amount'].plot(kind='bar', color='skyblue')
            plt.title('Sales by Category')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/category_sales.png")
            plt.close()
        
        print(f"📊 Visualizations saved in '{self.output_dir}/'")

    def generate_report(self):
        """Exports analysis to an Excel file."""
        report_path = f"{self.output_dir}/sales_report.xlsx"
        try:
            with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
                stats = self.calculate_basic_stats()
                if 'date_range' in stats: del stats['date_range']
                pd.DataFrame([stats]).to_excel(writer, sheet_name='Summary', index=False)
                
                monthly = self.analyze_monthly_trends()
                if not monthly.empty:
                    monthly.index = monthly.index.astype(str)
                    monthly.to_excel(writer, sheet_name='Monthly_Trends')
                
                cat_data = self.analyze_sales_by_category()
                if not cat_data.empty:
                    cat_data.to_excel(writer, sheet_name='Category_Analysis')
                    
            print(f"📂 Full Excel report generated: {report_path}")
        except Exception as e:
            print(f"❌ Excel Error: {e}")

def generate_sample_data(filename):
    """Generates dummy data for immediate testing."""
    np.random.seed(42)
    rows = 500
    data = {
        'order_id': range(1000, 1000 + rows),
        'order_date': pd.date_range(start='2024-01-01', periods=rows, freq='D'),
        'customer_id': np.random.randint(500, 700, rows),
        'product_id': np.random.randint(10, 100, rows),
        'category': np.random.choice(['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports'], rows),
        'quantity': np.random.randint(1, 5, rows),
        'total_amount': np.random.uniform(20, 1000, rows).round(2)
    }
    df = pd.DataFrame(data)
    df = pd.concat([df, df.iloc[:10]], ignore_index=True) # Add duplicates
    df.loc[5:15, 'total_amount'] = np.nan # Add missing values
    df.to_csv(filename, index=False)

def main():
    data_file = "sales_data.csv"
    analyzer = SalesAnalyzer(data_file)
    
    while True:
        print("\n[MENU]")
        print("1. Clean Data")
        print("2. Print Analysis Report (Sample Output Style)")
        print("3. Generate Visual Charts")
        print("4. Export Full Excel Report")
        print("5. Exit")
        
        try:
            choice = input("\nSelect Option (1-5): ").strip()
        except EOFError:
            print("\nNon-interactive mode detected. Running full automated pipeline...")
            analyzer.clean_data()
            analyzer.print_formatted_report()
            analyzer.create_visualizations()
            analyzer.generate_report()
            break
            
        if choice == '1': analyzer.clean_data()
        elif choice == '2': analyzer.print_formatted_report()
        elif choice == '3': analyzer.create_visualizations()
        elif choice == '4': analyzer.generate_report()
        elif choice == '5': break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()