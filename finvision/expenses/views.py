from django.shortcuts import render
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json
from django.db.models.functions import TruncMonth
from .ml_kmeans import user_spending_type

@login_required
def dashboard(request):

    user = request.user
    expenses = Expense.objects.filter(user=user)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    category_data = (
        expenses.values('category')
        .annotate(total=Sum('amount'))
    )

    # Pie chart data
    categories = []
    amounts = []
    for item in category_data:
        categories.append(item['category'])
        amounts.append(float(item['total']))

    # Bar chart data
    monthly_data = (
        expenses
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    months = []
    month_totals = []
    for m in monthly_data:
        months.append(m['month'].strftime("%b %Y"))
        month_totals.append(float(m['total']))
    
    user_type, ml_data = user_spending_type()
    # ML BASED INSIGHTS
    ml_tips = []

    if user_type == "Saver":
        ml_tips.append("Excellent! You are managing your money very well.")
        ml_tips.append("Consider investing some savings for future goals.")

    elif user_type == "Balanced":
        ml_tips.append("Good job! Your spending is balanced.")
        ml_tips.append("Try to save a little more each month.")

    elif user_type == "Spender":
        ml_tips.append("Alert! You are spending too much.")
        ml_tips.append("Create a strict monthly budget.")
        ml_tips.append("Cut unnecessary expenses like shopping & food delivery.")


    # 🧠 AI TIPS LOGIC
    # AI TIPS
    # SMART AI TIPS (ONCE PER MONTH)
    tips = []

# 1. Overall spending
    if total > 4000:
        tips.append("Your overall spending is high this month. Consider budgeting.")
    elif total < 3000:
        tips.append("Great job! You are managing your expenses well this month.")

# 2. Highest category detection
    highest_category = max(category_data, key=lambda x: x['total'])
    highest_percent = (highest_category['total'] / total) * 100

    if highest_percent > 40:
        tips.append(
            f"You spent {highest_percent:.1f}% on {highest_category['category']}. "
            f"Try reducing this category next month."
        )

# 3. Savings suggestion
    tips.append("Try to save at least 20% of your income every month.")

    context = {
        'expenses': expenses,
        'total': total,
        'category_data': category_data,
        'categories': json.dumps(categories),
        'amounts': json.dumps(amounts),
        'months': json.dumps(months),
        'month_totals': json.dumps(month_totals),
        'tips': tips,
        'user_type': user_type,
        'ml_tips': ml_tips
    }

    return render(request, 'dashboard.html', context)
