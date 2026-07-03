import os
import numpy as np
import pandas as pd

def generate_customer_dataset(output_path, num_records=25000, seed=42):
    np.random.seed(seed)
    
    # 1. Customer ID
    customer_ids = [f"CUST{i:05d}" for i in range(1, num_records + 1)]
    
    # 2. Age (Normal distribution centered at 34, clipped between 18 and 75)
    ages = np.random.normal(loc=34, scale=12, size=num_records)
    ages = np.clip(ages, 18, 75).astype(int)
    
    # 3. Gender (Male: 48%, Female: 48%, Other: 4%)
    genders = np.random.choice(["Male", "Female", "Other"], size=num_records, p=[0.48, 0.48, 0.04])
    
    # 4. State & City Mapping
    state_city_map = {
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
        "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
        "Delhi": ["New Delhi", "Dwarka", "Rohini"],
        "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur", "Ghaziabad", "Varanasi"],
        "West Bengal": ["Kolkata", "Howrah", "Darjeeling", "Asansol"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
        "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"]
    }
    states_list = list(state_city_map.keys())
    # State probabilities based on e-commerce activity
    state_probs = [0.18, 0.15, 0.12, 0.10, 0.10, 0.09, 0.08, 0.08, 0.06, 0.04]
    
    selected_states = np.random.choice(states_list, size=num_records, p=state_probs)
    selected_cities = []
    for state in selected_states:
        cities = state_city_map[state]
        selected_cities.append(np.random.choice(cities))
        
    # 5. Education Level (correlated slightly with Age)
    education_options = ["High School", "Graduate", "Post Graduate", "Doctorate"]
    educations = []
    for age in ages:
        if age < 22:
            p = [0.60, 0.38, 0.02, 0.00]
        elif age < 26:
            p = [0.15, 0.65, 0.18, 0.02]
        else:
            p = [0.10, 0.50, 0.32, 0.08]
        educations.append(np.random.choice(education_options, p=p))
        
    # 6. Occupation (correlated with Age)
    occupations = []
    for age in ages:
        if age < 23:
            occupations.append(np.random.choice(["Student", "Professional", "Self-Employed"], p=[0.85, 0.10, 0.05]))
        elif age > 60:
            occupations.append(np.random.choice(["Retired", "Professional", "Self-Employed"], p=[0.75, 0.10, 0.15]))
        else:
            occupations.append(np.random.choice(["Professional", "Self-Employed", "Homemaker", "Student"], p=[0.65, 0.20, 0.10, 0.05]))
            
    # 7. Annual Income (in INR, correlated with Occupation and Education)
    annual_incomes = []
    for occ, edu in zip(occupations, educations):
        if occ == "Student":
            base = np.random.uniform(20000, 150000)
        elif occ == "Retired":
            base = np.random.uniform(200000, 800000)
        elif occ == "Homemaker":
            base = np.random.uniform(100000, 400000)
        elif occ == "Self-Employed":
            mult = 1.5 if edu in ["Post Graduate", "Doctorate"] else 1.0
            base = np.random.uniform(300000, 1500000) * mult
        else: # Professional
            if edu == "Doctorate":
                base = np.random.uniform(800000, 2500000)
            elif edu == "Post Graduate":
                base = np.random.uniform(600000, 2000000)
            elif edu == "Graduate":
                base = np.random.uniform(400000, 1500000)
            else:
                base = np.random.uniform(250000, 700000)
        annual_incomes.append(int(base))
        
    # 8. Membership Type (correlated with Annual Income)
    membership_types = []
    for income in annual_incomes:
        if income > 1500000:
            membership_types.append(np.random.choice(["VIP", "Gold", "Silver"], p=[0.40, 0.40, 0.20]))
        elif income > 800000:
            membership_types.append(np.random.choice(["VIP", "Gold", "Silver", "Bronze", "None"], p=[0.10, 0.30, 0.40, 0.15, 0.05]))
        elif income > 400000:
            membership_types.append(np.random.choice(["Gold", "Silver", "Bronze", "None"], p=[0.05, 0.25, 0.50, 0.20]))
        else:
            membership_types.append(np.random.choice(["Silver", "Bronze", "None"], p=[0.05, 0.45, 0.50]))
            
    # 9. Preferred Category
    categories = ["Electronics", "Apparel", "Home & Kitchen", "Beauty & Personal Care", "Books", "Sports & Outdoors"]
    cat_probs = [0.30, 0.28, 0.15, 0.12, 0.08, 0.07]
    preferred_categories = np.random.choice(categories, size=num_records, p=cat_probs)
    
    # 10. Items Purchased & Average Order Value (AOV)
    # VIP & Gold should buy more items and have higher AOV
    items_purchased = []
    aov_list = []
    for mem, income in zip(membership_types, annual_incomes):
        if mem == "VIP":
            items = np.random.randint(40, 180)
            aov = np.random.uniform(3000, 12000)
        elif mem == "Gold":
            items = np.random.randint(25, 120)
            aov = np.random.uniform(2000, 8000)
        elif mem == "Silver":
            items = np.random.randint(15, 80)
            aov = np.random.uniform(1200, 5000)
        elif mem == "Bronze":
            items = np.random.randint(5, 45)
            aov = np.random.uniform(800, 3000)
        else: # None
            items = np.random.randint(2, 30)
            aov = np.random.uniform(500, 2000)
            
        # Add income scaling factor
        scaling = 1.0 + (income / 3000000)
        aov = aov * scaling
        
        items_purchased.append(items)
        aov_list.append(round(aov, 2))
        
    # 11. Total Spend (Items * AOV)
    total_spends = [round(i * a, 2) for i, a in zip(items_purchased, aov_list)]
    
    # 12. Monthly Orders Average (correlated with items purchased)
    monthly_orders = []
    for items in items_purchased:
        orders = np.clip(items / 12.0 + np.random.normal(0, 1), 0.5, 15.0)
        monthly_orders.append(round(orders, 1))
        
    # 13. Purchase Frequency (correlated with Monthly Orders Avg)
    purchase_frequencies = []
    for mo in monthly_orders:
        if mo >= 8:
            purchase_frequencies.append("Daily")
        elif mo >= 3:
            purchase_frequencies.append("Weekly")
        elif mo >= 1:
            purchase_frequencies.append("Monthly")
        else:
            purchase_frequencies.append("Occasional")
            
    # 14. Discount Applied Ratio (percentage of purchases with discount)
    discount_applied_ratios = np.random.uniform(0.1, 0.85, size=num_records)
    discount_applied_ratios = np.round(discount_applied_ratios, 2)
    
    # 15. Discount Rate Average (when applied, e.g. 5% to 40%)
    discount_rate_avgs = np.random.uniform(5.0, 35.0, size=num_records)
    discount_rate_avgs = np.round(discount_rate_avgs, 1)
    
    # 16. Payment Method (UPI: 42%, Credit Card: 28%, Debit Card: 15%, Net Banking: 8%, Cash on Delivery: 7%)
    payment_methods = np.random.choice(
        ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"],
        size=num_records,
        p=[0.42, 0.28, 0.15, 0.08, 0.07]
    )
    
    # 17. Days Since Last Purchase (Recency)
    days_since_last_purchases = []
    for pf in purchase_frequencies:
        if pf == "Daily":
            d = np.random.randint(0, 5)
        elif pf == "Weekly":
            d = np.random.randint(1, 15)
        elif pf == "Monthly":
            d = np.random.randint(10, 45)
        else: # Occasional
            d = np.random.randint(30, 210)
        days_since_last_purchases.append(d)
        
    # 18. Customer Service Calls
    # Lower rating / satisfaction -> higher calls
    customer_service_calls = np.random.poisson(lam=1.5, size=num_records)
    customer_service_calls = np.clip(customer_service_calls, 0, 10)
    
    # 19. Average Rating (out of 5, correlated with service calls)
    average_ratings = []
    for calls in customer_service_calls:
        # Base rating centered around 4.2
        rating = 4.3 - (calls * 0.45) + np.random.normal(0, 0.5)
        average_ratings.append(np.clip(round(rating, 2), 1.0, 5.0))
        
    # 20. Satisfaction Level (correlated with Average Rating)
    satisfaction_levels = []
    for rating in average_ratings:
        if rating >= 4.5:
            satisfaction_levels.append("Very Satisfied")
        elif rating >= 3.7:
            satisfaction_levels.append("Satisfied")
        elif rating >= 2.8:
            satisfaction_levels.append("Neutral")
        elif rating >= 1.8:
            satisfaction_levels.append("Unsatisfied")
        else:
            satisfaction_levels.append("Very Unsatisfied")
            
    # 21. Cart Abandonment Rate
    cart_abandonment_rates = np.random.beta(a=2, b=5, size=num_records) # peak around 28%
    cart_abandonment_rates = np.round(cart_abandonment_rates, 2)
    
    # 22. Login Frequency (times per month)
    login_frequencies = np.random.randint(1, 30, size=num_records)
    # membership boost
    for idx, mem in enumerate(membership_types):
        if mem in ["VIP", "Gold"]:
            login_frequencies[idx] = min(30, login_frequencies[idx] + np.random.randint(5, 12))
            
    # 23. Session Duration Average (in minutes)
    session_durations = np.random.normal(loc=18, scale=10, size=num_records)
    session_durations = np.clip(session_durations, 2.0, 90.0)
    session_durations = np.round(session_durations, 1)
    
    # 24. Pages Per Session
    pages_per_sessions = []
    for sd in session_durations:
        pages = int(sd / 2.5 + np.random.randint(1, 5))
        pages_per_sessions.append(max(1, pages))
        
    # 25. Wishlist Items
    wishlist_items_count = np.random.negative_binomial(n=3, p=0.4, size=num_records)
    wishlist_items_count = np.clip(wishlist_items_count, 0, 35)
    
    # 26. Email Open Rate
    email_open_rates = np.random.uniform(0.0, 1.0, size=num_records)
    # VIPs open more emails
    for idx, mem in enumerate(membership_types):
        if mem == "VIP":
            email_open_rates[idx] = min(1.0, email_open_rates[idx] + 0.25)
    email_open_rates = np.round(email_open_rates, 2)
    
    # 27. Product Reviews Written
    product_reviews_written = []
    for rating in average_ratings:
        # Customers who give very high or very low reviews write more reviews
        if rating >= 4.5 or rating <= 2.0:
            reviews = np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.08, 0.02])
        else:
            reviews = np.random.choice([0, 1, 2], p=[0.7, 0.25, 0.05])
        product_reviews_written.append(reviews)
        
    # 28. Returns Ratio (correlated with Category and satisfaction)
    returns_ratios = []
    for cat, rating in zip(preferred_categories, average_ratings):
        # Electronics and Apparel have higher return rates
        base_return = 0.08 if cat in ["Electronics", "Apparel"] else 0.03
        if rating <= 2.5:
            base_return += 0.12
        ret = base_return + np.random.uniform(0.0, 0.1)
        returns_ratios.append(round(min(0.5, ret), 2))
        
    # 29. Preferred Purchase Time
    purchase_times = np.random.choice(
        ["Morning", "Afternoon", "Evening", "Night"],
        size=num_records,
        p=[0.20, 0.25, 0.40, 0.15]
    )
    
    # 30. Device Preference (App: 74%, Website: 26%)
    device_preferences = np.random.choice(["App", "Website"], size=num_records, p=[0.74, 0.26])
    
    # 31. Loyalty Score (1 to 10 scale)
    # loyalty = f(Total Spend, Days Since Last Purchase, Satisfaction)
    loyalty_scores = []
    for spend, days, sat in zip(total_spends, days_since_last_purchases, satisfaction_levels):
        score = 5.0
        
        # Spend component
        if spend > 150000:
            score += 2.5
        elif spend > 60000:
            score += 1.5
        elif spend > 20000:
            score += 0.5
            
        # Recency component (negative impact if inactive)
        if days > 120:
            score -= 2.0
        elif days > 60:
            score -= 1.0
        elif days < 15:
            score += 1.0
            
        # Satisfaction component
        if sat in ["Very Satisfied", "Satisfied"]:
            score += 1.5
        elif sat in ["Unsatisfied", "Very Unsatisfied"]:
            score -= 1.5
            
        score = np.clip(score + np.random.normal(0, 0.5), 1.0, 10.0)
        loyalty_scores.append(round(score, 1))
        
    # 32. Churn Status (True/False)
    # Churned if recency > 90 days AND low loyalty AND low satisfaction
    churn_status = []
    for days, loyalty, sat in zip(days_since_last_purchases, loyalty_scores, satisfaction_levels):
        if days > 90 and loyalty < 4.5 and sat in ["Neutral", "Unsatisfied", "Very Unsatisfied"]:
            churn = np.random.choice([True, False], p=[0.85, 0.15])
        elif days > 120:
            churn = np.random.choice([True, False], p=[0.70, 0.30])
        else:
            churn = np.random.choice([True, False], p=[0.05, 0.95])
        churn_status.append(churn)
        
    # 33. Feedback Category
    feedbacks = []
    for sat in satisfaction_levels:
        if sat in ["Very Satisfied", "Satisfied"]:
            feedbacks.append(np.random.choice(["Delivery Speed", "Product Quality", "Pricing", "None"], p=[0.2, 0.3, 0.1, 0.4]))
        elif sat in ["Unsatisfied", "Very Unsatisfied"]:
            feedbacks.append(np.random.choice(["Delivery Speed", "Product Quality", "Customer Service", "Pricing", "UI Experience"], p=[0.25, 0.35, 0.20, 0.10, 0.10]))
        else:
            feedbacks.append(np.random.choice(["Delivery Speed", "Product Quality", "Pricing", "UI Experience", "None"], p=[0.15, 0.15, 0.10, 0.10, 0.50]))

    # Construct DataFrame
    df = pd.DataFrame({
        "Customer_ID": customer_ids,
        "Age": ages,
        "Gender": genders,
        "City": selected_cities,
        "State": selected_states,
        "Education": educations,
        "Occupation": occupations,
        "Annual_Income": annual_incomes,
        "Membership_Type": membership_types,
        "Preferred_Category": preferred_categories,
        "Items_Purchased": items_purchased,
        "Average_Order_Value": aov_list,
        "Total_Spend": total_spends,
        "Monthly_Orders_Avg": monthly_orders,
        "Purchase_Frequency": purchase_frequencies,
        "Discount_Applied_Ratio": discount_applied_ratios,
        "Discount_Rate_Avg": discount_rate_avgs,
        "Payment_Method": payment_methods,
        "Days_Since_Last_Purchase": days_since_last_purchases,
        "Customer_Service_Calls": customer_service_calls,
        "Average_Rating": average_ratings,
        "Satisfaction_Level": satisfaction_levels,
        "Cart_Abandonment_Rate": cart_abandonment_rates,
        "Login_Frequency": login_frequencies,
        "Session_Duration_Avg": session_durations,
        "Pages_Per_Session": pages_per_sessions,
        "Wishlist_Items": wishlist_items_count,
        "Email_Open_Rate": email_open_rates,
        "Product_Reviews_Written": product_reviews_written,
        "Returns_Ratio": returns_ratios,
        "Preferred_Purchase_Time": purchase_times,
        "Device_Preference": device_preferences,
        "Loyalty_Score": loyalty_scores,
        "Churn_Status": churn_status,
        "Feedback_Category": feedbacks
    })
    
    # Save directory verification
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset generated successfully at {output_path} with shape {df.shape}")

if __name__ == "__main__":
    # Generate in the data directory relative to the workspace root
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "customer_data.csv")
    generate_customer_dataset(data_path)
