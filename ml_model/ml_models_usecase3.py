from ml_model import TaskModel
from preload_models_usecase3 import bart_large_cnn_model
from ml_model import logger, db
from bson import ObjectId

# Use Case 3: Summarize a text
class GenerateSummaryModel(TaskModel):
    def run(self):
        self.summarize_text(self.message_data['prompt'])
    
    def summarize_text(self, text, max_length=130, min_length=30):
        logger.info(f"{type(text)}")
        logger.info(f"Summarizing text: {text}")
        # max_input_length = 1024
        # text = text[:max_input_length]  # Cut off text to avoid exceed input limitation of the model
        summary = bart_large_cnn_model(text, max_length, min_length, do_sample=False)
        summary_text = summary[0]['summary_text']
        self.update_task(self.message_data['task_id'], summary_text)
        return summary_text

    def update_task(self, _id, summary_text):
        collection = db['generate-text']
        collection.update_one(
            {'_id': ObjectId(_id)},
            {'$set': {'summary': summary_text}}
        )
        logger.info(f"Updated task {_id} with summary: {summary_text}")