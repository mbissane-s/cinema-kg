from pykeen.pipeline import pipeline

# run KGE pipeline
result = pipeline(
    training='train.txt',
    testing='test.txt',
    validation='valid.txt',
    model='TransE',
    training_kwargs=dict(num_epochs=50),
)

# print metrics
print(result.metric_results)

# save model
result.save_to_directory('kge_model')

print("Model trained and saved.")