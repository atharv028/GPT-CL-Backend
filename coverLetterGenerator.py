from dotenv import load_dotenv
import os,openai
def getPrompt(resumeText):
  text=""
  if 'job_title' in resumeText.keys():
    text += f"""
      You are a cover letter generator.
      You will be given a job description along with the job applicant's resume.
      You will write a very short cover letter for the applicant named "{resumeText['name']}" that matches their past experiences and skills from the resume with the job description.
      Rather than simply outlining the applicant's past experiences, you will give more detail and explain how those experiences will help the applicant succeed in the new job.
      You will write the cover letter in a modern, {"creative and realxed" if resumeText['creative'] else "professional"} style without being too formal, as a human might do naturally.
      {"You will also be witty and funny" if resumeText['witty'] else ""}      
      Job title : {resumeText['job_title']}.
      Job description : {resumeText['job_description']}
    """
  else:
    text += f"""
      You are a cover letter generator.
      You will have to generate seperate Cover Letter for different roles this person can appy for.
      You will write a very short cover letter for the applicant named "{resumeText['name']}" that matches their past experiences and skills from the resume.
      Rather than simply outlining the applicant's past experiences, you will give more detail and explain how those experiences will help the applicant succeed in the new job.
      You will write the cover letter in a modern, {"creative and realxed" if resumeText['creative'] else "professional"} style without being too formal, as a human might do naturally.
      {"You will also be witty and funny" if resumeText['witty'] else ""}
    """
  for key, value in resumeText.items():
    if key not in ['job_title','job_description','creative','witty','name']:
      text += f"""
      {key}:

      {value}
      
      """
  return text
def generateCoverLetter(resumeText):
  load_dotenv()

  PROMPT=getPrompt(resumeText)
  openai.api_key = os.getenv("OPENAI_API_KEY")
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "user", 
          "content": PROMPT
      }
    ],
  )
  return completion.choices[0].message