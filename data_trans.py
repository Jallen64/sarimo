data = pd.read_csv('PersonalFinance.csv', delimiter = ',')
data


#min_required

#data['source'] = None
#data.loc[data['Detail1'] == 'Post-tax_monthly_income'].values[0]

##Create dataframe
columns = ['source', 'target', 'weight']
df = pd.DataFrame(columns = columns)
Budget = float(data.loc[data.Detail1 == 'Post-tax_monthly_income'].values[0].tolist()[1])
Rent = int(data.loc[data.Detail1 == 'Rent_Mortgage'].values[0].tolist()[1])
Contribution_401k = int(data.loc[data.Detail1 == '401k_Contribution'].values[0].tolist()[1])
Food_and_essential_items = int(data.loc[data.Detail1 == 'Food_and_essential_items'].values[0].tolist()[1])
Utilities = int(data.loc[data.Detail1 == 'Utilities'].values[0].tolist()[1])
Non_essential_utilities = int(data.loc[data.Detail1 == 'Non_essential_utilities'].values[0].tolist()[1])
Transportation = int(data.loc[data.Detail1 == 'Transportation'].values[0].tolist()[1])
Healthcare = int(data.loc[data.Detail1 == 'Healthcare'].values[0].tolist()[1])
Student_loan_payment = int(data.loc[data.Detail1 == 'Student_loan_payment'].values[0].tolist()[1])
Minimum_Credit_Card_Payment1 = int(data.loc[data.Detail1 == 'Minimum payment'].values[0].tolist()[1])
Minimum_Credit_Card_Payment2 = int(data.loc[data.Detail1 == 'Minimum payment'].values[0].tolist()[2])
df.loc['0'] = ['Post_Tax_Income','Budget',  data.loc[data.Detail1 == 'Post-tax_monthly_income'].values[0].tolist()[1]]


#Calculate essential costs
blue = Rent + Food_and_essential_items + Utilities + Transportation + Healthcare
df.loc['1'] = ['Budget','Necessary_Expenses',  int(blue)]
df.loc['2'] = ['Necessary_Expenses', 'Rent', int(data.loc[data.Detail1 == 'Rent_Mortgage'].values[0].tolist()[1])]
df.loc['3'] = ['Necessary_Expenses', 'Food_and_essential_items', int(data.loc[data.Detail1 == 'Food_and_essential_items'].values[0].tolist()[1])]
df.loc['4'] = ['Necessary_Expenses', 'Utilities', int(data.loc[data.Detail1 == 'Utilities'].values[0].tolist()[1])]
df.loc['5'] = ['Necessary_Expenses', 'Transportation', int(data.loc[data.Detail1 == 'Transportation'].values[0].tolist()[1])]
df.loc['6'] = ['Necessary_Expenses', 'Healthcare', int(data.loc[data.Detail1 == 'Healthcare'].values[0].tolist()[1])]

#Calculate employer match
df.loc['7'] = ['Budget', 'Employer_sponsored_matching_funds', int(Contribution_401k)]
df.loc['8'] = ['Employer_sponsored_matching_funds', 'Contribution_401k', int(Contribution_401k)]


#Check if emergency fund is sufficient
min_required = data.loc[data.Detail1 == 'Required Minimum Emergency Fund '].values[0].tolist()[1]
current = data.loc[data.Detail1 == 'Current Emergency Fund'].values[0].tolist()[1]

#Increase emergency fund to cover at least one month worth of expenses
remaining_budget = data.loc[data.Detail1 == 'Money remaining'].values[0].tolist()[1]


diff = int(min_required) - int(current)
print(diff)
APR1 = int(data.loc[data.Detail1 == 'APR'].values[0].tolist()[1])
APR2 = int(data.loc[data.Detail1 == 'APR'].values[0].tolist()[2])
minimum1 = int(data.loc[data.Detail1 == 'Minimum payment'].values[0].tolist()[1])
minimum2 = int(data.loc[data.Detail1 == 'Minimum payment'].values[0].tolist()[2])
if diff > 0:
        
        if float(remaining_budget) > diff:
            #There is going to be leftover from budget allocation for emergency fund
            remaining_budget = float(remaining_budget) - float(diff)
            df.loc['9'] = ['Budget', 'Emergency_Fund', int(float(diff) + Non_essential_utilities)]
            df.loc['10'] = ['Emergency_Fund', 'Build_Emergency_Fund', float(diff)]
            df.loc['11'] = ['Emergency_Fund', 'Non_essential_utilities', int(Non_essential_utilities)]
            
        elif remaining_budget == (diff):
            #Just enough so allocate everything to emergency fund
            remaining_budget = 0
            df.loc['9'] = ['Budget', 'Emergency_Fund', float(diff) + Non_essential_utilities]
            df.loc['10'] = ['Emergency_Fund', 'Build_Emergency_Fund', float(diff)]
            df.loc['11'] = ['Emergency_Fund', 'Non_essential_utilities', int(Non_essential_utilities)]
        else:
            #Just allocate everything and do not continue
            remaining_budget = 0
            df.loc['9'] = ['Budget', 'Emergency_Fund', float(diff)]
            df.loc['10'] = ['Emergency_Fund', 'Build_Emergency_Fund', float(diff)]
            
print('Remaining budget is ' + str(remaining_budget))
if remaining_budget > 0:
    if APR1 > APR2:
        #Use avalanche technique
        df.loc['12'] = ['Budget', 'Loan_payments', Student_loan_payment + Minimum_Credit_Card_Payment1 + Minimum_Credit_Card_Payment2]
        df.loc['13'] = ['Loan_payments', 'Minimum Credit Card Payment1', float(remaining_budget) + Minimum_Credit_Card_Payment1]
        df.loc['14'] = ['Loan_payments', 'Minimum Credit Card Payment2', Minimum_Credit_Card_Payment2]
        df.loc['15'] = ['Budget', 'Student_loan_payment', Student_loan_payment]
    else:
        df.loc['12'] = ['Budget', 'Loan_payments', Student_loan_payment + Minimum_Credit_Card_Payment1 + Minimum_Credit_Card_Payment2]
        df.loc['13'] = ['Loan_payments', 'Minimum Credit Card Payment1', Minimum_Credit_Card_Payment1]
        df.loc['14'] = ['Loan_payments', 'Minimum Credit Card Payment2', Minimum_Credit_Card_Payment2 + float(remaining_budget)]
        df.loc['15'] = ['Budget', 'Student_loan_payment', Student_loan_payment]
df.columns = [''] * len(df.columns)