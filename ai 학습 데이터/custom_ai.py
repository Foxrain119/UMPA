import openai

# OpenAI API 키 설정
openai.api_key = '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'

# # 파일 업로드
# response = openai.File.create(
#   file=open("fine_tuning_data_prepared.jsonl", "rb"),
#   purpose="fine-tune"
# )

# print(response)

# # 파인튜닝 작업 생성
# response = openai.FineTuning.create(
#   training_file="fine_tuning_data_prepared.jsonl",  # 업로드된 훈련 파일의 ID
#   model="gpt-3.5-turbo",        # 파인튜닝할 모델의 이름
#   suffix="custom-recommend-model",  # (선택 사항) 사용자 정의 모델 이름
#   n_epochs=4,  # 에포크 수
#   learning_rate_multiplier=0.1  # 학습률 배수
# )

# print(response)

from openai import OpenAI
client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )

# print(completion.choices[0].message)

# 훈련 파일 업로드
# response = client.files.create(
#   file=open("fine_tuning_data_prepared.jsonl", "rb"),
#   purpose="fine-tune"
# )
# print(response)

# # 미세 조정 모델 생성
# response = client.fine_tuning.jobs.create(
#   training_file="file-6SGMqxPz9QJP2KnXMXg1Jx",
#   model="gpt-4o-mini-2024-07-18"
# )
# print(response)

# id = ftjob-DfIsYT7W7teVmOv6briv8Jz0
# FineTuningJob(id='ftjob-DfIsYT7W7teVmOv6briv8Jz0', created_at=1732525011, error=Error(code=None, message=None, param=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='gpt-4o-mini-2024-07-18', object='fine_tuning.job', organization_id='org-IXoNrsw32kBeTEghLnl6ZYzD', result_files=[], seed=1950629790, status='validating_files', trained_tokens=None, training_file='file-6SGMqxPz9QJP2KnXMXg1Jx', validation_file=None, estimated_finish=None, integrations=[], user_provided_suffix=None)


# 미세 조정 작업 완료 확인
job_id = "ftjob-DfIsYT7W7teVmOv6briv8Jz0"  # 미세 조정 작업의 ID를 입력하세요
job = client.fine_tuning.jobs.retrieve(job_id)

print(f"Job Status: {job.status}")
if job.fine_tuned_model:
    print(f"Fine Tuned Model ID: {job.fine_tuned_model}")
else:
    print("Fine Tuned Model is not yet available.")


# # 미세 조정 모델 사용
# completion = client.chat.completions.create(
#   model="ft:gpt-4o-mini:my-org:custom_suffix:id",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"}
#   ]
# )
# print(completion.choices[0].message)
