import pandas as pd
import pymysql as psql
import matplotlib.pyplot as plt

# Make SQL Conn
connection = psql.connect(host='amdata.green.rkgoffice',
                             user='ae',
                             password='ae',
                             charset='utf8mb4',
                             cursorclass=psql.cursors.DictCursor)


query = '''
Select day, sum(adcostcents)/100 as 'cost', sum(rkgsalescents)/100 as 'sales' from rktrack2.adday
where client = 638 and engine in (1, 27) and day > curdate() - interval 30 day
group by day
'''


# For grouping by
# df.groupby(['column1', 'column2']).sum()
#

# Output is a pandas DF
df = pd.read_sql_query(query, connection)

# To filter
df = df[df['cost'] != 0]
# To add a new column
df['ROI'] = (df.sales - df.cost)/(df.cost)

# Use this to add multiple data series to one graph
ax = plt.gca()

# allow you to plot with a 2nd y axis on the same graph
ax2 = ax.twinx()
df.plot(kind='line', x='day', y='cost', color='red', ax=ax)
df.plot(kind='line', x='day', y='sales', color='blue', ax=ax)


df.plot(kind='line', x='day', y='ROI', color='green', ax=ax2) #specify the 2nd y axis
plt.tight_layout()
plt.savefig('c:/users/ndima/desktop/output.png')
plt.show()

print(df)
