# Fintech Bootcamp Project 2: Algorithmic Cryptocurrency Trading Bot

## **Group 5:**

Julia Milin<br/>
Jose Sampedro<br/>
Donna Salinas<br/>
Anthony Mirete<br/>

## **Project Overview:**

As new investors learn more about the world of cryptocurrency, oftentimes than not, it can be an information overload when it comes to selecting a coin to invest in. The overall idea for this project is to create an A.I chat training bot to help new traders with the overall concept of trading and encourage new users to create their own trading strategies. Through Amazon Lex, this robo-advisor will buy and sell cryptocurrency orders using simulated trading. We use the Sandbox API to retrieve fundamental data (market cap, volume, circulating supply, total supply, and other relevant information) for the following crypto coins: ...  

## **Research Questions:**

During the early planning stages, we came up with the following questions to build and set an overall foundation for the project. 

1. What messages to display and what information from the trader is needed for the robo-advisor?
2. What cryptocurrency fundamentals will be used (market cap, volume, supply, volatility, close and open price (daily, weekly, monthly)?
3. How detailed will this project be? How will it be organized? 

## **Data Collection:**

We will be using Sandbox APIs to fetch the information for supply for this project. We will set up the Amazon Lex to look like a dashboard and will use pandas for data frames to display the information provided by the API. 

**Libraries Utilized:**

- Pandas - Python library and data cleaning
- NumPy - Calculations
- hvPlot - Visual graphics
- sklearn - Supervised learning algorithm 

***Image 1: Generalized Overview of the Algorithmic Cryptocurrency Trading Bot***

The Algorithmic Cryptocurrency Trading Bot works overall is like the following:

Description...

**Source Code**

Source code description...

***Image 2: Source Code***

**Sandbox API via Coinbase**

**Choosing certain asset metrics from Sandbox API via the Coinbase Client:**

When it came to organizing the content of our tool, we picked certain metrics that would be most appropriate for the beginner crypto investor. For this tool the following asset metrics were selected: 

description...

**sklearn**

Sklearn description...

***Image 3: sklearn***

## **Interactive Trading Bot User Inteface:**

**Amazon Lex**

Amazon Lex description...

SatoshiBot...

***Image 4: Amazon Lex: SatoshiBot***

## **Conclusion:**

Reintroduce our tool again. Briefly mention how we collected data and made our tool...

## **Model Performance:**

**Scikit Learn Supervised Machine Learning**

The trading strategy I used made a .64% return using BTC-USD.  I used rolling windows of 25 and 100.  I could have made more money if I used smaller rolling windows, resulting in more trades, but the data did not make great predictions.  I made better predictions with the larger window.

![alt text](https://github.com/IJASI/Team-5---Project/blob/main/cumulatin_returns.png)


Model Performance.  I used a SVM model and a Decision Tree model.  I tested about 5 models, which did not perform as well as SVM and DecisionTree. For this algorithm, it was important to use a classifier model to predict 1 of 2 outcomes, the trading signal: 1 or -1

Here is the png of the Decision Tree model:

![alt text](https://github.com/IJASI/Team-5---Project/blob/main/decisiontree.png)

The SVM model did not perform as well

![alt text](https://github.com/IJASI/Team-5---Project/blob/main/svm_model.png)

Overall I am very happy with the results from the Decision Tree model.  I would like more time to optimize it before using testing it will real money

If I had more time, I want to create an optimize a neural network model using Keras.  

The problem I am facing regarding the last for loop and if else statements is:  I am running a for loop to loop through all the predicted signals, but since I am using a binary classifier model, I can only use 2 signals 1 and -1.  I tried running it with 3 signals 1, -1, 0, but I was not able to find a good enough multiclass model to predict the signals in the time allotted to me.  What is happening is that those signals are causing the program to buy every single day, when it should be holding.  I want the bot to hold if the previous row is the same as the last one.  I am working to solve this problem.

