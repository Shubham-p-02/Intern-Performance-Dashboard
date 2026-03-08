import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_intern_data(num_interns=50, num_weeks=12):
    domains = ['Data Analytics', 'Web Development', 'Marketing', 'Data Science', 'UI/UX Design']
    
    data = []
    
    # Generate unique intern profiles
    interns = []
    for i in range(1, num_interns + 1):
        domain = random.choice(domains)
        base_performance = random.uniform(60, 95) # base performance capability
        interns.append({
            'Intern_ID': f"INT-{i:03d}",
            'Name': f"Intern {i}",
            'Domain': domain,
            'Base_Performance': base_performance
        })
        
    # Generate weekly records for each intern
    start_date = datetime(2025, 1, 6) # Starting on a Monday
    
    for intern in interns:
        for week in range(1, num_weeks + 1):
            # Tasks assigned varies
            tasks_assigned = random.randint(5, 15)
            
            # Tasks completed depends on base performance and some randomness
            completion_rate = min(1.0, max(0.4, (intern['Base_Performance'] / 100) + random.uniform(-0.1, 0.1)))
            tasks_completed = int(tasks_assigned * completion_rate)
            
            # Attendance (out of 5 working days)
            # Higher performers tend to attend more
            attendance_prob = min(1.0, (intern['Base_Performance'] / 100) + 0.1)
            days_present = sum([1 if random.random() < attendance_prob else 0 for _ in range(5)])
            total_working_days = 5
            
            # Calculate performance score for the week
            # Formula: 60% task completion + 40% attendance
            task_score = (tasks_completed / tasks_assigned) * 100 if tasks_assigned > 0 else 0
            attendance_score = (days_present / total_working_days) * 100
            performance_score = (0.6 * task_score) + (0.4 * attendance_score)
            
            week_start = start_date + timedelta(weeks=week-1)
            
            data.append({
                'Intern_ID': intern['Intern_ID'],
                'Name': intern['Name'],
                'Domain': intern['Domain'],
                'Week_Number': week,
                'Week_Start_Date': week_start.strftime("%Y-%m-%d"),
                'Tasks_Assigned': tasks_assigned,
                'Tasks_Completed': tasks_completed,
                'Days_Present': days_present,
                'Total_Working_Days': total_working_days,
                'Performance_Score': round(performance_score, 2)
            })
            
    df = pd.DataFrame(data)
    df.to_csv('intern_data.csv', index=False)
    print(f"Generated data for {num_interns} interns across {num_weeks} weeks.")
    print(f"Data saved to 'intern_data.csv'")

if __name__ == "__main__":
    generate_intern_data()
