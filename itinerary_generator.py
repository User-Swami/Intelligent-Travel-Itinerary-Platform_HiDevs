from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    api_key="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"
)


def generate_itinerary(destination, days, interests):
    prompt = PromptTemplate.from_template(
        "Plan a personalized travel itinerary for {days} days in {destination}. Interests include: {interests}."
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(destination=destination, days=days, interests=", ".join(interests))
