import boto3
import pandas as pd
from io import BytesIO
import vertexai
import re
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
from fuzzywuzzy import process

# s3 config
BUCKET_NAME = "s3-aws-bucket-storage"
FILE_KEY = "q&a.xlsx"
REGION = "us-east-1"

s3 = boto3.client("s3")

def download_xlsx_from_s3():
    response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
    df = pd.read_excel(BytesIO(response["Body"].read()))

    df.columns = ["Question", "Answer"]

    df.dropna(inplace=True)
    df.drop_duplicates(subset=["Question"], inplace=True)

    return df

xlsx_contents = download_xlsx_from_s3()

def find_best_match(question, xlsx_contents):
    questions_list = xlsx_contents["Question"].tolist()
    best_match, score = process.extractOne(question, questions_list)

    if score > 90:
        answer = xlsx_contents.loc[xlsx_contents["Question"] == best_match, "Answer"].values[0]
        return answer
    elif 40 < score >= 90:
        return "Sorry could not find a matching answer to your question. You can contact the support at +075757737 or open a support case at /support-case/create-case"

    return "no response"
