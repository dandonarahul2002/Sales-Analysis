import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
st.set_option('deprecation.showPyplotGlobalUse', False)



@st.cache(persist=True, allow_output_mutation=True)
def explore_data(dataset):
        df = pd.read_csv(os.path.join(dataset))
        return df


def main():
    #Dataset
    my_dataset = "updated.csv"
    group = "grouped.csv"

    #Load Dataset
    data = explore_data(my_dataset)
    data_g = explore_data(group)

    st.title("Sales Analysis using Pandas")
    menu = ['Home', 'Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.text("We have used Python Pandas & Python Matplotlib to analyze and ")
        st.text("answer business questions about 12 months worth of sales data. ")
        st.text("The data contains hundreds of thousands of electronics store ")
        st.text("purchases broken down by month, product type, cost,")
        st.text("purchase address, etc")

        if st.checkbox("Show Entire DataFrame"):
            st.dataframe(data)






    if choice == "Question 1":
        st.subheader("Question 1: What was the best month for sales? How much was earned that month?")
        data = explore_data(my_dataset)
        data['Sales'] = data['Quantity Ordered'].astype('int') * data['Price Each'].astype('float')
        data.groupby(['Month']).sum()
        months = range(1, 13)
        plt.bar(months, data.groupby(['Month']).sum()['Sales'])
        plt.xticks(months)
        plt.ylabel('Sales in USD ($)')
        plt.xlabel('Month number')
        plt.show()
        st.pyplot()
        st.subheader("From the bar chart we can conclude that the best month for sales was December.")
        st.text("The reason for it could be the festive gifting season of Christmas and New Year")


    if choice == "Question 2":
        st.subheader('Question 2: What city had the highest number of sales?')
        data = explore_data(my_dataset)
        data.groupby(['City']).sum()
        keys = [city for city, df in data.groupby(['City'])]
        plt.bar(keys, data.groupby(['City']).sum()['Sales'])
        plt.ylabel('Sales in USD ($)')
        plt.xlabel('City')
        plt.xticks(keys, rotation='vertical', size=8)
        plt.show()
        st.pyplot()
        st.subheader("It is evident from the bar chart that most no. of products were sold in San Francisco.")
        st.text("The reason of this could be San Francisco having the highest household median income")
        st.text("in the United States")


    if choice == "Question 3":
        st.subheader("Question 3: What time should we display advertisements to maximize likelihood to customer's buying product?")
        data = explore_data(my_dataset)
        # Add hour column
        data['Hour'] = pd.to_datetime(data['Order Date']).dt.hour
        data['Minute'] = pd.to_datetime(data['Order Date']).dt.minute
        data['Count'] = 1
        data.head()

        keys = [pair for pair, df in data.groupby(['Hour'])]
        plt.plot(keys, data.groupby(['Hour']).count()['Count'])
        plt.xticks(keys)
        plt.ylabel('Number of Orders')
        plt.xlabel('Hour')
        plt.grid()
        plt.show()
        st.pyplot()
        st.text("From the line graph, we can conclude that, 11AM and 7PM are the timings with ")
        st.text("the heaviest site traffic")
        st.subheader("Hence, I recommend to display advertisments around 11 AM or 7 PM.")


    if choice == 'Question 4':
        st.subheader("Question 4:What products are most often sold together?")
        data = explore_data(my_dataset)
        df = data[data['Order ID'].duplicated(keep=False)]


        df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
        df2 = df[['Order ID', 'Grouped']].drop_duplicates()


        from itertools import combinations
        from collections import Counter

        count = Counter()

        for row in df2['Grouped']:
            row_list = row.split(',')
            count.update(Counter(combinations(row_list, 2)))

        for key, value in count.most_common(10):
            print(key, value)

        st.dataframe(data_g)
        st.subheader("We can offer grouped deals on products bought together most often. ")




    if choice == 'Question 5':
        st.subheader('Question 5:What product sold the most? Why do you think it sold the most')

        product_group = data.groupby('Product')
        quantity_ordered = product_group.sum()['Quantity Ordered']

        products = [product for product, df in product_group]

        plt.bar(products, quantity_ordered)
        plt.xticks(products, rotation='vertical', size=8, color='r')
        plt.yticks(color='r')
        plt.ylabel('Quantity Ordered', color='r')
        plt.xlabel('Product', color='r')
        plt.show()
        st.pyplot()
        st.subheader("AA and AAA batteries were sold the most.")

        prices = data.groupby('Product').mean()['Price Each']

        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx()
        ax1.bar(products, quantity_ordered, color='g')
        ax2.plot(products, prices, 'b-')

        ax1.set_xlabel('Product Name', color='r')
        ax1.set_ylabel('Quantity Ordered', color='g')
        ax2.set_ylabel('Price in USD ($)', color='b')
        ax1.set_xticklabels(products, rotation='vertical', size=8, color='r')
        ax1.set_yticklabels(products, rotation='horizontal', color='g')
        ax2.set_yticklabels(products, rotation='horizontal', color='b')
        plt.show()
        st.pyplot()
        st.subheader("From the above graph we can prove that batteries being the cheapest commodity was sold the most.")


if __name__ =='__main__':
    main()
