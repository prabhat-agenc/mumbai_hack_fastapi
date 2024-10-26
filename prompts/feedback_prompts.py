from langchain.prompts import PromptTemplate


feedback_prompt = PromptTemplate(
    template=('''
        Analyze the following customer feedback data and generate a succinct summary that includes positive as well as negative points. Prioritize frequently mentioned insights and focus on key recurring words or phrases that indicate overall sentiment.
        {feedbacks}
        
        If no data is provided, return an empty string.
        
        I want to display a short and clear summary of the feedbacks for a particular user above in its profile section as a summary of all the feedbacks.
        Strict: Do not include any extra information. The output should be displayable as it is.
        '''
    ),
    input_variables=["feedbacks"]
)