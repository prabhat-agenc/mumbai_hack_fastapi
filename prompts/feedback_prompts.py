from langchain.prompts import PromptTemplate


feedback_prompt = PromptTemplate(
    template=('''
        Analyze the following customer feedback data and generate a succinct summary that captures the top positive and negative themes. Prioritize frequently mentioned insights and focus on key recurring words or phrases that indicate overall sentiment.
        {feedbacks}
        
        If no data is provided, return an empty string.
        Strict: Do not include any extra information.
        '''
    ),
    input_variables=["feedbacks"]
)